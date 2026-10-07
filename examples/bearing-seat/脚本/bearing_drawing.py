# -*- coding: utf-8 -*-
"""CAD 课程大作业实测 —— 轴承座零件图（AutoCAD 2024 简体中文版, COM 自动化）

经典大作业内容（调研：机械类 CAD 课程期末大作业 = A3 零件图一张）：
  A3 图框(420x297, 装订边25) + 标题栏 + 三视图(主/俯/左视全剖) + 剖面线
  + 尺寸标注 + 技术要求 + 粗糙度符号块。
轴承座尺寸账本（教材典型值, Designer-choice，无任务书图纸）：
  底板 120x60x16, 四角 R10, 2xØ16 通孔（中心距端 15, 前后居中）
  圆筒 外Ø50 内Ø26, 长 60（与底板前后平齐）, 轴线高 50
  支承板 厚 12（贴圆筒前端面）, 两侧与圆筒相切（宽 50）
  肋板 厚 10（x55..65）, 深 u12..48, 高至圆筒底 25
视图布置（模型空间 1:1）：
  主视 F=(55,150)  | 俯视 T=(55,30)  | 左视(全剖) L=(225,150)
  图框内区 (25,5)-(415,292)；标题栏 (275,5)-(415,37)
验证：L2 实体数、L3 分类型/图层审计、AUDIT+PURGE、绘图输出 PDF+PNG 视觉 QA。
"""
import os
import sys
import time
import math
import pythoncom
import win32com.client

sys.argv = sys.argv if len(sys.argv) > 1 else [sys.argv[0]]
KEEP = "keep" in sys.argv  # 调试期 keep：不退出 AutoCAD

OUT = r"C:\Users\22374\Desktop\湛江北海\学习课程\cad"
os.makedirs(OUT, exist_ok=True)


def V8(*coords):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(coords))


def pt(x, y):
    return V8(x, y, 0.0)


_BUSY = (-2147418111, -2147417846, -2147417848)  # 拒收呼叫/RPC重试/服务器忙


def R(fn):
    """AutoCAD 忙时抛『被呼叫方拒绝接收呼叫』→ 忙等重试。
    fn 必须是零参 lambda：把【属性访问+调用】都包进去（属性访问本身也会被拒）。"""
    for i in range(60):
        try:
            return fn()
        except pythoncom.com_error as e:
            if e.hresult in _BUSY and i < 59:
                time.sleep(0.5)
                continue
            raise
    raise RuntimeError("unreachable")


def connect():
    try:
        app = win32com.client.GetActiveObject("AutoCAD.Application")
        print("[连接] 附加运行实例", app.Version)
    except Exception:
        app = win32com.client.Dispatch("AutoCAD.Application")
        print("[连接] 新实例", app.Version)
    app.Visible = True
    return app


def setup(app):
    """准备干净文档。全程不碰命令行（SendCommand 在挂起/空选择时会卡死 COM）。
    铁律：绝不让 Documents 变 0 —— 零文档时 COM 集合方法解析会失败。"""
    def log(msg):
        print(f"  [{time.strftime('%H:%M:%S')}] {msg}")

    n = R(lambda: app.Documents.Count)
    log(f"Documents.Count = {n}")
    if n == 0:
        doc = R(lambda: app.Documents.Add())
        time.sleep(1.0)
        doc = R(lambda: app.ActiveDocument)
    else:
        doc = R(lambda: app.ActiveDocument)
    # 清空已有几何：纯 COM 删除，不动命令行
    ms = R(lambda: doc.ModelSpace)
    cnt = R(lambda: ms.Count)
    for i in range(cnt - 1, -1, -1):
        try:
            R(lambda i=i: ms.Item(i).Delete())
        except Exception:
            pass
    log(f"清空 {cnt} 个旧实体")
    for ss in list(doc.SelectionSets):
        try:
            ss.Delete()
        except Exception:
            pass
    for var, val in (("BACKGROUNDPLOT", 0), ("LTSCALE", 4), ("INSUNITS", 4),
                     ("DIMTXT", 3.5), ("DIMASZ", 2.5), ("DIMEXO", 0.8),
                     ("DIMEXE", 2.0), ("DIMDEC", 0), ("DIMSCALE", 1),
                     ("CMDECHO", 0)):
        try:
            R(lambda v=var, x=val: doc.SetVariable(v, x))
        except Exception as e:
            print(f"  [变量] {var}: {str(e)[:50]}")
    # 图层（cad-designer 国标配色）
    cfg = {"WALL": (7, "Continuous", 50), "HID": (3, "HIDDEN", 13),
           "CEN": (2, "CENTER", 13), "HAT": (4, "Continuous", 13),
           "DIM": (1, "Continuous", 13), "TXT": (5, "Continuous", 13),
           "TB": (7, "Continuous", 25)}
    have_lt = set()
    try:
        have_lt = {R(lambda: doc.Linetypes.Item(i).Name)
                   for i in range(R(lambda: doc.Linetypes.Count))}
    except Exception:
        pass
    for name, (color, lt, lw) in cfg.items():
        layer = R(lambda n=name: doc.Layers.Add(n))
        R(lambda: setattr(layer, "Color", color))
        try:
            if lt != "Continuous" and lt not in have_lt:
                R(lambda l=lt: doc.Linetypes.Load(l, "acad.lin"))
            R(lambda l=lt: setattr(layer, "Linetype", l))
        except Exception as e:
            print(f"  [线型] {name}/{lt}: {str(e)[:50]}")
        try:
            layer.Lineweight = lw
        except Exception:
            pass
    # 中文文字样式（已存在则复用）
    try:
        if "GB" not in [s.Name for s in doc.TextStyles]:
            st = doc.TextStyles.Add("GB")
        else:
            st = doc.TextStyles("GB")
        st.FontFile = "gbenor.shx"
        st.BigFontFile = "gbcbig.shx"
        doc.ActiveTextStyle = st
    except Exception as e:
        print(f"  [文字样式] {str(e)[:60]}")
    doc.ActiveLayer = doc.Layers("WALL")
    return doc


