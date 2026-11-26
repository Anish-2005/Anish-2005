#!/usr/bin/env python3
"""Generate every profile SVG in ./assets from one design system.

    python scripts/build_assets.py                 # defaults for live metrics
    PROFILE_VIEWS=3,714 FOLLOWERS=23 STAR_COUNT=30 python scripts/build_assets.py
"""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import *

OUT = Path(__file__).resolve().parent.parent / "assets"
TOTAL = 8


# ═════════════════════════════ header ═══════════════════════════════════
def header():
    views = os.environ.get("PROFILE_VIEWS") or "3,714"
    followers = os.environ.get("FOLLOWERS") or "23"
    stars = os.environ.get("STAR_COUNT") or "30"
    s = Svg(1200, 590, "Anish Seth, AI systems engineering",
            "Header: name, role, system spec, system path from data to product, live GitHub metrics.")
    s.defs.append(f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">'
                  f'<path d="M32 0H0V32" fill="none" stroke="#141A28" stroke-width="1"/></pattern>')
    s.rect(.5, .5, 1199, 589, INK0, LINE, rx=16)
    s.rect(1, 1, 1198, 588, "url(#grid)", rx=15)
    for (cx, cy, sx, sy) in ((22, 22, 1, 1), (1178, 22, -1, 1), (22, 568, 1, -1), (1178, 568, -1, -1)):
        s.path(f"M{cx} {cy+sy*9}V{cy}H{cx+sx*9}", stroke=LINE2)

    # status
    s.circle(60, 62, 4, CYA)
    s.circle(60, 62, 8, "none", CYA, 1, 'opacity=".35"')
    s.text(78, 66, "Open to connect", 12.5, 500, MID, mono=True)

    # identity
    s.text(52, 172, "Anish Seth", 94, 700, HI, ls=-3.5)
    s.text(56, 224, "Engineering intelligent systems.", 28, 500, HI, ls=-.4)
    s.text(56, 258, "AI/ML engineering intern building agentic, retrieval and", 16.5, 400, MID)
    s.text(56, 282, "document-intelligence systems on a full-stack foundation.", 16.5, 400, MID)

    # system spec panel
    px, py, pw, ph = 716, 48, 428, 238
    s.rect(px + .5, py + .5, pw - 1, ph - 1, INK1, LINE2, rx=10)
    s.text(px + 24, py + 32, "system spec", 11.5, 500, LO, mono=True)
    rows = [("role", "AI/ML engineering intern"),
            ("focus", "Agentic, RAG, document AI"),
            ("measured by", "Benchmarks, quality, latency"),
            ("foundation", "Full-stack, APIs, cloud")]
    for i, (k, v) in enumerate(rows):
        y = py + 46 + i * 46
        s.line(px + 24, y, px + pw - 24, y, LINE)
        s.text(px + 24, y + 29, k, 12, 400, LO, mono=True)
        s.text(px + 144, y + 29, v, 14.5, 500, HI)

    # system path
    s.text(56, 340, "system path", 11.5, 500, LO, mono=True)
    nodes = [("Data", "SQL, vector search"), ("Retrieval", "RAG, GraphRAG"),
             ("Orchestration", "Agents, LangChain"), ("API", "FastAPI, Node.js"),
             ("Product", "React, Next.js")]
    nw, nh, ny = 176, 62, 358
    gap = (1088 - 5 * nw) / 4
    cy = ny + nh / 2
    xs = [56 + i * (nw + gap) for i in range(5)]
    # signal line under everything
    s.line(xs[0] + nw, cy, xs[-1], cy, LINE2, 1.25)
    for i in range(4):
        x2 = xs[i + 1]
        s.path(f"M{x2-8} {cy-4.5}L{x2-1} {cy}L{x2-8} {cy+4.5}", stroke=LINE2, sw=1.25)
    # traveling signal (one orchestrated moment)
    pth = f"M{xs[0]} {cy}H{xs[-1]+nw}"
    s.add(f'<g class="pulse"><circle r="4" fill="{CYA}"><animateMotion dur="7s" repeatCount="indefinite" '
          f'path="{pth}" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/>'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.92;1" dur="7s" repeatCount="indefinite"/></circle></g>')

    for i, (lab, sub) in enumerate(nodes):
        x = xs[i]
        last = i == 4
        s.rect(x + .5, ny + .5, nw - 1, nh - 1, INK1, (CYA if last else LINE2), rx=8)
        s.text(x + 18, ny + 28, lab, 17, 650, HI, ls=-.2)
        s.text(x + 18, ny + 48, sub, 11.5, 400, LO, mono=True)
        s.circle(x, cy, 3.5, INK0, LINE2, 1.25)
        s.circle(x + nw, cy, 3.5, INK0, LINE2, 1.25)
    # metrics
    my = 466
    s.line(56, my, 1144, my, LINE2)
    cw = 1088 / 3
    for i, (lab, val) in enumerate([("profile views", views), ("followers", followers),
                                    ("repository stars", stars)]):
        x = 56 + i * cw
        if i: s.line(x, my + 20, x, my + 96, LINE)
        x0 = x + (24 if i else 0)
        s.text(x0, my + 40, lab, 12, 400, LO, mono=True)
        s.text(x0, my + 86, val, 40, 700, HI, ls=-1.2)
        s.rect(x0, my + 100, 28, 2, VIO if i != 1 else CYA)
    s.line(56, my + 124, 1144, my + 124, LINE)
    return s


# ═════════════════════════════ 01 about ═════════════════════════════════
def about():
    s = Svg(1200, 520, "About Anish Seth",
            "Profile summary: AI systems beyond the prototype, current role, scope and current build areas.")
    s.frame("about", 1, TOTAL, "AI systems that move beyond the prototype.",
            "LLMs, agentic systems, retrieval, document intelligence and backend engineering.")
    # left: narrative + role
    for i, ln in enumerate(["Turning research ideas into systems that can be",
                            "evaluated, deployed and used. I think past the model:",
                            "data and retrieval, orchestration, APIs, infrastructure",
                            "and the product people touch."]):
        s.text(56, 184 + i * 27, ln, 17, 400, MID)
    s.line(56, 316, 568, 316, LINE)
    s.text(56, 346, "current role", 11.5, 500, LO, mono=True)
    s.text(56, 380, "AI/ML Engineering Intern", 22, 650, HI, ls=-.4)
    s.text(56, 406, "Agentic research and report-generation systems, plus", 14.5, 400, MID)
    s.text(56, 428, "document-intelligence and LLM evaluation workflows.", 14.5, 400, MID)
    # vertical divider
    s.line(620, 152, 620, 428, LINE)
    # right: scope table
    X = 668
    s.text(X, 170, "scope", 11.5, 500, LO, mono=True)
    scope = [("AI", "LLM applications, agentic AI, RAG"),
             ("Engineering", "Systems, cloud, data"),
             ("Machine learning", "NLP, vision, evaluation")]
    for i, (k, v) in enumerate(scope):
        y = 184 + i * 50
        s.line(X, y, 1144, y, LINE)
        s.text(X, y + 31, k, 17, 650, HI, ls=-.2)
        s.text(X + 200, y + 31, v, 14.5, 400, MID)
    s.line(X, 334, 1144, 334, LINE)
    s.text(X, 366, "currently building", 11.5, 500, LO, mono=True)
    items = ["Agentic systems", "RAG and GraphRAG", "Document intelligence", "LLM evaluation"]
    for i, it in enumerate(items):
        cx = X + (i % 2) * 240
        cy = 392 + (i // 2) * 30
        s.rect(cx, cy - 8, 8, 8, "none", CYA if i % 2 else VIO, rx=2, sw=1.5)
        s.text(cx + 20, cy, it, 15, 500, HI)
    return s


# ═════════════════════════════ 02 experience ════════════════════════════
def experience():
    s = Svg(1200, 640, "Experience", "Experience: AI/ML engineering and a full-stack engineering foundation.")
    s.frame("experience", 2, TOTAL, "Building systems from intelligence to production.",
            "AI engineering layered on a full-stack engineering foundation.")
    # rail
    s.line(70, 196, 70, 408, LINE2, 1.5)
    s.rect(69, 196, 2, 212, "url(#sig)")
    # entry 1
    s.circle(70, 196, 9, INK0, CYA, 2); s.circle(70, 196, 3.5, CYA)
    s.text(110, 204, "AI/ML Engineering", 25, 700, HI, ls=-.6)
    s.tag(110, 220, "Current", "amber", mono=True, size=11.5, h=24)
    s.text(110, 272, "Production-oriented AI systems,", 14.5, 400, MID)
    s.text(110, 294, "agentic workflows and LLM engineering.", 14.5, 400, MID)
    cols = [("Agentic AI", ["Plan, retrieve, reason", "Synthesize, execute"]),
            ("Document AI", ["OCR, layout parsing", "Vision extraction"]),
            ("LLM systems", ["Orchestration, RAG", "Multi-step agents"]),
            ("Evaluation", ["Benchmarking", "Quality and latency"])]
    X0, CW = 470, 169
    s.line(X0, 168, 1144, 168, LINE2)
    for i, (h, ls) in enumerate(cols):
        x = X0 + i * CW
        if i: s.line(x, 180, x, 300, LINE)
        x0 = x + (18 if i else 0)
        s.text(x0, 202, h, 16, 650, HI, ls=-.2)
        for j, l in enumerate(ls):
            s.text(x0, 232 + j * 22, l, 13.5, 400, MID)
    s.line(X0, 316, 1144, 316, LINE)
    # entry 2
    s.circle(70, 408, 9, INK0, VIO, 2); s.circle(70, 408, 3.5, VIO)
    s.text(110, 416, "Full-stack engineering", 25, 700, HI, ls=-.6)
    s.text(110, 446, "Independent projects and client work.", 14.5, 400, MID)
    chain = ["Frontend", "Backend", "Database", "Cloud", "Integration", "Production"]
    cw_, gap = 92, 24.4
    s.line(X0, 384, 1144, 384, LINE2)
    s.text(X0, 408, "delivery path", 11.5, 500, LO, mono=True)
    for i, c in enumerate(chain):
        x = X0 + i * (cw_ + gap)
        last = i == len(chain) - 1
        s.rect(x + .5, 422.5, cw_ - 1, 33, INK1, CYA if last else LINE2, rx=6)
        s.text(x + cw_ / 2, 443, c, 13, 600, HI, anchor="middle")
        if not last: s.arrow(x + cw_ + 3, 439, x + cw_ + gap - 3)
    s.text(X0, 496, "foundation", 11.5, 500, LO, mono=True)
    s.text(X0, 520, "Full-stack systems, APIs, databases,", 14.5, 400, MID)
    s.text(X0, 542, "cloud infrastructure", 14.5, 400, MID)
    s.text(X0 + 340, 496, "domain experience", 11.5, 500, LO, mono=True)
    s.text(X0 + 340, 520, "Legal-tech, health-tech, agri-tech,", 14.5, 400, MID)
    s.text(X0 + 340, 542, "environmental systems", 14.5, 400, MID)
    return s


# ═════════════════════════════ 03 focus ═════════════════════════════════
def _glyph(s, kind, x, y, col):
    k = dict(stroke=col, sw=1.6)
    if kind == "agent":
        s.circle(x + 20, y + 20, 7, "none", col, 1.6)
        for (dx, dy) in ((20, 2), (3, 34), (37, 34)):
            s.line(x + 20, y + 20, x + dx, y + dy, LINE2)
            s.circle(x + dx, y + dy, 3.5, INK0, col, 1.6)
    elif kind == "graph":
        pts = [(6, 10), (32, 6), (14, 32), (36, 30)]
        for a, b in ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)):
            s.line(x + pts[a][0], y + pts[a][1], x + pts[b][0], y + pts[b][1], LINE2)
        for (dx, dy) in pts: s.circle(x + dx, y + dy, 4, INK0, col, 1.6)
    elif kind == "doc":
        s.path(f"M{x+8} {y+2}H{x+26}L{x+34} {y+10}V{y+38}H{x+8}Z", **k)
        s.path(f"M{x+26} {y+2}V{y+10}H{x+34}", **k)
        for i in range(3): s.line(x + 14, y + 20 + i * 6, x + 28, y + 20 + i * 6, LINE2, 1.6)
    else:
        for i, hh in enumerate((12, 22, 32)):
            s.rect(x + 6 + i * 11, y + 38 - hh, 7, hh, "none", col, rx=1.5, sw=1.6)
        s.line(x + 2, y + 39, x + 38, y + 39, LINE2)


