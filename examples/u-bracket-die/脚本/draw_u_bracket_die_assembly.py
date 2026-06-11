from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import win32com.client


DESKTOP = Path.home() / "Desktop"
OUT_DIR = DESKTOP / "CAD_heavy_validation"
OUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class PartSpec:
    thickness: float = 2.0
    a1: float = 42.0
    a2: float = 46.0  # inferred
    b: float = 25.0
    c: float = 30.0
    d: float = 57.0
    e: float = 13.0  # nominalized from truncated source
    r: float = 5.0


def pt(x: float, y: float, z: float = 0.0):
    return win32com.client.VARIANT(8197, (float(x), float(y), float(z)))


def doubles(*values: float):
    return win32com.client.VARIANT(8197, tuple(float(v) for v in values))


def com_retry(fn, timeout: float = 20.0, delay: float = 0.4):
    deadline = time.time() + timeout
    last_exc = None
    while time.time() < deadline:
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            time.sleep(delay)
    raise RuntimeError(f"AutoCAD COM failure: {last_exc}")


def ensure_layer(doc, name: str, color: int):
    def get_or_add():
        try:
            return doc.Layers.Item(name)
        except Exception:
            return doc.Layers.Add(name)

    lyr = com_retry(get_or_add)
    try:
        lyr.Color = color
    except Exception:
        pass
    return lyr


def add_line(ms, p1, p2, layer: str):
    obj = com_retry(lambda: ms.AddLine(pt(*p1), pt(*p2)))
    obj.Layer = layer
    return obj


def add_circle(ms, center, radius: float, layer: str):
    obj = com_retry(lambda: ms.AddCircle(pt(*center), radius))
    obj.Layer = layer
    return obj


def add_arc(ms, center, radius: float, start_deg: float, end_deg: float, layer: str):
    obj = com_retry(
        lambda: ms.AddArc(pt(*center), radius, math.radians(start_deg), math.radians(end_deg))
    )
    obj.Layer = layer
    return obj


def add_text(ms, text: str, x: float, y: float, height: float, layer: str):
    obj = com_retry(lambda: ms.AddText(text, pt(x, y), height))
    obj.Layer = layer
    return obj


def add_mtext(ms, text: str, x: float, y: float, width: float, layer: str):
    obj = com_retry(lambda: ms.AddMText(pt(x, y), width, text))
    obj.Layer = layer
    return obj


def add_poly(ms, points: list[tuple[float, float]], layer: str, closed: bool = False):
    coords: list[float] = []
    for x, y in points:
        coords.extend((x, y))
    obj = com_retry(lambda: ms.AddLightWeightPolyline(doubles(*coords)))
    obj.Closed = closed
    obj.Layer = layer
    return obj


def add_dim_aligned(ms, p1, p2, text_pt, layer: str):
    obj = com_retry(lambda: ms.AddDimAligned(pt(*p1), pt(*p2), pt(*text_pt)))
    obj.Layer = layer
    return obj


def add_dim_rotated(ms, p1, p2, text_pt, angle_deg: float, layer: str):
    obj = com_retry(
        lambda: ms.AddDimRotated(pt(*p1), pt(*p2), pt(*text_pt), math.radians(angle_deg))
    )
    obj.Layer = layer
    return obj


def rect(ms, x: float, y: float, w: float, h: float, layer: str):
    return add_poly(
        ms,
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
        layer,
        closed=True,
    )


def centerline(ms, x1, y1, x2, y2):
    add_line(ms, (x1, y1), (x2, y2), "CENTER")


