import html, re
from data import BOOKS, SEGMENTS

SITE_TITLE = "The Fear That Sets You Free"
SITE_DESC = "Scripture for when you\u2019re afraid, stuck, or growing cold. Verses on the fear of God, with links to read each chapter and a commentary."


def esc(s):
    return html.escape(s, quote=False)


def lordify(s):
    # ESV prints the divine name in small capitals.
    s = esc(s)
    s = re.sub(r"\bLORD\b", '<span class="sc">Lord</span>', s)
    s = re.sub(r"\bGOD\b", '<span class="sc">God</span>', s)
    return s


def links(book, ch):
    code, slug = BOOKS[book]
    return (
        f"https://www.bible.com/bible/59/{code}.{ch}.ESV",
        f"https://enduringword.com/bible-commentary/{slug}-{ch}/",
    )


def verse_count(label):
    n = 0
    for part in label.split(","):
        part = part.strip()
        if "\u2013" in part:
            a, b = part.split("\u2013")
            n += int(b) - int(a) + 1
        else:
            n += 1
    return n


def verse_html(v):
    book, ch, label, text = v
    read, mean = links(book, ch)
    ref = f"{book} {ch}:{label}"
    return f'''
      <article class="v">
        <h4 class="ref">{esc(ref)}</h4>
        <p class="txt">{lordify(text)}</p>
        <div class="acts">
          <a class="b b-read" href="{read}" target="_blank" rel="noopener">Read the whole chapter</a>
          <a class="b b-mean" href="{mean}" target="_blank" rel="noopener">What does this mean?</a>
        </div>
      </article>'''


def segment_html(seg):
    sid = seg["id"]
    toc = "\n".join(
        f'<li><a href="#{sid}-{i+1}">{esc(t["title"])}</a></li>' for i, t in enumerate(seg["themes"])
    )
    themes = []
    for i, t in enumerate(seg["themes"]):
        note = f'<p class="note">{esc(t["note"])}</p>' if t["note"] else ""
        verses = "".join(verse_html(v) for v in t["verses"])
        themes.append(f'''
    <section class="theme" id="{sid}-{i+1}" aria-labelledby="{sid}-{i+1}-h">
      <h3 id="{sid}-{i+1}-h">{esc(t["title"])}</h3>
      {note}
      {verses}
    </section>''')
    others = [s for s in SEGMENTS if s["id"] != sid]
    other_links = "".join(
        f'<a class="other other-{o["id"]}" href="#{o["id"]}">{esc(o["title"])}</a>' for o in others
    )
    framing = "".join(f"<p>{esc(p)}</p>" for p in seg["framing"])
    return f'''
  <section class="seg seg-{sid}" id="{sid}" aria-labelledby="{sid}-title">
    <header class="seg-head">
      <div class="wrap">
        <h2 id="{sid}-title">{esc(seg["title"])}</h2>
        <p class="foryou">{esc(seg["foryou"])}</p>
      </div>
    </header>
    <div class="wrap seg-body">
      <div class="framing">{framing}</div>
      <aside class="prayer" aria-label="Prayer">
        <h3>Start with this prayer</h3>
        <p>{esc(seg["prayer"])}</p>
      </aside>
      <nav class="toc" aria-label="In this section">
        <h3>In this section</h3>
        <p class="toc-hint">Tap a heading to jump to it.</p>
        <ul>{toc}</ul>
      </nav>
      {"".join(themes)}
      <div class="seg-end">
        <a class="btn-top" href="#choose">Back to the top</a>
        <p class="others-label">Or go to another section:</p>
        <div class="others">{other_links}</div>
      </div>
    </div>
  </section>'''


def doors_html():
    out = []
    for s in SEGMENTS:
        out.append(f'''
      <a class="door door-{s["id"]}" href="#{s["id"]}">
        <span class="door-title">{esc(s["title"])}</span>
        <span class="door-desc">{esc(s["door"])}</span>
        <span class="door-go">Tap here to go there <span aria-hidden="true">\u2193</span></span>
      </a>''')
    return "".join(out)