def focus():
    s = Svg(1200, 600, "Current focus", "Four focus areas and the engineering loop from prototype to monitored system.")
    s.frame("focus", 3, TOTAL, "What I'm building toward.",
            "Exploring the systems layer where intelligence becomes reliable software.")
    items = [("agent", "Agentic AI", ["Autonomous workflows,", "orchestration and tool use."], VIO),
             ("graph", "Retrieval", ["RAG, GraphRAG and", "knowledge systems."], CYA),
             ("doc", "Document AI", ["OCR, vision and", "intelligent extraction."], VIO),
             ("bars", "Evaluation", ["Benchmarking, reliability", "and AI quality."], CYA)]
    s.line(56, 160, 1144, 160, LINE2)
    for i, (g, t, d, c) in enumerate(items):
        x = 56 + i * 272
        if i: s.line(x, 176, x, 330, LINE)
        x0 = x + (26 if i else 0)
        _glyph(s, g, x0, 184, c)
        s.text(x0, 262, t, 21, 700, HI, ls=-.5)
        s.text(x0, 290, d[0], 14, 400, MID); s.text(x0, 310, d[1], 14, 400, MID)
    s.line(56, 336, 1144, 336, LINE)
    s.text(56, 380, "engineering loop", 11.5, 500, LO, mono=True)
    s.text(56, 408, "From prototype to dependable system", 19, 650, HI, ls=-.3)
    stages = ["Prototype", "Evaluate", "Harden", "Deploy", "Monitor"]
    x1, x2, y = 120, 1080, 460
    s.line(x1, y, x2, y, LINE2, 1.5)
    s.rect(x1, y - 1, x2 - x1, 2, "url(#sig)")
    for i, st in enumerate(stages):
        x = x1 + i * (x2 - x1) / 4
        s.circle(x, y, 8, INK0, VIO if i < 2 else CYA, 2)
        s.text(x, y - 22, st, 14.5, 600, HI, anchor="middle")
    # feedback path
    s.path(f"M{x2} {y+12}C{x2} {y+58} {x1} {y+58} {x1} {y+14}", stroke=LINE2, sw=1.25, extra='stroke-dasharray="4 5"')
    s.path(f"M{x1-4.5} {y+21}L{x1} {y+13}L{x1+4.5} {y+21}", stroke=LINE2, sw=1.25)
    s.text(600, y + 64, "feedback into the next iteration", 11.5, 400, LO, mono=True, anchor="middle")
    return s


