import streamlit as st
import os
import subprocess
import random
import io
import zipfile
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

    .stTextInput > div > div > input {
        background: #f8fafc !important;
        border: 1px solid #e2e6ec !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 12px 32px !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
        border-radius: 4px !important;
    }

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

    hr {
        border: none !important;
        border-top: 1px solid #e2e6ec !important;
        margin: 20px 0 !important;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# FONT LOADING
# =========================
@st.cache_resource
def load_fonts():
    """Cache fonts so they are loaded only once."""
    font_options = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "DejaVuSansMono.ttf",
        "consola.ttf",
        "cour.ttf",
    ]
    found = None
    for f in font_options:
        if os.path.exists(f):
            found = f
            break
    return found

FONT_PATH = load_fonts()

def get_font(size):
    if FONT_PATH:
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    return ImageFont.load_default()


# =========================
# TEMPLATE DEFINITIONS
# =========================
TEMPLATES = {
    "Catppuccin Mocha": {
        "code_bg": (30, 30, 46), "bar_bg": (49, 50, 68), "gutter_bg": (24, 24, 37),
        "border": (69, 71, 90), "line_num": (69, 71, 90), "alt_row": (27, 27, 42),
        "status_bg": (24, 24, 37), "status_text": (69, 71, 90), "title_text": (166, 173, 200),
        "tab_bg": (30, 30, 46), "tab_active": (49, 50, 68), "tab_text": (205, 214, 244),
        "syntax": {
            "comment": (108, 112, 134), "preprocessor": (203, 166, 247),
            "output": (137, 180, 250), "input_cin": (148, 226, 213),
            "declaration": (249, 226, 175), "control": (203, 166, 247),
            "default": (205, 214, 244),
        },
        "term_bg": (30, 30, 46), "term_bar": (49, 50, 68),
        "term_prompt": (166, 227, 161), "term_input": (148, 226, 213),
        "term_output": (205, 214, 244), "term_error": (243, 139, 168),
    },
    "GitHub Dark": {
        "code_bg": (13, 17, 23), "bar_bg": (22, 27, 34), "gutter_bg": (17, 22, 29),
        "border": (48, 54, 61), "line_num": (70, 80, 94), "alt_row": (15, 20, 27),
        "status_bg": (17, 22, 29), "status_text": (70, 80, 94), "title_text": (140, 150, 165),
        "tab_bg": (17, 22, 29), "tab_active": (22, 27, 34), "tab_text": (200, 210, 220),
        "syntax": {
            "comment": (106, 153, 85), "preprocessor": (197, 134, 192),
            "output": (86, 156, 214), "input_cin": (78, 201, 176),
            "declaration": (244, 180, 30), "control": (197, 134, 192),
            "default": (220, 223, 228),
        },
        "term_bg": (12, 12, 12), "term_bar": (30, 30, 30),
        "term_prompt": (80, 200, 80), "term_input": (78, 201, 176),
        "term_output": (220, 220, 220), "term_error": (255, 80, 80),
    },
    "GitHub Light": {
        "code_bg": (255, 255, 255), "bar_bg": (246, 248, 250), "gutter_bg": (250, 251, 252),
        "border": (208, 215, 222), "line_num": (140, 149, 159), "alt_row": (248, 250, 252),
        "status_bg": (246, 248, 250), "status_text": (140, 149, 159), "title_text": (101, 109, 118),
        "tab_bg": (246, 248, 250), "tab_active": (255, 255, 255), "tab_text": (36, 41, 47),
        "syntax": {
            "comment": (110, 119, 129), "preprocessor": (130, 80, 223),
            "output": (5, 80, 174), "input_cin": (3, 101, 111),
            "declaration": (134, 46, 18), "control": (130, 80, 223),
            "default": (36, 41, 47),
        },
        "term_bg": (255, 255, 255), "term_bar": (246, 248, 250),
        "term_prompt": (31, 136, 61), "term_input": (3, 101, 111),
        "term_output": (36, 41, 47), "term_error": (207, 34, 46),
    },
}


# =========================
# SYNTAX HIGHLIGHTING
# =========================
def get_line_color(line, tmpl_name):
    s = TEMPLATES[tmpl_name]["syntax"]
    stripped = line.strip()
    if stripped.startswith("//"):
        return s["comment"]
    if stripped.startswith("#"):
        return s["preprocessor"]
    if "cout" in stripped:
        return s["output"]
    if "cin" in stripped:
        return s["input_cin"]
    if any(stripped.startswith(k) for k in ["int ", "float ", "char ", "string ", "bool "]):
        return s["declaration"]
    if stripped.startswith("return") or any(stripped.startswith(k) for k in ["if", "else", "for", "while", "do"]):
        return s["control"]
    return s["default"]


