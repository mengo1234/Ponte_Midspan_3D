#!/usr/bin/env python3
"""HTML viewer v2 - molto più luminoso, con due STL FE nuove."""
import base64, os

BASE = "/var/home/fabio/Documenti/Claude/Ponte_Midspan_3D"


def b64(name):
    with open(os.path.join(BASE, name), "rb") as f:
        return base64.b64encode(f.read()).decode()


glb_exact_b64 = b64("local_midspan_repaired_FE_surface_100mm.glb")
glb_print_b64 = b64("local_midspan_repaired_FE_surface_100mm_print_repaired.glb")
stl_exact_b64 = b64("local_midspan_repaired_FE_surface_100mm.stl")
stl_print_b64 = b64("local_midspan_repaired_FE_surface_100mm_print_repaired.stl")

HTML = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Ponte Midspan 3D</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: linear-gradient(180deg, #9fb9d8 0%, #c4d5e8 58%, #e5edf7 100%);
    color: #1a2541;
    overflow: hidden; height: 100vh;
  }
  #header {
    position: fixed; top:0; left:0; right:0;
    padding: 14px 22px;
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0,0,0,0.06);
    z-index: 10;
    display: flex; justify-content: space-between; align-items: center;
  }
  #header h1 { font-size: 17px; font-weight: 700; }
  #header h1 .accent { color: #ff6b1a; }
  #header .stats { font-size: 12px; color: #5a6b86; }
  #viewer { width: 100vw; height: 100vh; cursor: grab; }
  #viewer:active { cursor: grabbing; }
  #loading {
    position: fixed; inset:0;
    display: flex; align-items:center; justify-content:center;
    background: rgba(232,240,250,0.95);
    z-index: 100; transition: opacity .4s;
  }
  #loading.hidden { opacity: 0; pointer-events: none; }
  #loading .spinner {
    width: 48px; height: 48px;
    border: 3px solid rgba(255,107,26,0.2);
    border-top-color: #ff6b1a;
    border-radius: 50%; animation: spin 0.9s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  #controls {
    position: fixed; bottom: 22px; left: 50%; transform: translateX(-50%);
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 16px;
    padding: 10px;
    display: flex; gap: 6px; align-items: center;
    z-index: 10; max-width: 96vw; flex-wrap: wrap; justify-content: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  }
  .btn {
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(0,0,0,0.08);
    color: #1a2541;
    padding: 9px 14px;
    border-radius: 10px; cursor: pointer;
    font-size: 13px; font-weight: 500;
    transition: all .15s;
    display: inline-flex; align-items: center; gap: 6px; user-select: none;
  }
  .btn:hover { background: white; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
  .btn.primary {
    background: linear-gradient(135deg, #ff6b1a 0%, #ff8c42 100%);
    border: none; color: white; font-weight: 600;
    box-shadow: 0 4px 14px rgba(255,107,26,0.35);
  }
  .btn.primary:hover { box-shadow: 0 6px 20px rgba(255,107,26,0.5); }
  .btn.active { background: #ff8c42; color: white; border-color: transparent; }
  #info {
    position: fixed; top: 64px; right: 14px;
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 12px; line-height: 1.7;
    color: #2a3957;
    z-index: 5; max-width: 250px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  }
  #info b { color: #ff6b1a; font-weight: 700; }
  #info .label { color: #5a6b86; }
  @media (max-width: 600px) {
    #header h1 { font-size: 13px; }
    #header .stats { display: none; }
    #info { display: none; }
    .btn { padding: 7px 10px; font-size: 11px; }
  }
</style>
</head>
<body>
<div id="header">
  <h1>Ponte Midspan <span class="accent">3D</span></h1>
  <div class="stats">Mesh FE estratta dal file · 10 cm · 2 STL</div>
</div>

<div id="info">
  <div><b id="model-title">FE esatta</b></div>
  <div><span class="label">Origine:</span> <span id="model-source">blocchi _NODE/_ELEM del file</span></div>
  <div><span class="label">Larghezza:</span> <span id="model-width">100 mm</span></div>
  <div><span class="label">Lunghezza:</span> <span id="model-length">65,6 mm</span></div>
  <div><span class="label">Altezza:</span> <span id="model-height">48,3 mm</span></div>
  <div><span class="label">Stato:</span> <span id="model-status">mesh FE non remeshata</span></div>
  <div><span class="label">Facce:</span> <span id="model-faces">313.806</span></div>
  <div style="margin-top:8px; font-size:11px; color:#7a8aa5;">Trascina = ruota · Scroll = zoom · Tasto destro = pan</div>
</div>

<div id="viewer"></div>

<div id="controls">
  <button class="btn active" data-model="exact">FE esatta</button>
  <button class="btn" data-model="print">Stampa</button>
  <button class="btn" id="rotate-btn">⟲ Ruota</button>
  <button class="btn" id="wire-btn">▦ Wireframe</button>
  <button class="btn" id="reset-btn">⟳ Reset</button>
  <button class="btn primary" data-download="exact">⬇ FE esatta</button>
  <button class="btn primary" data-download="print">⬇ Stampa STL</button>
</div>

<div id="loading"><div class="spinner"></div></div>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const MODELS = {
  exact: {
    title: 'FE esatta',
    source: 'blocchi _NODE/_ELEM del file',
    status: 'non watertight · mesh non remeshata',
    width: '100 mm',
    length: '65,6 mm',
    height: '48,3 mm',
    faces: '313.806',
    file: 'local_midspan_repaired_FE_surface_100mm.stl',
    color: 0x9aa4af,
    glb: "__GLB_EXACT_B64__",
    stl: "__STL_EXACT_B64__",
  },
  print: {
    title: 'Stampa watertight',
    source: 'FE esatta riparata per slicer',
    status: 'watertight · 1 componente · 0 bordi aperti',
    width: '100 mm',
    length: '65,5 mm',
    height: '47,5 mm',
    faces: '116.528',
    file: 'local_midspan_repaired_FE_surface_100mm_print_repaired.stl',
    color: 0xa6b4c2,
    glb: "__GLB_PRINT_B64__",
    stl: "__STL_PRINT_B64__",
  }
};

// === SCENE ===
const scene = new THREE.Scene();
// Sky gradient background
const canvasBg = document.createElement('canvas');
canvasBg.width = 2; canvasBg.height = 256;
const ctx = canvasBg.getContext('2d');
const grad = ctx.createLinearGradient(0, 0, 0, 256);
grad.addColorStop(0, '#6f99c5');
grad.addColorStop(0.55, '#aac2dc');
grad.addColorStop(1, '#dce7f2');
ctx.fillStyle = grad;
ctx.fillRect(0, 0, 2, 256);
const bgTex = new THREE.CanvasTexture(canvasBg);
bgTex.colorSpace = THREE.SRGBColorSpace;
scene.background = bgTex;

const w = window.innerWidth, h = window.innerHeight;
const camera = new THREE.PerspectiveCamera(40, w/h, 0.1, 500);
camera.position.set(35, -38, 18);
camera.up.set(0, 0, 1);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(w, h);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
document.getElementById('viewer').appendChild(renderer.domElement);

// PMREM env for nice reflections + ambient
const pmrem = new THREE.PMREMGenerator(renderer);
const envScene = new RoomEnvironment();
scene.environment = pmrem.fromScene(envScene, 0.04).texture;

// === LIGHTS ===
const hemi = new THREE.HemisphereLight(0xffffff, 0x7088a4, 1.0);
hemi.position.set(0, 0, 50);
scene.add(hemi);

const ambient = new THREE.AmbientLight(0xffffff, 0.25);
scene.add(ambient);

const sun = new THREE.DirectionalLight(0xfff4d6, 2.0);
sun.position.set(25, -18, 40);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 1;
sun.shadow.camera.far = 200;
sun.shadow.camera.left = -30;
sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30;
sun.shadow.camera.bottom = -30;
sun.shadow.bias = -0.0005;
scene.add(sun);

const fill = new THREE.DirectionalLight(0xc0d8f0, 0.9);
fill.position.set(-15, 25, 12);
scene.add(fill);

const rim = new THREE.DirectionalLight(0xffe4b3, 0.8);
rim.position.set(-20, -15, 8);
scene.add(rim);

const bottomFill = new THREE.DirectionalLight(0xe8f0ff, 0.25);
bottomFill.position.set(0, 0, -5);
scene.add(bottomFill);

// Ground
const groundGeo = new THREE.PlaneGeometry(120, 120);
const groundMat = new THREE.MeshStandardMaterial({
  color: 0xd4dcea, roughness: 0.95, metalness: 0
});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI/2;
ground.position.z = -12;
ground.receiveShadow = true;
scene.add(ground);

// === CONTROLS ===
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.8;
controls.target.set(0, 0, 0);
controls.minDistance = 8;
controls.maxDistance = 260;

// === LOAD GLB ===
function b64ToArrayBuffer(b64) {
  const bin = atob(b64);
  const len = bin.length;
  const buf = new Uint8Array(len);
  for (let i=0; i<len; i++) buf[i] = bin.charCodeAt(i);
  return buf.buffer;
}

const loader = new GLTFLoader();
let resetCamera = null;
let currentRoot = null;
let activeModel = 'exact';

function setLoading(visible) {
  const loading = document.getElementById('loading');
  loading.innerHTML = '<div class="spinner"></div>';
  loading.classList.toggle('hidden', !visible);
}

function disposeRoot(root) {
  root.traverse(o => {
    if (o.geometry) o.geometry.dispose();
    if (o.material) {
      const materials = Array.isArray(o.material) ? o.material : [o.material];
      materials.forEach(m => m.dispose());
    }
  });
}

function updateInfo(model) {
  document.getElementById('model-title').textContent = model.title;
  document.getElementById('model-source').textContent = model.source;
  document.getElementById('model-width').textContent = model.width;
  document.getElementById('model-length').textContent = model.length;
  document.getElementById('model-height').textContent = model.height;
  document.getElementById('model-status').textContent = model.status;
  document.getElementById('model-faces').textContent = model.faces;
}

function loadModel(key) {
  const model = MODELS[key];
  activeModel = key;
  setLoading(true);
  updateInfo(model);
  document.querySelectorAll('[data-model]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.model === key);
  });

  if (currentRoot) {
    scene.remove(currentRoot);
    disposeRoot(currentRoot);
    currentRoot = null;
  }

  const arrayBuffer = b64ToArrayBuffer(model.glb);
  loader.parse(arrayBuffer, '', (gltf) => {
    const root = gltf.scene;
    const box = new THREE.Box3().setFromObject(root);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());

    root.position.x -= center.x;
    root.position.y -= center.y;
    root.position.z -= box.min.z;

const concreteMat = new THREE.MeshLambertMaterial({
      color: model.color,
      side: THREE.DoubleSide,
      wireframe: wireframeOn,
    });
    const edgeMat = new THREE.LineBasicMaterial({
      color: 0x1f2d44,
      transparent: true,
      opacity: 0.42,
      depthTest: true,
    });

    root.traverse(o => {
      if (o.isMesh) {
        o.geometry.computeVertexNormals();
        o.material = concreteMat;
        o.castShadow = true;
        o.receiveShadow = true;
        const edges = new THREE.EdgesGeometry(o.geometry, 18);
        const edgeLines = new THREE.LineSegments(edges, edgeMat.clone());
        edgeLines.renderOrder = 2;
        o.add(edgeLines);
      }
    });

    scene.add(root);
    currentRoot = root;
    ground.position.z = -0.5;

    resetCamera = () => {
      const maxDim = Math.max(size.x, size.y, size.z);
      camera.position.set(maxDim*1.35, -maxDim*1.45, maxDim*0.75);
      controls.target.set(0, 0, size.z*0.28);
      controls.update();
    };
    resetCamera();

    setTimeout(() => setLoading(false), 200);
  }, undefined, (err) => {
    console.error('GLB load error', err);
    document.getElementById('loading').innerHTML = '<div style="color:#c0392b">Errore caricamento modello</div>';
  });
}

