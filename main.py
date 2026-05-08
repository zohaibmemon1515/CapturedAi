import streamlit as st
import os
import subprocess
import random
import tempfile
import io
import zipfile
from PIL import Image, ImageDraw, ImageFont

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="CAPTURED AI",
    page_icon="🖥️",
    layout="wide"
)

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
        font-weight: 500;
        display: inline-block;
    }

    .badge-blue {
        border-color: #bfdbfe;
        background: #eff6ff;
        color: #1d4ed8;
    }

    .badge-green {
        border-color: #bbf7d0;
        background: #f0fdf4;
        color: #15803d;
    }

    .badge-amber {
        border-color: #fde68a;
        background: #fffbeb;
        color: #b45309;
    }

    .badge-purple {
        border-color: #ddd6fe;
        background: #f5f3ff;
        color: #6d28d9;
    }

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
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
    }

    .stSelectbox > div > div {
        background: #f8fafc !important;
        border: 1px solid #e2e6ec !important;
        border-radius: 10px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 12px 32px !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
    }

    .success-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 16px 20px;
        color: #166534;
        font-size: 0.875rem;
        margin-top: 16px;
        line-height: 1.7;
    }

</style>
""", unsafe_allow_html=True)

# =========================
# FONT LOADING
# =========================
def get_font(size):
    font_options = [
        "consola.ttf",
        "Consolas.ttf",
        "DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]

    for f in font_options:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass

    return ImageFont.load_default()

# =========================
# THEMES
# =========================
TEMPLATES = {
    "GitHub Dark": {
        "bg": (13, 17, 23),
        "text": (230, 230, 230),
        "line": (100, 100, 100),
        "header": (22, 27, 34),
    },

    "GitHub Light": {
        "bg": (255, 255, 255),
        "text": (36, 41, 47),
        "line": (200, 200, 200),
        "header": (246, 248, 250),
    },

    "Catppuccin Mocha": {
        "bg": (30, 30, 46),
        "text": (205, 214, 244),
        "line": (80, 80, 100),
        "header": (49, 50, 68),
    }
}

# =========================
# CODE SCREENSHOT
# =========================
def create_code_screenshot(code, filename, task_num, tmpl_name):

    t = TEMPLATES[tmpl_name]

    lines = code.split("\n")

    font = get_font(18)

    width = 1200
    height = max(500, 120 + len(lines) * 32)

    img = Image.new("RGB", (width, height), t["bg"])

    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, width, 60], fill=t["header"])

    draw.text(
        (20, 18),
        f"task_{task_num}.cpp",
        fill=t["text"],
        font=get_font(20)
    )

    # Traffic lights
    draw.ellipse([15, 15, 30, 30], fill=(255, 95, 87))
    draw.ellipse([40, 15, 55, 30], fill=(255, 189, 46))
    draw.ellipse([65, 15, 80, 30], fill=(39, 201, 63))

    y = 90

    for idx, line in enumerate(lines):

        draw.text(
            (25, y),
            str(idx + 1),
            fill=(120, 120, 120),
            font=get_font(16)
        )

        draw.text(
            (90, y),
            line,
            fill=t["text"],
            font=font
        )

        y += 30

    img.save(filename, quality=95)
    img.close()

# =========================
# OUTPUT SCREENSHOT
# =========================
def create_output_screenshot(output_text, filename, task_num, tmpl_name):

    t = TEMPLATES[tmpl_name]

    lines = output_text.split("\n")

    width = 1200
    height = max(400, 120 + len(lines) * 30)

    img = Image.new("RGB", (width, height), t["bg"])

    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, 60], fill=t["header"])

    draw.text(
        (20, 18),
        f"Output — Task {task_num}",
        fill=t["text"],
        font=get_font(20)
    )

    y = 90

    for line in lines:

        draw.text(
            (30, y),
            line,
            fill=t["text"],
            font=get_font(18)
        )

        y += 30

    img.save(filename, quality=95)
    img.close()

# =========================
# FORMATTER
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

        if line.endswith("{"):
            indent += 1

    return "\n".join(formatted)

# =========================
# TASKS
# =========================
def get_task(task_num, name):

    tasks = {

        "01": (
            f'cout << "Hello World!" << endl;\ncout << "Created By: {name}";',
            False,
            [],
            "Hello World"
        ),

        "02": (
            'int a,b;\ncin >> a >> b;\ncout << "Sum = " << a+b;',
            True,
            [("Enter First Number", "10"), ("Enter Second Number", "20")],
            "Addition"
        ),

        "03": (
            'int n;\ncin >> n;\nif(n%2==0)\ncout << "Even";\nelse\ncout << "Odd";',
            True,
            [("Enter Number", "7")],
            "Even Odd"
        ),

        "04": (
            'for(int i=1;i<=5;i++)\ncout << i << endl;',
            False,
            [],
            "Loop"
        ),

        "05": (
            'int n;\ncin >> n;\nlong long f=1;\nfor(int i=1;i<=n;i++)\nf*=i;\ncout << "Factorial = " << f;',
            True,
            [("Enter Number", "5")],
            "Factorial"
        ),
    }

    return tasks.get(task_num)

# =========================
# BUILD CPP
# =========================
def build_cpp(body_code):

    return f"""#include <iostream>
using namespace std;