# =========================
# ✅ FIX 1: Return BytesIO instead of saving to disk
# =========================
def create_code_image(code, task_num, title="Source Code", tmpl_name="GitHub Dark"):
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

    draw.rectangle([0, 0, width - 1, height - 1], outline=t["border"], width=1)
    draw.rectangle([0, 0, width, 48], fill=t["bar_bg"])
    draw.line([0, 48, width, 48], fill=t["border"], width=1)

    draw.ellipse([16, 16, 30, 30], fill=(255, 95, 87))
    draw.ellipse([42, 16, 56, 30], fill=(255, 189, 46))
    draw.ellipse([68, 16, 82, 30], fill=(39, 201, 63))

    title_text = f"task_{task_num:02d}.cpp — {title}"
    draw.text((width // 2 - len(title_text) * 4, 16), title_text, fill=t["title_text"], font=get_font(14))

    draw.rectangle([0, 48, width, 72], fill=t["tab_bg"])
    draw.rectangle([0, 48, 200, 72], fill=t["tab_active"])
    draw.line([0, 72, width, 72], fill=t["border"], width=1)
    draw.text((14, 54), f"  task_{task_num:02d}.cpp", fill=t["tab_text"], font=get_font(13))

    draw.rectangle([0, 72, left_margin - 10, height], fill=t["gutter_bg"])
    draw.line([left_margin - 10, 72, left_margin - 10, height], fill=t["border"], width=1)

    font_code = get_font(font_size)
    for i, line in enumerate(lines):
        y = top_margin + i * line_height - 18
        ln_text = str(i + 1)
        draw.text((left_margin - 10 - len(ln_text) * 7 - 4, y), ln_text, fill=t["line_num"], font=get_font(13))
        if i % 2 == 0:
            draw.rectangle([left_margin - 9, y - 2, width - 1, y + line_height - 4], fill=t["alt_row"])
        color = get_line_color(line, tmpl_name)
        draw.text((left_margin, y), line, fill=color, font=font_code)

    draw.rectangle([0, height - 24, width, height], fill=t["status_bg"])
    draw.line([0, height - 24, width, height - 24], fill=t["border"], width=1)
    draw.text((14, height - 18), f"  C++   UTF-8   Lines: {len(lines)}", fill=t["status_text"], font=get_font(12))

    # ✅ Return bytes directly — no disk write
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf.read()


def create_output_image(output_text, task_num, actual_output=True, tmpl_name="GitHub Dark"):
    t = TEMPLATES[tmpl_name]
    lines = output_text.split("\n")
    font_size = 16
    line_height = 26
    left_margin = 20
    max_len = max((len(l) for l in lines), default=40)

    if tmpl_name == "Catppuccin Mocha":
        sidebar_w = 180
        content_left = sidebar_w + 1
        top_margin = 88
        bottom_margin = 36
        width = max(720, int(content_left + left_margin + max_len * 9.6 + 40))
        height = top_margin + len(lines) * line_height + bottom_margin

        img = Image.new("RGB", (width, height), t["term_bg"])
        draw = ImageDraw.Draw(img)

        draw.rectangle([0, 0, width - 1, height - 1], outline=t["border"], width=1)
        draw.rectangle([0, 0, width, 46], fill=t["term_bar"])
        draw.line([0, 46, width, 46], fill=t["border"], width=1)

        draw.ellipse([16, 15, 28, 27], fill=(255, 95, 87))
        draw.ellipse([38, 15, 50, 27], fill=(255, 189, 46))
        draw.ellipse([60, 15, 72, 27], fill=(39, 201, 63))

        title = f"Task {task_num:02d}.cpp — Output"
        draw.text((width // 2 - len(title) * 4, 14), title, fill=t["title_text"], font=get_font(14))

        tab_bg = (24, 24, 37)
        draw.rectangle([0, 46, width, 68], fill=tab_bg)
        draw.rectangle([0, 46, 180, 68], fill=t["term_bar"])
        draw.line([0, 68, width, 68], fill=t["border"], width=1)
        draw.text((14, 52), "  Output", fill=(148, 226, 213), font=get_font(13))
        draw.text((200, 52), "  Console", fill=(108, 112, 134), font=get_font(13))

        draw.rectangle([0, 68, sidebar_w, height], fill=(20, 20, 35))
        draw.line([sidebar_w, 68, sidebar_w, height], fill=t["border"], width=1)

        sb_y = 80
        draw.text((10, sb_y), "EXPLORER", fill=(108, 112, 134), font=get_font(11))
        sb_y += 22
        draw.text((10, sb_y), f"  task_{task_num:02d}.cpp", fill=(203, 166, 247), font=get_font(13))
        sb_y += 20
        draw.text((10, sb_y), f"  task_{task_num:02d}.exe", fill=(148, 226, 213), font=get_font(13))
        sb_y += 28
        draw.text((10, sb_y), "STATUS", fill=(108, 112, 134), font=get_font(11))
        sb_y += 18
        ok_color = (166, 227, 161) if actual_output else (249, 226, 175)
        draw.text((10, sb_y), "  OK (code 0)" if actual_output else "  Simulated", fill=ok_color, font=get_font(13))

        px = content_left + left_margin
        draw.text((px, 76), f"~  g++ task_{task_num:02d}.cpp", fill=(108, 112, 134), font=get_font(14))
        draw.text((px, 98), f"~  ./task_{task_num:02d}", fill=(166, 227, 161), font=get_font(14))

        y = top_margin + 18
        for line in lines:
            color = t["term_input"] if line.startswith(">>") else (t["term_error"] if "error" in line.lower() else t["term_output"])
            draw.text((px, y), line, fill=color, font=get_font(font_size))
            y += line_height

        draw.rectangle([0, height - 22, width, height], fill=(24, 24, 37))
        draw.line([0, height - 22, width, height - 22], fill=t["border"], width=1)
        draw.text((sidebar_w + 10, height - 17), f"  bash   UTF-8   Ln {len(lines)}", fill=(108, 112, 134), font=get_font(12))

    elif tmpl_name == "GitHub Dark":
        top_margin = 100
        bottom_margin = 30
        width = max(700, int(left_margin + max_len * 9.8 + 40))
        height = top_margin + len(lines) * line_height + bottom_margin

        img = Image.new("RGB", (width, height), (10, 10, 10))
        draw = ImageDraw.Draw(img)

        draw.rectangle([0, 0, width - 1, height - 1], outline=(60, 60, 60), width=1)
        draw.rectangle([0, 0, width, 30], fill=(48, 48, 48))
        draw.rectangle([width - 84, 0, width - 56, 30], fill=(60, 60, 60))
        draw.rectangle([width - 56, 0, width - 28, 30], fill=(60, 60, 60))
        draw.rectangle([width - 28, 0, width, 30], fill=(196, 43, 28))
        draw.text((width - 78, 8), "—", fill=(220, 220, 220), font=get_font(12))
        draw.text((width - 48, 6), "□", fill=(220, 220, 220), font=get_font(14))
        draw.text((width - 20, 8), "x", fill=(255, 255, 255), font=get_font(12))
        draw.text((10, 8), f"Command Prompt — task_{task_num:02d}.cpp", fill=(204, 204, 204), font=get_font(13))
        draw.line([0, 30, width, 30], fill=(80, 80, 80), width=1)

        prompt_y = 38
        draw.text((left_margin, prompt_y), "Microsoft Windows [Version 10.0.26100]", fill=(180, 180, 180), font=get_font(14))
        draw.text((left_margin, prompt_y + 20), "(c) Microsoft Corporation. All rights reserved.", fill=(120, 120, 120), font=get_font(13))
        draw.text((left_margin, prompt_y + 40), f"C:\\Lab> g++ task_{task_num:02d}.cpp -o task_{task_num:02d}.exe", fill=(80, 200, 80), font=get_font(14))
        draw.text((left_margin, prompt_y + 58), f"C:\\Lab> task_{task_num:02d}.exe", fill=(80, 200, 80), font=get_font(14))

        y = top_margin + 10
        for line in lines:
            color = t["term_input"] if line.startswith(">>") else (t["term_error"] if "error" in line.lower() else t["term_output"])
            draw.text((left_margin, y), line, fill=color, font=get_font(font_size))
            y += line_height

        draw.text((left_margin, y + 4), "C:\\Lab> _", fill=(80, 200, 80), font=get_font(14))

    else:  # GitHub Light
        panel_header_h = 34
        tab_h = 28
        prompt_section_h = 52
        top_margin = panel_header_h + tab_h + prompt_section_h
        bottom_margin = 32
        width = max(700, int(left_margin + max_len * 9.8 + 40))
        height = top_margin + len(lines) * line_height + bottom_margin

        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.rectangle([0, 0, width - 1, height - 1], outline=(208, 215, 222), width=1)
        draw.rectangle([0, 0, width, panel_header_h], fill=(246, 248, 250))
        draw.line([0, panel_header_h, width, panel_header_h], fill=(208, 215, 222), width=1)

        tab_y = panel_header_h
        draw.rectangle([0, tab_y, width, tab_y + tab_h], fill=(246, 248, 250))
        draw.line([0, tab_y + tab_h, width, tab_y + tab_h], fill=(208, 215, 222), width=1)
        draw.rectangle([0, tab_y, 90, tab_y + tab_h], fill=(255, 255, 255))
        draw.text((8, tab_y + 7), "TERMINAL", fill=(36, 41, 47), font=get_font(12))
        draw.text((100, tab_y + 7), "PROBLEMS", fill=(140, 149, 159), font=get_font(12))
        draw.text((195, tab_y + 7), "OUTPUT", fill=(140, 149, 159), font=get_font(12))
        draw.text((left_margin, 10), f"task_{task_num:02d}.cpp — Integrated Terminal", fill=(101, 109, 118), font=get_font(13))

        ps_y = panel_header_h + tab_h
        draw.rectangle([0, ps_y, width, ps_y + prompt_section_h], fill=(240, 249, 255))
        draw.line([0, ps_y + prompt_section_h, width, ps_y + prompt_section_h], fill=(208, 215, 222), width=1)
        draw.text((left_margin, ps_y + 8), f"PS C:\\Lab> g++ task_{task_num:02d}.cpp -o task_{task_num:02d}", fill=(3, 101, 111), font=get_font(14))
        draw.text((left_margin, ps_y + 28), f"PS C:\\Lab> .\\task_{task_num:02d}.exe", fill=(3, 101, 111), font=get_font(14))

        y = top_margin + 10
        for line in lines:
            color = t["term_input"] if line.startswith(">>") else (t["term_error"] if "error" in line.lower() else t["term_output"])
            draw.text((left_margin, y), line, fill=color, font=get_font(font_size))
            y += line_height

        draw.rectangle([0, height - 22, width, height], fill=(0, 120, 212))
        status = "  Process exited with code 0" if actual_output else "  Simulated Output"
        draw.text((10, height - 17), status, fill=(255, 255, 255), font=get_font(12))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf.read()


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

    tasks = {
        "01": (f'cout << "Hello World!" << endl;\ncout << "Lab Setup by: {name}";', False, [], "Hello World + Name"),
        "02": ('cout << "*" << endl;\ncout << "**" << endl;\ncout << "***" << endl;\ncout << "****" << endl;\ncout << "*****";', False, [], "Star Triangle Pattern"),
        "03": ('char ch;\ncin >> ch;\nif(ch==\'a\'||ch==\'e\'||ch==\'i\'||ch==\'o\'||ch==\'u\')\n    cout << ch << " is a Vowel";\nelse\n    cout << ch << " is a Consonant";', True, [("Enter a character (e.g. a, b, x):", "char", "a")], "Vowel or Consonant"),
        "04": ('string u, p;\ncin >> u >> p;\nif(u=="admin" && p=="1234")\n    cout << "Access Granted!";\nelse\n    cout << "Access Denied!";', True, [("Enter username:", "str", "admin"), ("Enter password:", "str", "1234")], "Login System"),
        "05": ('int a, b, c;\ncin >> a >> b >> c;\ncout << "Max of " << a << ", " << b << ", " << c;\ncout << " is: " << max(a, max(b, c));', True, [("Enter 1st number:", "int", "15"), ("Enter 2nd number:", "int", "30"), ("Enter 3rd number:", "int", "22")], "Max of 3 Numbers"),
        "06": ('int n;\ncin >> n;\nif(n > 0)\n    cout << n << " is Positive";\nelse if(n < 0)\n    cout << n << " is Negative";\nelse\n    cout << "Number is Zero";', True, [("Enter a number:", "int", "42")], "Positive/Negative Check"),
        "07": (f'int n={v2}, s=0;\nfor(int i=1; i<=n; i++)\n    s += i;\ncout << "Sum of first " << n << " numbers: " << s << endl;\ncout << "Average: " << (float)s/n;', False, [], f"Sum & Average 1 to {v2}"),
        "08": ('int d;\ncin >> d;\nstring days[]={"","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"};\nif(d>=1 && d<=7)\n    cout << "Day " << d << ": " << days[d] << " | " << (d>=6 ? "Weekend" : "Weekday");\nelse\n    cout << "Invalid day number";', True, [("Enter day number (1-7):", "int", "3")], "Day of Week"),
        "09": ('float a, b;\ncin >> a >> b;\ncout << a << " + " << b << " = " << a+b << endl;\ncout << a << " - " << b << " = " << a-b << endl;\ncout << a << " * " << b << " = " << a*b << endl;\ncout << a << " / " << b << " = " << a/b;', True, [("Enter first number:", "float", "25.5"), ("Enter second number:", "float", "4.2")], "Basic Calculator"),
        "10": ('int choice;\ncin >> choice;\nif(choice==1)\n    cout << "Order: Burger - Rs.350";\nelse if(choice==2)\n    cout << "Order: Pizza - Rs.650";\nelse if(choice==3)\n    cout << "Order: Pasta - Rs.450";\nelse\n    cout << "Invalid choice";', True, [("Enter menu choice (1=Burger, 2=Pizza, 3=Pasta):", "int", "2")], "Restaurant Menu"),
        "11": ('float g;\ncin >> g;\ncout << g << " Grams = " << g/1000 << " Kilograms";', True, [("Enter weight in grams:", "float", "2500")], "Gram to KG"),
        "12": ('int a, b;\ncin >> a >> b;\ncout << "Sum: " << a+b << endl;\ncout << "Subtraction: " << a-b << endl;\ncout << "Product: " << a*b << endl;\ncout << "Quotient: " << a/b;', True, [("Enter first number:", "int", "20"), ("Enter second number:", "int", "5")], "Arithmetic Operations"),
        "13": ('int t;\ncin >> t;\nif(t > 35)\n    cout << t << "C: Very Hot!";\nelse if(t >= 25)\n    cout << t << "C: Pleasant";\nelse if(t >= 15)\n    cout << t << "C: Cool";\nelse\n    cout << t << "C: Cold!";', True, [("Enter temperature in Celsius:", "int", "38")], "Temperature Advisor"),
        "14": ('int age;\ncin >> age;\nif(age >= 18)\n    cout << "Age " << age << ": Eligible to Vote";\nelse\n    cout << "Age " << age << ": Not Eligible";', True, [("Enter age:", "int", "20")], "Voting Eligibility"),
        "15": ('int units;\ncin >> units;\nfloat bill;\nif(units <= 100)\n    bill = units * 1.5;\nelse\n    bill = 150 + (units-100) * 2.5;\ncout << "Units: " << units << endl;\ncout << "Bill: Rs." << bill;', True, [("Enter electricity units:", "int", "150")], "Electricity Bill"),
        "16": ('int percent;\ncin >> percent;\ncout << "Score: " << percent << "%" << endl;\nif(percent >= 80)\n    cout << "Scholarship: Awarded (Grade A)";\nelse\n    cout << "Scholarship: Not Awarded";', True, [("Enter percentage:", "int", "85")], "Scholarship Check"),
        "17": ('int y;\ncin >> y;\nif(y%400==0 || (y%4==0 && y%100!=0))\n    cout << y << " is a Leap Year";\nelse\n    cout << y << " is NOT a Leap Year";', True, [("Enter a year:", "int", "2024")], "Leap Year"),
        "18": ('int a[5] = {10, 20, 30, 40, 50};\ncout << "Array Elements:" << endl;\nfor(int i=0; i<5; i++)\n    cout << "  a[" << i << "] = " << a[i] << endl;', False, [], "Array Display"),
        "19": ('int a[3], b[3];\ncin >> a[0] >> a[1] >> a[2];\ncin >> b[0] >> b[1] >> b[2];\ncout << "Sum: ";\nfor(int i=0; i<3; i++)\n    cout << a[i]+b[i] << " ";', True, [("Enter Array A (3 numbers):", "str", "1 2 3"), ("Enter Array B (3 numbers):", "str", "4 5 6")], "Two Array Addition"),
        "20": (f'int a[]={{{v1}, {v2*3}, 30, {v1+10}}};\nfloat s=0;\nfor(int i=0; i<4; i++) s += a[i];\ncout << "Sum: " << s << endl;\ncout << "Average: " << s/4;', False, [], "Array Average"),
        "21": ('int a[5];\ncin >> a[0] >> a[1] >> a[2] >> a[3] >> a[4];\nint mx=a[0];\nfor(int i=1; i<5; i++)\n    if(a[i]>mx) mx=a[i];\ncout << "Max: " << mx;', True, [("Enter 5 numbers:", "str", "12 45 7 89 33")], "Array Maximum"),
        "22": ('int a[5]={11,22,33,44,55};\ncout << "Before: " << a[0] << " ... " << a[4] << endl;\nswap(a[0], a[4]);\ncout << "After:  " << a[0] << " ... " << a[4];', False, [], "Swap First & Last"),
        "23": ('int a[5]={10,20,30,40,50};\ncout << "Original: ";\nfor(int i=0; i<5; i++) cout << a[i] << " ";\ncout << endl << "Reversed: ";\nfor(int i=4; i>=0; i--) cout << a[i] << " ";', False, [], "Array Reverse"),
        "24": ('int a[5];\ncin >> a[0] >> a[1] >> a[2] >> a[3] >> a[4];\nbool pal=true;\nfor(int i=0; i<2; i++)\n    if(a[i]!=a[4-i]) pal=false;\ncout << (pal ? "Palindrome" : "Not Palindrome");', True, [("Enter 5 numbers:", "str", "1 2 3 2 1")], "Array Palindrome"),
        "25": (f'int a[5]={{0}};\na[2] = 999;\ncout << "Array after update:" << endl;\nfor(int i=0; i<5; i++)\n    cout << "  a[" << i << "] = " << a[i] << endl;', False, [], "Array Index Update"),
        "26": ('cout << "Numbers 1 to 10:" << endl;\nfor(int i=1; i<=10; i++)\n    cout << i << " ";', False, [], "1 to 10 Loop"),
        "27": ('cout << "Countdown:" << endl;\nfor(int i=10; i>=1; i--)\n    cout << i << " ";', False, [], "Countdown Loop"),
        "28": ('cout << "Even 1-20:" << endl;\nfor(int i=2; i<=20; i+=2)\n    cout << i << " ";', False, [], "Even Numbers"),
        "29": ('cout << "Odd 1-19:" << endl;\nfor(int i=1; i<=19; i+=2)\n    cout << i << " ";', False, [], "Odd Numbers"),
        "30": ('int s=0;\nfor(int i=1; i<=10; i++)\n    s += i;\ncout << "Sum 1 to 10 = " << s;', False, [], "Sum 1 to 10"),
        "31": ('int n;\ncin >> n;\ncout << "Table of " << n << ":" << endl;\nfor(int i=1; i<=10; i++)\n    cout << n << " x " << i << " = " << n*i << endl;', True, [("Enter number for table:", "int", "7")], "Multiplication Table"),
        "32": ('cout << "Squares:" << endl;\nfor(int i=1; i<=10; i++)\n    cout << i << "^2 = " << i*i << endl;', False, [], "Perfect Squares"),
        "33": ('cout << "Alphabet:" << endl;\nfor(char c=\'A\'; c<=\'Z\'; c++)\n    cout << c << " ";', False, [], "Alphabet Loop"),
        "34": ('int n;\ncin >> n;\ncout << "Counting to " << n << ":" << endl;\nfor(int i=1; i<=n; i++)\n    cout << i << " ";', True, [("Enter limit:", "int", "15")], "Count to N"),
        "35": ('int rows;\ncin >> rows;\nfor(int i=1; i<=rows; i++) {\n    for(int j=1; j<=i; j++)\n        cout << "* ";\n    cout << endl;\n}', True, [("Enter rows for pattern:", "int", "5")], "Star Pyramid"),
        "36": ('int i=1;\ndo {\n    cout << i << " ";\n    i++;\n} while(i<=10);', False, [], "Do-While 1 to 10"),
        "37": ('int secret, guess;\ncin >> secret >> guess;\nif(guess < secret) cout << "Too low!";\nelse if(guess > secret) cout << "Too high!";\nelse cout << "Correct! Number was " << secret;', True, [("Secret number:", "int", "42"), ("Your guess:", "int", "42")], "Guessing Game"),
        "38": ('int n;\ncin >> n;\nint i=1;\ndo {\n    cout << "Iteration " << i << endl;\n    i++;\n} while(i<=n);', True, [("Enter iterations:", "int", "4")], "Do-While Counter"),
        "39": ('char c;\ncin >> c;\ncout << "Character: " << c << endl;\ncout << (c==\'q\' ? "Loop Exited" : "Processing done");', True, [("Enter character (q to exit):", "char", "q")], "Char Do-While"),
        "40": ('int s;\ncin >> s;\ncout << "Side: " << s << endl;\ncout << "Area: " << s*s << endl;\ncout << "Perimeter: " << 4*s;', True, [("Enter side of square:", "int", "7")], "Square Properties"),
        "41": ('int n;\ncin >> n;\nif(n%5==0 && n%11==0)\n    cout << n << " divisible by BOTH 5 and 11";\nelse if(n%5==0)\n    cout << n << " divisible by 5 only";\nelse if(n%11==0)\n    cout << n << " divisible by 11 only";\nelse\n    cout << n << " NOT divisible by 5 or 11";', True, [("Enter a number:", "int", "55")], "Divisibility Check"),
        "42": ('float c;\ncin >> c;\nfloat f = (c*9/5)+32;\ncout << c << " C = " << f << " F" << endl;\ncout << c << " C = " << c+273.15 << " K";', True, [("Enter Celsius:", "float", "37")], "Temperature Converter"),
        "43": ('float r;\ncin >> r;\ncout << "Radius: " << r << endl;\ncout << "Area: " << 3.14159*r*r << endl;\ncout << "Circumference: " << 2*3.14159*r;', True, [("Enter radius:", "float", "5")], "Circle Calculator"),
        "44": ('int a, b;\ncin >> a >> b;\nif(a>b)\n    cout << a << " is Greater";\nelse if(b>a)\n    cout << b << " is Greater";\nelse\n    cout << "Equal";', True, [("Enter first number:", "int", "45"), ("Enter second number:", "int", "28")], "Greater Number"),
        "45": ('int n;\ncin >> n;\nfor(int i=1; i<=n; i++)\n    cout << i << endl;', True, [("Enter N:", "int", "6")], "Count to N (loop)"),
        "46": ('int r;\ncin >> r;\ncout << "Even up to " << r << ":" << endl;\nfor(int i=2; i<=r; i+=2)\n    cout << i << " ";', True, [("Enter range:", "int", "20")], "Even in Range"),
        "47": ('int n;\ncin >> n;\nbool prime=true;\nif(n<=1) prime=false;\nfor(int i=2; i*i<=n; i++)\n    if(n%i==0) { prime=false; break; }\ncout << n << (prime ? " is Prime" : " is NOT Prime");', True, [("Enter number:", "int", "17")], "Prime Check"),
        "48": ('int n;\ncin >> n;\nlong long f=1;\nfor(int i=1; i<=n; i++)\n    f *= i;\ncout << "Factorial of " << n << " = " << f;', True, [("Enter number:", "int", "6")], "Factorial"),
    }
    return tasks.get(task_num, ('cout << "Task Not Found";', False, [], "Unknown"))


def build_cpp(body_code):
    return f"""#include <iostream>
#include <string>
using namespace std;

int main() {{
{chr(10).join('    ' + l for l in body_code.split(chr(10)))}
    return 0;
}}"""


# =========================
# ✅ FIX 2: Safe subprocess with proper error handling
# =========================
def run_cpp(code, input_data=""):
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as tmp:
            cpp_path = os.path.join(tmp, "code.cpp")
            exe_path = os.path.join(tmp, "prog")
            with open(cpp_path, "w") as f:
                f.write(code)
            comp = subprocess.run(
                ["g++", cpp_path, "-o", exe_path, "-std=c++17"],
                capture_output=True, text=True, timeout=15
            )
            if comp.returncode != 0:
                return f"Compilation Error:\n{comp.stderr[:200]}", False
            res = subprocess.run(
                [exe_path], input=input_data,
                capture_output=True, text=True, timeout=8
            )
            output = res.stdout.strip()
            if not output:
                output = "(No output / Process exited with code 0)"
            return output, True
    except subprocess.TimeoutExpired:
        return "Timeout: Program took too long", False
    except FileNotFoundError:
        return "g++ not found. Add 'g++' and 'build-essential' to packages.txt", False
    except Exception as e:
        return f"Error: {str(e)}", False


# =========================
# MAIN UI
# =========================
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

st.markdown('<div class="section-card"><div class="section-title">👤 Student Info</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    name = st.text_input("Student Name", "Zohaib Memon", key="name")
with col2:
    task_range = st.selectbox("Task Range", ["All 48", "01–17", "18–25", "26–35", "36–48"], key="range")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card"><div class="section-title">🎨 Screenshot Theme</div>', unsafe_allow_html=True)
template_names = list(TEMPLATES.keys())
selected_tmpl = st.radio("Theme", template_names, horizontal=True, key="template", label_visibility="collapsed")

st.markdown("""
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px;">
  <div style="border:2px solid #313244;border-radius:12px;overflow:hidden;">
    <div style="background:#313244;padding:6px 10px;display:flex;gap:5px;">
      <span style="width:8px;height:8px;border-radius:50%;background:#f38ba8;display:inline-block;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#f9e2af;display:inline-block;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#a6e3a1;display:inline-block;"></span>
    </div>
    <div style="background:#1e1e2e;padding:8px;font-family:monospace;font-size:11px;">
      <div style="color:#cba6f7;">#include &lt;iostream&gt;</div>
      <div style="color:#6c7086;">// Catppuccin Mocha</div>
      <div style="color:#89b4fa;">cout &lt;&lt; "Hello";</div>
    </div>
    <div style="background:#181825;padding:6px 10px;font-size:11px;color:#a6adc8;">Catppuccin Mocha · Dark Purple</div>
  </div>
  <div style="border:2px solid #30363d;border-radius:12px;overflow:hidden;">
    <div style="background:#161b22;padding:6px 10px;display:flex;gap:5px;">
      <span style="width:8px;height:8px;border-radius:50%;background:#ff5f57;display:inline-block;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#ffbd2e;display:inline-block;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#27c93f;display:inline-block;"></span>
    </div>
    <div style="background:#0d1117;padding:8px;font-family:monospace;font-size:11px;">
      <div style="color:#ff7b72;">#include &lt;iostream&gt;</div>
      <div style="color:#8b949e;">// GitHub Dark</div>
      <div style="color:#d2a8ff;">cout &lt;&lt; "Hello";</div>
    </div>
    <div style="background:#010409;padding:6px 10px;font-size:11px;color:#8b949e;">GitHub Dark · CMD Prompt</div>
  </div>
  <div style="border:2px solid #d0d7de;border-radius:12px;overflow:hidden;">
    <div style="background:#f6f8fa;padding:6px 10px;display:flex;gap:5px;">
      <span style="width:8px;height:8px;border-radius:50%;background:#ff5f57;display:inline-block;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#ffbd2e;display:inline-block;"></span>
      <span style="width:8px;height:8px;border-radius:50%;background:#27c93f;display:inline-block;"></span>
    </div>
    <div style="background:#ffffff;padding:8px;font-family:monospace;font-size:11px;">
      <div style="color:#8250df;">#include &lt;iostream&gt;</div>
      <div style="color:#6e7781;">// GitHub Light</div>
      <div style="color:#0550ae;">cout &lt;&lt; "Hello";</div>
    </div>
    <div style="background:#f6f8fa;padding:6px 10px;font-size:11px;color:#57606a;">GitHub Light · VS Code Panel</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

range_map = {
    "All 48": range(1, 49),
    "01–17": range(1, 18),
    "18–25": range(18, 26),
    "26–35": range(26, 36),
    "36–48": range(36, 49),
}
task_ids = list(range_map[task_range])

st.markdown('<div class="section-card"><div class="section-title">⌨️ Input Values for cin Tasks</div>', unsafe_allow_html=True)
st.caption("Tasks that need user input — customize values below")

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
    st.info("No cin tasks in selected range.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

col_btn1, col_btn2 = st.columns([1, 3])
with col_btn1:
    generate = st.button(f"🚀 Generate {len(task_ids) * 2} Images", use_container_width=True)
with col_btn2:
    st.markdown(f"""
    <div style="padding-top:12px;font-size:0.82rem;color:#64748b;">
        {len(task_ids)} tasks × 2 screenshots &nbsp;·&nbsp; Theme: <strong>{selected_tmpl}</strong>
    </div>
    """, unsafe_allow_html=True)

# =========================
# ✅ FIX 3: Stream directly into ZIP — no disk writes at all
# =========================
if generate:
    progress = st.progress(0)
    status_text = st.empty()

    zip_buffer = io.BytesIO()
    generated_count = 0

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, tid in enumerate(task_ids):
            key = f"{tid:02d}"
            status_text.markdown(
                f'<p style="color:#2563eb;font-family:monospace;font-size:0.82rem;">⚙️ Task {key} / {len(task_ids)} — {selected_tmpl}...</p>',
                unsafe_allow_html=True
            )

            body, has_cin, prompts, desc = get_task(key, name)
            full_code = build_cpp(body)
            formatted_code = format_cpp(full_code)

            # Code image — pure in-memory
            code_bytes = create_code_image(formatted_code, tid, f"Task {key} — {desc}", tmpl_name=selected_tmpl)
            zf.writestr(f"task_{key}_code.png", code_bytes)

            # Build input string
            input_str = ""
            if has_cin and key in cin_inputs:
                vals = cin_inputs[key]
                input_str = "\n".join(v.strip() for v in vals if v.strip())

            output, success = run_cpp(full_code, input_str)

            if has_cin and key in cin_inputs and prompts:
                input_display = []
                for i, (prompt, ptype, _) in enumerate(prompts):
                    val = cin_inputs[key][i] if i < len(cin_inputs[key]) else "?"
                    input_display.append(f">> {val}   ({prompt.rstrip(':')})")
                output_display = "\n".join(input_display) + "\n" + "-" * 38 + "\n" + output
            else:
                output_display = output

            # Output image — pure in-memory
            out_bytes = create_output_image(output_display, tid, success, tmpl_name=selected_tmpl)
            zf.writestr(f"task_{key}_output.png", out_bytes)

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
        ⬇️ &nbsp;Neeche button se ZIP download karo
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label=f"⬇️ Download {zip_name}",
        data=zip_buffer,
        file_name=zip_name,
        mime="application/zip",
        use_container_width=True,
    )