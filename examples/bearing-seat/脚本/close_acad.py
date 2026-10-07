"""关闭 AutoCAD（建完即存、存完即关——窗口纪律）。"""
import pythoncom
import win32com.client
import time

pythoncom.CoInitialize()
_BUSY = (-2147418111, -2147417846, -2147417848)


def R(fn):
    for i in range(40):
        try:
            return fn()
        except pythoncom.com_error as e:
            if e.hresult in _BUSY and i < 39:
                time.sleep(0.5)
                continue
            raise
    raise RuntimeError("unreachable")


try:
    app = win32com.client.GetActiveObject("AutoCAD.Application")
    n = R(lambda: app.Documents.Count)
    for i in range(n - 1, -1, -1):
        d = R(lambda i=i: app.Documents.Item(i))
        name = R(lambda: d.Name)
        R(lambda: d.Close(False))
        print(f"closed {name}")
    R(lambda: app.Quit())
    print("AutoCAD 已退出")
except Exception as e:
    print("关闭失败:", str(e)[:120])
