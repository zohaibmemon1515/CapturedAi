import streamlit as st
import os
import subprocess
import random
import tempfile
from PIL import Image, ImageDraw, ImageFont

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="CAPTURED AI", page_icon="🖥️", layout="wide")

# =========================
# PREMIUM LIGHT THEME CSS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Sora:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif !important;
    }

    .stApp {
        background: #f0f2f5 !important;
        color: #1a1d23 !important;
    }

    /* Main header */
    .app-header {
        background: white;
        border: 1px solid #e2e6ec;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .app-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        font-family: 'Sora', sans-serif;
        letter-spacing: -0.02em;
    }

    .app-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 4px;
        letter-spacing: 0.04em;
    }

    /* Pill badges */
    .badge-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }

    .badge {
        background: white;
        border: 1px solid #e2e6ec;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.75rem;
        color: #475569;
        font-family: 'Sora', sans-serif;
        font-weight: 500;
        display: inline-block;
    }

    .badge-blue { border-color: #bfdbfe; background: #eff6ff; color: #1d4ed8; }
    .badge-green { border-color: #bbf7d0; background: #f0fdf4; color: #15803d; }
    .badge-amber { border-color: #fde68a; background: #fffbeb; color: #b45309; }
    .badge-purple { border-color: #ddd6fe; background: #f5f3ff; color: #6d28d9; }

    /* Section cards */
    .section-card {
        background: white;
        border: 1px solid #e2e6ec;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 16px;
    }

    .section-title {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        margin-bottom: 16px;
        font-family: 'Sora', sans-serif;
        display: flex;
        align-items: center;
        gap: 8px;
        padding-bottom: 10px;
        border-bottom: 1px solid #f1f5f9;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background: #f8fafc !important;
        border: 1px solid #e2e6ec !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
        transition: border-color 0.15s, box-shadow 0.15s !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12) !important;
        background: white !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #f8fafc !important;
        border: 1px solid #e2e6ec !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-family: 'Sora', sans-serif !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: #f8fafc !important;
        border: 1px solid #e2e6ec !important;
        border-radius: 10px !important;
    }

    /* Labels */
    label, .stTextInput label, .stSelectbox label {
        color: #475569 !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }

    /* Generate button */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 12px 32px !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
        border-radius: 4px !important;
    }

    .stProgress > div > div {
        background: #e2e8f0 !important;
        border-radius: 4px !important;
    }

    /* Task cin card */
    .cin-task-card {
        background: #f8fafc;
        border: 1px solid #e8ecf1;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }

    .cin-task-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }

    .cin-task-name {
        font-weight: 600;
        font-size: 0.85rem;
        color: #1e293b;
        font-family: 'Sora', sans-serif;
    }

    .cin-badge {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #c2410c;
        font-size: 0.68rem;
        padding: 2px 8px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }

    /* Template cards */
    .template-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 4px;
    }

    .template-preview {
        border: 2px solid #e2e6ec;
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
        transition: border-color 0.15s, box-shadow 0.15s;
    }

    .template-preview:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }

    .template-preview.selected {
        border-color: #2563eb;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.2);
    }

    .tmpl-bar {
        height: 22px;
        display: flex;
        align-items: center;
        padding: 0 10px;
        gap: 5px;
    }

    .tmpl-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
    }

    .tmpl-code-area {
        padding: 8px 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 7.5px;
        line-height: 1.65;
    }

    .tmpl-footer {
        padding: 8px 10px 10px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    .tmpl-name {
        font-size: 0.78rem;
        font-weight: 600;
        color: #1e293b;
        font-family: 'Sora', sans-serif;
    }

    .tmpl-desc {
        font-size: 0.69rem;
        color: #64748b;
        margin-top: 2px;
    }

    /* Success box */
    .success-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 16px 20px;
        color: #166534;
        font-family: 'Sora', sans-serif;
        font-size: 0.875rem;
        margin-top: 16px;
        line-height: 1.7;
    }

    /* Info box */
    .stInfo {
        background: #eff6ff !important;
        border-color: #bfdbfe !important;
        color: #1d4ed8 !important;
        border-radius: 10px !important;
    }

    /* Warning box */
    .stWarning {
        border-radius: 10px !important;
    }

    /* Divider */
    hr {
        border: none !important;
        border-top: 1px solid #e2e6ec !important;
        margin: 20px 0 !important;
    }

    /* Column spacing */
    [data-testid="column"] {
        padding: 0 6px !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)


