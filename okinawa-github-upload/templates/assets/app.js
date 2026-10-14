(function(){
  // Art switcher (dropdown) — navigates to the chosen art's page
  document.querySelectorAll('select[data-nav]').forEach(function(s){
    s.addEventListener('change',function(){ if(s.value) location.href=s.value; });
  });
  // Close the Arts menu when clicking elsewhere
  document.addEventListener('click',function(e){
    document.querySelectorAll('nav.main details[open]').forEach(function(d){ if(!d.contains(e.target)) d.removeAttribute('open'); });
  });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') document.querySelectorAll('nav.main details[open]').forEach(function(d){d.removeAttribute('open');}); });

  // Home search -> /find/
  var hs=document.getElementById('home-search');
  if(hs){ hs.addEventListener('submit',function(e){ e.preventDefault(); var f=new FormData(hs), p=new URLSearchParams();
      ['q','art','area'].forEach(function(k){ if(f.get(k)) p.set(k,f.get(k)); });
      location.href=hs.getAttribute('action')+(p.toString()?'?'+p.toString():''); }); }

  // Find page
  var root=document.getElementById('find-app'); if(!root || !window.DIR) return;
  var D=window.DIR, L=D.locations, U=D.ui;
  var norm=function(s){ return (s||'').normalize('NFKC').toLowerCase(); };
  L.forEach(function(x){ x._t=norm([x.n,x.j,x.ne,x.a,x.aj,x.c,x.s,x.al,x.m_en].join(' ')); });
  var el={q:document.getElementById('f-q'),art:document.getElementById('f-art'),area:document.getElementById('f-area'),
          ver:document.getElementById('f-ver'),eng:document.getElementById('f-eng'),org:document.getElementById('f-org'),
          out:document.getElementById('f-out'),cnt:document.getElementById('f-count'),rst:document.getElementById('f-reset'),
          more:document.getElementById('f-more'),near:document.getElementById('f-near'),msg:document.getElementById('f-msg')};
  var qs=new URLSearchParams(location.search);
  ['q','art','area','ver'].forEach(function(k){ if(qs.get(k)&&el[k]) el[k].value=qs.get(k); });
  var PAGE=40, shown=PAGE, me=null;
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function dist(a,b,c,d){ var R=6371,t=Math.PI/180,dl=(c-a)*t,dn=(d-b)*t,h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a*t)*Math.cos(c*t)*Math.sin(dn/2)*Math.sin(dn/2); return 2*R*Math.asin(Math.sqrt(h)); }
  function card(x){
    var h='<article class="card"><div class="pill-row"><span class="badge '+x.v+'" title="'+esc(D.verif[x.v][1])+'">'+esc(D.verif[x.v][0])+'</span>';
    if(x.k==='organization') h+='<span class="chip">'+esc(U.org)+'</span>';
    x.d.forEach(function(d){ h+='<span class="chip">'+esc(D.disc[d])+'</span>'; });
    h+='</div><h3><a href="'+D.base+D.pfx+'/l/'+x.id+'/">'+esc(x.n)+'</a></h3>';
    if(x.j) h+='<div class="ja">'+esc(x.j)+'</div>';
    h+='<div class="meta"><span>📍 '+esc(x.a||x.m_en||U.noloc)+'</span>';
    if(x._km!=null) h+='<span><b>'+x._km.toFixed(1)+' '+U.km+'</b></span>';
    if(x.p) h+='<a href="tel:'+esc(x.p.replace(/[^0-9+]/g,''))+'">☎ '+esc(x.p)+'</a>';
    if(x.w) h+='<a href="'+esc(x.w)+'" rel="noopener nofollow">'+U.website+'</a>';
    h+='</div></article>'; return h;
  }
  function run(reset){
    if(reset) shown=PAGE;
    var q=norm(el.q.value).trim(), art=el.art.value, area=el.area.value, ver=el.ver.value, eng=el.eng.checked, org=el.org.checked;
    var terms=q?q.split(/\s+/):[];
    var res=L.filter(function(x){
      if(art && x.d.indexOf(art)<0) return false;
      if(area && x.m!==area) return false;
      if(ver && ver.indexOf(x.v)<0) return false;
      if(eng && !x.e) return false;
      if(!org && x.k==='organization') return false;
      for(var i=0;i<terms.length;i++){ if(x._t.indexOf(terms[i])<0) return false; }
      return true; });
    res.forEach(function(x){ x._km=(me&&x.la!=null)? dist(me[0],me[1],x.la,x.lo):null; });
    if(me) res.sort(function(a,b){ var A=a._km==null?1e9:a._km, B=b._km==null?1e9:b._km; return A-B || a.v.localeCompare(b.v); });
    else res.sort(function(a,b){ return a.v.localeCompare(b.v) || a.n.localeCompare(b.n); });
    el.cnt.textContent=res.length+' '+(res.length===1?U.place:U.places);
    el.out.innerHTML=res.length? res.slice(0,shown).map(card).join('') : '<div class="empty">'+esc(U.none)+'</div>';
    el.more.hidden = res.length<=shown;
    var p=new URLSearchParams(); if(el.q.value)p.set('q',el.q.value); if(art)p.set('art',art); if(area)p.set('area',area); if(ver)p.set('ver',ver); if(eng)p.set('eng','1');
    try{ history.replaceState(null,'',location.pathname+(p.toString()?'?'+p.toString():'')); }catch(e){}
  }
  ['q','art','area','ver'].forEach(function(k){ el[k].addEventListener('input',function(){run(true);}); });
  el.eng.addEventListener('change',function(){run(true);}); el.org.addEventListener('change',function(){run(true);});
  el.rst.addEventListener('click',function(){ el.q.value='';el.art.value='';el.area.value='';el.ver.value='';el.eng.checked=false;el.org.checked=false;me=null;el.msg.textContent='';run(true); });
  el.more.addEventListener('click',function(){ shown+=PAGE; run(false); });
  el.near.addEventListener('click',function(){
    if(!navigator.geolocation){ el.msg.textContent=U.denied; return; }
    el.msg.textContent=U.locating;
    navigator.geolocation.getCurrentPosition(function(p){ me=[p.coords.latitude,p.coords.longitude];
      el.msg.textContent=L.some(function(x){return x.la!=null;})?'':U.nocoord; run(true); },
      function(){ el.msg.textContent=U.denied; }, {timeout:10000});
  });
  if(qs.get('eng')==='1') el.eng.checked=true;
  run(true);
})();