# ═════════════════════════════ 04 ai engineering ════════════════════════
def ai_engineering():
    s = Svg(1200, 640, "AI engineering capability map",
            "AI engineering as three layers: applied AI, LLM and agentic systems, infrastructure and tooling.")
    s.frame("ai engineering", 4, TOTAL, "Intelligence, engineered into systems.",
            "The AI layer across models, retrieval, applications, infrastructure and evaluation.")
    layers = [
        ("L3", "Applied AI", "Turning models into useful intelligence for real workflows.",
         ["Document intelligence", "OCR", "Computer vision", "Evaluation", "Benchmarking", "AI automation"], "cya"),
        ("L2", "LLM and agentic systems", "Building multi-step systems around modern language models.",
         ["Agentic pipelines", "RAG", "GraphRAG", "Orchestration", "Prompt engineering", "Multi-step agents"], "vio"),
        ("L1", "Infrastructure and tooling", "The layer that makes AI systems searchable, measurable and deployable.",
         ["Vector search", "Embeddings", "LangChain", "Model evaluation", "Cloud inference", "API design"], "core"),
    ]
    y = 156
    for i, (lid, name, desc, tags, tone) in enumerate(layers):
        s.line(56, y, 1144, y, LINE2)
        s.text(56, y + 34, lid, 12, 500, LO, mono=True)
        s.text(96, y + 36, name, 20, 700, HI, ls=-.4)
        # wrap desc
        words, lines, cur = desc.split(), [], ""
        for w_ in words:
            if tw(cur + " " + w_, 13.5) > 270 and cur: lines.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
        lines.append(cur)
        for j, l in enumerate(lines): s.text(96, y + 62 + j * 20, l, 13.5, 400, MID)
        s.tag_row(430, y + 26, tags, tone, maxw=714, gap=8, h=30, size=13.5)
        y += 112
    s.line(56, y, 1144, y, LINE2)
    s.text(56, y + 40, "currently exploring", 11.5, 500, LO, mono=True)
    for i, t in enumerate(["Multi-agent orchestration", "Small-model fine-tuning", "Structured evaluation harnesses"]):
        x = 296 + i * 280
        s.circle(x, y + 36, 4, CYA)
        s.text(x + 14, y + 41, t, 14.5, 500, HI)
    return s


