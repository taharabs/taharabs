#!/usr/bin/env python3
"""Generate the SVG assets used by the profile README (light + dark).

Run:  python scripts/build_assets.py      ->  writes ./assets/*.svg
Edit the CONTENT section below, re-run, commit.
Text widths are measured with Inter (if Pillow + Inter are installed) so chips
and wrapped lines never overflow; otherwise a safe character-width estimate is used.
"""
from __future__ import annotations

import html
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ----------------------------------------------------------------------------- CONTENT
NAME = "Mohamed Tahar Ababsa"
TITLE = "IT Engineer & Software Developer"
PITCH = [
    "I build the software that runs business infrastructure:",
    "automation, data pipelines and the internal tools teams rely on.",
]
CHIPS = ["Blida, Algeria", "Open to opportunities", "Arabic · French · English"]
LAYERS = [  # header diagram, top to bottom
    ("Software & AI", "web apps · APIs · edge AI", "purple"),
    ("Automation & Data", "Python · PowerShell · SQL", "blue"),
    ("Infrastructure", "servers · AD · networks", "rose"),
]

IMPACT = [
    ("~40%", "less manual work through Python & PowerShell automation"),
    ("4+ yrs", "building web apps and business tools as a freelancer"),
    ("FPGA", "U-Net image segmentation deployed on a PYNQ-Z2 board"),
    ("M.Sc.", "Embedded Systems Engineering, Saad Dahlab University"),
]

PROJECTS = [
    dict(slug="wach-ntayab", color="green", label="PWA · OFFLINE-FIRST", arabic="واش نطيبو اليوم؟",
         title="What should we cook today?",
         desc="Offline-first PWA that plans the day's Algerian meals from the ingredients at home. "
              "100+ dishes, weekly planner, WhatsApp shopping list.",
         tags=["JavaScript", "PWA", "Service Worker", "RTL"], cta="Live demo"),
    dict(slug="task-manager", color="blue", label="PRODUCTIVITY · ZERO DEPENDENCIES",
         title="Notion-style Task Manager",
         desc="Board, list, table and calendar views with drag and drop, plus a local "
              "assistant that understands dates like “next friday”.",
         tags=["JavaScript", "HTML5", "CSS3", "Vercel"], cta="Live demo"),
    dict(slug="unet-fpga", color="purple", label="EDGE AI · EMBEDDED",
         title="U-Net on FPGA",
         desc="Retinal image segmentation trained in TensorFlow/Keras and deployed "
              "on a Xilinx PYNQ-Z2 board (CDTA research internship).",
         tags=["TensorFlow", "Keras", "Python", "PYNQ-Z2"], cta="Read the write-up"),
    dict(slug="portfolio", color="rose", label="WEB · NODE.JS",
         title="techbytahar — Portfolio",
         desc="Personal site with project write-ups and an Express backend for the "
              "contact form, deployed on Vercel.",
         tags=["HTML/CSS", "JavaScript", "Node.js", "Express"], cta="Visit the site"),
]

STACK = [
    ("Languages", "purple", ["Python", "JavaScript", "C / C++", "PowerShell", "SQL", "HTML / CSS"]),
    ("Backend & web", "blue", ["FastAPI", "Django", "Node.js", "Express", "React", "REST APIs"]),
    ("Data", "green", ["SQL Server", "PostgreSQL", "MySQL", "MongoDB", "Oracle", "SQLite"]),
    ("Infrastructure", "rose", ["Windows Server", "Active Directory / GPO", "Linux", "VMware ESXi",
                                "Proxmox", "Docker", "Git"]),
    ("Network & monitoring", "amber", ["TCP/IP · LAN/WAN", "Wireshark", "PRTG", "Zabbix (learning)"]),
    ("AI & embedded", "purple", ["TensorFlow", "Keras", "Computer vision", "FPGA · PYNQ-Z2"]),
]

BUTTONS = [  # (file, label, icon, color)
    ("btn-portfolio", "Portfolio", "globe", "purple"),
    ("btn-linkedin", "LinkedIn", "in", "blue"),
    ("btn-email", "Email me", "mail", "rose"),
]

# ----------------------------------------------------------------------------- THEME
FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Inter, Helvetica, Arial, "
        "sans-serif")
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", ink="#f0f6fc", text="#c9d1d9",
                 muted="#8b949e", grid="#ffffff", grid_op="0.035",
                 purple="#a78bfa", blue="#60a5fa", rose="#fb7185", green="#4ade80", amber="#fbbf24",
                 tint_op="0.14"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", ink="#1f2328", text="#424a53",
                  muted="#656d76", grid="#1f2328", grid_op="0.04",
                  purple="#7c3aed", blue="#2563eb", rose="#e11d48", green="#16a34a", amber="#b45309",
                  tint_op="0.10"),
}