int main()
{{
{chr(10).join('    ' + l for l in body_code.split(chr(10)))}

    return 0;
}}
"""

# =========================
# RUN CPP
# =========================
def run_cpp(code, input_data=""):

    with tempfile.TemporaryDirectory() as tmp:

        cpp_path = os.path.join(tmp, "code.cpp")
        exe_path = os.path.join(tmp, "prog")

        with open(cpp_path, "w", encoding="utf-8") as f:
            f.write(code)

        try:

            compile_process = subprocess.run(
                [
                    "g++",
                    cpp_path,
                    "-std=c++17",
                    "-O2",
                    "-o",
                    exe_path
                ],
                capture_output=True,
                text=True,
                timeout=20
            )

            if compile_process.returncode != 0:
                return (
                    "Compilation Error:\n\n"
                    + compile_process.stderr,
                    False
                )

            os.chmod(exe_path, 0o755)

            run_process = subprocess.run(
                [exe_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=10
            )

            output = run_process.stdout.strip()

            if run_process.stderr:
                output += "\n" + run_process.stderr

            if not output:
                output = "(Program executed successfully with no output)"

            return output, True

        except subprocess.TimeoutExpired:
            return "Execution Timeout", False

        except FileNotFoundError:
            return (
                "g++ compiler not found.\n"
                "Add packages.txt with:\n"
                "g++\n"
                "build-essential"
            ), False

        except Exception as e:
            return f"Runtime Error:\n{str(e)}", False

# =========================
# UI
# =========================
st.markdown("""
<div class="app-header">
    <div>
        <div class="app-title">🖥️ CAPTURED AI</div>
        <div class="app-subtitle">
            Premium C++ Lab Manual Generator
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="badge-row">
    <span class="badge badge-blue">📸 Screenshots</span>
    <span class="badge badge-green">⚡ Real Output</span>
    <span class="badge badge-purple">🎨 Themes</span>
</div>
""", unsafe_allow_html=True)

# =========================
# INPUTS
# =========================
st.markdown("""
<div class="section-card">
<div class="section-title">
👤 Student Information
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Student Name",
        "Zohaib Memon"
    )

with col2:
    selected_tmpl = st.selectbox(
        "Theme",
        list(TEMPLATES.keys())
    )

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TASK INPUTS
# =========================
cin_inputs = {}

for tid in ["01", "02", "03", "04", "05"]:

    body, has_cin, prompts, desc = get_task(tid, name)

    if has_cin:

        st.markdown(f"""
        <div class="section-card">
        <div class="section-title">
        Task {tid} — {desc}
        </div>
        """, unsafe_allow_html=True)

        vals = []

        cols = st.columns(len(prompts))

        for i, prompt_data in enumerate(prompts):

            prompt, default = prompt_data

            with cols[i]:

                v = st.text_input(
                    prompt,
                    default,
                    key=f"{tid}_{i}"
                )

                vals.append(v)

        cin_inputs[tid] = vals

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# GENERATE
# =========================
generate = st.button(
    "🚀 Generate Screenshots",
    use_container_width=True
)

# =========================
# GENERATE LOGIC
# =========================
if generate:

    progress = st.progress(0)

    zip_buffer = io.BytesIO()

    task_ids = ["01", "02", "03", "04", "05"]

    total_images = len(task_ids) * 2

    done = 0

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zf:

        for idx, tid in enumerate(task_ids):

            body, has_cin, prompts, desc = get_task(tid, name)

            full_code = build_cpp(body)

            formatted_code = format_cpp(full_code)

            # =========================
            # CODE IMAGE
            # =========================
            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            ) as tmp_code:

                tmp_code_path = tmp_code.name

            create_code_screenshot(
                formatted_code,
                tmp_code_path,
                tid,
                selected_tmpl
            )

            with open(tmp_code_path, "rb") as f:

                zf.writestr(
                    f"task_{tid}_code.png",
                    f.read()
                )

            os.unlink(tmp_code_path)

            # =========================
            # INPUT STRING
            # =========================
            input_str = ""

            if has_cin and tid in cin_inputs:

                input_str = "\n".join(cin_inputs[tid])

            # =========================
            # RUN CODE
            # =========================
            output, success = run_cpp(
                full_code,
                input_str
            )

            # =========================
            # OUTPUT DISPLAY
            # =========================
            if has_cin and tid in cin_inputs:

                inp_lines = []

                for i, val in enumerate(cin_inputs[tid]):

                    inp_lines.append(f">> {val}")

                output_display = (
                    "\n".join(inp_lines)
                    + "\n----------------------\n"
                    + output
                )

            else:

                output_display = output

            # =========================
            # OUTPUT IMAGE
            # =========================
            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            ) as tmp_out:

                tmp_out_path = tmp_out.name

            create_output_screenshot(
                output_display,
                tmp_out_path,
                tid,
                selected_tmpl
            )

            with open(tmp_out_path, "rb") as f:

                zf.writestr(
                    f"task_{tid}_output.png",
                    f.read()
                )

            os.unlink(tmp_out_path)

            done += 2

            progress.progress(done / total_images)

    zip_buffer.seek(0)

    st.markdown(f"""
    <div class="success-box">
        ✅ Successfully Generated<br>
        📸 {total_images} Images<br>
        🎨 Theme: {selected_tmpl}
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download ZIP",
        data=zip_buffer,
        file_name="CapturedAI.zip",
        mime="application/zip",
        use_container_width=True
    )