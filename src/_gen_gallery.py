#!/usr/bin/env python3
"""Generate ABI 'black' cinematic 3D gallery (coverflow style).

Builds src/pages/gallery.html (content partial; build.py wraps it) from:
  - assets/img/gallery/*.jpg        (curated multi-people photos, committed)
  - src/data/gallery_videos.json    (videos embedded from public CDN, NOT in git)
Photos: horizontal 3D COVERFLOW carousel (distinct from blue's tilt-grid) + lightbox.
Videos: cinematic 9:16 reel strip, click-to-play, gold accents.
Injects a .cf3d-* CSS block into assets/css/landing.css (idempotent).
Run:  python3 src/_gen_gallery.py   (then python3 src/build.py)
"""
import json, glob, os, pathlib

REPO  = pathlib.Path(__file__).resolve().parent.parent
PAGES = REPO / "src" / "pages"
CSS   = REPO / "assets" / "css" / "landing.css"

imgs = sorted(os.path.basename(p) for p in glob.glob(str(REPO / "assets/img/gallery/*.jpg")))
vids = [v for v in json.load(open(REPO / "src/data/gallery_videos.json", encoding="utf-8"))
        if v.get("ext") == "mp4"]

photo_cards = "".join(
    f'<button class="cf3d-card" data-full="assets/img/gallery/{n}">'
    f'<img loading="lazy" src="assets/img/gallery/{n}" '
    f'alt="ABI barber students and instructors at work in NYC"></button>'
    for n in imgs
)

def reel_card(v):
    poster = f' data-poster="{v["poster"]}"' if v.get("poster") else ""
    return (f'<button class="cf3d-reel" data-src="{v["url"]}"{poster}>'
            f'<span class="cf3d-play">&#9658;</span></button>')

reel_cards = "".join(reel_card(v) for v in vids)

JS = """<script>(function(){
var track=document.getElementById('cf3dtrack');
if(track){var cards=[].slice.call(track.querySelectorAll('.cf3d-card'));
 function upd(){var c=track.getBoundingClientRect(),cx=c.left+c.width/2;
  cards.forEach(function(card){var r=card.getBoundingClientRect();var d=(r.left+r.width/2-cx)/c.width;
   var ry=Math.max(-60,Math.min(60,-d*80)),sc=Math.max(.74,1-Math.abs(d)*0.55);
   card.style.transform='perspective(1300px) rotateY('+ry.toFixed(1)+'deg) scale('+sc.toFixed(3)+')';
   card.style.opacity=Math.max(.4,1-Math.abs(d)*0.95).toFixed(2);
   card.style.zIndex=String(100-Math.round(Math.abs(d)*100));});}
 track.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);
 setTimeout(upd,60);
 var step=function(dir){track.scrollBy({left:dir*track.clientWidth*0.7,behavior:'smooth'});};
 var pv=document.getElementById('cf3dprev'),nx=document.getElementById('cf3dnext');
 if(pv)pv.addEventListener('click',function(){step(-1);});
 if(nx)nx.addEventListener('click',function(){step(1);});
 var lb=document.getElementById('cf3dlb'),im=document.getElementById('cf3dlbimg'),idx=0;
 var fulls=cards.map(function(c){return c.getAttribute('data-full');});
 function show(i){idx=(i+fulls.length)%fulls.length;im.src=fulls[idx];lb.classList.add('on');}
 cards.forEach(function(c,i){c.addEventListener('click',function(){show(i);});});
 document.getElementById('cf3dx').addEventListener('click',function(){lb.classList.remove('on');});
 lb.addEventListener('click',function(e){if(e.target===lb)lb.classList.remove('on');});
 document.addEventListener('keydown',function(e){if(!lb.classList.contains('on'))return;
  if(e.key==='Escape')lb.classList.remove('on');if(e.key==='ArrowRight')show(idx+1);if(e.key==='ArrowLeft')show(idx-1);});
}
[].slice.call(document.querySelectorAll('.cf3d-reel')).forEach(function(r){
 r.addEventListener('click',function(){if(r.dataset.loaded)return;r.dataset.loaded=1;
  var v=document.createElement('video');v.src=r.dataset.src;v.controls=true;v.autoplay=true;
  v.playsInline=true;v.setAttribute('playsinline','');if(r.dataset.poster)v.poster=r.dataset.poster;
  r.innerHTML='';r.appendChild(v);});
});
})();</script>"""

