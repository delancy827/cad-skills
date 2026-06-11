# 配置文件 - CAD输出目录
# 修改此文件以更改输出路径

from pathlib import Path

# 输出目录：默认为用户文档下的CAD_Output文件夹
OUTPUT_DIR = Path.home() / "Documents" / "CAD_Output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 如果不想使用默认路径，可以取消下面的注释并修改为你的路径
# OUTPUT_DIR = Path("D:/CAD_Projects/Output")
# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
