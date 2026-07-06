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

var MN={
  // utility bar (top): admissions EN, admissions ES, haircut clinic
  ubar:[
    {ico:PHONE_SVG,cls:"ubar-call ubar-call--admis",tag:"Admissions",num:"(212) 290-2289",tel:"+12122902289"},
    {ico:"ES",cls:"ubar-call ubar-call--es",tag:"Español",num:"(212) 290-0278",tel:"+12122900278"},
    {ico:SCISSORS_SVG,cls:"ubar-call ubar-call--cut",tag:"Haircut Clinic",num:"(856) 316-1551",tel:"+18563161551"}
  ],
  // compact mobile strip (2 tiles)
  mstrip:[
    {ico:PHONE_SVG,num:"(212) 290-2289",lab:"Admissions",tel:"+12122902289"},
    {ico:SCISSORS_SVG,num:"(856) 316-1551",lab:"Haircut Clinic",tel:"+18563161551"}
  ],
  footer:[
    {text:"(212) 290-2289 · English",tel:"+12122902289"},
    {text:"(212) 290-0278 · Español",tel:"+12122900278"},
    {text:"(856) 316-1551 · Haircut Clinic",tel:"+18563161551"}
  ],
  mbar:{call:"+12122902289",text:"+12122902289"}
};

var BX={
  ubar:[
    {ico:PHONE_SVG,cls:"ubar-call ubar-call--admis",tag:"Bronx Admissions",num:"(718) 676-0640",tel:"+17186760640"},
    {ico:SCISSORS_SVG,cls:"ubar-call ubar-call--cut",tag:"Haircut Clinic",num:"(856) 316-1551",tel:"+18563161551"}
  ],
  mstrip:[
    {ico:PHONE_SVG,num:"(718) 676-0640",lab:"Bronx Admissions",tel:"+17186760640"},
    {ico:SCISSORS_SVG,num:"(856) 316-1551",lab:"Haircut Clinic",tel:"+18563161551"}
  ],
  footer:[
    {text:"(718) 676-0640 · Bronx Admissions",tel:"+17186760640"},
    {text:"(856) 316-1551 · Haircut Clinic",tel:"+18563161551"}
  ],
  mbar:{call:"+17186760640",text:"+17186760640"}
};

// Haircuts page ("both"): show BOTH campuses' admissions + the haircut line.
var BOTH={
  ubar:[
    {ico:PHONE_SVG,cls:"ubar-call ubar-call--admis",tag:"Manhattan",num:"(212) 290-2289",tel:"+12122902289"},
    {ico:PHONE_SVG,cls:"ubar-call ubar-call--admis",tag:"Bronx",num:"(718) 676-0640",tel:"+17186760640"},
    {ico:SCISSORS_SVG,cls:"ubar-call ubar-call--cut",tag:"Haircut Clinic",num:"(856) 316-1551",tel:"+18563161551"}
  ],
  mstrip:[
    {ico:PHONE_SVG,num:"(212) 290-2289",lab:"Manhattan",tel:"+12122902289"},
    {ico:SCISSORS_SVG,num:"(856) 316-1551",lab:"Haircut Clinic",tel:"+18563161551"}
  ],
  footer:[
    {text:"(212) 290-2289 · Manhattan",tel:"+12122902289"},
    {text:"(718) 676-0640 · Bronx",tel:"+17186760640"},
    {text:"(856) 316-1551 · Haircut Clinic",tel:"+18563161551"}
  ],
  mbar:{call:"+12122902289",text:"+12122902289"}
};

var DATA={manhattan:MN,bronx:BX,both:BOTH};

function pageCampus(){
  var c=(document.body.getAttribute("data-campus")||"manhattan").toLowerCase();
  return DATA[c]?c:"manhattan";
}
function isFixedPage(){
  // Bronx + Haircuts pages have a fixed campus context (no live user switching).
  var c=pageCampus();
  return c==="bronx"||c==="both"||document.body.classList.contains("bx-gold");
}
function getCampus(){
  if(isFixedPage()) return pageCampus();
  try{return localStorage.getItem("abi-campus")||"manhattan";}catch(e){return "manhattan";}
}
function setCampus(c){try{localStorage.setItem("abi-campus",c);}catch(e){}}

