#!/usr/bin/env python3
"""Writes assets/components/layers-exploded.svg: the layers of a window drawn
apart, each plane holding what is typically drawn in it, and the window they
make together. Run from the site's folder: python3 tools/component-shots/layers_svg.py
"""
W, H = 260, 150            # one plane, in the window's own coordinates
ACCENT, INK, MUTED, LINE = "#3DAEE9", "#1F2328", "#5B6572", "#C3C9D1"


def background():
    return f'<rect width="{W}" height="{H}" fill="#E4E8EE"/>'


def content():
    out = [f'<rect width="{W}" height="20" fill="#FFFFFF"/>',
           f'<rect y="20" width="{W}" height="1" fill="{LINE}"/>',
           '<rect x="8" y="6" width="26" height="8" rx="2" fill="#D5DAE1"/>',
           '<rect x="40" y="6" width="26" height="8" rx="2" fill="#D5DAE1"/>',
           f'<rect y="21" width="62" height="{H - 21}" fill="#F6F7F9"/>',
           f'<rect x="62" y="21" width="1" height="{H - 21}" fill="{LINE}"/>']
    for i in range(4):
        out.append(f'<rect x="8" y="{32 + i * 14}" width="{44 - i * 5}" height="6" rx="2" fill="#C9CFD8"/>')
    out.append(f'<rect x="76" y="34" width="90" height="10" rx="2" fill="{INK}" fill-opacity="0.8"/>')
    for i in range(3):
        out.append(f'<rect x="76" y="{56 + i * 13}" width="{160 - i * 26}" height="6" rx="2" fill="#C9CFD8"/>')
    out.append(f'<rect x="76" y="104" width="46" height="18" rx="4" fill="#FFFFFF" stroke="{LINE}"/>')
    return "".join(out)


def floating():
    return (f'<circle cx="{W - 26}" cy="{H - 26}" r="14" fill="{ACCENT}"/>'
            f'<rect x="{W - 33}" y="{H - 27.5}" width="14" height="3" fill="#FFFFFF"/>'
            f'<rect x="{W - 27.5}" y="{H - 33}" width="3" height="14" fill="#FFFFFF"/>')


def modal():
    return (f'<rect width="{W}" height="{H}" fill="#000000" fill-opacity="0.22"/>'
            f'<rect x="58" y="38" width="144" height="76" rx="6" fill="#FFFFFF" stroke="{LINE}"/>'
            f'<rect x="70" y="50" width="60" height="8" rx="2" fill="{INK}" fill-opacity="0.8"/>'
            '<rect x="70" y="66" width="118" height="6" rx="2" fill="#C9CFD8"/>'
            f'<rect x="112" y="88" width="36" height="16" rx="4" fill="#FFFFFF" stroke="{LINE}"/>'
            f'<rect x="154" y="88" width="36" height="16" rx="4" fill="{ACCENT}"/>')


def popup():
    out = [f'<rect x="8" y="22" width="84" height="62" rx="4" fill="#FFFFFF" stroke="{LINE}"/>']
    for i in range(3):
        out.append(f'<rect x="16" y="{32 + i * 16}" width="{58 - i * 8}" height="6" rx="2" fill="#B9C0CA"/>')
    return "".join(out)


def tooltip():
    return ('<rect x="96" y="124" width="74" height="18" rx="4" fill="#2B3037"/>'
            '<rect x="104" y="130" width="58" height="6" rx="2" fill="#E7E9EC"/>')


def notification():
    return (f'<rect x="{W - 104}" y="28" width="96" height="26" rx="5" fill="#FFFFFF" stroke="{LINE}"/>'
            f'<circle cx="{W - 92}" cy="41" r="4" fill="#2E9E5B"/>'
            f'<rect x="{W - 82}" y="38" width="62" height="6" rx="2" fill="#B9C0CA"/>')


