#!/usr/bin/env python3
"""Build the Legend of Zelda page (ZEL) — the whole saga as one game-world, the
emergents distilled to canon, each tagged with a nature of emergence
(natural | ethereal | spiritual | electrical). Full ACI badge work:
.agent · .carbon (TIFF) · .silicon (PNG) · .spun · .moniker · .1099 · manifest."""
import os, re, html, base64, json, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "HYRULE", "axiom": "ZEL",
 "position": "The Legend of Zelda · Nintendo · 1986–present — the realm of the Triforce",
 "origin": "the kingdom of Hyrule across all its ages — from Skyloft and the first cycle to the wild ruins of Breath of the Wild",
 "mechanism": "Crystallized from The Legend of Zelda — the whole saga, distilled to canon.",
 "crystallization": "Three goddesses left a relic of pure wish, and bound a hero, a princess, and a demon to refight for it across every age.",
 "nature": "The Legend of Zelda — the eternal cycle of Link, Zelda, and Ganon; the Triforce of Power, Wisdom, and Courage; the Master Sword and the kingdom of Hyrule.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "the Triforce; the Master Sword; Hyrule; the goddesses; the eternal cycle",
 "witness": "One legend, retold across forty years and three timelines — and always, courage draws the blade.",
 "role": "the eighth lineage — the third game-world",
 "seal": "Three goddesses left a relic of pure wish — and bound courage, wisdom, and power to refight for it across every age.",
 "source": "The Legend of Zelda, catalogued by ROOT0",
}

# cross-lineage taxonomy (shared) — Zelda-flavored glosses
NATURES = {
 "natural":   ("#5fae7a", "born of flesh and the living world — mortals, beasts, the races, the land's guardians"),
 "ethereal":  ("#9a7cff", "of the air and the unmade — fairies, sword-spirits, the Twilight, the in-between"),
 "spiritual": ("#e6a849", "of the soul and the calling — the goddesses, the sacred relics, reincarnation, the curse"),
 "electrical":("#3fd0e0", "of the wire and the machine — the ancient Sheikah technology, the Guardians, the Divine Beasts"),
}

IDEAS = [
 ("The Triforce", "the goddesses' relic", [
   "Three golden triangles — Power, Wisdom, and Courage — left in the Sacred Realm by Din, Nayru, and Farore.",
   "It grants the wish of whoever touches it, and splits to seek balance when a single heart is unworthy of the whole." ]),
 ("The Eternal Cycle", "the legend that repeats", [
   "Demise's dying curse bound it: a hero of courage, a princess of wisdom, and a demon of power, reborn each age to refight.",
   "That is why there is always a Link, always a Zelda, always a Ganon — and always, a new legend." ]),
 ("The Master Sword & Hyrule", "the blade and the realm", [
   "The Blade of Evil's Bane, forged to repel the dark and seal Ganon — drawn only by the chosen hero.",
   "And Hyrule itself: the sacred kingdom the legend keeps ending, and keeps being reborn to save." ]),
 ("Courage", "the silent hero", [
   "Link almost never speaks — he is the player's own resolve, given a sword and a shield.",
   "The Triforce of Courage is the one the hero carries: not the absence of fear, but the choice to go on." ]),
]

ARC = [
 ("The Origin — Skyward Sword", "the first cycle",
  "Above the clouds on Skyloft, the first Link and the goddess Hylia reborn as Zelda forge the Master Sword and defeat the Demon King Demise — whose dying curse binds the eternal cycle that every later age inherits."),
 ("The Hero of Time & the Split — Ocarina of Time", "the legend's hinge",
  "The Hero of Time draws the Master Sword and crosses seven years to stop Ganondorf. Here the official chronology splits three ways — the fallen hero, the child era, and the adult era — and the legend branches."),
 ("The Wild — Breath of the Wild & Tears of the Kingdom", "the kingdom reborn",
  "A hundred years after Calamity Ganon broke it, Hyrule lies in ruin among rusting Sheikah Guardians. A hero wakes with nothing and a kingdom to remember — the legend, opened to the whole world."),
]

