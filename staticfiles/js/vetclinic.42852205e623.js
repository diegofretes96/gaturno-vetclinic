'use strict';
const sb=document.getElementById('sidebar'),mb=document.getElementById('menuToggle');
if(mb){mb.addEventListener('click',()=>sb.classList.toggle('open'));document.addEventListener('click',e=>{if(sb&&mb&&!sb.contains(e.target)&&!mb.contains(e.target))sb.classList.remove('open')})}
// Tabs
document.querySelectorAll('.ptab').forEach(t=>{t.addEventListener('click',function(){const parent=this.closest('[data-tabs]')||this.closest('.panel')||document;parent.querySelectorAll('.ptab').forEach(x=>x.classList.remove('active'));parent.querySelectorAll('.tab-pane').forEach(x=>x.classList.remove('active'));this.classList.add('active');const pane=document.getElementById('tp-'+this.dataset.tab);if(pane)pane.classList.add('active')})});
// Search
const si=document.getElementById('globalSearch'),sd=document.getElementById('srchDrop');
let _st;if(si&&sd){si.addEventListener('input',function(){clearTimeout(_st);const q=this.value.trim();if(q.length<2){sd.classList.add('d-none');return}_st=setTimeout(()=>{fetch('/pacientes/buscar/?q='+encodeURIComponent(q)).then(r=>r.json()).then(d=>{if(!d.results.length){sd.classList.add('d-none');return}sd.innerHTML=d.results.map(r=>'<a href="'+r.url+'" class="srch-item"><span class="si-nm">'+r.nombre+'</span><span class="si-dt">'+r.especie+' · '+r.propietario+'</span></a>').join('');sd.classList.remove('d-none')}).catch(()=>sd.classList.add('d-none'))},300)});document.addEventListener('click',e=>{if(si&&!si.contains(e.target))sd.classList.add('d-none')})}
// Alerts auto-close
document.querySelectorAll('.vc-alert').forEach(el=>{setTimeout(()=>{el.style.transition='opacity .4s';el.style.opacity='0';setTimeout(()=>el.remove(),400)},5000)});
// Confirm
document.querySelectorAll('[data-confirm]').forEach(el=>{el.addEventListener('click',function(e){if(!confirm(this.dataset.confirm||'¿Estás seguro?'))e.preventDefault()})});
// Print
document.querySelectorAll('.btn-print').forEach(b=>b.addEventListener('click',()=>window.print()));
// Raza cascade
const esp=document.getElementById('id_especie'),raz=document.getElementById('id_raza');
if(esp&&raz){esp.addEventListener('change',function(){raz.innerHTML='<option value="">---------</option>';if(!this.value)return;fetch('/pacientes/razas/?especie_id='+this.value).then(r=>r.json()).then(d=>{d.razas.forEach(r=>{const o=document.createElement('option');o.value=r.id;o.textContent=r.nombre;raz.appendChild(o)})})})}
setInterval(()=>{fetch('/agenda/sala-espera/count/').then(r=>r.json()).then(d=>{document.querySelectorAll('.sala-ct').forEach(el=>el.textContent=d.count)}).catch(()=>{})},60000);