def drag():
    return (f'<rect x="150" y="62" width="58" height="18" rx="9" fill="#FFFFFF" fill-opacity="0.9" stroke="{ACCENT}" stroke-dasharray="4 3"/>'
            '<rect x="160" y="68" width="38" height="6" rx="2" fill="#B9C0CA"/>'
            f'<path d="M204 74 l0 16 l4 -4 l3 7 l3 -1.5 l-3 -7 l6 0 z" fill="{INK}" stroke="#FFFFFF" stroke-width="1"/>')


def debug():
    return ('<rect x="1" y="22" width="61" height="127" fill="none" stroke="#D6336C" stroke-dasharray="5 3"/>'
            '<rect x="4" y="132" width="40" height="13" rx="2" fill="#D6336C"/>'
            '<rect x="9" y="136" width="30" height="5" rx="1.5" fill="#FFFFFF"/>')


LAYERS = [
    ("Background", "wallpapers, backdrops", background),
    ("Content", "where components draw by default", content),
    ("Floating", "sticky headers, floating buttons", floating),
    ("Modal", "dialogs, over a dimmed page", modal),
    ("Popup", "menus, dropdowns", popup),
    ("Tooltip", "tooltips", tooltip),
    ("Notification", "toasts", notification),
    ("Drag", "what follows the pointer in a drag", drag),
    ("Debug", "inspector overlays", debug),
]

SKEW, SQUASH, STEP = -0.8, 0.4, 62
LEFT, TOP = 156, 44
width, height = 760, TOP + 8 * STEP + int(H * SQUASH) + 250
bottom = TOP + 8 * STEP

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" '
       'aria-label="The layers of a window drawn apart, Background at the bottom and Debug at the top, each with what is drawn in it, and the window they make together">',
       '<style>.n{font:600 14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#1F2328}'
       '.d{font:13px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#5B6572}'
       '.t{font:600 13px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#1F2328}</style>',
       f'<rect width="{width}" height="{height}" fill="#F1F2F4"/>',
       f'<clipPath id="plane"><rect width="{W}" height="{H}"/></clipPath>']
for i, (name, desc, draw) in enumerate(LAYERS):
    f = bottom - i * STEP
    out.append(f'<g transform="matrix(1 0 {SKEW} {SQUASH} {LEFT} {f})">'
               f'<rect width="{W}" height="{H}" fill="#FFFFFF" fill-opacity="{1 if i < 2 else 0.28}"/>'
               f'<g clip-path="url(#plane)">{draw()}</g>'
               f'<rect width="{W}" height="{H}" fill="none" stroke="{ACCENT if name == "Content" else LINE}" stroke-width="1.6"/></g>')
    y = f + H * SQUASH / 2
    edge = LEFT + W + SKEW * H / 2
    out.append(f'<line x1="{edge + 8}" y1="{y}" x2="472" y2="{y}" stroke="{LINE}"/>')
    out.append(f'<text class="n" x="482" y="{y - 2}">{name}</text>')
    out.append(f'<text class="d" x="482" y="{y + 14}">{desc}</text>')
# the order they are drawn in
ax = 18
out.append(f'<line x1="{ax}" y1="{bottom + H * SQUASH}" x2="{ax}" y2="{TOP + 8}" stroke="{MUTED}" stroke-width="1.2"/>')
out.append(f'<polygon points="{ax - 4},{TOP + 10} {ax + 4},{TOP + 10} {ax},{TOP}" fill="{MUTED}"/>')
out.append(f'<text class="d" x="{ax + 8}" y="{TOP + 4}">drawn last</text>')
out.append(f'<text class="d" x="{ax + 8}" y="{bottom + H * SQUASH + 4}">drawn first</text>')
# what they make together
cy = bottom + int(H * SQUASH) + 60
out.append(f'<text class="t" x="{LEFT - 120}" y="{cy - 12}">Together: what the window shows</text>')
out.append(f'<g transform="translate({LEFT - 120} {cy})"><g clip-path="url(#plane)">'
           + "".join(draw() for _, _, draw in LAYERS)
           + f'</g><rect width="{W}" height="{H}" fill="none" stroke="{LINE}" stroke-width="1.2"/></g>')
out.append('</svg>')
open("assets/components/layers-exploded.svg", "w").write("\n".join(out) + "\n")
print("layers-exploded.svg", width, height)