# ═════════════════════════════ 05 tech stack ════════════════════════════
STACK = [
    ("L7", "Frontend and product", "Interfaces and product layers for AI-powered applications.",
     ["React", "Next.js", "Tailwind CSS", "Figma"], ["TypeScript", "JavaScript", "HTML/CSS"], "core"),
    ("L6", "AI and LLM engineering", "Models, frameworks and patterns used to build applied intelligence.",
     ["Python", "OpenAI", "Gemini", "Claude", "LangChain", "PyTorch", "Scikit-learn", "RAG", "GraphRAG", "Agentic AI"],
     ["NLP", "OCR", "Prompt engineering", "LLM evaluation"], "vio"),
    ("L5", "Programming and backend", "Languages, frameworks and APIs powering production systems.",
     ["Java", "Python", "C++", "C#", "JavaScript / TS"], ["Node.js", "Express", "FastAPI", "Django"], "core"),
    ("L4", "Databases and data", "Persistence, retrieval and data systems.",
     ["PostgreSQL", "MongoDB", "Firebase", "Supabase", "Firestore", "Vector search"], [], "core"),
    ("L3", "Cloud and infrastructure", "Deployment, runtime and infrastructure layers.",
     ["AWS", "Google Cloud", "Cloud Run", "Docker", "Vercel"], ["Cloud architecture"], "core"),
    ("L2", "Developer and automation", "Tooling, workflows and engineering productivity.",
     ["Git", "GitHub", "VS Code", "Postman", "Linux", "n8n", "Zapier"], [], "core"),
    ("L1", "Engineering fundamentals", "Theory every layer depends on.",
     ["DSA", "OOP", "DBMS", "Operating systems", "Computer networks", "Software engineering", "System design"], [], "core"),
]


