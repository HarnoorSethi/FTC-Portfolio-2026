import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import FIN from './finish.json';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';
const W = 2400, H = 1800;
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.setClearColor(0x000000, 0);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05; renderer.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene();
const pm = new THREE.PMREMGenerator(renderer);
scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.9;
const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(2, 3, 2.2); scene.add(key);
const fill = new THREE.DirectionalLight(0xdfe9ff, 0.6); fill.position.set(-2, 1.2, -1.5); scene.add(fill);
scene.add(new THREE.HemisphereLight(0xffffff, 0x8899aa, 0.35));
const camera = new THREE.PerspectiveCamera(24, W / H, 0.01, 50);
await MeshoptDecoder.ready;
const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
const FILES = { base: 'model.glb', turret: 'model_0.glb', hood: 'model_1.glb', intakeFront: 'model_2.glb', intakeBack: 'model_3.glb', flowerSlide: 'model_4.glb', flowerRamp: 'model_5.glb' };

const finish = (o) => {
  // same finishes as the sim's current robot (tools/robot/finishes.mjs), chosen by colour then part name
  const nm = (o.name || '') + ' ' + (o.parent?.name || '');
  const c0 = o.material.color; const lum = 0.3 * c0.r + 0.59 * c0.g + 0.11 * c0.b;
  let key = FIN.map[o.material.name] ?? (lum < 0.03 ? 'anodised' : lum < 0.12 ? 'plastic' : 'aluminium');
  if (/Mecanum/.test(nm)) key = key === 'yellow' ? 'yellow' : (lum < 0.1 ? 'rubber' : 'aluminium');
  else if (/Gecko Wheel/.test(nm)) key = key === 'plastic' ? 'plastic' : 'gecko';
  else if (/Belt|Bellypan|Omni Wheel/.test(nm)) key = 'rubber';
  else if (/Cable Carrier/.test(nm)) key = 'plastic';
  const f = FIN.fin[key];
  return new THREE.MeshStandardMaterial({ color: new THREE.Color(f.color), metalness: f.metal, roughness: f.rough });
};
const root = new THREE.Group(); root.rotation.x = -Math.PI / 2; scene.add(root);
const parts = {};
for (const [id, f] of Object.entries(FILES)) {
  const buf = await (await fetch('/robot/' + f)).arrayBuffer();
  const gltf = await new Promise((res, rej) => loader.parse(buf, '', res, rej));
  const g = new THREE.Group(); g.name = id; g.add(gltf.scene); root.add(g); parts[id] = g;
  g.traverse((o) => { if (o.isMesh) { o.material = finish(o); } });
}
root.updateMatrixWorld(true);
const bounds = (ids) => { const b = new THREE.Box3(); ids.forEach((i) => b.expandByObject(parts[i])); const s = b.getBoundingSphere(new THREE.Sphere()); return [s.center.x, s.center.y, s.center.z, s.radius]; };
const NAVY = new THREE.Color(0x24365e); const DARK = new THREE.Color(0x232a3a);
const posePart = (g, m) => { g.matrixAutoUpdate = false; g.matrix.copy(m); g.updateMatrixWorld(true); };
const applyFlower = (t) => {
  const ax = new THREE.Vector3(0.999391, 0, 0.034899).normalize();
  const slide = new THREE.Matrix4().makeTranslation(ax.x * 0.06 * t, ax.y * 0.06 * t, ax.z * 0.06 * t);
  const p = new THREE.Vector3(0.143368, -0.095825, 0.035567).add(ax.clone().multiplyScalar(0.06 * t));
  const rot = new THREE.Matrix4().makeRotationAxis(new THREE.Vector3(0, -1, 0), THREE.MathUtils.degToRad(-33.95 * t));
  const about = new THREE.Matrix4().makeTranslation(p.x, p.y, p.z).multiply(rot).multiply(new THREE.Matrix4().makeTranslation(-p.x, -p.y, -p.z));
  posePart(parts.flowerSlide, slide);
  posePart(parts.flowerRamp, about.multiply(slide));
};
const focus = (ids, ghost) => { for (const [id, g] of Object.entries(parts)) { const on = ids.includes(id); g.visible = on || ghost > 0; g.traverse((o) => { if (o.isMesh) { if (!o.userData.m0) o.userData.m0 = o.material.clone(); const m0 = o.userData.m0; o.material.copy(m0); o.material.transparent = !on; o.material.opacity = on ? 1 : ghost; o.material.depthWrite = on; if (!on) o.material.color.lerp(NAVY, 0.7); } }); } };
window.ready = true;
window.bounds = bounds;
window.shot = (s) => {
  applyFlower(s.flower ?? 0);
  focus(s.focus || Object.keys(parts), s.ghost ?? 0.12);
  const c = new THREE.Vector3(...s.center), r = s.radius;
  const az = THREE.MathUtils.degToRad(s.az), el = THREE.MathUtils.degToRad(s.el);
  const d = new THREE.Vector3(Math.cos(el) * Math.cos(az), Math.sin(el), -Math.cos(el) * Math.sin(az));
  const fov = THREE.MathUtils.degToRad(camera.fov);
  const dist = r / Math.sin(Math.min(fov, fov * camera.aspect) / 2);
  camera.position.copy(c).addScaledVector(d, dist); camera.lookAt(c); camera.updateProjectionMatrix();
  renderer.render(scene, camera);
  return canvas.toDataURL('image/png');
};
window.shotAuto = async (spec) => {
  const s = { ...spec };
  applyFlower(s.flower ?? 0);
  const ids = s.boundsOf || Object.keys(parts);
  const b = bounds(ids); s.center = b.slice(0, 3); s.radius = b[3] * (s.pad || 1.02);
  return window.shot(s);
};