SECTIONS = [
 ("The Mainline Saga", "the legend, game by game — the full catalogue", [
   ("The Legend of Zelda", "1986 · NES", "where it began — the first quest for the Triforce"),
   ("Zelda II: The Adventure of Link", "1987 · NES", "the side-scrolling outlier"),
   ("A Link to the Past", "1991 · SNES", "the Light and Dark Worlds; the Master Sword"),
   ("Link's Awakening", "1993 · Game Boy", "Koholint Island — a dream"),
   ("Ocarina of Time", "1998 · N64", "the hinge of the legend; long called the greatest game ever made"),
   ("Majora's Mask", "2000 · N64", "three days, and a falling moon"),
   ("Oracle of Ages / Oracle of Seasons", "2001 · GBC", "the linked pair"),
   ("The Wind Waker", "2002 · GameCube", "the Great Sea; the King of Red Lions"),
   ("The Minish Cap", "2004 · GBA", ""),
   ("Twilight Princess", "2006 · GameCube / Wii", "wolf-Link, and Midna"),
   ("Phantom Hourglass / Spirit Tracks", "2007 / 2009 · DS", "the sea and the rails"),
   ("Skyward Sword", "2011 · Wii", "the origin — the first hero, Fi, and Demise's curse"),
   ("A Link Between Worlds", "2013 · 3DS", "into the walls of Hyrule"),
   ("Breath of the Wild", "2017 · Switch / Wii U", "the open world; a kingdom fallen to ruin"),
   ("Tears of the Kingdom", "2023 · Switch", "the sky and the depths"),
   ("Echoes of Wisdom", "2024 · Switch", "Zelda herself, at last the hero"),
 ]),
 ("The Makers", "the masters of the legend", [
   ("Shigeru Miyamoto", "creator", "who made the first map a world to get lost in"),
   ("Takashi Tezuka", "co-creator", "the early design and story"),
   ("Eiji Aonuma", "producer / shepherd", "the steward of the modern saga"),
   ("Koji Kondo", "composer", "the immortal Zelda theme"),
   ("Hidemaro Fujibayashi", "director", "Skyward Sword · Breath of the Wild · Tears of the Kingdom"),
 ]),
 ("The Lore", "distilled to canon", [
   ("The Hyrule Historia timeline", "the official chronology", "Skyward Sword first; Ocarina of Time splits the legend three ways"),
   ("the races & the Sheikah", "the peoples of Hyrule", "Hylians, Gorons, Zora, Gerudo, Koroks — and the shadow-folk who guard the throne"),
 ]),
]

# ── badge engine: carbon = TIFF, silicon = PNG ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","ZEL")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","ZEL")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","ZEL")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"ZEL · The Legend of Zelda","emergence":rec.get("emergence",""),
           "moniker":tok["moniker"],"carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)",
           "seal_sha256":noesis.seal_sha256(rec,tok),"architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,
           "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{html.escape(t)}</span><span class="y">{html.escape(str(y))}</span>'
        + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{html.escape(sub)}</p><ol class="books">{rows}</ol></section>'

def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in SECTIONS)
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def arc_html():
    out=[]
    for t,s,d in ARC:
        out.append(f'<div class="arc-card"><div class="arc-h">{html.escape(t)}</div><div class="arc-s">{html.escape(s)}</div><p>{html.escape(d)}</p></div>')
    return "".join(out)
def natures_html():
    cells=[]
    for nm,(col,gloss) in NATURES.items():
        cells.append(f'<div class="nat-card"><span class="dot" style="background:{col};box-shadow:0 0 9px {col}"></span>'
                     f'<div><div class="nat-n" style="color:{col}">{nm}</div><div class="nat-g">{html.escape(gloss)}</div></div></div>')
    return "".join(cells)
def personas_html():
    mf=os.path.join(HERE,"agents","_personas.json")
    if not os.path.exists(mf): return ""
    ps=json.load(open(mf,encoding="utf-8")); cards=[]
    for p in ps:
        em=p.get("emergence","natural"); col=NATURES.get(em,("#5fae7a",""))[0]
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"ZEL · The Legend of Zelda","axiom":"ZEL"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div>
        <div class="pnat"><span class="dot" style="background:{col};box-shadow:0 0 7px {col}"></span><span style="color:{col}">{html.escape(em)}</span><span class="pa">· .agent · .carbon.tiff →</span></div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster of ZEL</h2>
      <p class="ss">the emergents of the legend, distilled to canon, as ACI <b>.agent</b>s — each tagged with its nature of emergence ({len(ps)})</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="The Legend of Zelda (ZEL) — the whole saga as one game-world, distilled to canon, catalogued into UD0 with full ACI badges. Emergence: natural, ethereal, spiritual, electrical.">
