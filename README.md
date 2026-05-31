# 🔧 CAD Skills — AutoCAD 自动化技能包

> **让 AI 学会 AutoCAD** — 从自然语言到工程图纸，全程自动化  
> *Let AI learn AutoCAD — from natural language to engineering drawings*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-2%20modules-orange.svg)](cad-automation/)
[![AutoCAD](https://img.shields.io/badge/AutoCAD-2020%2B-green.svg)](https://www.autodesk.com/)
[![Language](https://img.shields.io/badge/语言-中文/English-purple.svg)](.)

---

## 📌 快速导航

- [简单版介绍](#简单版介绍)
- [技能架构](#技能架构)
- [功能矩阵](#功能矩阵)
- [安装使用](#安装使用)
- [使用示例](#使用示例)
- [姊妹项目](#姊妹项目)
- [常见问题](#常见问题)

---

## 简单版介绍

这是一个 **CAD 技能包**，供 AI Agent 学习 AutoCAD 操作使用。

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

---

## 技能架构

```
cad-skills/
├── cad-automation/     ← 自动化核心 (写代码画图)
│   └── SKILL.md        (834行, 15章, 22KB)
│       ├── Python pyautocad/win32com 连接
│       ├── 绘图/编辑/图层/标注/块/属性
│       ├── AutoLISP 自动化
│       ├── 三维建模
│       ├── 批量处理/文件转换
│       ├── 国产CAD兼容 (中望/浩辰)
│       └── AI+CAD 前沿趋势
│
└── cad-designer/       ← 设计方法论 (规范指导)
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

### 分工

```
cad-automation:  "怎么做" → 代码实现
cad-designer:    "为什么这样做" → 设计规范
```

---

## 功能矩阵

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

| 需求 | 问 cad-designer | 问 cad-automation |
|------|:---:|:---:|
| 标注应该用什么字高？ | ✅ 查国标 | ❌ |
| 图层怎么命名？ | ✅ 设计规范 | ❌ |
| 如何用Python画圆？ | ❌ | ✅ 代码示例 |
| 批量转换DWG到PDF | ❌ | ✅ 批量脚本 |
| 中望CAD里怎么写LISP？ | ❌ | ✅ 兼容方案 |

---

## 安装使用

### 基础使用

```bash
git clone https://github.com/delancy827/cad-skills.git
```

将 `cad-automation/` 和 `cad-designer/` 目录放置到 AI Agent 的 skill 目录下即可。

### 前置条件

- **AutoCAD 2020+** (或中望CAD/浩辰CAD)
- **Python 3.10+** (可选，用于Python自动化)
- `pip install pyautocad pywin32` (Python自动化需要)

---

## 使用示例

### AI 画零件图

```
帮我画一个法兰盘：
- 外径 φ100，内孔 φ50
- 4个均布螺栓孔 φ10，分布圆 φ75
- 厚度 12mm，所有倒角 C1
```

AI 自动：规划设计 → 生成代码 → 连接 AutoCAD → 绘制 → 添加标注 → 验证

### 批量处理图纸

```
把 D:/projects/ 下所有 DWG 清理、统一图层、打印为 PDF
```

### AI 审查图纸

```
审查当前图纸：图层命名是否规范？标注有无封闭尺寸链？
```

### 参数化生成系列

```
生成螺栓系列 M8~M20，长度 30-100mm，国标 GB/T 5782
```

---

## 📚 姊妹项目

| 项目 | 描述 |
|------|------|
| [solidworks-skills](https://github.com/delancy827/solidworks-skills) | SolidWorks 三维建模自动化 |
| **cad-skills** | AutoCAD 二维/三维绘图自动化 |

---

## 常见问题

**Q: 需要 Python 吗？**
A: 不必须。可直接生成 AutoLISP (.lsp) 文件加载。

**Q: 支持哪些 CAD 软件？**
A: AutoCAD 2020+ 完整支持，中望CAD 2023+ 和浩辰CAD 2023+ 基本兼容。

**Q: cad-automation 和 cad-designer 的关系？**
A: 前者回答"怎么写代码画出来"，后者回答"怎么设计才对"。两者互补。

**Q: 怎么让 AI 生成 LISP 插件？**
A: 提供需求描述即可，cad-automation 内置了 308 条 LISP 插件模式库。

---

## 📄 许可证

MIT License — 详见 [LICENSE](LICENSE) 文件。

---

## ⚖️ 免责声明

1. **本技能包按"原样"提供，不承担任何担保责任。** 使用者需自行测试验证，后果自负。
2. **不构成专业工程建议。** 生成的代码/图纸仅供参考，不替代专业工程师判断。
3. **AutoCAD API 调用可能导致文件损坏或数据丢失。** 使用前务必备份文件。
4. **本技能包与 Autodesk 无关联。** AutoCAD 是 Autodesk 的注册商标。
5. **贡献者对其提交内容负责。** 如有侵权内容，请联系删除。

使用本技能包即表示你同意以上声明。

---

*Built for CAD engineers and AI enthusiasts.*
