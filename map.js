(function(){
  if(!window.L || !window.DIR) return;
  var D=window.DIR, U=D.ui, qs=new URLSearchParams(location.search);
  var map=L.map('map',{scrollWheelZoom:false}).setView([26.4,127.9],9);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'© OpenStreetMap contributors'}).addTo(map);
  var layer=L.layerGroup().addTo(map), sel=document.getElementById('m-art'), cnt=document.getElementById('m-count'), me=null, meMarker=null;
  var colors={A:'#17695f',B:'#b9770e',C:'#6b7385',D:'#9b2c2c'};
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  var focus=qs.get('id'), focusMarker=null;
  function draw(){
    layer.clearLayers(); var art=sel.value, n=0, pts=[];
    D.locations.forEach(function(x){
      if(x.la==null || x.k==='organization') return;
      if(art && x.d.indexOf(art)<0) return;
      var m=L.circleMarker([x.la,x.lo],{radius:7,color:'#fff',weight:1.5,fillColor:colors[x.v],fillOpacity:.9});
      m.bindPopup('<b><a href="'+D.base+D.pfx+'/l/'+x.id+'/">'+esc(x.n)+'</a></b><br>'+esc(D.verif[x.v][0])+'<br>'+esc(x.a||''));
      m.addTo(layer); n++; pts.push([x.la,x.lo]);
      if(x.id===focus) focusMarker=m;
    });
    cnt.textContent=n+' '+(n===1?U.place:U.places);
    return pts;
  }
  if(qs.get('art')) sel.value=qs.get('art');
  var pts=draw();
  if(focusMarker){ map.setView(focusMarker.getLatLng(),15); focusMarker.openPopup(); }
  else if(pts.length) map.fitBounds(pts,{padding:[30,30]});
  sel.addEventListener('change',function(){ var p=draw(); if(p.length) map.fitBounds(p,{padding:[30,30]}); });
  document.getElementById('m-near').addEventListener('click',function(){
    if(!navigator.geolocation){ cnt.textContent=U.denied; return; }
    navigator.geolocation.getCurrentPosition(function(p){
      me=[p.coords.latitude,p.coords.longitude]; if(meMarker) map.removeLayer(meMarker);
      meMarker=L.circleMarker(me,{radius:9,color:'#1f2f5a',fillColor:'#4e7cff',fillOpacity:.9}).addTo(map); map.setView(me,13);
    },function(){ cnt.textContent=U.denied; },{timeout:10000});
  });
})();