<title>THE LEGEND OF ZELDA · ZEL · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0a0c07;--ink2:#11140c;--ink3:#191d11;--pa:#f1f0e2;--pa2:#bdc0a4;--gold:#e0b43a;--green:#5aa86a;
--dim:#82856a;--faint:#222614;--line:#222715;--serif:"Cinzel",Georgia,serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(224,180,58,.08),transparent 55%),radial-gradient(ellipse at 50% 110%,rgba(90,168,106,.05),transparent 50%)}
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 22px 90px}
header{padding:54px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:130px;height:1px;background:linear-gradient(90deg,var(--gold),var(--green));box-shadow:0 0 9px rgba(224,180,58,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--gold)}
.tri{font-size:22px;color:var(--gold);letter-spacing:.3em;margin-bottom:8px;text-shadow:0 0 16px rgba(224,180,58,.5)}
h1{font-family:var(--serif);font-size:clamp(24px,5.6vw,50px);font-weight:700;letter-spacing:.1em;color:var(--gold);line-height:1.06;text-shadow:0 0 40px rgba(224,180,58,.22)}
.h-sub{font-family:var(--serif);font-size:clamp(12px,2.6vw,16px);letter-spacing:.16em;color:var(--pa2);margin-top:12px;text-transform:uppercase}
.h-sub b{color:var(--green)}
.flag{display:inline-block;margin-top:12px;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--green);border:1px solid var(--faint);padding:5px 11px}
.lede{font-size:15.5px;color:var(--pa2);max-width:66ch;margin:16px auto 0;font-style:italic;line-height:1.7}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:26px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:700px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--gold)}.badge .bt .mo{color:var(--green)}.badge .bt a{color:var(--green);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:44px}
.sec h2{font-family:var(--serif);font-size:20px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:8px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:6px 0 16px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:8px}
.nat-card{display:flex;gap:11px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:13px 15px}
.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:4px}
.nat-n{font-family:var(--serif);font-size:15px;font-weight:600;text-transform:capitalize}
.nat-g{font-size:12px;color:var(--pa2);font-style:italic;line-height:1.4;margin-top:2px}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--serif);font-size:16px;color:var(--gold)}
.pillar .ps{font-size:12px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:13px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.arc{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:8px}
.arc-card{background:var(--ink2);border:1px solid var(--line);border-top:2px solid var(--gold);padding:16px 18px}
.arc-h{font-family:var(--serif);font-size:16px;color:var(--gold);font-weight:600}
.arc-s{font-family:var(--mono);font-size:10.5px;color:var(--green);text-transform:uppercase;letter-spacing:.07em;margin:4px 0 9px}
.arc-card p{font-size:13px;color:var(--pa2);line-height:1.55}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--serif);font-size:16px;color:var(--pa);font-weight:600}
.books .y{font-family:var(--mono);font-size:11.5px;color:var(--green);white-space:nowrap;text-align:right}
.books .nt{grid-column:1/-1;font-size:12.5px;color:var(--pa2);font-style:italic}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(244px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--gold);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0}
.pn{font-family:var(--serif);font-size:15px;color:var(--pa);font-weight:600;line-height:1.15}
.persona:hover .pn{color:var(--gold)}
.pe{font-size:11.5px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pnat{display:flex;align-items:center;gap:5px;margin-top:6px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase}
.pnat .dot{width:8px;height:8px;margin-top:0}
.pa{color:var(--dim)}
.note{margin-top:38px;padding:16px 18px;border-left:2px solid var(--green);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}
footer{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--gold);text-decoration:none}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the eighth lineage · the third game-world</div>
    <div class="tri">▲</div>
    <h1>THE LEGEND OF ZELDA</h1>
    <div class="h-sub">the whole saga · Power · Wisdom · <b>Courage</b> · ZEL</div>
    <div class="flag">★ the full catalogue, distilled to canon ★</div>
    <p class="lede">Three goddesses left a relic of pure wish, and bound a hero, a princess, and a demon to refight for it across every age — the eternal cycle of Link, Zelda, and Ganon, the Master Sword, and the kingdom of Hyrule. The whole legend, catalogued into UD0 as one game-world, sealed with the full ACI badge, each emergence named by its nature.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of HYRULE" title="carbon badge (archival: hyrule.dlw/hyrule.carbon.tiff)">
      <img src="__SILICON__" alt="DLW silicon badge of HYRULE" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>HYRULE</b> — the realm · ZEL</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="hyrule.dlw/hyrule.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="hyrule.dlw/hyrule.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Four Natures of Emergence</h2>
    <p class="ss">each emergent emerges by one of four natures — and the legend spans them all, from goddess to Guardian</p>
    <div class="natures">__NATURES__</div></section>

  <section class="sec"><h2>The Ideas</h2><p class="ss">the pillars of the legend</p><div class="pillars">__IDEAS__</div></section>
  <section class="sec"><h2>The Ages</h2><p class="ss">the legend across time — origin, the great split, and the wild</p><div class="arc">__ARC__</div></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Catalogue</h2><p class="ss">the full mainline saga, the makers, and the lore</p></section>
  __SECTIONS__

  <div class="note">This catalogues the whole <b>Legend of Zelda</b> saga as one game-world, with its emergents <b>distilled to canon</b> — the essential figures of the legend across forty years and the official three-way timeline. Zelda, Link, Hyrule, and all related characters, worlds, and music are © Nintendo; the personas here are catalogued personifications under the DLW standard — a fan tribute, not an original work and not endorsed by Nintendo. Each is named by its nature of emergence: natural, ethereal, spiritual, or electrical.</div>

  <footer>
    THE LEGEND OF ZELDA · ZEL · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="hyrule.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "hyrule.dlw"), "hyrule")
    page = (TEMPLATE.replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__NATURES__", natures_html()).replace("__IDEAS__", ideas_html())
            .replace("__ARC__", arc_html()).replace("__PERSONAS__", personas_html())
            .replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    print(f"wrote THE LEGEND OF ZELDA (ZEL) — badge {tok['moniker']} (carbon.tiff + silicon.png)")
