"""Generate the original animated GIFs used by the profile README."""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

COLORS = {
    "bg": (7, 17, 31),
    "panel": (7, 21, 33),
    "panel_2": (13, 37, 48),
    "border": (40, 69, 88),
    "grid": (19, 42, 57),
    "muted": (100, 116, 139),
    "text": (226, 232, 240),
    "subtext": (148, 163, 184),
    "teal": (94, 234, 212),
    "teal_2": (45, 212, 191),
    "blue": (56, 189, 248),
    "amber": (251, 191, 36),
    "rose": (251, 113, 133),
    "green": (52, 211, 153),
}

FONT_DIR = Path("C:/Windows/Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


FONTS = {
    "ui_13": font("segoeui.ttf", 13),
    "ui_14": font("segoeui.ttf", 14),
    "ui_15": font("segoeui.ttf", 15),
    "ui_16": font("segoeui.ttf", 16),
    "ui_17": font("segoeui.ttf", 17),
    "ui_24": font("segoeui.ttf", 24),
    "ui_b14": font("segoeuib.ttf", 14),
    "ui_b16": font("segoeuib.ttf", 16),
    "ui_b20": font("segoeuib.ttf", 20),
    "ui_b58": font("segoeuib.ttf", 58),
    "mono_12": font("consola.ttf", 12),
    "mono_13": font("consola.ttf", 13),
    "mono_15": font("consola.ttf", 15),
    "mono_b14": font("consolab.ttf", 14),
}


@lru_cache(maxsize=4)
def gradient_base(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, COLORS["bg"])
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            horizontal = x / max(width - 1, 1)
            vertical = y / max(height - 1, 1)
            glow = max(0.0, 1.0 - math.hypot((x - width * 0.9) / width, (y - height * 0.05) / height))
            pixels[x, y] = (
                int(7 + horizontal * 7),
                int(17 + horizontal * 21 + glow * 8),
                int(31 + vertical * 9 + glow * 11),
            )
    return image


def gradient_canvas(size: tuple[int, int]) -> Image.Image:
    return gradient_base(size).copy()


def rounded_panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int = 18) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=COLORS["panel"], outline=COLORS["border"], width=2)


def glow_dot(image: Image.Image, center: tuple[int, int], color: tuple[int, int, int], radius: int = 7) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    for r, alpha in ((radius * 3, 18), (radius * 2, 34), (radius + 3, 70)):
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*color, alpha))
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(*color, 255))
    image.paste(overlay, (0, 0), overlay)