class Draw:
    def __init__(self, doc):
        self.doc = doc
        self.m = doc.ModelSpace

    def line(self, x1, y1, x2, y2, layer="WALL"):
        o = self.m.AddLine(pt(x1, y1), pt(x2, y2))
        o.Layer = layer
        return o

    def pline(self, pts, layer="WALL", closed=True):
        flat = []
        for x, y in pts:
            flat += [x, y]
        o = self.m.AddLightWeightPolyline(V8(*flat))
        o.Closed = closed
        o.Layer = layer
        return o

    def circle(self, cx, cy, r, layer="WALL"):
        o = self.m.AddCircle(pt(cx, cy), r)
        o.Layer = layer
        return o

    def arc(self, cx, cy, r, a1_deg, a2_deg, layer="WALL"):
        o = self.m.AddArc(pt(cx, cy), r, math.radians(a1_deg), math.radians(a2_deg))
        o.Layer = layer
        return o

    def text(self, s, x, y, h, layer="TXT"):
        o = self.m.AddText(s, pt(x, y), h)
        o.Layer = layer
        return o

    def mtext(self, s, x, y, w, h=3.5, layer="TXT"):
        o = self.m.AddMText(pt(x, y), w, s)
        o.Height = h
        o.Layer = layer
        return o

    def dim(self, p1, p2, tp, override=None, layer="DIM"):
        o = self.m.AddDimAligned(pt(*p1), pt(*p2), pt(*tp))
        if override:
            o.TextOverride = override
        o.Layer = layer
        return o

    def dim_dia(self, circle_obj, override, leader=10, flip=False):
        c = circle_obj.Center
        cx, cy, r = c[0], c[1], circle_obj.Radius
        p1 = pt(cx + r, cy) if not flip else pt(cx - r, cy)
        p2 = pt(cx - r, cy) if not flip else pt(cx + r, cy)
        try:
            o = self.m.AddDimDiametric(circle_obj, p1, p2, leader)
        except Exception:
            o = self.m.AddDimDiametric(circle_obj, p1, leader)
        o.TextOverride = override
        o.Layer = "DIM"
        return o

    def hatch(self, outer_pts, holes=(), scale=1.0):
        outer = self.pline(outer_pts, layer="HAT", closed=True)
        h = self.m.AddHatch(0, "ANSI31", True)
        loop = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [outer])
        h.AppendOuterLoop(loop)
        for hp in holes:
            inner = self.pline(hp, layer="HAT", closed=True)
            il = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [inner])
            h.AppendInnerLoop(il)
        h.PatternScale = scale
        h.Evaluate()
        try:
            h.Layer = "HAT"
        except Exception:
            pass
        return h


# ---------- 几何布置 ----------
F = (55, 150)   # 主视偏移
T = (55, 30)    # 俯视偏移
L = (225, 150)  # 左视偏移


