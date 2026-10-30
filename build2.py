import json, re
from data import SEGMENTS, BOOKS
import build as B

used = sorted({v[0] for s in SEGMENTS for t in s["themes"] for v in t["verses"]})
BK = {b: BOOKS[b] for b in used}
D = [[s["id"], s["title"], s["door"], s["foryou"], s["framing"], s["prayer"],
      [[t["title"], t["note"], [[v[0], v[1], v[2], v[3]] for v in t["verses"]]] for t in s["themes"]]] for s in SEGMENTS]

css = re.sub(r"\s*\n\s*", "", B.CSS.strip())
css = re.sub(r"/\*.*?\*/", "", css)

RENDER = r"""
var BK=__BK__,D=__D__;
function e(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function sc(s){return e(s).replace(/\bLORD\b/g,'<span class="sc">Lord</span>').replace(/\bGOD\b/g,'<span class="sc">God</span>')}
function card(v){var k=BK[v[0]];return '<article class="v"><h4 class="ref">'+e(v[0]+' '+v[1]+':'+v[2])+'</h4><p class="txt">'+sc(v[3])+'</p><div class="acts"><a class="b b-read" href="https://www.bible.com/bible/59/'+k[0]+'.'+v[1]+'.ESV" target="_blank" rel="noopener">Read the whole chapter</a><a class="b b-mean" href="https://enduringword.com/bible-commentary/'+k[1]+'-'+v[1]+'/" target="_blank" rel="noopener">What does this mean?</a></div></article>'}
var doors='',segs='';
D.forEach(function(s){
  var id=s[0];
  doors+='<a class="door door-'+id+'" href="#'+id+'"><span class="door-title">'+e(s[1])+'</span><span class="door-desc">'+e(s[2])+'</span><span class="door-go">Tap here to go there <span aria-hidden="true">\u2193</span></span></a>';
  var toc='',th='';
  s[6].forEach(function(t,i){
    var tid=id+'-'+(i+1);
    toc+='<li><a href="#'+tid+'">'+e(t[0])+'</a></li>';
    th+='<section class="theme" id="'+tid+'"><h3>'+e(t[0])+'</h3>'+(t[1]?'<p class="note">'+e(t[1])+'</p>':'')+t[2].map(card).join('')+'</section>';
  });
  var others=D.filter(function(o){return o[0]!==id}).map(function(o){return '<a class="other other-'+o[0]+'" href="#'+o[0]+'">'+e(o[1])+'</a>'}).join('');
  segs+='<section class="seg seg-'+id+'" id="'+id+'"><header class="seg-head"><div class="wrap"><h2>'+e(s[1])+'</h2><p class="foryou">'+e(s[3])+'</p></div></header><div class="wrap seg-body"><div class="framing">'+s[4].map(function(p){return '<p>'+e(p)+'</p>'}).join('')+'</div><aside class="prayer" aria-label="Prayer"><h3>Start with this prayer</h3><p>'+e(s[5])+'</p></aside><nav class="toc" aria-label="In this section"><h3>In this section</h3><p class="toc-hint">Tap a heading to jump to it.</p><ul>'+toc+'</ul></nav>'+th+'<div class="seg-end"><a class="btn-top" href="#choose">Back to the top</a><p class="others-label">Or go to another section:</p><div class="others">'+others+'</div></div></div></section>';
});
document.getElementById('doors').innerHTML=doors;
document.getElementById('segs').innerHTML=segs;
if(location.hash){var t=document.getElementById(location.hash.slice(1));if(t)t.scrollIntoView();}
"""
render = RENDER.replace("__BK__", json.dumps(BK, ensure_ascii=False, separators=(",",":"))).replace("__D__", json.dumps(D, ensure_ascii=False, separators=(",",":")))
render = render.replace("\\u2193", "\u2193")
js = re.sub(r"\n\s*", "", B.JS.strip())