def hero_frame(index: int, total: int = 36) -> Image.Image:
    image = gradient_canvas((1200, 360))
    draw = ImageDraw.Draw(image)

    for x in range(0, 1200, 32):
        draw.line((x, 0, x, 360), fill=COLORS["grid"], width=1)
    for y in range(0, 360, 32):
        draw.line((0, y, 1200, y), fill=COLORS["grid"], width=1)
    draw.rounded_rectangle((1, 1, 1198, 358), radius=28, outline=COLORS["border"], width=2)

    for x, color in ((60, COLORS["rose"]), (78, COLORS["amber"]), (96, COLORS["green"])):
        draw.ellipse((x - 5, 43, x + 5, 53), fill=color)
    draw.text((116, 39), "MOHAMED@GITHUB:~/PROFILE", font=FONTS["mono_12"], fill=COLORS["muted"])

    draw.rounded_rectangle((62, 90, 405, 122), radius=16, fill=(15, 44, 54), outline=(29, 87, 96), width=1)
    glow_dot(image, (80, 106), COLORS["teal"], radius=4)
    draw.text((94, 95), "FULL-STACK  ·  AI SYSTEMS  ·  DEVOPS", font=FONTS["ui_b14"], fill=COLORS["teal"])

    draw.text((58, 138), "Mohamed Anwar", font=FONTS["ui_b58"], fill=COLORS["teal"])
    draw.text((62, 211), "I turn complex workflows into dependable products.", font=FONTS["ui_24"], fill=COLORS["text"])

    role = "React · NestJS · FastAPI · RAG · Docker · Kubernetes"
    reveal = min(len(role), max(1, int((index / (total - 1)) * (len(role) + 16))))
    draw.text((62, 256), role[:reveal], font=FONTS["ui_17"], fill=COLORS["subtext"])
    if index % 8 < 5:
        cursor_x = 62 + draw.textlength(role[:reveal], font=FONTS["ui_17"])
        draw.rectangle((cursor_x + 3, 258, cursor_x + 5, 277), fill=COLORS["blue"])

    draw.polygon(((62, 303), (68, 297), (74, 303), (68, 309)), fill=COLORS["blue"])
    draw.text((82, 294), "Tenkasi, India", font=FONTS["ui_14"], fill=COLORS["text"])
    draw.polygon(((204, 303), (210, 297), (216, 303), (210, 309)), fill=COLORS["teal"])
    draw.text((224, 294), "Open to full-time roles", font=FONTS["ui_14"], fill=COLORS["text"])

    rounded_panel(draw, (803, 48, 1133, 315), radius=22)
    draw.text((830, 68), "END-TO-END BUILD PATH", font=FONTS["mono_12"], fill=COLORS["muted"])
    draw.line((851, 111, 851, 274), fill=COLORS["border"], width=2)

    stages = [
        ("01", "INTERFACE", "React", COLORS["teal"]),
        ("02", "SERVICES", "Nest", COLORS["teal_2"]),
        ("03", "INTELLIGENCE", "RAG", COLORS["blue"]),
        ("04", "DELIVERY", "K8s", COLORS["amber"]),
    ]
    active = (index // 5) % len(stages)
    for stage_index, (number, label, tech, color) in enumerate(stages):
        y = 120 + stage_index * 50
        is_active = stage_index == active
        if is_active:
            glow_dot(image, (851, y), color, radius=8)
        else:
            draw.ellipse((845, y - 6, 857, y + 6), fill=(45, 61, 75))
        fill = (13, 50, 61) if is_active else COLORS["panel_2"]
        outline = color if is_active else (31, 75, 85)
        draw.rounded_rectangle((879, y - 20, 1099, y + 20), radius=10, fill=fill, outline=outline, width=1)
        draw.text((896, y - 10), f"{number}  {label}", font=FONTS["ui_b14"], fill=COLORS["text"] if is_active else (199, 210, 221))
        tech_width = draw.textlength(tech, font=FONTS["mono_12"])
        draw.text((1080 - tech_width, y - 8), tech, font=FONTS["mono_12"], fill=COLORS["muted"])

    return image


def rag_frame(index: int, total: int = 30) -> Image.Image:
    image = gradient_canvas((760, 270))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, 758, 268), radius=24, outline=COLORS["border"], width=2)
    draw.text((30, 25), "RAG WORKFLOW", font=FONTS["ui_b20"], fill=COLORS["teal"])
    draw.text((30, 57), "Useful context in. Grounded answers out.", font=FONTS["ui_15"], fill=COLORS["subtext"])

    nodes = [
        ((98, 164), "01", "QUERY", COLORS["blue"]),
        ((240, 164), "02", "RETRIEVE", COLORS["teal"]),
        ((380, 164), "03", "CONTEXT", COLORS["teal_2"]),
        ((520, 164), "04", "LLM", COLORS["amber"]),
        ((660, 164), "05", "ANSWER", COLORS["green"]),
    ]
    for node_index in range(len(nodes) - 1):
        start = nodes[node_index][0]
        end = nodes[node_index + 1][0]
        draw.line((start[0] + 42, start[1], end[0] - 42, end[1]), fill=COLORS["border"], width=3)
        draw.polygon(((end[0] - 48, end[1] - 5), (end[0] - 38, end[1]), (end[0] - 48, end[1] + 5)), fill=COLORS["border"])

    active_position = (index / total) * (len(nodes) - 1)
    active_segment = min(len(nodes) - 2, int(active_position))
    progress = active_position - active_segment
    start = nodes[active_segment][0]
    end = nodes[active_segment + 1][0]
    pulse_x = int(start[0] + (end[0] - start[0]) * progress)
    glow_dot(image, (pulse_x, 164), COLORS["blue"], radius=5)

    active_node = (index // 6) % len(nodes)
    for node_index, (center, number, label, color) in enumerate(nodes):
        cx, cy = center
        is_active = node_index == active_node
        if is_active:
            glow_dot(image, center, color, radius=31)
        draw.ellipse((cx - 32, cy - 32, cx + 32, cy + 32), fill=COLORS["panel_2"], outline=color if is_active else COLORS["border"], width=3 if is_active else 2)
        number_width = draw.textlength(number, font=FONTS["mono_b14"])
        draw.text((cx - number_width / 2, cy - 10), number, font=FONTS["mono_b14"], fill=color)
        label_width = draw.textlength(label, font=FONTS["ui_b14"])
        draw.text((cx - label_width / 2, 215), label, font=FONTS["ui_b14"], fill=COLORS["text"] if is_active else COLORS["subtext"])

    return image


def save_gif(path: Path, frames: list[Image.Image], duration: int) -> None:
    shared_palette = frames[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    palette_frames = [
        frame.quantize(palette=shared_palette, dither=Image.Dither.NONE)
        for frame in frames
    ]
    palette_frames[0].save(
        path,
        save_all=True,
        append_images=palette_frames[1:],
        optimize=False,
        duration=duration,
        loop=0,
        disposal=2,
    )


def main() -> None:
    hero_frames = [hero_frame(i) for i in range(36)]
    rag_frames = [rag_frame(i) for i in range(30)]
    save_gif(ASSETS / "profile-terminal.gif", hero_frames, 95)
    save_gif(ASSETS / "rag-workflow.gif", rag_frames, 105)
    rag_frames[0].save(ASSETS / "rag-workflow-static.png", optimize=True)
    for path in (ASSETS / "profile-terminal.gif", ASSETS / "rag-workflow.gif"):
        print(f"generated {path.relative_to(ROOT)} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