def _stack(h):
    s = Svg(1200, h, "Technology stack", "Seven-layer technology stack from engineering fundamentals up to frontend and product.")
    s.frame("tech stack", 5, TOTAL, "Tools for building intelligent systems.",
            "A seven-layer stack, from fundamentals up to the interface.")
    y = 156
    for lid, name, desc, core, sup, tone in STACK:
        s.line(56, y, 1144, y, LINE2)
        s.text(56, y + 36, lid, 12, 500, LO, mono=True)
        s.text(96, y + 38, name, 18, 700, HI, ls=-.3)
        words, lines, cur = desc.split(), [], ""
        for w_ in words:
            if tw(cur + " " + w_, 13) > 250 and cur: lines.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
        lines.append(cur)
        for j, l in enumerate(lines): s.text(96, y + 62 + j * 19, l, 13, 400, MID)
        b = s.tag_row(380, y + 22, core, tone, maxw=764, gap=8, h=28, size=13)
        if sup:
            b = s.tag_row(380, b + 8, sup, "sup", maxw=764, gap=8, h=28, size=13)
        y = max(b + 26, y + 62 + (len(lines) - 1) * 19 + 34)
    s.line(56, y, 1144, y, LINE2)
    return s, y


def tech_stack():
    _, y = _stack(2000)
    s, _ = _stack(y + 110)
    return s


# ═════════════════════════════ 06 projects ══════════════════════════════
def _pipeline(s, x, y, steps, col):
    cx = x
    for i, st in enumerate(steps):
        w = round(tw(st, 12.5, 600) + 22)
        s.rect(cx + .5, y + .5, w - 1, 27, INK2, LINE2, rx=5)
        s.text(cx + w / 2, y + 19, st, 12.5, 600, HI, anchor="middle")
        cx += w
        if i < len(steps) - 1:
            s.arrow(cx + 4, y + 14, cx + 26, col); cx += 30


