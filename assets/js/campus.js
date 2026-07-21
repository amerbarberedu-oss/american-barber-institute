(function(){
/* ══════════════════════════════════════════════════════════════════════════
   ABI shared-shell campus + language + nav controller (shell2).
   - Routes header/footer phone numbers per campus (Manhattan / Bronx / both).
   - Drives the segmented campus + EN/ES switchers (sliding glider + live swap).
   - Adds click/keyboard support to the desktop nav dropdowns (touch + a11y).
   Facts (do not change):
     Manhattan admissions (212) 290-2289 EN / (212) 290-0278 ES
     Bronx admissions     (718) 676-0640
     Haircut clinic line  (856) 316-1551 (serves both campuses)
   ══════════════════════════════════════════════════════════════════════════ */

var PHONE_SVG='<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>';
var SCISSORS_SVG='<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88"/><path d="M14.47 14.48 20 20"/><path d="M8.12 8.12 12 12"/></svg>';
var PIN_SVG='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>';

/* Detect if current page is Spanish */
function isSpanish(){
  var p=location.pathname;
  return /\/spanish(\/|$)/.test(p)||/\/es(\/|$)/.test(p);
}

/* Labels: language of the phone line, NOT location */
function L(en,es){ return isSpanish()?es:en; }

function buildMN(){return{
  addr:"48 W. 39th St., New York, NY 10018",
  ubar:[
    {ico:PHONE_SVG,cls:"ubar-call ubar-call--admis",tag:L("English","Inglés"),num:"(212) 290-2289",tel:"+12122902289"},
    {ico:SCISSORS_SVG,cls:"ubar-call ubar-call--cut",tag:L("Haircut","Corte"),num:"(856) 316-1551",tel:"+18563161551"},
    {ico:"ES",cls:"ubar-call ubar-call--es",tag:L("Spanish","Español"),num:"(212) 290-0278",tel:"+12122900278"}
  ],
  mstrip:[
    {ico:PHONE_SVG,num:"(212) 290-2289",lab:L("English","Inglés"),tel:"+12122902289"},
    {ico:SCISSORS_SVG,num:"(856) 316-1551",lab:L("Haircut","Corte"),tel:"+18563161551"},
    {ico:PHONE_SVG,num:"(212) 290-0278",lab:L("Spanish","Español"),tel:"+12122900278"}
  ],
  footer:[
    {text:"(212) 290-2289 · "+L("English","Inglés"),tel:"+12122902289"},
    {text:"(212) 290-0278 · "+L("Spanish","Español"),tel:"+12122900278"},
    {text:"(856) 316-1551 · "+L("Haircut","Corte"),tel:"+18563161551"}
  ],
  mbar:{call:"+12122902289",text:"+12122902289"}
};}

function buildBX(){return{
  addr:"121 Westchester Square, Bronx, NY 10461",
  ubar:[
    {ico:PHONE_SVG,cls:"ubar-call ubar-call--admis",tag:L("English","Inglés"),num:"(718) 676-0640",tel:"+17186760640"},
    {ico:SCISSORS_SVG,cls:"ubar-call ubar-call--cut",tag:L("Haircut","Corte"),num:"(856) 316-1551",tel:"+18563161551"}
  ],
  mstrip:[
    {ico:PHONE_SVG,num:"(718) 676-0640",lab:L("English","Inglés"),tel:"+17186760640"},
    {ico:SCISSORS_SVG,num:"(856) 316-1551",lab:L("Haircut","Corte"),tel:"+18563161551"}
  ],
  footer:[
    {text:"(718) 676-0640 · "+L("English","Inglés"),tel:"+17186760640"},
    {text:"(856) 316-1551 · "+L("Haircut","Corte"),tel:"+18563161551"}
  ],
  mbar:{call:"+17186760640",text:"+17186760640"}
};}

function buildBOTH(){return{
  addr:"48 W. 39th St., New York, NY 10018",
  ubar:[
    {ico:PHONE_SVG,cls:"ubar-call ubar-call--admis",tag:"Manhattan",num:"(212) 290-2289",tel:"+12122902289"},
    {ico:PHONE_SVG,cls:"ubar-call ubar-call--admis",tag:"Bronx",num:"(718) 676-0640",tel:"+17186760640"},
    {ico:SCISSORS_SVG,cls:"ubar-call ubar-call--cut",tag:L("Haircut","Corte"),num:"(856) 316-1551",tel:"+18563161551"}
  ],
  mstrip:[
    {ico:PHONE_SVG,num:"(212) 290-2289",lab:"Manhattan",tel:"+12122902289"},
    {ico:SCISSORS_SVG,num:"(856) 316-1551",lab:L("Haircut","Corte"),tel:"+18563161551"}
  ],
  footer:[
    {text:"(212) 290-2289 · Manhattan",tel:"+12122902289"},
    {text:"(718) 676-0640 · Bronx",tel:"+17186760640"},
    {text:"(856) 316-1551 · "+L("Haircut","Corte"),tel:"+18563161551"}
  ],
  mbar:{call:"+12122902289",text:"+12122902289"}
};}

/* Landing-funnel pages (body.lf-page) show campus-only numbers — no haircut/walk-in line */
function isLandingPage(){return document.body.classList.contains("lf-page");}
function stripHaircut(d){
  var isCut=function(p){return p.tel==="+18563161551";};
  return{
    addr:d.addr,
    ubar:d.ubar.filter(function(p){return !isCut(p);}),
    mstrip:d.mstrip.filter(function(p){return !isCut(p);}),
    footer:d.footer.filter(function(p){return !isCut(p);}),
    mbar:d.mbar
  };
}
function getData(){
  var d={manhattan:buildMN(),bronx:buildBX(),both:buildBOTH()};
  if(isLandingPage()){
    d.manhattan=stripHaircut(d.manhattan);
    d.bronx=stripHaircut(d.bronx);
    d.both=stripHaircut(d.both);
  }
  return d;
}

function pageCampus(){
  var c=(document.body.getAttribute("data-campus")||"manhattan").toLowerCase();
  var d=getData();
  return d[c]?c:"manhattan";
}
function isFixedPage(){
  return document.body.getAttribute("data-campus-locked")==="true";
}
function getCampus(){
  if(isFixedPage()) return pageCampus();
  try{return localStorage.getItem("abi-campus")||"manhattan";}catch(e){return "manhattan";}
}
function setCampus(c){try{localStorage.setItem("abi-campus",c);}catch(e){}}

function swapPhones(data){
  var ubar=document.querySelector("[data-campus-phones]");
  if(ubar){
    ubar.innerHTML=data.ubar.map(function(p){
      var ico=(p.ico==="ES")?'<span class="ubar-ico" aria-hidden="true">ES</span>'
                            :'<span class="ubar-ico" aria-hidden="true">'+p.ico+'</span>';
      return '<a class="'+p.cls+'" href="tel:'+p.tel+'">'+ico+
             '<span class="ubar-tag">'+p.tag+'</span><span class="ubar-num">'+p.num+'</span></a>';
    }).join("");
  }
  var strip=document.querySelector("[data-mstrip-phones]");
  if(strip){
    strip.innerHTML=data.mstrip.map(function(p){
      return '<a class="mstrip-phone" href="tel:'+p.tel+'">'+p.ico+
             '<span class="mstrip-t"><b>'+p.num+'</b><i>'+p.lab+'</i></span></a>';
    }).join("");
  }
  var ftr=document.querySelector("[data-footer-phones]");
  if(ftr){
    ftr.innerHTML=data.footer.map(function(p){
      return '<a href="tel:'+p.tel+'">'+p.text+'</a>';
    }).join("");
  }
  var mbarCall=document.querySelector(".mbar-call"),mbarText=document.querySelector(".mbar-text");
  if(mbarCall) mbarCall.href="tel:"+data.mbar.call;
  if(mbarText) mbarText.href="sms:"+data.mbar.text;
}

/* ── Segmented switcher glider ── */
function syncSeg(seg){
  if(!seg) return;
  var opts=seg.querySelectorAll(".seg-opt");
  var activeIdx=0;
  opts.forEach(function(o,i){ if(o.classList.contains("is-active")) activeIdx=i; });
  seg.setAttribute("data-active",String(activeIdx));
}
function setCampusActive(campus){
  var seg=document.querySelector('.seg-campus');
  if(!seg) return;
  seg.querySelectorAll(".seg-opt").forEach(function(o){
    var on=(o.getAttribute("data-campus-opt")===campus);
    o.classList.toggle("is-active",on);
    if(on) o.setAttribute("aria-current","true"); else o.setAttribute("aria-current","false");
  });
  syncSeg(seg);
}

/* ── Address under the header logo (client mockup): wrap the logo in a column and
   inject the per-campus street address beneath it. Runs once, then just updates text. ── */
function applyAddr(data){
  var inRow=document.querySelector(".hdr2 .hdr2-in");
  if(!inRow) return;
  var logo=inRow.querySelector(".logo2");
  if(!logo) return;
  var col=inRow.querySelector(".logo2-col");
  if(!col){
    col=document.createElement("div");
    col.className="logo2-col";
    inRow.insertBefore(col,logo);
    col.appendChild(logo);
    var a=document.createElement("div");
    a.className="hdr2-addr";
    col.appendChild(a);
  }
  var addrEl=col.querySelector(".hdr2-addr");
  if(addrEl&&data&&data.addr){
    addrEl.innerHTML=PIN_SVG+'<span>'+data.addr+'</span>';
  }
}

function applyCampus(campus){
  var d=getData();
  var data=d[campus]||d.manhattan;
  swapPhones(data);
  setCampusActive(campus);
  applyAddr(data);
}

/* ── Nav dropdown: click/keyboard support (hover works via CSS) ── */
function initDropdowns(){
  var items=document.querySelectorAll(".nav2-has");
  items.forEach(function(item){
    var btn=item.querySelector(".nav2-top");
    var menu=item.querySelector(".nav2-menu");
    if(!btn||!menu) return;
    btn.addEventListener("click",function(e){
      e.preventDefault();
      var open=menu.classList.toggle("open");
      btn.setAttribute("aria-expanded",String(open));
      items.forEach(function(o){ if(o!==item){var m=o.querySelector(".nav2-menu"),b=o.querySelector(".nav2-top");
        if(m)m.classList.remove("open"); if(b)b.setAttribute("aria-expanded","false");}});
    });
    btn.addEventListener("keydown",function(e){
      if(e.key==="Escape"){menu.classList.remove("open");btn.setAttribute("aria-expanded","false");}
    });
    /* CSS opens the menu on :focus-within for keyboard users, but aria-expanded
       was only ever toggled by the click handler above -- screen readers were
       told the menu was collapsed while it was actually open and navigable. */
    item.addEventListener("focusin",function(){
      btn.setAttribute("aria-expanded","true");
    });
    item.addEventListener("focusout",function(e){
      if(!item.contains(e.relatedTarget)){
        btn.setAttribute("aria-expanded","false");
        menu.classList.remove("open");
      }
    });
  });
  document.addEventListener("click",function(e){
    if(e.target.closest(".nav2-has")) return;
    items.forEach(function(o){var m=o.querySelector(".nav2-menu"),b=o.querySelector(".nav2-top");
      if(m)m.classList.remove("open"); if(b)b.setAttribute("aria-expanded","false");});
  });
}

function isProgramsPage(){var p=location.pathname;return /\/programs\//.test(p)||/\/programs$/.test(p);}
function isBronxProgramsPage(){var p=location.pathname;return /\/programs\/bronx(\.html)?$/.test(p)||/\/500-hour-master-barber-bronx/.test(p);}
function isManhattanProgramsPage(){var p=location.pathname;return /\/programs\/manhattan(\.html)?$/.test(p)||/\/programs\/500-hour-master-barber(\.html)?$/.test(p)||/\/50-hour-barber-refresher/.test(p);}

function rewriteProgramsLinks(campus){
  var target=campus==="bronx"?"bronx.html":"manhattan.html";
  var links=document.querySelectorAll('a[href]');
  links.forEach(function(a){
    var href=a.getAttribute("href")||"";
    var raw=href.split("?")[0].split("#")[0];
    if(/(^|\/)programs\/?(index\.html)?$/.test(raw)){
      var base=raw.replace(/(index\.html)?$/, "").replace(/\/$/, "");
      var newHref=base+"/"+target;
      if(href.charAt(0)==="/"&&newHref.charAt(0)!=="/") newHref="/"+newHref;
      a.setAttribute("href", newHref);
      a.setAttribute("data-abi-programs-rewritten", campus);
    }
  });
}

function init(){
  syncSeg(document.querySelector(".seg-lang"));

  if(isBronxProgramsPage()){setCampus("bronx");}
  else if(isManhattanProgramsPage()){setCampus("manhattan");}

  var seg=document.querySelector(".seg-campus");
  if(isFixedPage()){
    setCampus(pageCampus()==="bronx"?"bronx":"manhattan");
    applyCampus(pageCampus());
    rewriteProgramsLinks(pageCampus());
  }else{
    var campus=getCampus();
    applyCampus(campus);
    rewriteProgramsLinks(campus);
    if(seg){
      seg.addEventListener("click",function(e){
        var opt=e.target.closest(".seg-opt");
        if(!opt) return;
        var to=opt.getAttribute("data-campus-opt");
        var esPrefix=/\/spanish(\/|$)/.test(location.pathname)?"/spanish":(/\/es\//.test(location.pathname)?"/es":"");
        if(to==="bronx"){
          setCampus("bronx");
          if(isProgramsPage()){
            e.preventDefault();
            location.href=esPrefix+"/programs/bronx.html";
            return;
          }
          return;
        }
        e.preventDefault();
        setCampus("manhattan");
        if(isProgramsPage()){
          location.href=esPrefix+"/programs/manhattan.html";
          return;
        }
        applyCampus("manhattan");
        rewriteProgramsLinks("manhattan");
      });
    }
  }

  initDropdowns();
}

if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",init);
else init();
})();
