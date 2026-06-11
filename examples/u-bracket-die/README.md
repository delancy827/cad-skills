# U形支架冲压模具CAD自动化设计

[English](#english) | [中文](#中文)

<a name="english"></a>
## English

Automated CAD drawing scripts for U-bracket stamping die design, generated using AutoCAD COM automation (Python + pywin32).

### Features

- **Parametric design**: All dimensions are defined in `Spec` dataclass
- **Automated drawing**: Generates DWG files for blank layout, punch, die block, and assembly
- **Design report**: Automatically generates MD and DOCX design reports
- **Layer management**: Organized layer system (PART, DIE, DIM, etc.)
- **COM retry mechanism**: Handles AutoCAD COM call failures gracefully

### Files

| File | Description |
|------|-------------|
| `脚本/draw_u_bracket_die_assembly.py` | Draws assembly sketch (section view + plan view) |
| `脚本/draw_u_bracket_die_detail_set.py` | Draws detail set (blank layout + punch + die block + calculation) |
| `脚本/generate_u_bracket_design_report.py` | Generates design report in MD and DOCX formats |
| `脚本/config.py` | Configuration file for output directory |

### Requirements

- Python 3.8+
- pywin32 (`pip install pywin32`)
- python-docx (`pip install python-docx`)
- AutoCAD 2020+ (for DWG generation)

### Usage

1. Modify `脚本/config.py` to set your output directory
2. Run the scripts:
   ```bash
   python 脚本/draw_u_bracket_die_assembly.py
   python 脚本/draw_u_bracket_die_detail_set.py
   python 脚本/generate_u_bracket_design_report.py
   ```

### Notes

- This is a **course design validation version**, not for production use
- Dimensions A2 and E are assumed values, need verification before formal submission
- Blank length calculated using neutral layer radius Rn = R + 0.5t (course design approximation)

---

<a name="中文"></a>
## 中文

U形支架冲压模具CAD自动化设计脚本，使用AutoCAD COM自动化（Python + pywin32）生成。

### 功能特点

- **参数化设计**：所有尺寸在 `Spec` dataclass 中定义
- **自动绘图**：生成毛坯展开、凸模、凹模块、总装草图的DWG文件
- **设计报告**：自动生成MD和DOCX格式的设计报告
- **图层管理**：完整的图层系统（PART, DIE, DIM等）
- **COM重试机制**：优雅地处理AutoCAD COM调用失败

### 文件说明

| 文件 | 说明 |
|------|------|
| `脚本/draw_u_bracket_die_assembly.py` | 绘制总装草图（剖视图 + 俯视图） |
| `脚本/draw_u_bracket_die_detail_set.py` | 绘制零件图集（毛坯展开 + 凸模 + 凹模块 + 计算摘要） |
| `脚本/generate_u_bracket_design_report.py` | 生成MD和DOCX格式的设计报告 |
| `脚本/config.py` | 输出目录配置文件 |

### 环境要求

- Python 3.8+
- pywin32 (`pip install pywin32`)
- python-docx (`pip install python-docx`)
- AutoCAD 2020+（用于生成DWG）

### 使用方法

1. 修改 `脚本/config.py` 设置输出目录
2. 运行脚本：
   ```bash
   python 脚本/draw_u_bracket_die_assembly.py
   python 脚本/draw_u_bracket_die_detail_set.py
   python 脚本/generate_u_bracket_design_report.py
   ```

### 注意事项

- 本包为**课程设计验证版**，不适合直接用于生产加工
- A2和E尺寸为暂定值，正式提交前需复核
- 毛坯展开长度采用中性层半径 Rn = R + 0.5t（课程设计近似算法）

## License

MIT License

## Acknowledgments

- Inspired by stamping die design textbooks and course materials
- AutoCAD COM automation via pywin32