def projects():
    s = Svg(1200, 970, "Featured projects", "Two flagship AI systems and five further projects across AI/ML and systems engineering.")
    s.frame("projects", 6, TOTAL, "Systems I've built.",
            "AI systems, engineering projects and production-oriented experiments.")
    s.text(56, 166, "ai and ml: flagship", 11.5, 500, LO, mono=True)
    feat = [("Report-Forge", "Agentic research and automated report generation.",
             ["Plans research tasks, retrieves sources and", "synthesizes structured reports autonomously."],
             ["Plan", "Retrieve", "Reason", "Synthesize"], VIO),
            ("GraphRAG Knowledge Engine", "Graph-based retrieval for grounded LLM reasoning.",
             ["Connects entities and relationships in a", "knowledge graph instead of flat retrieval."],
             ["Knowledge graph", "Retrieval", "Grounded reasoning"], CYA)]
    for i, (t, d1, d2, steps, col) in enumerate(feat):
        x, y, w, h = 56 + i * 558, 182, 530, 232
        s.rect(x + .5, y + .5, w - 1, h - 1, INK1, LINE, rx=10)
        s.rect(x, y + 10, 3, 56, col)
        s.text(x + 28, y + 50, t, 24, 700, HI, ls=-.6)
        s.text(x + 28, y + 80, d1, 15, 500, HI)
        s.text(x + 28, y + 106, d2[0], 13.5, 400, MID); s.text(x + 28, y + 126, d2[1], 13.5, 400, MID)
        s.line(x + 28, y + 150, x + w - 28, y + 150, LINE)
        s.text(x + 28, y + 174, "pipeline", 11.5, 500, LO, mono=True)
        _pipeline(s, x + 28, y + 186, steps, col)
    ledger = [("ai and ml: also built", [
        ("AI Scam Detection Agent", "LLM-driven fraud detection for text and transaction signals.", ["OpenAI", "Python"]),
        ("Vanmitra", "AI-powered environmental monitoring using sensor and imagery data.", ["Computer vision", "PyTorch"]),
        ("AgriLink", "AI and sustainability platform for data-driven agricultural insight.", ["scikit-learn", "Node.js"])]),
        ("systems engineering", [
        ("NEXORA", "Real-time collaboration with live editing and multi-user presence.", ["React", "Node.js", "MongoDB"]),
        ("MiniGit", "Git built from scratch in Java: objects, commits, branching, diffing.", ["Java", "Systems design"])])]
    y = 452
    for label, rows in ledger:
        s.text(56, y, label, 11.5, 500, LO, mono=True)
        y += 14
        for (n, d, tg) in rows:
            s.line(56, y, 1144, y, LINE)
            s.text(56, y + 38, n, 18, 700, HI, ls=-.3)
            s.text(346, y + 38, d, 14, 400, MID)
            s.tag_row(930, y + 20, tg, "sup", gap=6, h=26, size=12)
            y += 62
        s.line(56, y, 1144, y, LINE)
        y += 34
    s.text(56, y + 6, "More projects and live demos at anishseth.xyz", 13, 400, LO, mono=True)
    return s


# ═════════════════════════════ 07 achievements ══════════════════════════
def _tile(s, x, y, label, col):
    s.rect(x + .5, y + .5, 43, 43, INK2, LINE2, rx=9)
    s.text(x + 22, y + 28, label, 14 if len(label) < 3 else 12, 700, col, anchor="middle")