partial = (
    '<div class="page-hero dark"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Gallery</p>'
    '<h1>Our Gallery</h1><p>Real students, instructors and moments from inside our Midtown Manhattan campus — '
    'in photos and motion.</p></div></div>\n'
    '<section><div class="wrap"><div class="section-head"><p class="kicker">Student Work</p>'
    '<h2>Cuts &amp; Moments</h2></div></div>'
    '<div class="cf3d-stage"><button class="cf3d-arrow prev" id="cf3dprev" aria-label="Previous">&lsaquo;</button>'
    f'<div class="cf3d-track" id="cf3dtrack">{photo_cards}</div>'
    '<button class="cf3d-arrow next" id="cf3dnext" aria-label="Next">&rsaquo;</button></div>\n'
    '<section><div class="wrap"><div class="section-head"><p class="kicker">In Motion</p>'
    f'<h2>ABI Reels</h2></div><p class="cf3d-sub">{len(vids)} clips from the floor — tap to play.</p>'
    f'<div class="cf3d-reels">{reel_cards}</div></div></section>'
    '<div class="cf3d-lb" id="cf3dlb"><button class="cf3d-lb-x" id="cf3dx" aria-label="Close">&times;</button>'
    '<img id="cf3dlbimg" alt="ABI gallery photo"></div>'
    + JS
)
(PAGES / "gallery.html").write_text(partial, encoding="utf-8")

CSS_BLOCK = """
/* cf3d — black cinematic 3D coverflow gallery */
.cf3d-stage{position:relative;margin:8px 0 10px}
.cf3d-track{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;padding:46px 44vw;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.cf3d-track::-webkit-scrollbar{display:none}
.cf3d-card{flex:0 0 auto;width:300px;aspect-ratio:3/4;scroll-snap-align:center;position:relative;border:0;padding:0;cursor:pointer;background:#0b0e14;border-radius:16px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6);transition:opacity .2s ease;will-change:transform}
.cf3d-card img{width:100%;height:100%;object-fit:cover;display:block}
.cf3d-arrow{position:absolute;top:50%;transform:translateY(-50%);z-index:120;width:52px;height:52px;border-radius:50%;border:1px solid rgba(217,164,65,.5);background:rgba(11,14,20,.7);color:#d9a441;font-size:30px;cursor:pointer;backdrop-filter:blur(6px)}
.cf3d-arrow.prev{left:12px}.cf3d-arrow.next{right:12px}
.cf3d-sub{color:#9aa3b2;margin:.3rem 0 1rem}
.cf3d-reels{display:flex;gap:16px;overflow-x:auto;padding:6px 2px 18px;scroll-snap-type:x mandatory;scrollbar-width:none}
.cf3d-reels::-webkit-scrollbar{display:none}
.cf3d-reel{position:relative;flex:0 0 auto;width:190px;aspect-ratio:9/16;scroll-snap-align:start;border:1px solid rgba(217,164,65,.25);cursor:pointer;background:linear-gradient(160deg,#15110a,#0b0e14);border-radius:16px;overflow:hidden;box-shadow:0 18px 44px rgba(0,0,0,.55);transition:transform .2s ease,border-color .2s ease}
.cf3d-reel:hover{transform:translateY(-5px);border-color:rgba(217,164,65,.7)}
.cf3d-reel video{width:100%;height:100%;object-fit:cover;display:block}
.cf3d-play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:30px;color:#d9a441;background:radial-gradient(circle,rgba(0,0,0,.1),rgba(0,0,0,.55))}
.cf3d-lb{position:fixed;inset:0;z-index:300;background:rgba(2,3,6,.96);display:none;align-items:center;justify-content:center;padding:20px}
.cf3d-lb.on{display:flex}
.cf3d-lb img{max-width:94vw;max-height:90vh;border-radius:10px;box-shadow:0 30px 80px rgba(0,0,0,.8)}
.cf3d-lb-x{position:absolute;top:14px;right:20px;font-size:34px;color:#d9a441;background:0;border:0;cursor:pointer;line-height:1}
@media(max-width:640px){.cf3d-track{padding:36px 30vw}.cf3d-card{width:230px}}
@media(prefers-reduced-motion:reduce){.cf3d-card,.cf3d-reel{transition:none}}
"""
css = CSS.read_text(encoding="utf-8")
if "cf3d — black cinematic" not in css:
    CSS.write_text(css + CSS_BLOCK, encoding="utf-8")
    print("injected cf3d CSS")
print(f"black gallery: {len(imgs)} photos + {len(vids)} mp4 reels")