def draw_section(ms, spec: PartSpec, ox: float, oy: float):
    # Base plates
    lower_w = 160.0
    lower_h = 26.0
    die_block_w = 120.0
    die_block_h = 28.0
    upper_w = 150.0
    upper_h = 24.0
    clamp_h = 16.0
    guide_x = 52.0

    rect(ms, ox - lower_w / 2, oy - lower_h, lower_w, lower_h, "DIE")
    rect(ms, ox - die_block_w / 2, oy, die_block_w, die_block_h, "DIE")
    rect(ms, ox - upper_w / 2, oy + 95.0, upper_w, upper_h, "DIE")
    rect(ms, ox - (upper_w - 10) / 2, oy + 95.0 - clamp_h, upper_w - 10, clamp_h, "DIE")

    # U-bending punch
    punch_top = oy + 95.0 - clamp_h
    punch_bottom = oy + 46.0
    left = ox - spec.a1 / 2
    right = ox + spec.a1 / 2
    r = spec.r

    add_line(ms, (left, punch_bottom + r), (left, punch_top), "DIE")
    add_line(ms, (right, punch_bottom + r), (right, punch_top), "DIE")
    add_line(ms, (left + r, punch_bottom), (right - r, punch_bottom), "DIE")
    add_arc(ms, (left + r, punch_bottom + r), r, 180, 270, "DIE")
    add_arc(ms, (right - r, punch_bottom + r), r, 270, 360, "DIE")

    # Die cavity
    cavity_w = spec.a2 + 4.4
    cavity_depth = 18.0
    c_left = ox - cavity_w / 2
    c_right = ox + cavity_w / 2
    c_top = oy + die_block_h
    c_bot = oy + die_block_h - cavity_depth
    add_line(ms, (c_left, c_top), (c_left, c_bot), "DIE")
    add_line(ms, (c_right, c_top), (c_right, c_bot), "DIE")
    add_line(ms, (c_left, c_bot), (c_right, c_bot), "DIE")

    # Workpiece in section
    wp_y = oy + 28.0
    add_line(ms, (ox - spec.a2 / 2 + r, wp_y), (ox + spec.a2 / 2 - r, wp_y), "PART")
    add_line(ms, (ox - spec.a2 / 2, wp_y + r), (ox - spec.a2 / 2, wp_y + r + 20), "PART")
    add_line(ms, (ox + spec.a2 / 2, wp_y + r), (ox + spec.a2 / 2, wp_y + r + 20), "PART")
    add_arc(ms, (ox - spec.a2 / 2 + r, wp_y + r), r, 180, 270, "PART")
    add_arc(ms, (ox + spec.a2 / 2 - r, wp_y + r), r, 270, 360, "PART")

    # Guide posts
    for gx in (-guide_x, guide_x):
        rect(ms, ox + gx - 6, oy - lower_h, 12, 125.0 + lower_h, "GUIDE")
        add_text(ms, "导柱", ox + gx - 6, oy + 102, 2.5, "TEXT")

    centerline(ms, ox, oy - 35, ox, oy + 140)
    add_text(ms, "A-A剖视图", ox - 18, oy + 128, 4, "TEXT")
    add_text(ms, "上模座", ox - 65, oy + 104, 3.2, "TEXT")
    add_text(ms, "凸模固定板/垫板", ox - 62, oy + 84, 3.2, "TEXT")
    add_text(ms, "U形弯曲凸模", ox + 16, oy + 76, 3.2, "TEXT")
    add_text(ms, "凹模块", ox + 22, oy + 12, 3.2, "TEXT")
    add_text(ms, "下模座", ox + 20, oy - 18, 3.2, "TEXT")
    add_text(ms, "工件", ox + 26, oy + 46, 3.2, "TEXT")

    add_dim_aligned(ms, (ox - spec.a1 / 2, oy - 40), (ox + spec.a1 / 2, oy - 40), (ox, oy - 52), "DIM")
    add_dim_aligned(ms, (c_left, oy - 52), (c_right, oy - 52), (ox, oy - 64), "DIM")
    add_dim_rotated(ms, (ox + 82, wp_y), (ox + 82, wp_y + spec.b), (ox + 96, wp_y + spec.b / 2), 90, "DIM")


