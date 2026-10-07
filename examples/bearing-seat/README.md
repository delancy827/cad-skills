# 例：轴承座零件图（经典 CAD 课程大作业）

用 Python + pywin32 COM 驱动 AutoCAD 2024 全流程绘制 A3 零件图：
图框+标题栏、三视图（主/俯/左）、左视全剖+剖面线、11 处尺寸标注、技术要求、
粗糙度属性块、PDF/PNG 出图。82 实体，纯绘制 5.5s / 含出图 11.7s。

## 目录
- `脚本/`：probe.py（COM 通道探针）/ bearing_drawing.py（主绘制+标注+出图）/ close_acad.py（关窗纪律）
- `出图/`：轴承座零件图.png（校验渲染图）
- `报告/`：大作业报告.md（尺寸账本、简化说明、L2/L3/L4 验证结果）

## 覆盖的实测怪癖
见 cad-automation SKILL.md **第十八章**：COM 忙等重试（属性链 lambda 包裹）、
Documents 归零陷阱、`_AUDIT _Y` 追加提示导致 SendCommand 挂起（→ `doc.PurgeAll()`）、
AddDimDiametric 3 参签名与迭代引用失效（→ 跨象限 AddDimAligned + %%c）、
BACKGROUNDPLOT=0 + DWG To PDF.pc3 / PublishToWeb PNG.pc3 出图管线。
