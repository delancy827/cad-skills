from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import win32com.client


OUT_DIR = Path.home() / "Documents" / "CAD_Output"
OUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class Spec:
    t: float = 2.0
    a1: float = 42.0
    a2: float = 46.0  # assumed from sketch
    b: float = 25.0
    c: float = 30.0
    d: float = 57.0
    e: float = 13.0  # nominal from truncated text
    r: float = 5.0
    material: str = "10钢"

    @property
    def neutral_radius(self) -> float:
        # Common course-design approximation for low carbon steel when r/t > 0.5.
        return self.r + 0.5 * self.t

    @property
    def bend_allowance_one_90(self) -> float:
        return math.pi / 2 * self.neutral_radius

    @property
    def estimated_flat_length(self) -> float:
        # Two 90-degree bends. Simplified validation estimate:
        # bottom straight + two vertical sides + two bend allowances.
        bottom_straight = max(self.a1 - 2 * self.r, 0)
        side_straight = max(self.b - self.r, 0)
        return bottom_straight + 2 * side_straight + 2 * self.bend_allowance_one_90


def pt(x: float, y: float, z: float = 0.0):
    return win32com.client.VARIANT(8197, (float(x), float(y), float(z)))


def doubles(*values: float):
    return win32com.client.VARIANT(8197, tuple(float(v) for v in values))


def retry(fn, timeout: float = 20.0, delay: float = 0.35):
    end = time.time() + timeout
    err = None
    while time.time() < end:
        try:
            return fn()
        except Exception as exc:
            err = exc
            time.sleep(delay)
    raise RuntimeError(f"AutoCAD COM retry failed: {err}")


def layer(doc, name: str, color: int):
    def create():
        try:
            return doc.Layers.Item(name)
        except Exception:
            return doc.Layers.Add(name)

    obj = retry(create)
    try:
        obj.Color = color
    except Exception:
        pass
    return obj


def line(ms, p1, p2, lyr: str):
    obj = retry(lambda: ms.AddLine(pt(*p1), pt(*p2)))
    obj.Layer = lyr
    return obj


def circle(ms, c, r: float, lyr: str):
    obj = retry(lambda: ms.AddCircle(pt(*c), r))
    obj.Layer = lyr
    return obj


def arc(ms, c, r: float, a1: float, a2: float, lyr: str):
    obj = retry(lambda: ms.AddArc(pt(*c), r, math.radians(a1), math.radians(a2)))
    obj.Layer = lyr
    return obj


def text(ms, s: str, x: float, y: float, h: float, lyr: str):
    obj = retry(lambda: ms.AddText(s, pt(x, y), h))
    obj.Layer = lyr
    return obj


def mtext(ms, s: str, x: float, y: float, w: float, lyr: str):
    obj = retry(lambda: ms.AddMText(pt(x, y), w, s))
    try:
        obj.Layer = lyr
    except Exception:
        pass
    return obj


def poly(ms, pts: list[tuple[float, float]], lyr: str, closed: bool = False):
    coords: list[float] = []
    for x, y in pts:
        coords.extend((x, y))
    obj = retry(lambda: ms.AddLightWeightPolyline(doubles(*coords)))
    obj.Closed = closed
    obj.Layer = lyr
    return obj


def rect(ms, x: float, y: float, w: float, h: float, lyr: str):
    return poly(ms, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], lyr, True)


def dim(ms, p1, p2, tp, lyr: str):
    obj = retry(lambda: ms.AddDimAligned(pt(*p1), pt(*p2), pt(*tp)))
    obj.Layer = lyr
    return obj


def dimv(ms, p1, p2, tp, lyr: str):
    obj = retry(lambda: ms.AddDimRotated(pt(*p1), pt(*p2), pt(*tp), math.radians(90)))
    obj.Layer = lyr
    return obj


def center(ms, x1, y1, x2, y2):
    line(ms, (x1, y1), (x2, y2), "CENTER")


def draw_blank_layout(ms, s: Spec, ox: float, oy: float):
    flat_len = s.estimated_flat_length
    half_l = flat_len / 2
    half_w = s.d / 2
    rect(ms, ox - half_l, oy - half_w, flat_len, s.d, "PART")

    # Bend lines, assuming symmetric U-bend.
    side_zone = max(s.b - s.r, 0) + s.bend_allowance_one_90 / 2
    left_bend = ox - half_l + side_zone
    right_bend = ox + half_l - side_zone
    line(ms, (left_bend, oy - half_w), (left_bend, oy + half_w), "BEND")
    line(ms, (right_bend, oy - half_w), (right_bend, oy + half_w), "BEND")

    circle(ms, (ox, oy + s.c / 2), s.e / 2, "PART")
    circle(ms, (ox, oy - s.c / 2), s.e / 2, "PART")
    center(ms, ox - 12, oy + s.c / 2, ox + 12, oy + s.c / 2)
    center(ms, ox - 12, oy - s.c / 2, ox + 12, oy - s.c / 2)
    center(ms, ox, oy - half_w - 12, ox, oy + half_w + 12)

    text(ms, "毛坯展开图（工艺参考）", ox - 60, oy + half_w + 14, 4, "TEXT")
    text(ms, "弯曲线", left_bend - 10, oy + half_w + 4, 2.8, "TEXT")
    text(ms, f"2-%%c{s.e:.0f}", ox + 8, oy + 4, 3.2, "TEXT")
    dim(ms, (ox - half_l, oy - half_w - 8), (ox + half_l, oy - half_w - 8), (ox, oy - half_w - 20), "DIM")
    dimv(ms, (ox + half_l + 8, oy - half_w), (ox + half_l + 8, oy + half_w), (ox + half_l + 20, oy), "DIM")
    dimv(ms, (ox + 18, oy - s.c / 2), (ox + 18, oy + s.c / 2), (ox + 32, oy), "DIM")