# =========================
# FONT LOADING
# =========================
def get_font(size, bold=False):
    font_options = [
        "consola.ttf", "Consolas.ttf", "consolab.ttf",
        "DejaVuSansMono.ttf", "cour.ttf", "LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]
    for f in font_options:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()


# =========================
# TEMPLATE DEFINITIONS
# =========================
TEMPLATES = {
    "Catppuccin Mocha": {
        "code_bg": (30, 30, 46),
        "bar_bg": (49, 50, 68),
        "gutter_bg": (24, 24, 37),
        "border": (69, 71, 90),
        "line_num": (69, 71, 90),
        "alt_row": (27, 27, 42),
        "status_bg": (24, 24, 37),
        "status_text": (69, 71, 90),
        "title_text": (166, 173, 200),
        "tab_bg": (30, 30, 46),
        "tab_active": (49, 50, 68),
        "tab_text": (205, 214, 244),
        "syntax": {
            "comment": (108, 112, 134),
            "preprocessor": (203, 166, 247),
            "output": (137, 180, 250),
            "input_cin": (148, 226, 213),
            "declaration": (249, 226, 175),
            "control": (203, 166, 247),
            "default": (205, 214, 244),
        },
        "term_bg": (30, 30, 46),
        "term_bar": (49, 50, 68),
        "term_prompt": (166, 227, 161),
        "term_input": (148, 226, 213),
        "term_output": (205, 214, 244),
        "term_error": (243, 139, 168),
        "term_status_ok": (166, 227, 161),
        "term_status_warn": (249, 226, 175),
    },
    "GitHub Dark": {
        "code_bg": (13, 17, 23),
        "bar_bg": (22, 27, 34),
        "gutter_bg": (17, 22, 29),
        "border": (48, 54, 61),
        "line_num": (70, 80, 94),
        "alt_row": (15, 20, 27),
        "status_bg": (17, 22, 29),
        "status_text": (70, 80, 94),
        "title_text": (140, 150, 165),
        "tab_bg": (17, 22, 29),
        "tab_active": (22, 27, 34),
        "tab_text": (200, 210, 220),
        "syntax": {
            "comment": (106, 153, 85),
            "preprocessor": (197, 134, 192),
            "output": (86, 156, 214),
            "input_cin": (78, 201, 176),
            "declaration": (244, 180, 30),
            "control": (197, 134, 192),
            "default": (220, 223, 228),
        },
        "term_bg": (12, 12, 12),
        "term_bar": (30, 30, 30),
        "term_prompt": (80, 200, 80),
        "term_input": (78, 201, 176),
        "term_output": (220, 220, 220),
        "term_error": (255, 80, 80),
        "term_status_ok": (80, 200, 80),
        "term_status_warn": (200, 150, 50),
    },
    "GitHub Light": {
        "code_bg": (255, 255, 255),
        "bar_bg": (246, 248, 250),
        "gutter_bg": (250, 251, 252),
        "border": (208, 215, 222),
        "line_num": (140, 149, 159),
        "alt_row": (248, 250, 252),
        "status_bg": (246, 248, 250),
        "status_text": (140, 149, 159),
        "title_text": (101, 109, 118),
        "tab_bg": (246, 248, 250),
        "tab_active": (255, 255, 255),
        "tab_text": (36, 41, 47),
        "syntax": {
            "comment": (110, 119, 129),
            "preprocessor": (130, 80, 223),
            "output": (5, 80, 174),
            "input_cin": (3, 101, 111),
            "declaration": (134, 46, 18),
            "control": (130, 80, 223),
            "default": (36, 41, 47),
        },
        "term_bg": (255, 255, 255),
        "term_bar": (246, 248, 250),
        "term_prompt": (31, 136, 61),
        "term_input": (3, 101, 111),
        "term_output": (36, 41, 47),
        "term_error": (207, 34, 46),
        "term_status_ok": (31, 136, 61),
        "term_status_warn": (130, 80, 0),
    },
}


# =========================
# SYNTAX HIGHLIGHTING
# =========================
def get_line_color(line, tmpl_name):
    t = TEMPLATES[tmpl_name]
    s = t["syntax"]
    stripped = line.strip()
    if stripped.startswith("//"):
        return s["comment"]
    if stripped.startswith("#"):
        return s["preprocessor"]
    if "cout" in stripped:
        return s["output"]
    if "cin" in stripped:
        return s["input_cin"]
    if any(stripped.startswith(k + " ") for k in ["int ", "float ", "char ", "string ", "bool "]):
        return s["declaration"]
    if stripped.startswith("return"):
        return s["control"]
    if any(stripped.startswith(k) for k in ["if", "else", "for", "while", "do"]):
        return s["control"]
    return s["default"]


# =========================
# CODE SCREENSHOT
# =========================
def create_code_screenshot(code, filename, task_num, title="Source Code", tmpl_name="GitHub Dark"):
    t = TEMPLATES[tmpl_name]
    lines = code.split("\n")

    font_size = 16
    line_height = 26
    char_width = 9.6
    left_margin = 70
    right_margin = 30
    top_margin = 90
    bottom_margin = 40

    max_line_len = max((len(l) for l in lines), default=40)
    width = max(750, int(left_margin + max_line_len * char_width + right_margin))
    height = top_margin + len(lines) * line_height + bottom_margin

    img = Image.new("RGB", (width, height), t["code_bg"])
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([0, 0, width - 1, height - 1], outline=t["border"], width=1)

    # Title bar
    draw.rectangle([0, 0, width, 48], fill=t["bar_bg"])
    draw.line([0, 48, width, 48], fill=t["border"], width=1)

    # Traffic lights
    draw.ellipse([16, 16, 30, 30], fill=(255, 95, 87))
    draw.ellipse([42, 16, 56, 30], fill=(255, 189, 46))
    draw.ellipse([68, 16, 82, 30], fill=(39, 201, 63))

    # Title
    font_title = get_font(14)
    title_text = f"task_{task_num:02d}.cpp — {title}"
    draw.text((width // 2 - len(title_text) * 4, 16), title_text, fill=t["title_text"], font=font_title)

    # Tab bar
    draw.rectangle([0, 48, width, 72], fill=t["tab_bg"])
    draw.rectangle([0, 48, 200, 72], fill=t["tab_active"])
    draw.line([0, 72, width, 72], fill=t["border"], width=1)
    draw.text((14, 54), f"  task_{task_num:02d}.cpp", fill=t["tab_text"], font=get_font(13))

    # Gutter
    draw.rectangle([0, 72, left_margin - 10, height], fill=t["gutter_bg"])
    draw.line([left_margin - 10, 72, left_margin - 10, height], fill=t["border"], width=1)

    font_code = get_font(font_size)

    for i, line in enumerate(lines):
        y = top_margin + i * line_height - 18

        # Line number
        ln_text = str(i + 1)
        draw.text((left_margin - 10 - len(ln_text) * 7 - 4, y), ln_text, fill=t["line_num"], font=get_font(13))

        # Alternate row
        if i % 2 == 0:
            draw.rectangle([left_margin - 9, y - 2, width - 1, y + line_height - 4], fill=t["alt_row"])

        # Code
        color = get_line_color(line, tmpl_name)
        draw.text((left_margin, y), line, fill=color, font=font_code)

    # Status bar
    draw.rectangle([0, height - 24, width, height], fill=t["status_bg"])
    draw.line([0, height - 24, width, height - 24], fill=t["border"], width=1)
    draw.text((14, height - 18), f"  C++   UTF-8   Lines: {len(lines)}", fill=t["status_text"], font=get_font(12))

    img.save(filename, quality=95)


# =========================
# OUTPUT SCREENSHOT — 3 FULLY DIFFERENT LAYOUTS
# =========================
def create_output_screenshot(output_text, filename, task_num, actual_output=True, tmpl_name="GitHub Dark"):
    t = TEMPLATES[tmpl_name]
    lines = output_text.split("\n")
    font_size = 16
    line_height = 26
    left_margin = 20
    max_len = max((len(l) for l in lines), default=40)

    # -------------------------------------------------------
    # TEMPLATE 1: Catppuccin Mocha
    # Layout: macOS-style terminal, rounded top bar, sidebar
    # with task info panel on the left, output on the right
    # -------------------------------------------------------
    if tmpl_name == "Catppuccin Mocha":
        sidebar_w = 180
        content_left = sidebar_w + 1
        top_margin = 88
        bottom_margin = 36
        width = max(720, int(content_left + left_margin + max_len * 9.6 + 40))
        height = top_margin + len(lines) * line_height + bottom_margin

        img = Image.new("RGB", (width, height), t["term_bg"])
        draw = ImageDraw.Draw(img)

        # Outer rounded border simulation
        draw.rectangle([0, 0, width - 1, height - 1], outline=t["border"], width=1)

        # Title bar — full width, macOS style
        draw.rectangle([0, 0, width, 46], fill=t["term_bar"])
        draw.line([0, 46, width, 46], fill=t["border"], width=1)

        # Traffic lights
        draw.ellipse([16, 15, 28, 27], fill=(255, 95, 87))
        draw.ellipse([38, 15, 50, 27], fill=(255, 189, 46))
        draw.ellipse([60, 15, 72, 27], fill=(39, 201, 63))

        # Title centered
        title = f"Task {task_num:02d}.cpp — Output"
        draw.text((width // 2 - len(title) * 4, 14), title, fill=t["title_text"], font=get_font(14))

        # Tab bar
        tab_bg = (24, 24, 37)
        draw.rectangle([0, 46, width, 68], fill=tab_bg)
        draw.rectangle([0, 46, 180, 68], fill=t["term_bar"])
        draw.line([0, 68, width, 68], fill=t["border"], width=1)
        draw.text((14, 52), "  Output", fill=(148, 226, 213), font=get_font(13))
        draw.text((200, 52), "  Console", fill=(108, 112, 134), font=get_font(13))

        # Sidebar background
        draw.rectangle([0, 68, sidebar_w, height], fill=(20, 20, 35))
        draw.line([sidebar_w, 68, sidebar_w, height], fill=t["border"], width=1)

        # Sidebar content
        sb_y = 80
        draw.text((10, sb_y), "EXPLORER", fill=(108, 112, 134), font=get_font(11))
        sb_y += 22
        draw.text((10, sb_y), f"  task_{task_num:02d}.cpp", fill=(203, 166, 247), font=get_font(13))
        sb_y += 20
        draw.text((10, sb_y), f"  task_{task_num:02d}.exe", fill=(148, 226, 213), font=get_font(13))
        sb_y += 28
        draw.text((10, sb_y), "TERMINAL", fill=(108, 112, 134), font=get_font(11))
        sb_y += 18
        draw.text((10, sb_y), "  bash", fill=(166, 227, 161), font=get_font(13))
        sb_y += 36
        draw.text((10, sb_y), "STATUS", fill=(108, 112, 134), font=get_font(11))
        sb_y += 18
        ok_color = (166, 227, 161) if actual_output else (249, 226, 175)
        ok_text = "  OK (code 0)" if actual_output else "  Simulated"
        draw.text((10, sb_y), ok_text, fill=ok_color, font=get_font(13))

        # Prompt lines in content area
        px = content_left + left_margin
        prompt_y = 76
        draw.text((px, prompt_y), f"~  g++ task_{task_num:02d}.cpp", fill=(108, 112, 134), font=get_font(14))
        draw.text((px, prompt_y + 22), f"~  ./task_{task_num:02d}", fill=(166, 227, 161), font=get_font(14))

        # Output lines
        font_out = get_font(font_size)
        y = top_margin + 18
        for line in lines:
            if line.startswith(">>"):
                draw.text((px, y), line, fill=t["term_input"], font=font_out)
            elif "Error" in line or "error" in line:
                draw.text((px, y), line, fill=t["term_error"], font=font_out)
            else:
                draw.text((px, y), line, fill=t["term_output"], font=font_out)
            y += line_height

        # Status bar
        draw.rectangle([0, height - 22, width, height], fill=(24, 24, 37))
        draw.line([0, height - 22, width, height - 22], fill=t["border"], width=1)
        draw.text((sidebar_w + 10, height - 17), f"  bash   UTF-8   Ln {len(lines)}", fill=(108, 112, 134), font=get_font(12))
        draw.rectangle([0, height - 22, sidebar_w, height], fill=(20, 20, 35))
        draw.text((10, height - 17), "  Catppuccin", fill=(108, 112, 134), font=get_font(12))

    # -------------------------------------------------------
    # TEMPLATE 2: GitHub Dark
    # Layout: Classic Windows CMD / black terminal
    # Full-width black box, no sidebar, old-school DOS prompt
    # -------------------------------------------------------
    elif tmpl_name == "GitHub Dark":
        top_margin = 100
        bottom_margin = 30
        width = max(700, int(left_margin + max_len * 9.8 + 40))
        height = top_margin + len(lines) * line_height + bottom_margin

        img = Image.new("RGB", (width, height), (10, 10, 10))
        draw = ImageDraw.Draw(img)

        # Outer border — thin white
        draw.rectangle([0, 0, width - 1, height - 1], outline=(60, 60, 60), width=1)

        # Windows-style title bar — flat dark gray
        draw.rectangle([0, 0, width, 30], fill=(48, 48, 48))
        # Windows minimize/max/close boxes on the RIGHT
        draw.rectangle([width - 84, 0, width - 56, 30], fill=(60, 60, 60))
        draw.rectangle([width - 56, 0, width - 28, 30], fill=(60, 60, 60))
        draw.rectangle([width - 28, 0, width, 30], fill=(196, 43, 28))
        draw.text((width - 78, 8), "—", fill=(220, 220, 220), font=get_font(12))
        draw.text((width - 48, 6), "□", fill=(220, 220, 220), font=get_font(14))
        draw.text((width - 20, 8), "✕", fill=(255, 255, 255), font=get_font(12))

        # Title left-aligned — CMD style
        cmd_icon = "C:\\>"
        draw.text((10, 8), f"Command Prompt — task_{task_num:02d}.cpp", fill=(204, 204, 204), font=get_font(13))

        # Separator line
        draw.line([0, 30, width, 30], fill=(80, 80, 80), width=1)

        # CMD prompt lines — DOS style
        prompt_y = 38
        draw.text((left_margin, prompt_y),
                  f"Microsoft Windows [Version 10.0.26100]", fill=(180, 180, 180), font=get_font(14))
        draw.text((left_margin, prompt_y + 20),
                  f"(c) Microsoft Corporation. All rights reserved.", fill=(120, 120, 120), font=get_font(13))
        draw.text((left_margin, prompt_y + 40),
                  f"C:\\Users\\Student\\Lab> g++ task_{task_num:02d}.cpp -o task_{task_num:02d}.exe", fill=(80, 200, 80), font=get_font(14))
        draw.text((left_margin, prompt_y + 58),
                  f"C:\\Users\\Student\\Lab> task_{task_num:02d}.exe", fill=(80, 200, 80), font=get_font(14))

        # Output lines
        font_out = get_font(font_size)
        y = top_margin + 10
        for line in lines:
            if line.startswith(">>"):
                draw.text((left_margin, y), line, fill=(78, 201, 176), font=font_out)
            elif "Error" in line or "error" in line:
                draw.text((left_margin, y), line, fill=(255, 80, 80), font=font_out)
            else:
                draw.text((left_margin, y), line, fill=(204, 204, 204), font=font_out)
            y += line_height

        # Blinking cursor effect
        draw.text((left_margin, y + 4), "C:\\Users\\Student\\Lab> _", fill=(80, 200, 80), font=get_font(14))

    # -------------------------------------------------------
    # TEMPLATE 3: GitHub Light
    # Layout: VS Code integrated terminal panel
    # Light theme, panel tabs (TERMINAL / PROBLEMS / OUTPUT),
    # PS> prompt style, clean white background
    # -------------------------------------------------------
    else:
        panel_header_h = 34
        tab_h = 28
        prompt_section_h = 52
        top_margin = panel_header_h + tab_h + prompt_section_h
        bottom_margin = 32
        width = max(700, int(left_margin + max_len * 9.8 + 40))
        height = top_margin + len(lines) * line_height + bottom_margin

        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Outer border
        draw.rectangle([0, 0, width - 1, height - 1], outline=(208, 215, 222), width=1)

        # VS Code panel header bar (drag bar)
        draw.rectangle([0, 0, width, panel_header_h], fill=(246, 248, 250))
        draw.line([0, panel_header_h, width, panel_header_h], fill=(208, 215, 222), width=1)

        # Panel tab row
        tab_y = panel_header_h
        draw.rectangle([0, tab_y, width, tab_y + tab_h], fill=(246, 248, 250))
        draw.line([0, tab_y + tab_h, width, tab_y + tab_h], fill=(208, 215, 222), width=1)

        # Active tab: TERMINAL
        draw.rectangle([0, tab_y, 90, tab_y + tab_h], fill=(255, 255, 255))
        draw.line([0, tab_y + tab_h - 1, 90, tab_y + tab_h - 1], fill=(255, 255, 255), width=2)
        draw.text((8, tab_y + 7), "TERMINAL", fill=(36, 41, 47), font=get_font(12))
        # Inactive tabs
        draw.text((100, tab_y + 7), "PROBLEMS", fill=(140, 149, 159), font=get_font(12))
        draw.text((195, tab_y + 7), "OUTPUT", fill=(140, 149, 159), font=get_font(12))
        draw.text((265, tab_y + 7), "DEBUG CONSOLE", fill=(140, 149, 159), font=get_font(12))

        # Right-side controls in tab bar
        draw.text((width - 80, tab_y + 7), "+ ∨  ×", fill=(140, 149, 159), font=get_font(13))

        # Panel title in header
        draw.text((left_margin, 10), f"task_{task_num:02d}.cpp — Integrated Terminal", fill=(101, 109, 118), font=get_font(13))

        # PS prompt area — light teal background strip
        ps_y = panel_header_h + tab_h
        draw.rectangle([0, ps_y, width, ps_y + prompt_section_h], fill=(240, 249, 255))
        draw.line([0, ps_y + prompt_section_h, width, ps_y + prompt_section_h], fill=(208, 215, 222), width=1)

        draw.text((left_margin, ps_y + 8),
                  f"PS C:\\Lab> g++ task_{task_num:02d}.cpp -o task_{task_num:02d}",
                  fill=(3, 101, 111), font=get_font(14))
        draw.text((left_margin, ps_y + 28),
                  f"PS C:\\Lab> .\\task_{task_num:02d}.exe",
                  fill=(3, 101, 111), font=get_font(14))

        # Output lines on white
        font_out = get_font(font_size)
        y = top_margin + 10
        for line in lines:
            if line.startswith(">>"):
                draw.text((left_margin, y), line, fill=(3, 101, 111), font=font_out)
            elif "Error" in line or "error" in line:
                draw.text((left_margin, y), line, fill=(207, 34, 46), font=font_out)
            else:
                draw.text((left_margin, y), line, fill=(36, 41, 47), font=font_out)
            y += line_height

        # Bottom status bar — VS Code style blue
        draw.rectangle([0, height - 22, width, height], fill=(0, 120, 212))
        status = "  ✓ Process exited with code 0" if actual_output else "  ⚠ Simulated Output"
        draw.text((10, height - 17), status, fill=(255, 255, 255), font=get_font(12))
        draw.text((width - 120, height - 17), f"UTF-8   C++   Ln {len(lines)}", fill=(200, 230, 255), font=get_font(12))

    img.save(filename, quality=95)


# =========================
# C++ FORMATTER
# =========================
def format_cpp(code):
    lines = code.split("\n")
    formatted = []
    indent = 0
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            formatted.append("")
            continue
        if line.startswith("}"):
            indent = max(0, indent - 1)
        formatted.append("    " * indent + line)
        if line.endswith("{") and not line.endswith("{}"):
            indent += 1
    return "\n".join(formatted)


# =========================
# TASK DEFINITIONS
# =========================
def get_task(task_num, name, inputs=None):
    v1 = random.randint(10, 50)
    v2 = random.randint(2, 9)
    v3 = random.randint(100, 999)

    tasks = {
        "01": (f'cout << "Hello World!" << endl;\ncout << "Lab Setup by: {name}";', False, [], "Hello World + Name"),
        "02": ('cout << "*" << endl;\ncout << "**" << endl;\ncout << "***" << endl;\ncout << "****" << endl;\ncout << "*****";', False, [], "Star Triangle Pattern"),
        "03": ('char ch;\ncin >> ch;\nif(ch==\'a\'||ch==\'e\'||ch==\'i\'||ch==\'o\'||ch==\'u\')\n    cout << ch << " is a Vowel";\nelse\n    cout << ch << " is a Consonant";', True, [("Enter a character (e.g. a, b, x):", "char", "a")], "Vowel or Consonant"),
        "04": ('string u, p;\ncin >> u >> p;\nif(u=="admin" && p=="1234")\n    cout << "Access Granted!";\nelse\n    cout << "Access Denied!";', True, [("Enter username:", "str", "admin"), ("Enter password:", "str", "1234")], "Login System"),
        "05": ('int a, b, c;\ncin >> a >> b >> c;\ncout << "Max of " << a << ", " << b << ", " << c;\ncout << " is: " << max(a, max(b, c));', True, [("Enter 1st number:", "int", "15"), ("Enter 2nd number:", "int", "30"), ("Enter 3rd number:", "int", "22")], "Max of 3 Numbers"),
        "06": ('int n;\ncin >> n;\nif(n > 0)\n    cout << n << " is Positive";\nelse if(n < 0)\n    cout << n << " is Negative";\nelse\n    cout << "Number is Zero";', True, [("Enter a number:", "int", "42")], "Positive/Negative Check"),
        "07": (f'int n={v2}, s=0;\nfor(int i=1; i<=n; i++)\n    s += i;\ncout << "Sum of first " << n << " numbers: " << s << endl;\ncout << "Average: " << (float)s/n;', False, [], f"Sum & Average of 1 to {v2}"),
        "08": ('int d;\ncin >> d;\nstring days[]={"","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"};\nif(d>=1 && d<=7)\n    cout << "Day " << d << ": " << days[d] << " | " << (d>=6 ? "Weekend" : "Weekday");\nelse\n    cout << "Invalid day number";', True, [("Enter day number (1-7):", "int", "3")], "Day of Week Checker"),
        "09": ('float a, b;\ncin >> a >> b;\ncout << a << " + " << b << " = " << a+b << endl;\ncout << a << " - " << b << " = " << a-b << endl;\ncout << a << " * " << b << " = " << a*b << endl;\ncout << a << " / " << b << " = " << a/b;', True, [("Enter first number:", "float", "25.5"), ("Enter second number:", "float", "4.2")], "Basic Calculator"),
        "10": ('int choice;\ncin >> choice;\nif(choice==1)\n    cout << "Order: Burger - Rs.350";\nelse if(choice==2)\n    cout << "Order: Pizza - Rs.650";\nelse if(choice==3)\n    cout << "Order: Pasta - Rs.450";\nelse\n    cout << "Invalid choice";', True, [("Enter menu choice (1=Burger, 2=Pizza, 3=Pasta):", "int", "2")], "Restaurant Menu"),
        "11": ('float g;\ncin >> g;\ncout << g << " Grams = " << g/1000 << " Kilograms" << endl;\ncout << g << " Grams = " << g*0.001 << " KG (scientific)";', True, [("Enter weight in grams:", "float", "2500")], "Gram to KG Converter"),
        "12": ('int a, b;\ncin >> a >> b;\ncout << "Sum: " << a+b << endl;\ncout << "Subtraction: " << a-b << endl;\ncout << "Product: " << a*b << endl;\ncout << "Quotient: " << a/b;', True, [("Enter first number:", "int", "20"), ("Enter second number:", "int", "5")], "Arithmetic Operations"),
        "13": ('int t;\ncin >> t;\nif(t > 35)\n    cout << t << "C: Very Hot! Stay hydrated";\nelse if(t >= 25)\n    cout << t << "C: Pleasant weather";\nelse if(t >= 15)\n    cout << t << "C: Cool weather";\nelse\n    cout << t << "C: Cold! Wear jacket";', True, [("Enter temperature in Celsius:", "int", "38")], "Temperature Advisor"),
        "14": ('int age;\ncin >> age;\nif(age >= 18)\n    cout << "Age " << age << ": Eligible to Vote";\nelse\n    cout << "Age " << age << ": Not Eligible (need " << 18-age << " more years)";', True, [("Enter age:", "int", "20")], "Voting Eligibility"),
        "15": ('int units;\ncin >> units;\nfloat bill;\nif(units <= 100)\n    bill = units * 1.5;\nelse\n    bill = 150 + (units-100) * 2.5;\ncout << "Units: " << units << endl;\ncout << "Electricity Bill: Rs." << bill;', True, [("Enter electricity units consumed:", "int", "150")], "Electricity Bill Calculator"),
        "16": ('int percent;\ncin >> percent;\ncout << "Score: " << percent << "%" << endl;\nif(percent >= 80)\n    cout << "Scholarship: Awarded (Grade A)";\nelse if(percent >= 60)\n    cout << "Scholarship: Not Awarded (Grade B)";\nelse\n    cout << "Scholarship: Not Awarded (Grade C)";', True, [("Enter percentage:", "int", "85")], "Scholarship Check"),
        "17": ('int y;\ncin >> y;\nif(y%400==0 || (y%4==0 && y%100!=0))\n    cout << y << " is a Leap Year";\nelse\n    cout << y << " is NOT a Leap Year";', True, [("Enter a year:", "int", "2024")], "Leap Year Checker"),
        "18": ('int a[5] = {10, 20, 30, 40, 50};\ncout << "Array Elements:" << endl;\nfor(int i=0; i<5; i++)\n    cout << "  a[" << i << "] = " << a[i] << endl;', False, [], "Array Display"),
        "19": ('int a[3], b[3];\ncin >> a[0] >> a[1] >> a[2];\ncin >> b[0] >> b[1] >> b[2];\ncout << "Sum Arrays: ";\nfor(int i=0; i<3; i++)\n    cout << a[i]+b[i] << " ";', True, [("Enter Array A (3 numbers):", "str", "1 2 3"), ("Enter Array B (3 numbers):", "str", "4 5 6")], "Two Array Addition"),
        "20": (f'int a[]={{{v1}, {v2*3}, 30, {v1+10}}};\nfloat s=0;\nfor(int i=0; i<4; i++) s += a[i];\ncout << "Array: {v1}, {v2*3}, 30, {v1+10}" << endl;\ncout << "Sum: " << s << endl;\ncout << "Average: " << s/4;', False, [], "Array Average"),
        "21": ('int a[5];\ncin >> a[0] >> a[1] >> a[2] >> a[3] >> a[4];\nint mx=a[0];\nfor(int i=1; i<5; i++)\n    if(a[i]>mx) mx=a[i];\ncout << "Max in Array: " << mx;', True, [("Enter 5 numbers for array:", "str", "12 45 7 89 33")], "Array Maximum"),
        "22": ('int a[5]={11, 22, 33, 44, 55};\ncout << "Before swap: " << a[0] << " ... " << a[4] << endl;\nswap(a[0], a[4]);\ncout << "After swap:  " << a[0] << " ... " << a[4];', False, [], "Swap First & Last"),
        "23": ('int a[5]={10, 20, 30, 40, 50};\ncout << "Original: ";\nfor(int i=0; i<5; i++) cout << a[i] << " ";\ncout << endl << "Reversed: ";\nfor(int i=4; i>=0; i--) cout << a[i] << " ";', False, [], "Array Reverse"),
        "24": ('int a[5];\ncin >> a[0] >> a[1] >> a[2] >> a[3] >> a[4];\nbool pal=true;\nfor(int i=0; i<2; i++)\n    if(a[i]!=a[4-i]) pal=false;\ncout << (pal ? "Array is Palindrome" : "Not Palindrome");', True, [("Enter 5 numbers:", "str", "1 2 3 2 1")], "Array Palindrome"),
        "25": (f'int a[5]={{0}};\na[2] = {v3};\ncout << "Array after update:" << endl;\nfor(int i=0; i<5; i++)\n    cout << "  a[" << i << "] = " << a[i] << endl;', False, [], "Array Index Update"),
        "26": ('cout << "Numbers 1 to 10:" << endl;\nfor(int i=1; i<=10; i++)\n    cout << i << " ";', False, [], "1 to 10 Loop"),
        "27": ('cout << "Countdown 10 to 1:" << endl;\nfor(int i=10; i>=1; i--)\n    cout << i << " ";', False, [], "Countdown Loop"),
        "28": ('cout << "Even numbers 1-20:" << endl;\nfor(int i=2; i<=20; i+=2)\n    cout << i << " ";', False, [], "Even Numbers"),
        "29": ('cout << "Odd numbers 1-19:" << endl;\nfor(int i=1; i<=19; i+=2)\n    cout << i << " ";', False, [], "Odd Numbers"),
        "30": ('int s=0;\nfor(int i=1; i<=10; i++)\n    s += i;\ncout << "Sum of 1 to 10 = " << s;', False, [], "Sum 1 to 10"),
        "31": ('int n;\ncin >> n;\ncout << "Multiplication Table of " << n << ":" << endl;\nfor(int i=1; i<=10; i++)\n    cout << n << " x " << i << " = " << n*i << endl;', True, [("Enter number for table:", "int", "7")], "Multiplication Table"),
        "32": ('cout << "Squares of 1-10:" << endl;\nfor(int i=1; i<=10; i++)\n    cout << i << "^2 = " << i*i << endl;', False, [], "Perfect Squares"),
        "33": ('cout << "Uppercase Alphabet:" << endl;\nfor(char c=\'A\'; c<=\'Z\'; c++)\n    cout << c << " ";', False, [], "Alphabet Loop"),
        "34": ('int n;\ncin >> n;\ncout << "Counting 1 to " << n << ":" << endl;\nfor(int i=1; i<=n; i++)\n    cout << i << " ";', True, [("Enter limit (n):", "int", "15")], "User-defined Count"),
        "35": ('int rows;\ncin >> rows;\ncout << "Star Pattern:" << endl;\nfor(int i=1; i<=rows; i++) {\n    for(int j=1; j<=i; j++)\n        cout << "* ";\n    cout << endl;\n}', True, [("Enter number of rows for pattern:", "int", "5")], "Star Pyramid Pattern"),
        "36": ('int i=1;\ncout << "Do-While 1 to 10:" << endl;\ndo {\n    cout << i << " ";\n    i++;\n} while(i<=10);', False, [], "Do-While Loop"),
        "37": ('int secret, guess;\ncin >> secret;\ncout << "Start guessing:" << endl;\ndo {\n    cin >> guess;\n    if(guess < secret) cout << "Too low! Try again: ";\n    else if(guess > secret) cout << "Too high! Try again: ";\n} while(guess != secret);\ncout << "Correct! The number was " << secret;', True, [("Set secret number:", "int", "42"), ("Your guess:", "int", "42")], "Guessing Game"),
        "38": ('int n;\ncin >> n;\nint i=1;\ncout << "Iterating " << n << " times:" << endl;\ndo {\n    cout << "  Iteration " << i << endl;\n    i++;\n} while(i<=n);', True, [("Enter number of iterations:", "int", "4")], "Do-While Counter"),
        "39": ('char c;\ncin >> c;\ncout << "Entered: " << c << endl;\ndo {\n    cout << "Character \'" << c << "\' processed" << endl;\n} while(c != \'q\');\ncout << "Loop Exited";', True, [("Enter a character (q to exit loop logic):", "char", "q")], "Char Do-While"),
        "40": ('int s;\ncin >> s;\ncout << "Square Side: " << s << endl;\ncout << "Area: " << s*s << endl;\ncout << "Perimeter: " << 4*s;', True, [("Enter side length of square:", "int", "7")], "Square Properties"),
        "41": ('int n;\ncin >> n;\nif(n%5==0 && n%11==0)\n    cout << n << " is divisible by BOTH 5 and 11";\nelse if(n%5==0)\n    cout << n << " is divisible by 5 only";\nelse if(n%11==0)\n    cout << n << " is divisible by 11 only";\nelse\n    cout << n << " is NOT divisible by 5 or 11";', True, [("Enter a number:", "int", "55")], "Divisibility Check"),
        "42": ('float c;\ncin >> c;\nfloat f = (c*9/5)+32;\ncout << c << " Celsius = " << f << " Fahrenheit" << endl;\ncout << c << " Celsius = " << c+273.15 << " Kelvin";', True, [("Enter temperature in Celsius:", "float", "37")], "Temperature Converter"),
        "43": ('float r;\ncin >> r;\ncout << "Radius: " << r << endl;\ncout << "Area: " << 3.14159*r*r << endl;\ncout << "Circumference: " << 2*3.14159*r;', True, [("Enter radius of circle:", "float", "5")], "Circle Calculator"),
        "44": ('int a, b;\ncin >> a >> b;\nif(a>b)\n    cout << a << " is Greater than " << b;\nelse if(b>a)\n    cout << b << " is Greater than " << a;\nelse\n    cout << a << " and " << b << " are Equal";', True, [("Enter first number:", "int", "45"), ("Enter second number:", "int", "28")], "Greater Number"),
        "45": ('int n;\ncin >> n;\ncout << "Count from 1 to " << n << ":" << endl;\nfor(int i=1; i<=n; i++)\n    cout << i << endl;', True, [("Enter a number to count up to:", "int", "6")], "Count to N"),
        "46": ('int r;\ncin >> r;\ncout << "Even numbers from 2 to " << r << ":" << endl;\nfor(int i=2; i<=r; i+=2)\n    cout << i << " ";', True, [("Enter range for even numbers:", "int", "20")], "Even in Range"),
        "47": ('int n;\ncin >> n;\nbool prime=true;\nif(n<=1) prime=false;\nfor(int i=2; i*i<=n; i++)\n    if(n%i==0) { prime=false; break; }\ncout << n << (prime ? " is a Prime Number" : " is NOT a Prime Number");', True, [("Enter number to check if prime:", "int", "17")], "Prime Number Check"),
        "48": ('int n;\ncin >> n;\nlong long f=1;\nfor(int i=1; i<=n; i++)\n    f *= i;\ncout << "Factorial of " << n << " = " << f;', True, [("Enter number for factorial:", "int", "6")], "Factorial Calculator"),
    }
    return tasks.get(task_num, ('cout << "Task Not Found";', False, [], "Unknown"))


# =========================
# CODE BUILDER
# =========================
def build_cpp(body_code):
    return f"""#include <iostream>
#include <string>
using namespace std;

int main() {{
{chr(10).join('    ' + l for l in body_code.split(chr(10)))}
    return 0;
}}"""


# =========================
# RUN C++
# =========================
def run_cpp(code, input_data=""):
    with tempfile.TemporaryDirectory() as tmp:
        cpp_path = os.path.join(tmp, "code.cpp")
        exe_path = os.path.join(tmp, "prog")
        with open(cpp_path, "w") as f:
            f.write(code)
        try:
            comp = subprocess.run(
                ["g++", cpp_path, "-o", exe_path, "-std=c++17"],
                capture_output=True, text=True, timeout=10
            )
            if comp.returncode != 0:
                return f"Compilation Error:\n{comp.stderr}", False
            res = subprocess.run(
                [exe_path], input=input_data,
                capture_output=True, text=True, timeout=5
            )
            output = res.stdout.strip()
            if not output:
                output = "(No output / Process exited with code 0)"
            return output, True
        except subprocess.TimeoutExpired:
            return "Timeout: Program took too long", False
        except FileNotFoundError:
            return "g++ compiler not found. Please install build-essential.", False
        except Exception as e:
            return f"Runtime Error: {str(e)}", False


# =========================
# MAIN UI
# =========================

# --- Header ---
st.markdown("""
<div class="app-header">
    <div>
        <div class="app-title">🖥️ CAPTURED AI</div>
        <div class="app-subtitle">// Premium C++ Lab Manual Generator — 96 Images</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="badge-row">
    <span class="badge badge-blue">📸 96 Images</span>
    <span class="badge badge-green">📝 48 Tasks</span>
    <span class="badge badge-purple">🎨 3 Themes</span>
    <span class="badge badge-amber">⚡ Real Output</span>
</div>
""", unsafe_allow_html=True)

# --- Student Info Card ---
st.markdown('<div class="section-card"><div class="section-title">👤 Student Info</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    name = st.text_input("Student Name", "Zohaib Memon", key="name", placeholder="Enter full name")
with col2:
    task_range = st.selectbox("Task Range", ["All 48", "01–17", "18–25", "26–35", "36–48"], key="range")

st.markdown('</div>', unsafe_allow_html=True)

# --- Template Selector ---
st.markdown('<div class="section-card"><div class="section-title">🎨 Screenshot Theme</div>', unsafe_allow_html=True)

template_names = list(TEMPLATES.keys())
selected_tmpl = st.radio(
    "Choose theme for screenshots",
    template_names,
    horizontal=True,
    key="template",
    label_visibility="collapsed"
)

# Visual template previews using HTML
st.markdown("""
<div class="template-grid">

  <div class="template-preview" id="tmpl-catppuccin">
    <div class="tmpl-bar" style="background:#313244;">
      <span class="tmpl-dot" style="background:#f38ba8;"></span>
      <span class="tmpl-dot" style="background:#f9e2af;"></span>
      <span class="tmpl-dot" style="background:#a6e3a1;"></span>
    </div>
    <div class="tmpl-code-area" style="background:#1e1e2e;">
      <div><span style="color:#45475a;">1 </span><span style="color:#cba6f7;">#include</span> <span style="color:#a6e3a1;">&lt;iostream&gt;</span></div>
      <div><span style="color:#45475a;">2 </span><span style="color:#cba6f7;">using namespace</span> <span style="color:#cdd6f4;">std;</span></div>
      <div><span style="color:#45475a;">3 </span><span style="color:#6c7086;">// main entry</span></div>
      <div><span style="color:#45475a;">4 </span><span style="color:#cba6f7;">int</span> <span style="color:#89b4fa;">main</span><span style="color:#cdd6f4;">() {</span></div>
      <div><span style="color:#45475a;">5 </span>&nbsp;&nbsp;<span style="color:#89b4fa;">cout</span> <span style="color:#cdd6f4;">&lt;&lt;</span> <span style="color:#a6e3a1;">"Hello"</span><span style="color:#cdd6f4;">;</span></div>
    </div>
    <div class="tmpl-footer" style="background:#181825; border-color:#313244;">
      <div class="tmpl-name">Catppuccin Mocha</div>
      <div class="tmpl-desc">macOS terminal · sidebar explorer · dark purple</div>
    </div>
  </div>

  <div class="template-preview">
    <div class="tmpl-bar" style="background:#161b22;">
      <span class="tmpl-dot" style="background:#ff5f57;"></span>
      <span class="tmpl-dot" style="background:#ffbd2e;"></span>
      <span class="tmpl-dot" style="background:#27c93f;"></span>
    </div>
    <div class="tmpl-code-area" style="background:#0d1117;">
      <div><span style="color:#484f58;">1 </span><span style="color:#ff7b72;">#include</span> <span style="color:#a5d6ff;">&lt;iostream&gt;</span></div>
      <div><span style="color:#484f58;">2 </span><span style="color:#ff7b72;">using namespace</span> <span style="color:#e6edf3;">std;</span></div>
      <div><span style="color:#484f58;">3 </span><span style="color:#8b949e;">// main entry</span></div>
      <div><span style="color:#484f58;">4 </span><span style="color:#ff7b72;">int</span> <span style="color:#d2a8ff;">main</span><span style="color:#e6edf3;">() {</span></div>
      <div><span style="color:#484f58;">5 </span>&nbsp;&nbsp;<span style="color:#d2a8ff;">cout</span> <span style="color:#e6edf3;">&lt;&lt;</span> <span style="color:#a5d6ff;">"Hello"</span><span style="color:#e6edf3;">;</span></div>
    </div>
    <div class="tmpl-footer" style="background:#010409; border-color:#30363d;">
      <div class="tmpl-name">GitHub Dark</div>
      <div class="tmpl-desc">Windows CMD prompt · classic DOS output</div>
    </div>
  </div>

  <div class="template-preview">
    <div class="tmpl-bar" style="background:#f6f8fa; border-bottom:1px solid #d0d7de;">
      <span class="tmpl-dot" style="background:#ff5f57;"></span>
      <span class="tmpl-dot" style="background:#ffbd2e;"></span>
      <span class="tmpl-dot" style="background:#27c93f;"></span>
    </div>
    <div class="tmpl-code-area" style="background:#ffffff;">
      <div><span style="color:#8c959f;">1 </span><span style="color:#8250df;">#include</span> <span style="color:#0a3069;">&lt;iostream&gt;</span></div>
      <div><span style="color:#8c959f;">2 </span><span style="color:#8250df;">using namespace</span> <span style="color:#24292f;">std;</span></div>
      <div><span style="color:#8c959f;">3 </span><span style="color:#6e7781;font-style:italic;">// main entry</span></div>
      <div><span style="color:#8c959f;">4 </span><span style="color:#cf222e;">int</span> <span style="color:#8250df;">main</span><span style="color:#24292f;">() {</span></div>
      <div><span style="color:#8c959f;">5 </span>&nbsp;&nbsp;<span style="color:#8250df;">cout</span> <span style="color:#24292f;">&lt;&lt;</span> <span style="color:#0a3069;">"Hello"</span><span style="color:#24292f;">;</span></div>
    </div>
    <div class="tmpl-footer" style="background:#f6f8fa; border-color:#d0d7de;">
      <div class="tmpl-name">GitHub Light</div>
      <div class="tmpl-desc">VS Code panel · PS prompt · blue status bar</div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Task range mapping ---
range_map = {
    "All 48": range(1, 49),
    "01–17": range(1, 18),
    "18–25": range(18, 26),
    "26–35": range(26, 36),
    "36–48": range(36, 49),
}
task_ids = list(range_map[task_range])

# --- CIN Input Section ---
st.markdown('<div class="section-card"><div class="section-title">⌨️ Input Values for cin Tasks</div>', unsafe_allow_html=True)
st.caption("Tasks that need user input — provide values below so output images show real results")

cin_inputs = {}
cin_tasks_in_range = []
for tid in task_ids:
    key = f"{tid:02d}"
    _, has_cin, prompts, desc = get_task(key, name)
    if has_cin and prompts:
        cin_tasks_in_range.append((key, desc, prompts))

if cin_tasks_in_range:
    for key, desc, prompts in cin_tasks_in_range:
        st.markdown(f"""
        <div class="cin-task-card">
            <div class="cin-task-header">
                <span class="cin-task-name">Task {key} — {desc}</span>
                <span class="cin-badge">cin</span>
            </div>
        </div>""", unsafe_allow_html=True)

        task_vals = []
        cols = st.columns(min(len(prompts), 3))
        for idx, (prompt, ptype, default) in enumerate(prompts):
            with cols[idx % len(cols)]:
                val = st.text_input(prompt, default, key=f"inp_{key}_{idx}")
                task_vals.append(val)
        cin_inputs[key] = task_vals
else:
    st.info("No cin tasks in selected range — all tasks use fixed values.")

st.markdown('</div>', unsafe_allow_html=True)

# --- Generate Button ---
st.markdown("---")

col_btn1, col_btn2 = st.columns([1, 3])
with col_btn1:
    generate = st.button(f"🚀 Generate {len(task_ids) * 2} Images", use_container_width=True)
with col_btn2:
    st.markdown(f"""
    <div style="padding-top: 12px; font-size: 0.82rem; color: #64748b; font-family: 'Sora', sans-serif;">
        {len(task_ids)} tasks × 2 screenshots &nbsp;·&nbsp; Theme: <strong>{selected_tmpl}</strong>
        &nbsp;·&nbsp; ZIP file download hogi browser se
    </div>
    """, unsafe_allow_html=True)

# --- Generate Logic ---
if generate:
    import io
    import zipfile

    progress = st.progress(0)
    status_text = st.empty()
    generated_count = 0

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, tid in enumerate(task_ids):
            key = f"{tid:02d}"
            status_text.markdown(
                f'<p style="color:#2563eb; font-family:JetBrains Mono,monospace; font-size:0.82rem;">⚙️ Processing Task {key} — {selected_tmpl}...</p>',
                unsafe_allow_html=True
            )

            body, has_cin, prompts, desc = get_task(key, name)
            full_code = build_cpp(body)
            formatted_code = format_cpp(full_code)

            # --- Code screenshot → in-memory ---
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_code:
                tmp_code_path = tmp_code.name
            create_code_screenshot(formatted_code, tmp_code_path, tid, f"Task {key} — {desc}", tmpl_name=selected_tmpl)
            with open(tmp_code_path, "rb") as f:
                zf.writestr(f"task_{key}_code.png", f.read())
            os.unlink(tmp_code_path)

            # --- Build input string ---
            input_str = ""
            if has_cin and key in cin_inputs:
                vals = cin_inputs[key]
                input_str = "\n".join(v.strip() for v in vals if v.strip())
                input_str = "\n".join(input_str.split())

            output, success = run_cpp(full_code, input_str)

            if has_cin and key in cin_inputs and prompts:
                input_display = []
                for i, (prompt, ptype, _) in enumerate(prompts):
                    val = cin_inputs[key][i] if i < len(cin_inputs[key]) else "?"
                    input_display.append(f">> {val}   ({prompt.rstrip(':')})")
                output_display = "\n".join(input_display) + "\n" + "-" * 40 + "\n" + output
            else:
                output_display = output

            # --- Output screenshot → in-memory ---
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_out:
                tmp_out_path = tmp_out.name
            create_output_screenshot(output_display, tmp_out_path, tid, success, tmpl_name=selected_tmpl)
            with open(tmp_out_path, "rb") as f:
                zf.writestr(f"task_{key}_output.png", f.read())
            os.unlink(tmp_out_path)

            generated_count += 2
            progress.progress((idx + 1) / len(task_ids))

    status_text.empty()
    progress.progress(1.0)
    zip_buffer.seek(0)

    zip_name = f"Lab_{name.replace(' ', '_')}_{selected_tmpl.replace(' ', '_')}.zip"

    st.markdown(f"""
    <div class="success-box">
        ✅ &nbsp;<strong>{generated_count} images</strong> generated for <strong>{len(task_ids)} tasks</strong><br>
        🎨 &nbsp;Theme: <strong>{selected_tmpl}</strong><br>
        🖼️ &nbsp;{len(task_ids)} Code Screenshots + {len(task_ids)} Output Screenshots<br>
        ⬇️ &nbsp;Neeche Download button se ZIP save karo
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label=f"⬇️ Download {zip_name}",
        data=zip_buffer,
        file_name=zip_name,
        mime="application/zip",
        use_container_width=True,
    )