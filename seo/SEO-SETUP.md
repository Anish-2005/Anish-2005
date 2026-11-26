# SEO setup — Anish Seth

## 1. Drop-in (this repo)
- Replace `README.md` with the provided one. All SVGs, workflows, layout untouched.
- Commit message: `docs: SEO — descriptive alt text, crawlable links, profile summary`

## 2. GitHub settings (5 min, biggest on-page win)
- Name: `Anish Seth`
- Bio: `Anish Seth · AI/ML engineer & full-stack dev, Kolkata. LLM agents, GraphRAG, document AI. SIH 2024/25 finalist. CSBS '27 · anishseth.xyz`
- Website: `https://www.anishseth.xyz`
- Pin: Report-Forge, GraphRAG Knowledge Engine, AI Scam Detection Agent, VanMitra, AgriLink, NEXORA
- Each pinned repo: description starts with keywords, 6–10 topics, homepage URL, 1280×640 social preview, README H1 = `Name — keyword description`

## 3. Fix inconsistencies (hurts entity matching)
- LinkedIn: sidebar/SVG use `in/anishseth`; old README used `in/anish-seth-202200290`. Keep ONE.
- Instagram: `_anish.seth_` (sidebar) vs `anish_seth.ai` (SVG). Keep ONE.
- `assets/header.svg` hardcodes followers 23 / stars 30; GitHub shows 25 / 13. Update or remove.

## 4. Website (`website/head-snippet.html`)
- Title/meta/OG + Person JSON-LD with `sameAs` to GitHub, LinkedIn, X, Instagram.
- `rel="me"` back to GitHub; add sitemap.xml, robots.txt, submit in Google Search Console + Bing Webmaster.
- 301 non-www ↔ www. One H1: `Anish Seth`. Projects page linking every repo.

## 5. Backlinks (what actually moves "anish seth")
Link GitHub + site from LinkedIn (Contact info + Featured), X bio, Instagram bio, resume, Devpost / SIH / Hack4Bengal pages, college/club pages. Use the exact name "Anish Seth" as anchor text. Publish 2–3 posts (LinkedIn/Dev.to/Hashnode) per project, linking to repos.

## Reality check
"Anish Seth" is a common name with established namesakes; no edit can guarantee #1–2. Realistic target: top results for "Anish Seth AI engineer", "Anish Seth Kolkata", "Anish Seth GitHub" within weeks; plain "Anish Seth" depends on backlinks and time.