fav = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%231B2532'/%3E"
       "%3Cpath d='M32 12c4 9 13 14 13 26a13 13 0 0 1-26 0c0-7 4-11 7-15 1 5 3 7 6 8-1-7 0-13 0-19z' fill='%23D2AE60'/%3E%3C/svg%3E")

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>The Fear That Sets You Free</title>
<meta name="description" content="{B.SITE_DESC}">
<meta property="og:title" content="The Fear That Sets You Free">
<meta property="og:description" content="{B.SITE_DESC}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1B2532">
<link rel="icon" href="{fav}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=Public+Sans:wght@500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header class="cover" id="top"><div class="wrap">
<h1><span>The Fear</span><span>That Sets</span><span>You Free</span></h1>
<p class="sub">Scripture for when you’re afraid, stuck, or growing cold.</p>
<blockquote class="cover-verse">“Do not fear, for God has come to test you, that the fear of him may be before you, that you may not sin.”<cite>Exodus 20:20</cite></blockquote>
</div></header>
<main>
<section class="block wrap">
<h2>Start here</h2>
<p>The Bible talks about two kinds of fear. One makes you run from God, like Adam hiding in the garden. The other draws you close to him, like Moses walking into the thick darkness where God was (Exodus 20:21).</p>
<p>The first fear chains you. The second sets you free. It is the awe of knowing how holy and how good God is, and it makes every other fear smaller.</p>
</section>
<section class="block wrap" id="choose">
<h2>Where are you right now?</h2>
<p class="hint">Tap the box that fits you. It will take you straight to that part of the page.</p>
<div class="doors" id="doors"></div>
<noscript><p>This page needs JavaScript turned on to show the verses.</p></noscript>
</section>
<section class="block wrap how">
<h2>How the links work</h2>
<p>Under every verse you’ll see two buttons:</p>
<div class="demo" aria-hidden="true"><span class="b b-read">Read the whole chapter</span><span class="b b-mean">What does this mean?</span></div>
<h3>“Read the whole chapter”</h3>
<p>Opens the full chapter on Bible.com in the ESV. If you have the Bible App (YouVersion) on your phone, it may open there instead. Reading the whole chapter shows you who is speaking, to whom, and why, because a verse means what it means in its chapter.</p>
<h3>“What does this mean?”</h3>
<p>Opens a free commentary on that chapter by Pastor David Guzik (Enduring Word). It covers the whole chapter, so scroll down to find your verse number. Guzik quotes the New King James Version, so the wording will look slightly different.</p>
<h3>What is a commentary?</h3>
<p>A commentary is written by a Bible teacher who walks through Scripture verse by verse. It explains the background, the meaning of key words, and how a passage fits with the rest of the Bible. It’s like reading with an experienced teacher beside you.</p>
<h3>Why use one?</h3>
<p>The Bible was first written to people in a different time, language and culture. A good commentary fills in what they knew and we don’t, and it helps keep us from reading our own ideas into the text.</p>
<h3>When should I read it?</h3>
<p>Read the verse first, then the whole chapter, and ask what God is saying to you. Open the commentary when something is unclear, when you want to go deeper, or before you share the verse with someone else. Scripture first, commentary second.</p>
<p class="tip">Links open in a new tab. When you’re done, tap your phone’s Back button or back arrow to return here. If a link opened the Bible App, switch back to your browser.</p>
</section>
<div id="segs"></div>
</main>
<footer><div class="wrap">
<button class="share" id="share" type="button">Share this page</button>
<p>Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved.</p>
<p>“Read the whole chapter” links go to Bible.com (YouVersion). “What does this mean?” links go to the Enduring Word Bible Commentary by David Guzik.</p>
</div></footer>
<a class="fab" id="fab" href="#choose" aria-label="Back to the top"><span aria-hidden="true">↑</span> Top</a>
<script>{render.strip()}
{js}</script>
</body>
</html>
'''
open("index.html","w").write(page)
print("bytes", len(page.encode()))
