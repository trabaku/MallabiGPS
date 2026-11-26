from pathlib import Path
import shutil
root=Path("MallabiGPS-integracion")
def replace(file,a,b):
    p=root/file
    s=p.read_text()
    assert s.count(a)==1, (file,a)
    p.write_text(s.replace(a,b))
replace("android/app/build.gradle.kts",'versionCode = 150; versionName = "1.0.6"','versionCode = 151; versionName = "1.0.7"')
replace("engine-mallabi/adapter.js","integraRotondas,planificaOSRM};","integraRotondas,planificaOSRM,fetchAlternatives};")
replace("engine-mallabi/tests/integration.test.cjs","app.indexOf('function drawingContext(')","app.indexOf('async function replan(')")
replace("scripts/construye.cjs","appMallabi.indexOf('function drawingContext(')","appMallabi.indexOf('async function replan(')")
replace("src/js/03-rutas.js","if(m!=='create'){cancelaMapaGps();","if(m!=='create'){if(typeof cancelaAlternativas==='function')cancelaAlternativas();cancelaMapaGps();")
replace("src/js/05-creador-tramos.js"," // 8% del recorrido total como escala vertical mínima: no amplificar\n // una cuesta suave para que parezca una pared.\n const verticalSpan=Math.max(35,creating?total*.08:0,(hMax-hMin)*1.18);"," // Escala por amplitud real de cotas, con margen y mínimo de 35 m.\n const verticalSpan=Math.max(35,(hMax-hMin)*1.18);")
replace("src/js/05-creador-tramos.js","info.textContent=(grade>0.5?","info.textContent='Último tramo · '+(grade>0.5?")
replace("src/js/05-creador-tramos.js","if(mode!=='create')return;\n if(!redGps){notice('Preparando red de caminos…');return}","if(mode!=='create')return;\n if(typeof capturaAlternativas==='function'&&capturaAlternativas(e))return;\n if(!redGps){notice('Preparando red de caminos…');return}")
css="""#creadorModo{display:none}body.creating-route #creadorModo{display:flex;gap:4px;position:absolute;z-index:1001;bottom:calc(var(--create-profile-height,145px) + 72px);left:50%;transform:translateX(-50%);background:#102632;padding:4px;border-radius:12px;white-space:nowrap}#creadorModo button{font-size:12px;min-height:44px;padding:6px 10px;border-radius:9px}#creadorModo button[aria-pressed=true]{background:#7ce4e6;color:#102632}#alternativasPanel{position:absolute;z-index:1002;left:10px;right:10px;bottom:12px;max-height:48%;overflow:auto;background:#102632f5;border:1px solid #4a7580;border-radius:18px;padding:12px;color:#f1f8fa;box-shadow:0 5px 24px #0008}#alternativasPanel.hidden,#alternativasLista.hidden{display:none}#alternativasPanel header{display:flex;align-items:center;justify-content:space-between;gap:8px}#alternativasLista{display:grid;gap:7px;margin-top:8px}.alternativa{display:grid;text-align:left;gap:4px;border-left:5px solid;background:#183642;border-radius:12px;padding:10px;color:#f1f8fa}.alternativa small{font-size:12px;color:#c5e5eb}body:not(.creating-route) #alternativasPanel{display:none}"""
replace("src/nuevo.plantilla.html","</style></head><body><div id=\"app\">",css+"\n</style></head><body><div id=\"app\">")
ui="""<div id="creadorModo"><button type="button" id="modoManual" aria-pressed="true">Punto a punto</button><button type="button" id="modoDosPuntos" aria-pressed="false">Inicio y destino</button></div><section id="alternativasPanel" class="hidden"><header><b>Elige tu recorrido</b><button type="button" id="alternativasCerrar" aria-label="Volver a punto a punto">✕</button></header><label>Actividad <select id="alternativasActividad"><option value="bike">BTT / e-bike</option><option value="foot">A pie</option><option value="car">Coche</option></select></label><p id="alternativasEstado" role="status"></p><div id="alternativasLista" class="hidden"></div></section>"""
replace("src/nuevo.plantilla.html",'<div id="mapRot"></div><div class="tools">','<div id="mapRot"></div>'+ui+'<div class="tools">')
shutil.copyfile("parches/1.0.7/11-alternativas.js",root/"src/js/11-alternativas.js")
p=root/"instalar.html"
p.write_text(p.read_text().replace("MallabiGPS 1.0.6 — versión candidata","MallabiGPS 1.0.7 — versión candidata"))

# Integrar selector y panel en un unico bloque inferior, sin tapar el centro.
p=root/"src/nuevo.plantilla.html"
s=p.read_text()
old='<div id="creadorModo">'
assert s.count(old)==1
s=s.replace(old,'<div id="creadorDock"><div id="creadorModo">',1)
s=s.replace('</div></section><div class="tools">','</div></section></div><div class="tools">',1)
dockcss="""#creadorDock{display:none}body.creating-route #creadorDock{display:flex;flex-direction:column;gap:6px;position:absolute;z-index:1002;left:10px;right:10px;bottom:calc(var(--create-profile-height,145px) + 8px);padding:7px;background:#102632f5;border:1px solid #4a7580;border-radius:16px;box-shadow:0 5px 20px #0006;color:#f1f8fa}body.creating-route #creadorDock:has(#alternativasPanel:not(.hidden)){bottom:12px}body.creating-route #creadorModo{position:static;transform:none;display:flex;gap:6px;padding:0;background:none;white-space:normal}#creadorModo button{flex:1;min-width:0;background:#162e3b;color:#d6eef2;border:1px solid #41616e;font-weight:650}#creadorModo button[aria-pressed=true]{background:#173c46;color:#8cecef;border-color:#75dce0;box-shadow:inset 0 -2px #75dce0}#alternativasPanel{position:static;max-height:32vh;padding:4px 5px 2px;border:0;border-radius:0;box-shadow:none;background:none}#alternativasPanel header{font-size:14px;margin:0 0 5px}#alternativasCerrar{min-width:44px;min-height:44px;color:#d6eef2;background:#183642;border:1px solid #41616e;border-radius:10px}#alternativasPanel label{display:flex;align-items:center;gap:8px;font-size:13px}#alternativasActividad{flex:1;min-height:44px;background:#183642;color:#e7f6f8;border:1px solid #41616e;border-radius:9px;padding:4px 8px;font:inherit;color-scheme:dark}#alternativasEstado{font-size:14px;margin:7px 0 2px;color:#bde5e8}#alternativasLista{margin-top:5px;gap:5px}.alternativa{padding:7px 10px;min-height:44px}"""
s=s.replace("</style></head><body>",dockcss+"</style></head><body>",1)
p.write_text(s)