def achievements():
    s = Svg(1200, 690, "Achievements and certifications",
            "Hackathon finalist placings, community leadership roles and technical certifications.")
    s.frame("achievements", 7, TOTAL, "Recognition earned along the way.",
            "Hackathons, community leadership and technical certifications.")
    s.text(56, 166, "hackathons", 11.5, 500, LO, mono=True)
    for i, (yr, n) in enumerate([("2024", "Smart India Hackathon"), ("2025", "Smart India Hackathon"), ("2025", "Hack4Bengal")]):
        x, y, w, h = 56 + i * 372, 182, 344, 112
        s.rect(x + .5, y + .5, w - 1, h - 1, INK1, LINE, rx=10)
        s.rect(x + 20, y, w - 40, 2, AMB)
        s.text(x + 24, y + 38, yr, 13, 500, AMB, mono=True)
        s.text(x + 24, y + 66, n, 21, 700, HI, ls=-.4)
        s.tag(x + 24, y + 78, "Finalist", "amber", size=12, h=24)
    s.text(56, 336, "leadership and community", 11.5, 500, LO, mono=True)
    for i, (g, r, d, c) in enumerate([("G", "Google Student Ambassador", "Developer community, tech outreach", CYA),
                                      ("C", "Campus Mantri", "Developer community, campus initiatives", VIO),
                                      ("O", "Outreach Head", "Educational society, outreach", CYA)]):
        x = 56 + i * 372
        s.line(x, 352, x + 344, 352, LINE2)
        _tile(s, x, 372, g, c)
        s.text(x + 60, 392, r, 17, 700, HI, ls=-.3)
        s.text(x + 60, 414, d, 13, 400, MID)
    s.text(56, 488, "certifications", 11.5, 500, LO, mono=True)
    for i, (g, r, d, c) in enumerate([("AI", "Google AI/ML", "Virtual internship, AICTE", VIO),
                                      ("AWS", "AWS Academy", "Cloud Architecting", AMB),
                                      ("OCI", "Oracle Cloud Infrastructure", "AI Foundations Associate", "#FF8A7A")]):
        x = 56 + i * 372
        s.line(x, 504, x + 344, 504, LINE2)
        _tile(s, x, 524, g, c)
        s.text(x + 60, 544, r, 17, 700, HI, ls=-.3)
        s.text(x + 60, 566, d, 13, 400, MID)
    return s


# ═════════════════════════════ 08 connect ═══════════════════════════════
def connect():
    s = Svg(1200, 390, "Connect with Anish Seth", "Contact channels: portfolio, LinkedIn, email, X and Instagram.")
    s.frame("connect", 8, TOTAL, "Let's build something intelligent.",
            "AI systems, LLM applications, engineering and products.")
    chans = [("Portfolio", "anishseth.xyz", "globe"), ("LinkedIn", "in/anish-seth-202200290", "in"),
             ("Email", "anishseth0510@gmail.com", "mail"), ("X", "@AnishSeth170734", "x"),
             ("Instagram", "@anish_seth.ai", "ig")]
    for i, (n, v, ic) in enumerate(chans):
        x = 56 + i * 220
        s.line(x, 164, x + 208, 164, LINE2)
        ix, iy = x, 184
        if ic == "globe":
            s.circle(ix + 12, iy + 12, 11, "none", CYA, 1.5); s.path(f"M{ix+12} {iy+1}C{ix+4} {iy+8} {ix+4} {iy+16} {ix+12} {iy+23}C{ix+20} {iy+16} {ix+20} {iy+8} {ix+12} {iy+1}", stroke=CYA, sw=1.5); s.line(ix + 1, iy + 12, ix + 23, iy + 12, CYA, 1.5)
        elif ic == "in":
            s.text(ix + 12, iy + 20, "in", 20, 800, CYA, anchor="middle")
        elif ic == "mail":
            s.rect(ix + 1, iy + 4, 22, 16, "none", VIO, rx=3, sw=1.5); s.path(f"M{ix+2} {iy+6}L{ix+12} {iy+14}L{ix+22} {iy+6}", stroke=VIO, sw=1.5)
        elif ic == "x":
            s.path(f"M{ix+3} {iy+3}L{ix+21} {iy+21}M{ix+21} {iy+3}L{ix+3} {iy+21}", stroke=HI, sw=2)
        else:
            s.rect(ix + 1, iy + 1, 22, 22, "none", VIO, rx=6, sw=1.5); s.circle(ix + 12, iy + 12, 5, "none", VIO, 1.5); s.circle(ix + 18, iy + 6, 1.3, VIO)
        s.text(x, 244, n, 17, 700, HI, ls=-.3)
        s.text(x, 266, v, 12, 400, MID, mono=True)
    s.text(56, 340, "Ship the model. Ship the system. Ship the product.", 21, 650, HI, ls=-.4)
    return s


SECTIONS = {
    "header": header,
    "about": about,
    "experience": experience,
    "focus": focus,
    "ai-engineering": ai_engineering,
    "tech-stack": tech_stack,
    "projects": projects,
    "achievements": achievements,
    "connect": connect,
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    OUT.mkdir(exist_ok=True)
    for name, fn in SECTIONS.items():
        if only and name not in only:
            continue
        (OUT / f"{name}.svg").write_text(fn().render(), encoding="utf-8")
        print("wrote", f"assets/{name}.svg")