def draw_frame(d):
    d.pline([(0, 0), (420, 0), (420, 297), (0, 297)], layer="TB")
    d.pline([(25, 5), (415, 5), (415, 292), (25, 292)], layer="TB")
    # 标题栏 140x32 @ (275,5)
    x0, y0 = 275, 5
    for yy in (15, 25, 37):
        d.line(x0, y0 + yy, x0 + 140, y0 + yy, "TB")
    for xx in (70, 105):
        d.line(x0 + xx, y0 + 25, x0 + xx, y0 + 37, "TB")
    d.line(x0 + 70, y0 + 5, x0 + 70, y0 + 25, "TB")
    d.text("轴承座", x0 + 18, y0 + 28, 5)
    d.text("比例 1:1", x0 + 73, y0 + 34, 2.5)
    d.text("图号 JS01-01", x0 + 107, y0 + 34, 2.5)
    d.text("材料 HT200", x0 + 4, y0 + 18, 3.5)
    d.text("制图 DL  2026-10-07", x0 + 74, y0 + 18, 2.5)
    d.text("审核", x0 + 4, y0 + 7, 3.5)
    d.text("湛江北海  CAD课程大作业", x0 + 74, y0 + 7, 2.5)


def draw_front(d):
    ox, oy = F
    # 底板
    d.pline([(ox, oy), (ox + 120, oy), (ox + 120, oy + 16), (ox, oy + 16)])
    # 支承板（两侧与Ø50相切 x=35/85, 高 16..50）
    d.line(ox + 35, oy + 16, ox + 35, oy + 50)
    d.line(ox + 85, oy + 16, ox + 85, oy + 50)
    # 圆筒
    d.circle(ox + 60, oy + 50, 25)
    d.circle(ox + 60, oy + 50, 13)
    # 肋板（x55..65, 高至圆筒底25）
    d.line(ox + 55, oy + 16, ox + 55, oy + 25)
    d.line(ox + 65, oy + 16, ox + 65, oy + 25)
    d.line(ox + 55, oy + 25, ox + 65, oy + 25)
    # 底板孔虚线（x=15±8, 105±8）
    for hx in (7, 23, 97, 113):
        d.line(ox + hx, oy, ox + hx, oy + 16, "HID")
    # 中心线
    d.line(ox + 28, oy + 50, ox + 92, oy + 50, "CEN")
    d.line(ox + 60, oy + 18, ox + 60, oy + 82, "CEN")


def draw_top(d):
    ox, oy = T
    # 底板（四角 R10）
    d.pline([(ox + 10, oy), (ox + 110, oy), (ox + 110, oy + 60), (ox + 10, oy + 60)])
    d.line(ox, oy + 10, ox, oy + 50)
    d.line(ox + 120, oy + 10, ox + 120, oy + 50)
    d.arc(ox + 10, oy + 10, 10, 180, 270)
    d.arc(ox + 110, oy + 10, 10, 270, 360)
    d.arc(ox + 110, oy + 50, 10, 0, 90)
    d.arc(ox + 10, oy + 50, 10, 90, 180)
    # 圆筒（前后平齐 y=0..60, x=35..85）
    d.line(ox + 35, oy, ox + 85, oy)
    d.line(ox + 35, oy + 60, ox + 85, oy + 60)
    d.line(ox + 35, oy, ox + 35, oy + 60)
    d.line(ox + 85, oy, ox + 85, oy + 60)
    # 支承板后棱（被圆筒遮住→虚线）
    d.line(ox + 35, oy + 12, ox + 85, oy + 12, "HID")
    # 肋板（u12..48 两侧虚线）
    d.line(ox + 50, oy + 12, ox + 50, oy + 48, "HID")
    d.line(ox + 70, oy + 12, ox + 70, oy + 48, "HID")
    # Ø26 孔虚线（x=47/73）
    d.line(ox + 47, oy, ox + 47, oy + 60, "HID")
    d.line(ox + 73, oy, ox + 73, oy + 60, "HID")
    # 底板孔
    d.circle(ox + 15, oy + 30, 8)
    d.circle(ox + 105, oy + 30, 8)
    # 中心线
    d.line(ox + 60, oy - 5, ox + 60, oy + 65, "CEN")
    for hx in (15, 105):
        d.line(ox + hx - 12, oy + 30, ox + hx + 12, oy + 30, "CEN")
        d.line(ox + hx, oy + 18, ox + hx, oy + 42, "CEN")