# ----------------------------------------------------------------------------- TEXT METRICS
_fonts: dict = {}


def _font(size: float, weight: str):
    try:
        from PIL import ImageFont
    except ImportError:
        return None
    key = (round(size * 4), weight)
    if key not in _fonts:
        name = {"400": "Inter-Regular.otf", "500": "Inter-Medium.otf",
                "600": "Inter-SemiBold.otf", "700": "Inter-Bold.otf"}[weight]
        for d in ("/usr/share/fonts/opentype/inter", "/Library/Fonts", os.path.expanduser("~/.fonts")):
            p = Path(d) / name
            if p.exists():
                _fonts[key] = ImageFont.truetype(str(p), int(size * 4))
                break
        else:
            _fonts[key] = None
    return _fonts[key]


def tw(text: str, size: float, weight: str = "400") -> float:
    """Width of text in px, with a 7% margin for font differences between OSes."""
    f = _font(size, weight)
    if f is not None:
        return f.getlength(text) / 4 * 1.07
    return len(text) * size * (0.58 if weight in ("600", "700") else 0.54)


def wrap(text: str, size: float, max_w: float, weight: str = "400") -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if tw(trial, size, weight) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def svg(w: int, h: int, body: str, label: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(label)}" font-family="{esc(FONT)}">\n'
            f"<title>{esc(label)}</title>\n{body}\n</svg>\n")


def chip(x, y, text, color, t, size=12.5, h=26, filled=False, weight="500"):
    w = tw(text, size, weight) + 22
    fill = t[color]
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" '
            f'fill-opacity="{t["tint_op"] if not filled else 1}" stroke="{fill}" stroke-opacity="0.45"/>'
            f'<text x="{x + w/2:.1f}" y="{y + h/2 + size*0.36:.1f}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="middle" fill="{t["ink"]}">{esc(text)}</text>'), w


def grid_pattern(t, pid):
    return (f'<defs><pattern id="{pid}" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<path d="M24 0H0V24" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_op"]}"/>'
            f"</pattern></defs>")


def accent_gradient(t, gid):
    return (f'<linearGradient id="{gid}" x1="0" x2="1" y1="0" y2="0">'
            f'<stop offset="0" stop-color="{t["purple"]}"/><stop offset="0.5" stop-color="{t["blue"]}"/>'
            f'<stop offset="1" stop-color="{t["rose"]}"/></linearGradient>')