function swapPhones(data){
  // Utility bar
  var ubar=document.querySelector("[data-campus-phones]");
  if(ubar){
    ubar.innerHTML=data.ubar.map(function(p){
      var ico=(p.ico==="ES")?'<span class="ubar-ico" aria-hidden="true">ES</span>'
                            :'<span class="ubar-ico" aria-hidden="true">'+p.ico+'</span>';
      return '<a class="'+p.cls+'" href="tel:'+p.tel+'">'+ico+
             '<span class="ubar-tag">'+p.tag+'</span><span class="ubar-num">'+p.num+'</span></a>';
    }).join("");
  }
  // Mobile strip
  var strip=document.querySelector("[data-mstrip-phones]");
  if(strip){
    strip.innerHTML=data.mstrip.map(function(p){
      return '<a class="mstrip-phone" href="tel:'+p.tel+'">'+p.ico+
             '<span class="mstrip-t"><b>'+p.num+'</b><i>'+p.lab+'</i></span></a>';
    }).join("");
  }
  // Footer phones
  var ftr=document.querySelector("[data-footer-phones]");
  if(ftr){
    ftr.innerHTML=data.footer.map(function(p){
      return '<a href="tel:'+p.tel+'">'+p.text+'</a>';
    }).join("");
  }
  // Sticky mobile bar (if present)
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

function applyCampus(campus){
  swapPhones(DATA[campus]||MN);
  setCampusActive(campus);
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
      // close siblings
      items.forEach(function(o){ if(o!==item){var m=o.querySelector(".nav2-menu"),b=o.querySelector(".nav2-top");
        if(m)m.classList.remove("open"); if(b)b.setAttribute("aria-expanded","false");}});
    });
    btn.addEventListener("keydown",function(e){
      if(e.key==="Escape"){menu.classList.remove("open");btn.setAttribute("aria-expanded","false");}
    });
  });
  document.addEventListener("click",function(e){
    if(e.target.closest(".nav2-has")) return;
    items.forEach(function(o){var m=o.querySelector(".nav2-menu"),b=o.querySelector(".nav2-top");
      if(m)m.classList.remove("open"); if(b)b.setAttribute("aria-expanded","false");});
  });
}

// Programs-page detection helpers (per-campus routing)
function isProgramsPage(){var p=location.pathname;return /\/programs\//.test(p)||/\/programs$/.test(p);}
function isBronxProgramsPage(){var p=location.pathname;return /\/programs\/bronx(\.html)?$/.test(p)||/\/500-hour-master-barber-bronx/.test(p);}
function isManhattanProgramsPage(){var p=location.pathname;return /\/programs\/manhattan(\.html)?$/.test(p)||/\/programs\/500-hour-master-barber(\.html)?$/.test(p)||/\/50-hour-barber-refresher/.test(p);}

// Rewrite any generic "Programs" nav link to the campus-specific programs page.
// Runs on every campus apply + init so nav always matches the visitor's campus.
function rewriteProgramsLinks(campus){
  var target=campus==="bronx"?"bronx.html":"manhattan.html";
  var links=document.querySelectorAll('a[href]');
  links.forEach(function(a){
    var href=a.getAttribute("href")||"";
    var raw=href.split("?")[0].split("#")[0];
    // Match /programs, /programs/, /programs/index.html (absolute or relative)
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
  // Language segment: position glider from the active option, no logic needed.
  syncSeg(document.querySelector(".seg-lang"));

  // Programs pages set campus preference to match the page they're on.
  if(isBronxProgramsPage()){setCampus("bronx");}
  else if(isManhattanProgramsPage()){setCampus("manhattan");}

  // Campus segment.
  var seg=document.querySelector(".seg-campus");
  if(isFixedPage()){
    // Fixed context (Bronx / Haircuts): render the page's own numbers, lock switcher.
    setCampus(pageCampus()==="bronx"?"bronx":"manhattan");
    applyCampus(pageCampus());
    rewriteProgramsLinks(pageCampus());
  }else{
    var campus=getCampus();
    applyCampus(campus);
    rewriteProgramsLinks(campus);
    // Live switching on neutral/Manhattan pages.
    if(seg){
      seg.addEventListener("click",function(e){
        var opt=e.target.closest(".seg-opt");
        if(!opt) return;
        var to=opt.getAttribute("data-campus-opt");
        // On a /programs/* page, switching campus goes straight to the OTHER
        // campus's programs page instead of the campus home.
        var esPrefix=/\/es\//.test(location.pathname)?"/es":"";
        if(to==="bronx"){
          setCampus("bronx");
          if(isProgramsPage()){
            e.preventDefault();
            location.href=esPrefix+"/programs/bronx.html";
            return;
          }
          return; // let the link navigate to /bronx
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
