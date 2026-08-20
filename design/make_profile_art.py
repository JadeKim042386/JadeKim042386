"""Renders the images the profile readme is built around.

A GitHub profile readme is markdown with a narrow subset of HTML: no stylesheets, no
scripts, no class attributes. Anything that looks designed has to arrive as an image, so
the header, the section strips and the project card are drawn here and rendered to PNG
with headless Chrome at twice the size, then committed next to the readme.
"""
import os
import subprocess

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

SHARED_STYLE = """
  html,body{margin:0;padding:0;background:transparent;}
  *{box-sizing:border-box;}
  .card{background:radial-gradient(900px 420px at 12% -20%, #1d3055 0%, #0b1020 60%);
        color:#e6edff;font-family:Inter,"Segoe UI",ui-sans-serif,system-ui,sans-serif;
        border-radius:18px;overflow:hidden;position:relative;}
  .grid{position:absolute;inset:0;
        background-image:linear-gradient(#ffffff08 1px,transparent 1px),
                         linear-gradient(90deg,#ffffff08 1px,transparent 1px);
        background-size:44px 44px;}
  .mono{font-family:"Cascadia Mono","JetBrains Mono",Consolas,monospace;}
"""

HEADER_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><style>%s
  .card{width:1200px;height:340px;padding:44px 52px;display:flex;
        align-items:center;justify-content:space-between;}
  h1{margin:0;font-size:52px;letter-spacing:-.02em;font-weight:800;}
  .role{margin-top:12px;font-size:23px;color:#8fb4f0;font-weight:600;letter-spacing:.01em;}
  .line{margin-top:18px;font-size:17px;line-height:1.55;color:#a9b6d4;max-width:46ch;}
  .chips{margin-top:24px;display:flex;gap:9px;flex-wrap:wrap;}
  .chip{border:1px solid #33477a;background:#131f3b;border-radius:999px;
        padding:7px 15px;font-size:13.5px;color:#9fc0f5;}
  svg{flex:none;}
</style></head><body>
<div class="card"><div class="grid"></div>
  <div style="position:relative">
    <h1>Juyoung Kim</h1>
    <div class="role">Backend engineer · plant-data &amp; ML tooling</div>
    <div class="line">Spring Boot services, Unity and Python pipelines for cable routing,
      and small local tools that make an assistant read less to answer more.</div>
    <div class="chips">
      <span class="chip">Java · Spring Boot</span>
      <span class="chip">Python</span>
      <span class="chip">Flutter</span>
      <span class="chip">Claude Code plugins</span>
    </div>
  </div>
  <svg width="330" height="250" viewBox="0 0 330 250" fill="none"
       xmlns="http://www.w3.org/2000/svg" style="position:relative">
    <g stroke="#33477a" stroke-width="1.6">
      <path d="M60 60 L165 125"/><path d="M270 55 L165 125"/>
      <path d="M60 195 L165 125"/><path d="M270 190 L165 125"/>
      <path d="M60 60 L60 195"/><path d="M270 55 L270 190"/>
    </g>
    <g fill="#12203f" stroke="#5478c4" stroke-width="2">
      <circle cx="60" cy="60" r="15"/><circle cx="270" cy="55" r="15"/>
      <circle cx="60" cy="195" r="15"/><circle cx="270" cy="190" r="15"/>
    </g>
    <circle cx="165" cy="125" r="34" fill="#5eead4" opacity="0.16"/>
    <circle cx="165" cy="125" r="22" fill="#5eead4" stroke="#8ff5e4" stroke-width="2"/>
  </svg>
</div></body></html>
""" % SHARED_STYLE

SECTION_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><style>%s
  .card{width:1200px;height:74px;padding:0 26px;display:flex;align-items:center;gap:16px;
        border-radius:12px;background:linear-gradient(90deg,#16233f 0%%,#0d1428 70%%);
        border:1px solid #24304d;}
  .mark{width:8px;height:34px;border-radius:4px;background:%s;}
  .title{font-family:Inter,"Segoe UI",sans-serif;font-size:22px;font-weight:700;
         letter-spacing:.01em;color:#e6edff;}
  .sub{margin-left:auto;font-size:14.5px;color:#7f8dad;}
</style></head><body>
<div class="card"><span class="mark"></span><span class="title">%s</span>
  <span class="sub mono">%s</span></div></body></html>
"""

SECTIONS = [
    ("section-featured.png", "#5eead4", "Featured work", "one tool, in depth"),
    ("section-projects.png", "#8ab4ff", "Projects", "what I have shipped"),
    ("section-skills.png", "#ffd479", "Skills", "what I reach for"),
    ("section-stats.png", "#f0a6ff", "GitHub", "activity"),
    ("section-more.png", "#9fb4d8", "Background", "certificates &amp; history"),
]


def render(html, output_name, width, height):
    """Write the page, screenshot it at twice the size, and return the file path."""
    page_path = os.path.join(OUTPUT_DIR, output_name.replace(".png", ".html"))
    image_path = os.path.join(OUTPUT_DIR, output_name)
    with open(page_path, "w", encoding="utf-8") as handle:
        handle.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--default-background-color=00000000",
                    f"--window-size={width},{height}", f"--screenshot={image_path}",
                    "file:///" + page_path.replace("\\", "/")], check=True, capture_output=True)
    return image_path


def main():
    made = [render(HEADER_HTML, "header.png", 1200, 340)]
    for file_name, colour, title, subtitle in SECTIONS:
        made.append(render(SECTION_HTML % (SHARED_STYLE, colour, title, subtitle),
                           file_name, 1200, 74))
    for path in made:
        print(f"{os.path.basename(path)} - {os.path.getsize(path) / 1000:.0f} KB")


if __name__ == "__main__":
    main()