# ----------------------------------------------------------------------------- ASSETS
def header(t):
    W, H = 830, 270
    b = [grid_pattern(t, "g"), f"<defs>{accent_gradient(t, 'acc')}</defs>",
         "<style>@keyframes p{0%,100%{opacity:.35}50%{opacity:1}}"
         ".d1{animation:p 2.4s ease-in-out infinite}.d2{animation:p 2.4s ease-in-out .8s infinite}"
         ".d3{animation:p 2.4s ease-in-out 1.6s infinite}"
         "@keyframes b{0%,100%{opacity:1}50%{opacity:.25}}.live{animation:b 1.6s ease-in-out infinite}"
         "@keyframes c{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:c 1.1s step-end infinite}</style>",
         f'<defs><clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>',
         f'<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#g)"/>',
         f'<rect x="0" y="0" width="{W}" height="4" fill="url(#acc)"/></g>',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{t["border"]}"/>']
    x = 36
    b.append(f'<text x="{x}" y="50" font-family="{esc(MONO)}" font-size="13" fill="{t["purple"]}">'
             f'$ whoami<tspan class="cur" fill="{t["purple"]}"> ▍</tspan></text>')
    b.append(f'<text x="{x}" y="92" font-size="34" font-weight="700" fill="{t["ink"]}" '
             f'letter-spacing="-0.5">{esc(NAME)}</text>')
    b.append(f'<text x="{x}" y="124" font-size="18" font-weight="600" fill="url(#acc)">{esc(TITLE)}</text>')
    for i, line in enumerate(PITCH):
        b.append(f'<text x="{x}" y="{160 + i*21}" font-size="14.5" fill="{t["text"]}">{esc(line)}</text>')
    cx = x
    for i, c in enumerate(CHIPS):
        color = ["blue", "green", "purple"][i]
        s, w = chip(cx + (14 if i == 1 else 0), 214, c, color, t, size=12.5, h=28)
        if i == 1:  # availability chip with live dot
            w2 = w + 14
            b.append(f'<rect x="{cx:.1f}" y="214" width="{w2:.1f}" height="28" rx="14" fill="{t["green"]}" '
                     f'fill-opacity="{t["tint_op"]}" stroke="{t["green"]}" stroke-opacity="0.45"/>')
            b.append(f'<circle class="live" cx="{cx + 15:.1f}" cy="228" r="4" fill="{t["green"]}"/>')
            b.append(f'<text x="{cx + 25:.1f}" y="{228 + 12.5*0.36:.1f}" font-size="12.5" font-weight="500" '
                     f'fill="{t["ink"]}">{esc(c)}</text>')
            w = w2
        else:
            b.append(s)
        cx += w + 10
    # right: three-layer diagram
    lx, lw, lh = 560, 236, 50
    ys = [44, 108, 172]
    b.append(f'<line x1="{lx - 18}" y1="{ys[0] + lh/2}" x2="{lx - 18}" y2="{ys[2] + lh/2}" '
             f'stroke="{t["border"]}" stroke-width="2" stroke-dasharray="3 5"/>')
    for i, ((name, sub, col), y) in enumerate(zip(LAYERS, ys)):
        b.append(f'<g><rect x="{lx}" y="{y}" width="{lw}" height="{lh}" rx="10" fill="{t[col]}" '
                 f'fill-opacity="{t["tint_op"]}" stroke="{t[col]}" stroke-opacity="0.7"/>'
                 f'<rect x="{lx}" y="{y}" width="4" height="{lh}" rx="2" fill="{t[col]}"/>'
                 f'<text x="{lx + 18}" y="{y + 21}" font-size="14" font-weight="600" fill="{t["ink"]}">{esc(name)}</text>'
                 f'<text x="{lx + 18}" y="{y + 39}" font-size="11.5" fill="{t["muted"]}">{esc(sub)}</text></g>')
        b.append(f'<circle class="d{i+1}" cx="{lx - 18}" cy="{y + lh/2}" r="6" fill="{t[col]}"/>')
        b.append(f'<line x1="{lx - 12}" y1="{y + lh/2}" x2="{lx}" y2="{y + lh/2}" stroke="{t[col]}" '
                 f'stroke-opacity="0.7" stroke-width="1.5"/>')
    b.append(f'<text x="{lx + lw/2}" y="246" font-size="11.5" text-anchor="middle" fill="{t["muted"]}">'
             f'end to end, from the server room to the UI</text>')
    return svg(W, H, "\n".join(b), f"{NAME} — {TITLE}. {' '.join(PITCH)}")


def impact(t):
    W, H, gap = 830, 128, 12
    tw_ = (W - 3 * gap) / 4
    b = [f"<defs>{accent_gradient(t, 'acc')}</defs>"]
    for i, (big, label) in enumerate(IMPACT):
        x = i * (tw_ + gap)
        b.append(f'<rect x="{x + .5:.1f}" y="0.5" width="{tw_ - 1:.1f}" height="{H-1}" rx="12" '
                 f'fill="{t["panel"]}" stroke="{t["border"]}"/>')
        b.append(f'<text x="{x + 18:.1f}" y="46" font-size="28" font-weight="700" fill="url(#acc)" '
                 f'letter-spacing="-0.5">{esc(big)}</text>')
        for j, line in enumerate(wrap(label, 12.5, tw_ - 36)[:3]):
            b.append(f'<text x="{x + 18:.1f}" y="{72 + j*17}" font-size="12.5" fill="{t["text"]}">'
                     f'{esc(line)}</text>')
    return svg(W, H, "\n".join(b), "Impact: " + "; ".join(f"{a} {b_}" for a, b_ in IMPACT))


def card(p, t):
    W, H = 410, 214
    col = t[p["color"]]
    b = [f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>',
         f'<rect x="0" y="0" width="{W}" height="4" fill="{col}" clip-path="url(#c)"/>',
         f'<text x="20" y="34" font-size="10.5" font-weight="600" letter-spacing="1" fill="{col}">'
         f'{esc(p["label"])}</text>']
    if p.get("arabic"):
        b.append(f'<text x="{W - 20}" y="35" font-size="13" text-anchor="end" fill="{t["muted"]}">'
                 f'{esc(p["arabic"])}</text>')
    b.append(f'<text x="20" y="62" font-size="18" font-weight="700" fill="{t["ink"]}">{esc(p["title"])}</text>')
    for j, line in enumerate(wrap(p["desc"], 13, W - 40)[:3]):
        b.append(f'<text x="20" y="{88 + j*19}" font-size="13" fill="{t["text"]}">{esc(line)}</text>')
    cx = 20
    for tag in p["tags"]:
        s, w = chip(cx, 146, tag, p["color"], t, size=11, h=22)
        b.append(s)
        cx += w + 6
    b.append(f'<line x1="20" y1="182" x2="{W-20}" y2="182" stroke="{t["border"]}"/>')
    b.append(f'<text x="20" y="202" font-size="12.5" font-weight="600" fill="{col}">{esc(p["cta"])} →</text>')
    b.append(f'<text x="{W - 20}" y="202" font-size="11.5" text-anchor="end" fill="{t["muted"]}">'
             f'github.com/taharabs</text>')
    return svg(W, H, "\n".join(b), f'{p["title"]}: {p["desc"]}')


def stack(t):
    W, row_h = 830, 40
    label_w = 40 + max(tw(n, 13, '600') for n, _, _ in STACK) + 22
    rows = []
    for name, col, items in STACK:  # flow chips, wrapping to new lines if needed
        lines, cur, cx = [], [], 0
        for it in items:
            w = tw(it, 12.5, "500") + 22
            if cx + w > W - label_w - 40 and cur:
                lines.append(cur)
                cur, cx = [], 0
            cur.append(it)
            cx += w + 8
        lines.append(cur)
        rows.append((name, col, lines))
    H = 24 + sum(len(r[2]) * row_h for r in rows) + 8
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>']
    y = 20
    for k, (name, col, lines) in enumerate(rows):
        if k:
            b.append(f'<line x1="20" y1="{y - 6}" x2="{W-20}" y2="{y - 6}" stroke="{t["border"]}" stroke-opacity="0.6"/>')
        b.append(f'<circle cx="28" cy="{y + 13}" r="4" fill="{t[col]}"/>')
        b.append(f'<text x="40" y="{y + 17.5}" font-size="13" font-weight="600" fill="{t["ink"]}">{esc(name)}</text>')
        for line in lines:
            cx = label_w
            for it in line:
                s, w = chip(cx, y, it, col, t)
                b.append(s)
                cx += w + 8
            y += row_h
    return svg(W, H, "\n".join(b), "Tech stack: " + "; ".join(f"{n}: {', '.join(i)}" for n, _, i in STACK))


def button(label, icon, color):
    t = THEMES["light"]
    col = t[color]
    W, H = 150, 38
    icons = {
        "globe": (f'<circle cx="23" cy="19" r="8" fill="none" stroke="#fff" stroke-width="1.6"/>'
                  f'<ellipse cx="23" cy="19" rx="3.6" ry="8" fill="none" stroke="#fff" stroke-width="1.4"/>'
                  f'<line x1="15" y1="19" x2="31" y2="19" stroke="#fff" stroke-width="1.4"/>'),
        "in": (f'<rect x="15" y="11" width="16" height="16" rx="3" fill="#fff"/>'
               f'<text x="23" y="23.5" font-size="11.5" font-weight="700" text-anchor="middle" fill="{col}">in</text>'),
        "mail": (f'<rect x="15" y="13" width="16" height="12" rx="2" fill="none" stroke="#fff" stroke-width="1.6"/>'
                 f'<path d="M15.8 14 23 20l7.2-6" fill="none" stroke="#fff" stroke-width="1.6"/>'),
    }
    b = (f'<rect width="{W}" height="{H}" rx="9" fill="{col}"/>{icons[icon]}'
         f'<text x="{(W + 40) / 2 - 2}" y="{H/2 + 13.5*0.36:.1f}" font-size="13.5" font-weight="600" '
         f'text-anchor="middle" fill="#ffffff">{esc(label)}</text>')
    return svg(W, H, b, label)


def footer(t):
    W, H = 830, 64
    b = [f"<defs>{accent_gradient(t, 'acc')}</defs>",
         f'<rect x="0" y="0" width="{W}" height="3" rx="1.5" fill="url(#acc)"/>',
         f'<text x="{W/2}" y="38" font-size="15" font-weight="600" text-anchor="middle" fill="{t["ink"]}">'
         f'Reliable systems, less manual work, clear documentation.</text>',
         f'<text x="{W/2}" y="58" font-size="12" text-anchor="middle" fill="{t["muted"]}">'
         f'Mohamed Tahar Ababsa · Blida, Algeria</text>']
    return svg(W, H, "\n".join(b), "Reliable systems, less manual work, clear documentation.")


def main():
    OUT.mkdir(exist_ok=True)
    files = {}
    for mode, t in THEMES.items():
        files[f"header-{mode}.svg"] = header(t)
        files[f"impact-{mode}.svg"] = impact(t)
        files[f"stack-{mode}.svg"] = stack(t)
        files[f"footer-{mode}.svg"] = footer(t)
        for p in PROJECTS:
            files[f'card-{p["slug"]}-{mode}.svg'] = card(p, t)
    for f, label, icon, color in BUTTONS:
        files[f"{f}.svg"] = button(label, icon, color)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