CSS = r"""
:root{
  --paper:#F5F0E6; --paper-2:#EDE6D8; --ink:#1B2532; --ink-soft:#4B5563; --line:#D9CFBE;
  --gold:#9C7A2E; --cover:#1B2532; --cover-ink:#F5F0E6; --cover-soft:#C9BFAE;
  --fears:#1D5C57; --fears-soft:#E1ECE8;
  --sin:#8B2E29;   --sin-soft:#F2E3DF;
  --wonder:#3D3A7C; --wonder-soft:#E6E5F2;
  --on-c:#FFFFFF;
  --serif:"Literata", Georgia, "Times New Roman", serif;
  --sans:"Public Sans", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
}
@media (prefers-color-scheme: dark){
  :root{
    color-scheme: dark;
    --paper:#12171E; --paper-2:#1A2029; --ink:#ECE5D8; --ink-soft:#B4AC9F; --line:#2B333E;
    --gold:#D2AE60; --cover:#0C1016; --cover-ink:#F2EBDD; --cover-soft:#A9A091;
    --fears:#7FC4BA; --fears-soft:#172826;
    --sin:#E99C92;   --sin-soft:#2C1C1B;
    --wonder:#B3B0F3; --wonder-soft:#20203A;
    --on-c:#12171E;
  }
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%; scroll-behavior:smooth; scroll-padding-top:calc(12px + env(safe-area-inset-top,0px)); background:var(--paper)}
@media (prefers-reduced-motion: reduce){ html{scroll-behavior:auto} }
body{margin:0; background:var(--paper); color:var(--ink); font-family:var(--serif); font-size:1.125rem; line-height:1.68;
  padding-bottom:env(safe-area-inset-bottom,0px); font-optical-sizing:auto; text-rendering:optimizeLegibility}
.wrap{max-width:38rem; margin:0 auto; padding-left:max(22px, env(safe-area-inset-left,0px)); padding-right:max(22px, env(safe-area-inset-right,0px))}
a{color:inherit}
:focus-visible{outline:3px solid var(--gold); outline-offset:3px; border-radius:6px}
.sc{font-variant-caps:all-small-caps; letter-spacing:.04em}
h1,h2,h3,h4{margin:0}

/* Cover */
.cover{background:var(--cover); color:var(--cover-ink); padding:calc(56px + env(safe-area-inset-top,0px)) 0 60px}
.cover h1{font-family:var(--serif); font-weight:600; font-size:clamp(3.3rem, 17vw, 6.2rem); line-height:.93; letter-spacing:-.028em; margin-bottom:28px}
.cover h1 span{display:block}
.cover .sub{font-family:var(--sans); font-size:1.08rem; line-height:1.5; color:var(--cover-soft); max-width:26rem; margin:0 0 40px}
.cover-verse{margin:0; padding:4px 0 4px 20px; border-left:2px solid var(--gold); font-style:italic; font-size:1.18rem; line-height:1.6}
.cover-verse cite{display:block; margin-top:10px; font-style:normal; font-family:var(--sans); font-size:.92rem; font-weight:600; color:var(--gold)}

/* Intro blocks */
.block{padding-top:52px; padding-bottom:8px}
.block h2{font-size:1.9rem; line-height:1.15; font-weight:600; letter-spacing:-.012em; margin-bottom:16px}
.block p{margin:0 0 16px}
.hint{font-family:var(--sans); font-size:1.05rem; font-weight:500; background:var(--paper-2); border-radius:10px; padding:14px 16px; margin:0 0 20px}

/* Doors */
.doors{display:grid; gap:14px}
.door{display:block; text-decoration:none; border-radius:16px; padding:22px 22px 20px; color:var(--on-c); min-height:44px}
.door-fears{background:var(--fears)} .door-sin{background:var(--sin)} .door-wonder{background:var(--wonder)}
.door-title{display:block; font-family:var(--serif); font-weight:600; font-size:1.55rem; line-height:1.15; margin-bottom:8px}
.door-desc{display:block; font-family:var(--sans); font-size:1rem; line-height:1.45; opacity:.95}
.door-go{display:inline-block; margin-top:14px; font-family:var(--sans); font-weight:700; font-size:.98rem; text-decoration:underline; text-underline-offset:4px}
.door:active{transform:scale(.99)}

/* How the links work */
.how h3{font-family:var(--sans); font-size:1.05rem; font-weight:700; margin:24px 0 6px}
.how p{margin:0 0 10px}
.demo{display:flex; flex-wrap:wrap; gap:10px; margin:18px 0 6px}
.demo .b{pointer-events:none}
.tip{font-family:var(--sans); font-size:1rem; background:var(--paper-2); border-radius:10px; padding:14px 16px; margin-top:22px}

/* Buttons (shared) */
.b{display:inline-flex; align-items:center; justify-content:center; min-height:46px; padding:10px 16px; border-radius:999px;
   font-family:var(--sans); font-weight:600; font-size:.98rem; line-height:1.2; text-decoration:none; text-align:center}
.b-read{background:var(--c, var(--ink)); color:var(--on-c); border:2px solid var(--c, var(--ink))}
.b-mean{background:transparent; color:var(--c, var(--ink)); border:2px solid var(--c, var(--ink))}

/* Segments */
.seg{--c:var(--ink); --c-soft:var(--paper-2); margin-top:64px}
.seg-fears{--c:var(--fears); --c-soft:var(--fears-soft)}
.seg-sin{--c:var(--sin); --c-soft:var(--sin-soft)}
.seg-wonder{--c:var(--wonder); --c-soft:var(--wonder-soft)}
.seg-head{background:var(--c); color:var(--on-c); padding:44px 0 36px}
.seg-head h2{font-size:clamp(2.1rem, 9vw, 2.9rem); line-height:1.05; font-weight:600; letter-spacing:-.02em; margin-bottom:16px}
.foryou{font-family:var(--sans); font-size:1.06rem; line-height:1.5; margin:0}
.seg-body{padding-top:30px}
.framing p{margin:0 0 16px}
.prayer{background:var(--c-soft); border-radius:16px; padding:22px 22px 8px; margin:28px 0}
.prayer h3{font-family:var(--sans); font-size:1.02rem; font-weight:700; color:var(--c); margin-bottom:10px}
.prayer p{font-style:italic; font-size:1.14rem; line-height:1.7; margin:0 0 16px}
.toc{border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:20px 0 12px; margin:8px 0 8px}
.toc h3{font-family:var(--sans); font-size:1.02rem; font-weight:700; margin-bottom:2px}
.toc-hint{font-family:var(--sans); font-size:.92rem; color:var(--ink-soft); margin:0 0 8px}
.toc ul{list-style:none; margin:0; padding:0}
.toc li a{display:block; padding:9px 0; font-family:var(--sans); font-size:1.02rem; color:var(--c); text-decoration:underline; text-underline-offset:4px; text-decoration-thickness:1px}
.theme{padding-top:40px}
.theme h3{font-family:var(--serif); font-size:1.5rem; line-height:1.2; font-weight:600; letter-spacing:-.01em; color:var(--c); margin-bottom:8px}
.note{font-family:var(--sans); font-size:1rem; line-height:1.5; color:var(--ink-soft); margin:0 0 6px}
.v{padding:24px 0 26px 18px; border-left:3px solid var(--c); margin-top:22px}
.ref{font-family:var(--sans); font-size:1rem; font-weight:700; letter-spacing:.01em; color:var(--c); margin-bottom:6px}
.txt{font-size:1.16rem; line-height:1.7; margin:0 0 16px}
.acts{display:flex; flex-wrap:wrap; gap:10px}
.acts .b{flex:1 1 13rem}
.seg-end{margin:48px 0 0; padding:28px 0 8px; border-top:1px solid var(--line)}
.btn-top{display:flex; align-items:center; justify-content:center; min-height:52px; border-radius:999px; background:var(--ink); color:var(--paper);
  font-family:var(--sans); font-weight:700; font-size:1.05rem; text-decoration:none}
.others-label{font-family:var(--sans); font-size:.95rem; color:var(--ink-soft); margin:20px 0 10px}
.others{display:grid; gap:10px}
.other{display:block; padding:14px 16px; border-radius:12px; font-family:var(--sans); font-weight:700; font-size:1rem; text-decoration:none; border:2px solid}
.other-fears{color:var(--fears); border-color:var(--fears)} .other-sin{color:var(--sin); border-color:var(--sin)} .other-wonder{color:var(--wonder); border-color:var(--wonder)}

/* Footer */
footer{margin-top:72px; padding:36px 0 calc(48px + env(safe-area-inset-bottom,0px)); border-top:1px solid var(--line)}
footer p{font-family:var(--sans); font-size:.88rem; line-height:1.55; color:var(--ink-soft); margin:0 0 12px}
.share{display:flex; align-items:center; justify-content:center; width:100%; min-height:52px; margin-bottom:28px; border-radius:999px; border:2px solid var(--ink);
  background:transparent; color:var(--ink); font-family:var(--sans); font-weight:700; font-size:1.02rem; cursor:pointer}

/* Floating back-to-top */
.fab{position:fixed; right:max(16px, env(safe-area-inset-right,0px)); bottom:calc(16px + env(safe-area-inset-bottom,0px)); z-index:20;
  display:flex; align-items:center; gap:6px; min-height:48px; padding:0 18px; border-radius:999px; background:var(--ink); color:var(--paper);
  font-family:var(--sans); font-weight:700; font-size:.98rem; text-decoration:none; box-shadow:0 6px 18px rgba(0,0,0,.18);
  opacity:0; transform:translateY(10px); pointer-events:none; transition:opacity .2s ease, transform .2s ease}
.fab.show{opacity:1; transform:none; pointer-events:auto}
@media (prefers-reduced-motion: reduce){ .fab{transition:none} }

@media (min-width:720px){
  .doors{gap:16px}
  .others{grid-template-columns:1fr 1fr}
}
"""