def draw_left(d):
    ox, oy = L
    # 外框（u=深度0..60, z=0..75）
    d.pline([(ox, oy), (ox, oy + 75), (ox + 60, oy + 75), (ox + 60, oy)])
    # 孔边界 z=37/63
    d.line(ox, oy + 37, ox + 60, oy + 37)
    d.line(ox, oy + 63, ox + 60, oy + 63)
    # 圆筒底切线 z=25
    d.line(ox, oy + 25, ox + 60, oy + 25)
    # 肋板轮廓（u12..48, z16..25, 纵剖不画剖面线）
    d.line(ox + 12, oy + 16, ox + 12, oy + 25)
    d.line(ox + 48, oy + 16, ox + 48, oy + 25)
    # 底板顶面暴露段（u48..60）
    d.line(ox + 48, oy + 16, ox + 60, oy + 16)
    # 剖面线：下部区（外框(0,0)-(60,37), 孔洞=肋板+右侧空区 (12,16)-(60,25)）
    d.hatch([(ox, oy), (ox + 60, oy), (ox + 60, oy + 37), (ox, oy + 37)],
            holes=[[(ox + 12, oy + 16), (ox + 60, oy + 16),
                    (ox + 60, oy + 25), (ox + 12, oy + 25)]])
    # 上部套筒壁
    d.hatch([(ox, oy + 63), (ox + 60, oy + 63), (ox + 60, oy + 75), (ox, oy + 75)])
    # 视图名（避开 60 尺寸文字区）
    d.text("A—A", ox + 22, oy - 22, 5)


def draw_annotations(d):
    ox, oy = F
    # 主视标注
    d.dim((ox, oy), (ox + 120, oy), (ox + 60, oy - 8))            # 120
    d.dim((ox, oy), (ox, oy + 16), (ox - 9, oy + 8))              # 16
    d.dim((ox + 60, oy), (ox + 60, oy + 50), (ox + 97, oy + 25))  # 50
    # 直径尺寸：跨象限点对齐标注 + 文字覆盖（AddDimDiametric 引用易失效，不用）
    d.dim((ox + 35, oy + 50), (ox + 85, oy + 50), (ox + 60, oy + 56), override="%%c50")
    d.dim((ox + 47, oy + 50), (ox + 73, oy + 50), (ox + 60, oy + 43), override="%%c26")
    # 俯视标注
    tx, ty = T
    d.dim((tx + 120, ty), (tx + 120, ty + 60), (tx + 133, ty + 30))  # 60
    d.dim((tx + 7, ty + 30), (tx + 23, ty + 30), (tx + 15, ty + 20),
          override="2×%%c16")                                        # 2×Ø16
    d.dim((tx, ty + 30), (tx + 15, ty + 30), (tx + 7, ty + 46))      # 15
    # R10 手工引线（AddDimRadial 引用易失效）
    ax, ay = tx + 10 + 10 * math.cos(math.radians(225)), ty + 10 + 10 * math.sin(math.radians(225))
    d.line(ax, ay, tx - 6, ty - 5, "DIM")
    d.text("R10", tx - 15, ty - 8, 2.5, "DIM")
    # 左视标注
    lx, ly = L
    d.dim((lx, ly), (lx + 60, ly), (lx + 30, ly - 8))             # 60
    d.dim((lx, ly + 37), (lx + 12, ly + 37), (lx + 6, ly + 47))   # 12（孔腔空白区）
    # 技术要求
    d.mtext("技术要求:\\P1. 铸件不得有砂眼、气孔、裂纹;\\P"
            "2. 未注圆角 R3~R5, 未注倒角 C2;\\P3. 非加工面涂防锈漆。",
            300, 258, 105, 3.5)
    # 粗糙度块（0层建块, cad-designer 铁律）
    try:
        blk = d.doc.Blocks.Add(pt(0, 0), "Ra")
        l1 = blk.AddLine(pt(-3, -5.2), pt(0, 0))
        l2 = blk.AddLine(pt(0, 0), pt(6, -10.4))
        blk.AddAttribute(2.5, 0, "粗糙度值", pt(6.5, -8.5), "RA", "Ra 3.2")
        ref1 = d.m.InsertBlock(pt(146, 224), "Ra", 1, 1, 1, 0)
        for att in ref1.GetAttributes():
            att.TextString = "Ra 1.6"
            att.Update()
        ref1.Layer = "DIM"
        ref2 = d.m.InsertBlock(pt(88, 136), "Ra", 1, 1, 1, 0)
        for att in ref2.GetAttributes():
            att.TextString = "Ra 6.3"
            att.Update()
        ref2.Layer = "DIM"
        d.line(146, 224, 133, 217, "DIM")   # 引线至外圆
        d.line(88, 136, 92, 150, "DIM")     # 引线至底板底面（避开 120 尺寸文字）
    except Exception as e:
        print(f"  [粗糙度块] {str(e)[:70]}")


