"""svgkit — tiny design-system layer used by build_assets.py.

Design system: "Schematic".
Every section of the profile is drawn as a sheet from an engineering
drawing set: hairline rules, labelled ports, a title block. One violet to
cyan gradient is reserved for signal paths; amber marks status only.
"""
from __future__ import annotations
from xml.sax.saxutils import escape

# ── tokens ──────────────────────────────────────────────────────────────
INK0, INK1, INK2 = "#0A0D14", "#0F131D", "#151A27"
LINE, LINE2 = "#222A3C", "#323C55"
HI, MID, LO = "#EEF1F8", "#A4ADC3", "#7A85A0"
VIO, CYA, AMB = "#8B80FF", "#2DD4F0", "#F5B544"

SANS = ("Inter,'SF Pro Text','Segoe UI',system-ui,-apple-system,"
        "'Helvetica Neue',Arial,sans-serif")
MONO = ("ui-monospace,'SF Mono','JetBrains Mono','Cascadia Code',Menlo,"
        "Consolas,'DejaVu Sans Mono',monospace")

REV = "2026.10"

# ── text measurement (Arial-class metrics + safety margin) ──────────────
try:
    from PIL import ImageFont
    _F = {}
    def _font(bold, mono, size):
        key = (bold, mono, size)
        if key not in _F:
            p = ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf" if mono else
                 "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf"
                 % ("Bold" if bold else "Regular"))
            _F[key] = ImageFont.truetype(p, size * 4)
        return _F[key]
    def tw(s, size, weight=400, mono=False):
        f = _font(weight >= 600, mono, size)
        w = f.getlength(s) / 4
        return w * (0.93 if mono else 1.06)       # DejaVu Mono is wide; sans margin
except Exception:                                  # pragma: no cover
    def tw(s, size, weight=400, mono=False):
        return len(s) * size * (0.56 if mono else 0.55)


class Svg:
    def __init__(self, w, h, title, desc):
        self.w, self.h = w, h
        self.title, self.desc = title, desc
        self.defs, self.body = [], []

    # primitives ----------------------------------------------------------
    def add(self, s): self.body.append(s)

    def rect(self, x, y, w, h, fill="none", stroke=None, rx=0, sw=1, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st} {extra}/>')

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1, dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d} {extra}/>')

    def circle(self, x, y, r, fill="none", stroke=None, sw=1, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{st} {extra}/>')

    def path(self, d, fill="none", stroke=None, sw=1, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
        self.add(f'<path d="{d}" fill="{fill}"{st} {extra}/>')

    def text(self, x, y, s, size=14, weight=400, fill=MID, mono=False,
             anchor="start", ls=None, extra=""):
        cls = "mono" if mono else "sans"
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        l = f' letter-spacing="{ls}"' if ls is not None else ""
        self.add(f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" '
                 f'font-weight="{weight}" fill="{fill}"{a}{l} {extra}>{escape(s)}</text>')

    # compound ------------------------------------------------------------
    def arrow(self, x1, y, x2, color=LINE2, sw=1.25):
        """Horizontal signal line with arrowhead."""
        self.line(x1, y, x2 - 6, y, color, sw)
        self.path(f"M{x2-7} {y-4}L{x2} {y}L{x2-7} {y+4}", stroke=color, sw=sw)

    def tag(self, x, y, label, tone="core", mono=False, size=12.5, h=26):
        """Outlined taxonomy tag. core = bright, sup = muted. Returns width."""
        pad = 11
        w = round(tw(label, size, 500, mono) + pad * 2)
        if tone == "core":
            stroke, fill, tc = LINE2, INK2, HI
        elif tone == "sup":
            stroke, fill, tc = LINE, "none", MID
        elif tone == "vio":
            stroke, fill, tc = "#4A4390", "#14132B", "#C9C4FF"
        elif tone == "cya":
            stroke, fill, tc = "#17697A", "#0B1E26", "#9BEAFA"
        else:
            stroke, fill, tc = "#7A5A1E", "#201A0C", "#FBD38A"
        self.rect(x + .5, y + .5, w - 1, h - 1, fill, stroke, rx=5)
        self.text(x + w / 2, y + h / 2 + size * .35, label, size, 500, tc,
                  mono=mono, anchor="middle")
        return w

    def tag_row(self, x, y, labels, tone="core", gap=8, maxw=None, **kw):
        """Lay tags out left to right, wrapping at maxw. Returns bottom y."""
        cx, cy = x, y
        h = kw.get("h", 26)
        for lab in labels:
            w = round(tw(lab, kw.get("size", 12.5), 500, kw.get("mono", False)) + 22)
            if maxw and cx + w > x + maxw:
                cx, cy = x, cy + h + gap
            self.tag(cx, cy, lab, tone, **kw)
            cx += w + gap
        return cy + h

    def frame(self, section, no, total, headline, sub):
        """Standard sheet chrome: border, crop marks, heading, title block."""
        w, h = self.w, self.h
        self.rect(.5, .5, w - 1, h - 1, INK0, LINE, rx=16)
        for (cx, cy, sx, sy) in ((22, 22, 1, 1), (w - 22, 22, -1, 1),
                                 (22, h - 22, 1, -1), (w - 22, h - 22, -1, -1)):
            self.path(f"M{cx} {cy+sy*9}V{cy}H{cx+sx*9}", stroke=LINE2, sw=1)
        self.text(56, 92, headline, 36, 700, HI, ls=-1)
        self.text(56, 124, sub, 16, 400, MID)
        # title block
        bw = [196, 120, 104]
        bx = w - 56 - sum(bw)
        by = h - 62
        self.rect(bx + .5, by + .5, sum(bw) - 1, 28 - 1, "none", LINE2, rx=4)
        x = bx
        for i, (cw, t) in enumerate(zip(bw, [f"anish seth / {section}",
                                             f"sheet {no:02d} of {total:02d}",
                                             f"rev {REV}"])):
            if i: self.line(x, by + 1, x, by + 27, LINE2)
            self.text(x + cw / 2, by + 18, t, 10.5, 400, LO, mono=True, anchor="middle")
            x += cw

    # output ----------------------------------------------------------------
    def render(self):
        style = (f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO};}}"
                 "@media (prefers-reduced-motion:reduce){.pulse{display:none}}")
        defs = "".join(self.defs)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="t d">\n'
                f'<title id="t">{escape(self.title)}</title>\n<desc id="d">{escape(self.desc)}</desc>\n'
                f'<defs><style>{style}</style>'
                f'<linearGradient id="sig" x1="0" y1="0" x2="1" y2="0">'
                f'<stop offset="0" stop-color="{VIO}"/><stop offset="1" stop-color="{CYA}"/></linearGradient>'
                f'{defs}</defs>\n' + "\n".join(self.body) + "\n</svg>\n")