JS = r"""
(function(){
  var fab = document.getElementById('fab');
  var choose = document.getElementById('choose');
  if ('IntersectionObserver' in window && fab && choose){
    var past = false;
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        past = !e.isIntersecting && e.boundingClientRect.top < 0;
        fab.classList.toggle('show', past);
      });
    });
    io.observe(choose);
  } else if (fab) { fab.classList.add('show'); }

  var share = document.getElementById('share');
  if (share){
    share.addEventListener('click', function(){
      var data = {title: document.title, url: location.href.split('#')[0]};
      if (navigator.share){ navigator.share(data).catch(function(){}); return; }
      try {
        navigator.clipboard.writeText(data.url).then(function(){ share.textContent = 'Link copied'; setTimeout(function(){ share.textContent = 'Share this page'; }, 2500); });
      } catch(e) { prompt('Copy this link:', data.url); }
    });
  }
})();
"""


def build():
    total = sum(verse_count(v[2]) for s in SEGMENTS for t in s["themes"] for v in t["verses"])
    cards = sum(len(t["verses"]) for s in SEGMENTS for t in s["themes"])
    for s in SEGMENTS:
        for t in s["themes"]:
            for v in t["verses"]:
                assert v[0] in BOOKS, v[0]

    favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
               "%3Crect width='64' height='64' rx='14' fill='%231B2532'/%3E"
               "%3Cpath d='M32 12c4 9 13 14 13 26a13 13 0 0 1-26 0c0-7 4-11 7-15 1 5 3 7 6 8-1-7 0-13 0-19z' fill='%23D2AE60'/%3E%3C/svg%3E")

    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{SITE_TITLE}</title>
