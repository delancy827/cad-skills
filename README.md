# 🔧 CAD Skills for WorkBuddy

> **CAD 自动化与设计技能包** — 让 AI Agent 真正学会用 AutoCAD  
> *Let AI Agent truly learn to use AutoCAD*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-2%20modules-orange.svg)](cad-automation/)
[![AutoCAD](https://img.shields.io/badge/AutoCAD-2020%2B-green.svg)](https://www.autodesk.com/)
[![Language](https://img.shields.io/badge/语言-中文/English-purple.svg)](.)
[![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 📌 快速导航 | Quick Navigation

- [简单版介绍 | Simple Intro](#简单版介绍-simple-intro)
- [详细版介绍 | Detailed Intro](#详细版介绍-detailed-intro)
- [功能对比 | Feature Matrix](#功能对比-feature-matrix)
- [安装方法 | Installation](#安装方法-installation)
- [使用示例 | Usage Examples](#使用示例-usage-examples)
- [本地开发 | Local Development](#本地开发-local-development)
- [贡献指南 | Contributing](#贡献指南-contributing)
- [常见问题 | FAQ](#常见问题-faq)

---

## 简单版介绍 | Simple Intro

### 🇨🇳 中文

这是一个 **CAD 技能包**，专门为 [WorkBuddy](https://workbuddy.ai) AI Agent 设计。

**它能做什么？**
- 🤖 **自动化绘图** — 用自然语言描述，AI 自动在 AutoCAD 中画图
- 📐 **参数化设计** — 修改参数，图形自动更新
- 🔍 **设计审查** — AI 检查你的图纸是否符合国标规范
- 📚 **知识库集成** — 内置 400+ CAD 自动化脚本和设计指南
- 🔌 **国产CAD兼容** — 同时支持中望CAD和浩辰CAD

**适合谁？**
- 机械工程师 — 想用 AI 加速图纸绘制
- 建筑设计 — 想自动化图层、标注和出图
- 市政/公路 — 需要批量处理桩位、断面、管网
- 学生 — 想学习 CAD 二次开发
- 开发者 — 想让 AI 帮你写绘图脚本

**2 分钟上手：**
```bash
# 1. 克隆这个库
git clone https://github.com/delancy827/cad-skills.git

# 2. 复制 skills 到 WorkBuddy
cp -r cad-skills/cad-automation ~/.workbuddy/skills/
cp -r cad-skills/cad-designer ~/.workbuddy/skills/

# 3. 在 WorkBuddy 中加载使用
# 直接说: "帮我画一个 100x50 的矩形，四角倒角 R5"
```

---

## 详细版介绍 | Detailed Intro

### 技能架构 | Skill Architecture

```
cad-skills/
├── cad-automation/     ← 自动化核心 (像 SW 的 solidworks-automation)
│   └── SKILL.md        (834行, 15章, 22KB)
│       ├── Python pyautocad/win32com 连接
│       ├── 绘图/编辑/图层/标注/块/属性
│       ├── AutoLISP 自动化
│       ├── 三维建模
│       ├── 批量处理/文件转换
│       ├── 国产CAD兼容 (中望/浩辰)
│       └── AI+CAD 前沿趋势
│
└── cad-designer/       ← 设计方法论 (像 SW 的 sw-designer)
    └── SKILL.md        (466行, 10章, 14KB)
        ├── 国标制图规范 (GB/T)
        ├── 图层管理系统
        ├── 标注标准与公差
        ├── 块设计规范
        ├── 模板系统 (DWT)
        ├── 打印出图策略
        ├── 性能优化
        ├── AI+CAD 工作流设计
        └── 设计检查清单
```

### 核心能力 | Core Capabilities

| 能力 | cad-automation | cad-designer | 说明 |
|------|:---:|:---:|------|
| Python 自动化 | ✅ | ❌ | pyautocad / win32com |
| AutoLISP 开发 | ✅ | ❌ | 308条实战经验 |
| SendCommand | ✅ | ❌ | 兼容性最好的方式 |
| 基本绘图 | ✅ | ❌ | 直线/圆/多段线/椭圆... |
| 编辑操作 | ✅ | ❌ | 移动/复制/旋转/缩放... |
| 图层管理 | ✅ | ✅ | 创建/自动化模板/规范 |
| 标注 | ✅ | ✅ | API标注/国标规范 |
| 块与属性 | ✅ | ✅ | 创建/属性/动态块规范 |
| 三维建模 | ✅ | ❌ | 实体/布尔/拉伸 |
| 批量处理 | ✅ | ❌ | 批量打开/修改/转换 |
| 国产CAD | ✅ | ❌ | 中望/浩辰COM兼容 |
| AI+CAD | ✅ | ✅ | Text-to-CAD/工作流 |
| 制图规范 | ❌ | ✅ | GB/T全系列 |
| 打印出图 | ✅ | ✅ | 批量PDF/策略 |
| 设计检查 | ❌ | ✅ | 四项检查清单 |

### 支持的工具链 | Supported Toolchains

| 工具/语言 | 适用场景 | 学习方法 |
|-----------|---------|---------|
| **Python (pyautocad)** | 复杂批量自动化 | 从 cad-automation 开始 |
| **AutoLISP** | AutoCAD原生插件 | cad-automation 第十章 |
| **SendCommand** | 快速脚本/通用兼容 | cad-automation 第二章 |
| **C# .NET API** | 企业级插件 | 需要额外 SDK |
| **LLM → Code → CAD** | AI辅助生成 | cad-designer 第八章 |
| **中望/浩辰** | 国产CAD环境 | cad-automation 第十二章 |

---

## 功能对比 | Feature Matrix

### cad-automation vs cad-designer

```
cad-automation:  "怎么做" → 代码实现
cad-designer:    "为什么这样做" → 设计规范
```

| 需求 | 问 cad-designer | 问 cad-automation |
|------|:---:|:---:|
| 标注应该用什么字高？ | ✅ 查国标 | ❌ |
| 图层怎么命名？ | ✅ 设计规范 | ❌ |
| 如何用Python画圆？ | ❌ | ✅ 代码示例 |
| 批量转换DWG到PDF | ❌ | ✅ 批量脚本 |
| 标注顺序对不对？ | ✅ 检查清单 | ❌ |
| 中望CAD里怎么写LISP？ | ❌ | ✅ 兼容方案 |
| AI能帮我画图吗？ | ✅ 工作流设计 | ✅ 代码生成 |

---

## 安装方法 | Installation

### 方式 1：克隆到 WorkBuddy

```bash
# 克隆仓库
git clone https://github.com/delancy827/cad-skills.git

# 安装到项目级别 (当前项目可用)
cp -r cad-skills/cad-automation your-project/.workbuddy/skills/
cp -r cad-skills/cad-designer your-project/.workbuddy/skills/

# 安装到用户级别 (所有项目可用)
cp -r cad-skills/cad-automation ~/.workbuddy/skills/
cp -r cad-skills/cad-designer ~/.workbuddy/skills/
```

### 方式 2：直接在 WorkBuddy 中使用

在 WorkBuddy 对话框中直接向 AI 描述任务，skill 会自动加载：

```
帮我画一个 φ50 的圆，在 (100,100) 处
检查一下这个标注符不符合国标
```

### 方式 3：手动复制 SKILL.md

```bash
mkdir -p ~/.workbuddy/skills/cad-automation
cp cad-automation/SKILL.md ~/.workbuddy/skills/cad-automation/
```

### 前置条件 | Prerequisites

- **WorkBuddy** 已安装
- **AutoCAD 2020+** (或中望CAD/浩辰CAD)
- **Python 3.10+** (可选，用于Python自动化)
- `pip install pyautocad pywin32` (Python自动化需要)

---

## 使用示例 | Usage Examples

### 示例 1：AI 画零件图

**你对 WorkBuddy 说:**
```
帮我画一个法兰盘：
- 外径 φ100，内孔 φ50
- 4个均布螺栓孔 φ10，分布圆 φ75
- 厚度 12mm
- 所有倒角 C1
```

**AI 自动执行:**
1. cad-designer 规划设计 → 确定图层、标注规范、比例
2. cad-automation 生成 Python/LISP 代码 → 连接 AutoCAD → 逐项绘制
3. 自动添加中心线、标注、粗糙度符号
4. 返回验证结果

### 示例 2：批量处理图纸

```
帮我把 D:/projects/ 下所有 DWG 文件:
1. 清理(PURGE)无用对象
2. 统一图层按国标命名
3. 打印为 PDF 到 D:/output/
```

### 示例 3：AI 审查图纸

```
帮我审查当前图纸:
- 图层命名是否规范
- 标注有无封闭尺寸链
- 打印设置是否正确
```

### 示例 4：参数化生成系列

```
帮我生成螺栓系列:
- M8/M10/M12/M16/M20
- 长度 30-100mm (每10mm一档)
- 国标 GB/T 5782
- 每个规格单独文件
```

---

## 本地开发 | Local Development

```bash
# 克隆
git clone https://github.com/delancy827/cad-skills.git
cd cad-skills

# 编辑 SKILL.md
vim cad-automation/SKILL.md

# 测试 (在 WorkBuddy 中加载)
cp cad-automation/SKILL.md ~/.workbuddy/skills/cad-automation/SKILL.md
```

---

## 贡献指南 | Contributing

欢迎提交 PR！请确保：

1. 遵循现有目录结构
2. SKILL.md 使用 YAML frontmatter + Markdown
3. 代码示例在 AutoCAD 2020+ 环境测试通过
4. 标注新功能的兼容性 (AutoCAD/中望/浩辰)

---

## 常见问题 | FAQ

**Q: 需要 Python 吗？**
A: 不必须。SendCommand 方式可以在不装 Python 的情况下使用，或直接生成 AutoLISP (.lsp) 文件加载。

**Q: 支持哪些 CAD 软件？**
A: AutoCAD 2020+ 完整支持，中望CAD 2023+ 和浩辰CAD 2023+ 基本兼容。

**Q: cad-automation 和 cad-designer 的关系？**
A: cad-designer 回答"怎么设计才对"（规范层面），cad-automation 回答"怎么写代码画出来"（代码层面）。两者互补。

**Q: 和 solidworks-skills 什么关系？**
A: 同系列产品。SW skills 用于 SolidWorks 三维建模，CAD skills 用于 AutoCAD 二维/三维绘图。结构和设计模式完全对称。

**Q: 怎么让 AI 生成 LISP 插件？**
A: 直接对 WorkBuddy 说需求即可。cad-automation 内置了 308 条 LISP 插件的模式库。

---

## 📚 姊妹项目

| 项目 | 描述 |
|------|------|
| [solidworks-skills](https://github.com/delancy827/solidworks-skills) | SolidWorks 三维建模自动化 |
| **cad-skills** (你在这里) | AutoCAD 二维/三维绘图自动化 |

---

## 📄 许可证 | License

MIT License — 详见 [LICENSE](LICENSE) 文件。

---

*Built with ❤️ for CAD engineers and AI enthusiasts.*
