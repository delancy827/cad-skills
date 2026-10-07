# Changelog

## 2026-10-07

### cad-automation v1.1.1 → v1.2.0

> 经典大作业"轴承座零件图"全流程二次实战验证（AutoCAD 2024 简体中文 24.3 + Python 3.14 + pywin32）。

#### 新增 Section 18：通用零件图全流程本机实证
- 🔴 **COM 忙等重试**：忙时抛 -2147418111「被呼叫方拒绝接收呼叫」；属性访问也会被拒，重试必须包住属性链（lambda 写法）
- 🔴 **文档生命周期**：Documents 归零后集合方法解析失败（AttributeError）；Add 后取 ActiveDocument 需重试+延时；清空旧图用纯 COM 逆序 Delete
- 🔴 **SendCommand 挂起陷阱**：`_AUDIT _Y` 会追加"写审计报告文件?"提示导致同步调用永久挂起（实测卡死 12 分钟）；`_PURGE` 应答序列易错位 → 清理改用 `doc.PurgeAll()` API（修正铁律4 的 AUDIT 写法）
- ⚡ **标注 API 实测**：AddDimDiametric 为 3 参签名；迭代集合引用传标注易报「对象已被删除」→ 直径尺寸用跨象限点 AddDimAligned + `%%c` 文字覆盖
- ✅ **实测可用**：VARIANT 包装填充循环（外环+岛）、gbenor/gbcbig 中文样式、BACKGROUNDPLOT=0 + DWG To PDF.pc3 / PublishToWeb PNG.pc3 出图
- ✅ **验证分层 L2/L3/L4 落地**：82 实体分类型清点 + PNG 视觉审查修复 3 处压线/错层

---


## 2026-06-11

### cad-automation v1.1.0 → v1.1.1

#### 优化内容
- **去掉自引用描述**：移除skill文件开头对自身知识库（"308条LISP"、"78篇前沿"等）的自引用描述
- **保留外部引用**：保留对开源项目（pyautocad, ezdxf, cadquery）的引用说明
- **架构优化**：将版本来源从"SW skill 架构移植"改为"架构优化"，更准确反映修改性质

### cad-designer v1.1.0 → v1.1.1

#### 优化内容
- **去掉自引用描述**：移除skill文件开头对自身知识库的自引用描述
- **保留外部引用**：保留对开源项目和方法论的引用
- **架构优化**：统一版本描述为"架构优化"

---

## 2026-06-01

### cad-automation v1.0.0 → v1.1.0

> 从 solidworks-automation v4.4.0 成功验证的架构模式移植而来。

#### Section 16：CAD 核心铁律速查

- 🔴 **铁律0：启动即清理** — 清理孤儿选择集 + PURGE（SW的CloseDoc铁律对应）
- 🔴 **铁律1：选择集用完必Delete** — CAD的"GetBodies2防假跑"，同名选择集累积导致COM异常
- 🔴 **铁律2：三级执行策略** — Python(pyautocad) → SendCommand → AutoLISP（SW的Python→VBA→C#对应）
- ⚡ **铁律3：CAD六大隐藏地雷速查表** — 选择集泄漏 / UCS混淆 / SendCommand编码 / 对象捕捉干扰 / LISP command陷阱 / APoint缺失
- 🔴 **铁律4：执行后强制审计** — AUDIT + PURGE + ZOOM_E + REGENALL（SW的ForceRebuild3对应）
- 🔴 **铁律5：SendCommand前置管线** — UCS_W + NON + 主命令 + REGENALL 四步安全顺序

#### 知识库更新记录
- 新增第十六章，记录版本变更历史

### cad-designer v1.0.0 → v1.1.0

> 从 sw-designer v2.5.0 成功验证的设计方法论移植而来。

#### 第十一章：设计验证层级体系

- **L1-L4 四级信任层**：API返回值 → ModelSpace实体数 → 选择集对象审计 → VLM视觉QA
- 设计验证的设计哲学："Python代码没报错 ≠ 图纸画对了"
- 从sw-designer移植的6项设计决策对照表

#### 第十二章：CAD设计-验证循环

- **CAD单环验证-迭代模型**（因CAD无编译步骤，适配为单环）
- **迭代中止决策**：简单图≤3轮 / 中等≤5轮 / 复杂≤8轮，同类型错误3次→熔断
- **CAD七铁律设计速查表**：启动清理 / WCS锁定 / 捕捉关闭 / 用完即删 / 审计验证 / 英文命令 / 0层禁忌

#### 知识库更新记录
- 新增第十二章末尾，记录版本变更历史

---

## 2026-05-24

### cad-automation v1.0.0
- 初始版本，含15大章节：绘图/编辑/图层/标注/块/选择集/3D/打印/LISP/批量/AI+CAD/中望浩辰兼容

### cad-designer v1.0.0
- 初始版本，含10大章节：制图规范/图层管理/标注标准/块设计/模板系统/打印策略/性能优化/AI+CAD工作流/行业模板/设计检查清单