<meta name="description" content="{esc(SITE_DESC)}">
<meta property="og:title" content="{SITE_TITLE}">
<meta property="og:description" content="{esc(SITE_DESC)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1B2532">
<link rel="icon" href="{favicon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=Public+Sans:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="cover" id="top">
  <div class="wrap">
    <h1><span>The Fear</span><span>That Sets</span><span>You Free</span></h1>
    <p class="sub">Scripture for when you\u2019re afraid, stuck, or growing cold.</p>
    <blockquote class="cover-verse">\u201cDo not fear, for God has come to test you, that the fear of him may be before you, that you may not sin.\u201d<cite>Exodus 20:20</cite></blockquote>
  </div>
</header>

<main>
  <section class="block wrap" aria-labelledby="start-h">
    <h2 id="start-h">Start here</h2>
    <p>The Bible talks about two kinds of fear. One makes you run from God, like Adam hiding in the garden. The other draws you close to him, like Moses walking into the thick darkness where God was (Exodus 20:21).</p>
    <p>The first fear chains you. The second sets you free. It is the awe of knowing how holy and how good God is, and it makes every other fear smaller.</p>
  </section>

  <section class="block wrap" id="choose" aria-labelledby="choose-h">
    <h2 id="choose-h">Where are you right now?</h2>
    <p class="hint">Tap the box that fits you. It will take you straight to that part of the page.</p>
    <div class="doors">{doors_html()}
    </div>
  </section>

  <section class="block wrap how" aria-labelledby="how-h">
    <h2 id="how-h">How the links work</h2>
    <p>Under every verse you\u2019ll see two buttons:</p>
    <div class="demo" aria-hidden="true">
      <span class="b b-read">Read the whole chapter</span>
      <span class="b b-mean">What does this mean?</span>
    </div>
    <h3>\u201cRead the whole chapter\u201d</h3>
    <p>Opens the full chapter on Bible.com in the ESV. If you have the Bible App (YouVersion) on your phone, it may open there instead. Reading the whole chapter shows you who is speaking, to whom, and why, because a verse means what it means in its chapter.</p>
    <h3>\u201cWhat does this mean?\u201d</h3>
    <p>Opens a free commentary on that chapter by Pastor David Guzik (Enduring Word). It covers the whole chapter, so scroll down to find your verse number. Guzik quotes the New King James Version, so the wording will look slightly different.</p>
    <h3>What is a commentary?</h3>
    <p>A commentary is written by a Bible teacher who walks through Scripture verse by verse. It explains the background, the meaning of key words, and how a passage fits with the rest of the Bible. It\u2019s like reading with an experienced teacher beside you.</p>
    <h3>Why use one?</h3>
    <p>The Bible was first written to people in a different time, language and culture. A good commentary fills in what they knew and we don\u2019t, and it helps keep us from reading our own ideas into the text.</p>
    <h3>When should I read it?</h3>
    <p>Read the verse first, then the whole chapter, and ask what God is saying to you. Open the commentary when something is unclear, when you want to go deeper, or before you share the verse with someone else. Scripture first, commentary second.</p>
    <p class="tip">Links open in a new tab. When you\u2019re done, tap your phone\u2019s Back button or back arrow to return here. If a link opened the Bible App, switch back to your browser.</p>
  </section>
{"".join(segment_html(s) for s in SEGMENTS)}
</main>

<footer>
  <div class="wrap">
    <button class="share" id="share" type="button">Share this page</button>
    <p>Scripture quotations are from the ESV\u00ae Bible (The Holy Bible, English Standard Version\u00ae), \u00a9 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved.</p>
    <p>\u201cRead the whole chapter\u201d links go to Bible.com (YouVersion). \u201cWhat does this mean?\u201d links go to the Enduring Word Bible Commentary by David Guzik.</p>
  </div>
</footer>

<a class="fab" id="fab" href="#choose" aria-label="Back to the top"><span aria-hidden="true">\u2191</span> Top</a>
<script>{JS}</script>
</body>
</html>
'''
    open("index.html", "w").write(page)
    print(f"cards={cards} verses={total} bytes={len(page.encode())}")


if __name__ == "__main__":
    build()