def draw_punch_detail(ms, s: Spec, ox: float, oy: float):
    w = s.a1
    h = 60
    r = s.r
    left = ox - w / 2
    right = ox + w / 2
    top = oy + h
    bottom = oy
    line(ms, (left, bottom + r), (left, top), "DIE")
    line(ms, (right, bottom + r), (right, top), "DIE")
    line(ms, (left + r, bottom), (right - r, bottom), "DIE")
    arc(ms, (left + r, bottom + r), r, 180, 270, "DIE")
    arc(ms, (right - r, bottom + r), r, 270, 360, "DIE")
    rect(ms, ox - 36, oy + h, 72, 16, "DIE")
    center(ms, ox, oy - 10, ox, oy + h + 24)
    text(ms, "U形弯曲凸模零件图", ox - 38, oy + h + 24, 4, "TEXT")
    text(ms, "R5", ox + 14, oy + 5, 3.2, "TEXT")
    dim(ms, (left, oy - 10), (right, oy - 10), (ox, oy - 22), "DIM")
    dimv(ms, (right + 8, bottom), (right + 8, top), (right + 20, oy + h / 2), "DIM")
    mtext(ms, "材料建议：T10A、Cr12或课程设计常用模具钢\\P热处理硬度和表面粗糙度按最终标准补充。", ox - 55, oy - 42, 110, "TEXT")


def draw_die_block_detail(ms, s: Spec, ox: float, oy: float):
    block_w = 110
    block_h = 45
    opening = s.a2 + 4.4
    depth = 22
    rect(ms, ox - block_w / 2, oy, block_w, block_h, "DIE")
    left = ox - opening / 2
    right = ox + opening / 2
    top = oy + block_h
    bottom = top - depth
    line(ms, (left, top), (left, bottom), "DIE")
    line(ms, (right, top), (right, bottom), "DIE")
    line(ms, (left, bottom), (right, bottom), "DIE")
    # screw/pin placeholders
    for x in (ox - 38, ox + 38):
        circle(ms, (x, oy + 18), 4, "AUX")
        center(ms, x - 8, oy + 18, x + 8, oy + 18)
        center(ms, x, oy + 10, x, oy + 26)
    text(ms, "凹模块零件图", ox - 30, oy + block_h + 12, 4, "TEXT")
    dim(ms, (left, oy - 10), (right, oy - 10), (ox, oy - 22), "DIM")
    dim(ms, (ox - block_w / 2, oy - 24), (ox + block_w / 2, oy - 24), (ox, oy - 36), "DIM")
    dimv(ms, (ox + block_w / 2 + 8, oy), (ox + block_w / 2 + 8, oy + block_h), (ox + block_w / 2 + 20, oy + block_h / 2), "DIM")
    mtext(ms, "凹模型腔按A2并考虑间隙示意。\\P最终尺寸需结合回弹补偿和教材标准复核。", ox - 54, oy - 56, 120, "TEXT")


def draw_calculation_panel(ms, s: Spec, ox: float, oy: float):
    rect(ms, ox, oy - 95, 150, 95, "AUX")
    text(ms, "计算摘要", ox + 5, oy - 10, 4, "TEXT")
    calc = (
        f"材料：{s.material}\\P"
        f"t = {s.t:.1f} mm, R = {s.r:.1f} mm\\P"
        f"中性层半径：Rn = R + 0.5t = {s.neutral_radius:.1f} mm\\P"
        f"单个90度弯曲展开：{s.bend_allowance_one_90:.2f} mm\\P"
        f"估算毛坯展开长度：{s.estimated_flat_length:.2f} mm\\P"
        "工艺路线：冲孔 -> 落料 -> U形弯曲\\P"
        "说明：A2和E为暂定值，正式提交前需复核。"
    )
    mtext(ms, calc, ox + 5, oy - 20, 140, "TEXT")


def draw_title(ms, ox: float, oy: float):
    rect(ms, ox, oy, 140, 28, "AUX")
    text(ms, "U形支架弯曲模主要零件图", ox + 6, oy + 18, 4, "TEXT")
    text(ms, "凸模 / 凹模块 / 毛坯展开", ox + 6, oy + 10, 3.0, "TEXT")
    text(ms, "自动生成，课程设计验证版", ox + 6, oy + 3, 2.6, "TEXT")


def main():
    spec = Spec()
    acad = win32com.client.Dispatch("AutoCAD.Application")
    acad.Visible = True
    doc = retry(lambda: acad.Documents.Add(), timeout=30)
    time.sleep(1.5)
    ms = doc.ModelSpace

    for name, color in {
        "PART": 7,
        "DIE": 1,
        "DIM": 4,
        "CENTER": 2,
        "BEND": 6,
        "TEXT": 5,
        "AUX": 8,
    }.items():
        layer(doc, name, color)

    draw_blank_layout(ms, spec, ox=0, oy=0)
    draw_punch_detail(ms, spec, ox=170, oy=-15)
    draw_die_block_detail(ms, spec, ox=330, oy=-10)
    draw_calculation_panel(ms, spec, ox=-75, oy=-85)
    draw_title(ms, ox=230, oy=-120)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = OUT_DIR / f"u_bracket_die_detail_set_cn_{stamp}.dwg"
    retry(lambda: doc.SendCommand("_ZOOM _E\n"), timeout=10)
    time.sleep(1)
    retry(lambda: doc.SaveAs(str(out)), timeout=20)
    print(f"saved={out}")
    print(f"flat_length_estimate={spec.estimated_flat_length:.2f}")
    print("scope=blank+punch+die_block+calculation_panel")


if __name__ == "__main__":
    main()