def draw_plan(ms, spec: PartSpec, ox: float, oy: float):
    die_len = 170.0
    die_w = 110.0
    rect(ms, ox - die_len / 2, oy - die_w / 2, die_len, die_w, "DIE")
    rect(ms, ox - 60.0, oy - 35.0, 120.0, 70.0, "DIE")

    # Material / part footprint
    rect(ms, ox - spec.a2 / 2, oy - spec.d / 2, spec.a2, spec.d, "PART")
    add_line(ms, (ox - spec.a1 / 2, oy - spec.d / 2), (ox - spec.a1 / 2, oy + spec.d / 2), "PART")
    add_line(ms, (ox + spec.a1 / 2, oy - spec.d / 2), (ox + spec.a1 / 2, oy + spec.d / 2), "PART")
    add_circle(ms, (ox, oy + spec.c / 2), spec.e / 2, "PART")
    add_circle(ms, (ox, oy - spec.c / 2), spec.e / 2, "PART")

    # Guide + fasteners
    for gx in (-58.0, 58.0):
        for gy in (-36.0, 36.0):
            add_circle(ms, (ox + gx, oy + gy), 8.0, "GUIDE")
    for gx in (-40.0, 40.0):
        add_circle(ms, (ox + gx, oy + 0.0), 5.0, "AUX")

    centerline(ms, ox - 80, oy, ox + 80, oy)
    centerline(ms, ox, oy - 60, ox, oy + 60)

    add_text(ms, "俯视图", ox - 22, oy + 68, 4, "TEXT")
    add_text(ms, f"2-%%c{spec.e:.0f}", ox + 8, oy + 4, 3.2, "TEXT")
    add_dim_aligned(ms, (ox - spec.a1 / 2, oy - 44), (ox + spec.a1 / 2, oy - 44), (ox, oy - 56), "DIM")
    add_dim_aligned(ms, (ox - spec.a2 / 2, oy - 56), (ox + spec.a2 / 2, oy - 56), (ox, oy - 68), "DIM")
    add_dim_rotated(ms, (ox + 34, oy - spec.c / 2), (ox + 34, oy + spec.c / 2), (ox + 48, oy), 90, "DIM")
    add_dim_rotated(ms, (ox + spec.a2 / 2 + 12, oy - spec.d / 2), (ox + spec.a2 / 2 + 12, oy + spec.d / 2), (ox + spec.a2 / 2 + 26, oy), 90, "DIM")


def draw_bom_notes(ms, spec: PartSpec, ox: float, oy: float):
    add_text(ms, "主要零件及说明", ox, oy, 4, "TEXT")
    note = (
        "1. 上模座\\P"
        "2. 凸模固定板/垫板\\P"
        "3. U形弯曲凸模\\P"
        "4. 导柱、导套\\P"
        "5. 凹模块\\P"
        "6. 下模座\\P"
        "7. 工件：U形支架，材料10钢，t=2.0\\P"
        "8. 暂定尺寸：A2=46，E=13，正式图需复核"
    )
    add_mtext(ms, note, ox, oy - 8, 90, "TEXT")


def draw_title(ms, ox: float, oy: float):
    rect(ms, ox, oy, 120, 28, "AUX")
    add_text(ms, "U形支架弯曲模", ox + 6, oy + 18, 4, "TEXT")
    add_text(ms, "总装草图（课程设计验证版）", ox + 6, oy + 10, 3.2, "TEXT")
    add_text(ms, "制图：AI辅助生成", ox + 6, oy + 3, 2.8, "TEXT")


def main():
    spec = PartSpec()
    acad = win32com.client.Dispatch("AutoCAD.Application")
    acad.Visible = True
    doc = com_retry(lambda: acad.Documents.Add(), timeout=30.0)
    time.sleep(1.5)
    ms = doc.ModelSpace

    for name, color in {
        "PART": 7,
        "DIE": 1,
        "DIM": 4,
        "CENTER": 2,
        "GUIDE": 3,
        "TEXT": 5,
        "AUX": 8,
    }.items():
        ensure_layer(doc, name, color)

    draw_section(ms, spec, ox=0.0, oy=0.0)
    draw_plan(ms, spec, ox=220.0, oy=18.0)
    draw_bom_notes(ms, spec, ox=310.0, oy=-70.0)
    draw_title(ms, ox=-95.0, oy=-95.0)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = OUT_DIR / f"u_bracket_bending_die_assembly_cn_{stamp}.dwg"
    com_retry(lambda: doc.SendCommand("_ZOOM _E\n"), timeout=10.0)
    time.sleep(1.0)
    com_retry(lambda: doc.SaveAs(str(out_path)), timeout=20.0)

    print(f"saved={out_path}")
    print("type=assembly_sketch")
    print("scope=section+plan+notes")


if __name__ == "__main__":
    main()