// === BUTTONS ===
document.querySelectorAll('[data-model]').forEach(btn => {
  btn.addEventListener('click', () => loadModel(btn.dataset.model));
});

document.getElementById('rotate-btn').addEventListener('click', (e) => {
  controls.autoRotate = !controls.autoRotate;
  e.target.classList.toggle('active', controls.autoRotate);
});

let wireframeOn = false;
document.getElementById('wire-btn').addEventListener('click', (e) => {
  wireframeOn = !wireframeOn;
  scene.traverse(o => {
    if (o.isMesh && o !== ground) o.material.wireframe = wireframeOn;
  });
  e.target.classList.toggle('active', wireframeOn);
});

document.getElementById('reset-btn').addEventListener('click', () => {
  if (resetCamera) resetCamera();
});

function downloadModel(key) {
  const model = MODELS[key];
  const buf = b64ToArrayBuffer(model.stl);
  const blob = new Blob([buf], { type: 'model/stl' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = model.file;
  document.body.appendChild(a); a.click();
  setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url); }, 100);
}

document.querySelectorAll('[data-download]').forEach(btn => {
  btn.addEventListener('click', () => downloadModel(btn.dataset.download));
});

loadModel(activeModel);

// === ANIMATE ===
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

// === RESIZE ===
window.addEventListener('resize', () => {
  const w = window.innerWidth, h = window.innerHeight;
  camera.aspect = w/h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
});
</script>
</body>
</html>
"""

html = (
    HTML.replace("__GLB_EXACT_B64__", glb_exact_b64)
    .replace("__GLB_PRINT_B64__", glb_print_b64)
    .replace("__STL_EXACT_B64__", stl_exact_b64)
    .replace("__STL_PRINT_B64__", stl_print_b64)
)
out = "/var/home/fabio/Documenti/Claude/Ponte_Midspan_3D/Ponte_Midspan_VIEWER.html"
with open(out, "w") as f:
    f.write(html)
print(f"HTML: {out} ({os.path.getsize(out)/1024/1024:.2f} MB)")