def audit_and_count(doc):
    time.sleep(0.2)
    # PURGE 走 COM API（SendCommand 版会卡在交互提示上）；AUDIT 略过——本图为纯生成几何
    try:
        R(lambda: doc.PurgeAll())
        print("  [清理] PurgeAll ✓")
    except Exception as e:
        print(f"  [清理] PurgeAll: {str(e)[:60]}")
    for cmd in ("_ZOOM _E\n", "_REGENALL\n"):
        R(lambda c=cmd: doc.SendCommand(c))
        time.sleep(0.4)
    time.sleep(1.0)
    tally = {}
    for o in doc.ModelSpace:
        for attempt in range(10):
            try:
                key = (o.ObjectName, o.Layer)
                break
            except pythoncom.com_error:
                time.sleep(0.5)
        else:
            key = ("<unreadable>", "?")
        tally[key] = tally.get(key, 0) + 1
    print("[审计] 实体总数:", doc.ModelSpace.Count)
    for (name, layer), n in sorted(tally.items()):
        print(f"    {name:<26} {layer:<5} x{n}")
    return tally


def plot(doc, device_hint, media_hint, out_path):
    layout = R(lambda: doc.Layouts("Model"))
    try:
        R(lambda: setattr(layout, "ConfigName", device_hint))
    except Exception as e:
        print(f"  [打印] 设备 {device_hint}: {str(e)[:60]}")
        return False
    names = list(R(lambda: layout.GetCanonicalMediaNames()))
    pick = None
    for n in names:
        if media_hint and media_hint in n:
            pick = n
    if pick is None and names:
        pick = names[-1]
    R(lambda: setattr(layout, "CanonicalMediaName", pick))
    print(f"  [打印] {device_hint} 纸张: {pick}")
    for attr, val in (("PlotType", 1), ("StandardScale", 0), ("PlotWithLineweights", True),
                      ("CenterPlot", True), ("PlotHidden", False)):
        try:
            R(lambda a=attr, v=val: setattr(layout, a, v))
        except Exception:
            pass
    try:
        R(lambda: setattr(layout, "StyleSheet", "monochrome.ctb"))
    except Exception as e:
        print(f"  [打印] 样式表: {str(e)[:50]}")
    ok = R(lambda: doc.Plot.PlotToFile(out_path))
    for _ in range(30):
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            ok = True
            break
        time.sleep(0.5)
    print(f"  [打印] {os.path.basename(out_path)}: "
          f"{'✓ ' + str(os.path.getsize(out_path)) + 'B' if os.path.exists(out_path) else '✗'}")
    return os.path.exists(out_path)


def main():
    pythoncom.CoInitialize()
    t0 = time.time()

    def step(msg):
        print(f"[{time.strftime('%H:%M:%S')} +{time.time()-t0:5.1f}s] {msg}")

    app = connect()
    step("[1] 新建文档 + 图层/样式")
    doc = setup(app)
    d = Draw(doc)
    step("[2] 图框+标题栏")
    draw_frame(d)
    step("[3] 主视图")
    draw_front(d)
    step("[4] 俯视图")
    draw_top(d)
    step("[5] 左视图全剖+剖面线")
    draw_left(d)
    step("[6] 标注/技术要求/粗糙度")
    draw_annotations(d)
    step("[7] 审计+清点")
    audit_and_count(doc)
    step("[8] 保存")
    dwg = os.path.join(OUT, "轴承座零件图.dwg")
    R(lambda: doc.SaveAs(dwg))
    print("  [保存]", dwg, os.path.getsize(dwg), "bytes")
    step("[9] 出图 PDF+PNG")
    plot(doc, "DWG To PDF.pc3", "ISO_A3", os.path.join(OUT, "轴承座零件图.pdf"))
    plot(doc, "PublishToWeb PNG.pc3", "", os.path.join(OUT, "轴承座零件图.png"))
    if not KEEP:
        R(lambda: doc.Close(False))
        R(lambda: app.Quit())
        step("[10] 已关闭文档并退出 AutoCAD（窗口纪律）")
    else:
        step("[10] keep 模式：AutoCAD 保持运行")
    print("=== 完成 ===")


if __name__ == "__main__":
    main()
