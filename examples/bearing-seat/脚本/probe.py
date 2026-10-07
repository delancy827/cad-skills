"""AutoCAD 2024 COM 探针：验证连接、建线、删除。不退出应用（主脚本复用会话）。"""
import pythoncom
import win32com.client

pythoncom.CoInitialize()


def V8(*coords):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(coords))


try:
    app = win32com.client.GetActiveObject("AutoCAD.Application")
    print("附加到运行中的实例, Version:", app.Version)
except Exception:
    print("启动新实例...")
    app = win32com.client.Dispatch("AutoCAD.Application")
    print("已启动, Version:", app.Version)

app.Visible = True

doc = app.ActiveDocument
if doc is None:
    doc = app.Documents.Add()
print("活动文档:", doc.Name, "| 模型空间对象数:", doc.ModelSpace.Count)

# 清理孤儿选择集（cad-automation 铁律0）
for ss in list(doc.SelectionSets):
    try:
        ss.Delete()
    except Exception:
        pass

p1, p2 = V8(0, 0, 0), V8(100, 0, 0)
line = doc.ModelSpace.AddLine(p1, p2)
print("AddLine ->", line.ObjectName, "| 对象数:", doc.ModelSpace.Count)
line.Delete()
print("Delete ->", doc.ModelSpace.Count)

print("图层 CENTER 线型加载测试:")
try:
    doc.Linetypes.Load("CENTER", "acad.lin")
    print("  CENTER 已加载")
except Exception as e:
    print("  CENTER:", str(e)[:60], "(可能已存在)")

print("PROBE OK")
