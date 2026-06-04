import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const cameraVideo = document.querySelector("#camera");
const sceneCanvas = document.querySelector("#scene");
const scanCanvas = document.querySelector("#scan");
const statusText = document.querySelector("#statusText");
const signal = document.querySelector("#signal");
const cameraButton = document.querySelector("#cameraButton");
const scanButton = document.querySelector("#scanButton");
const placeButton = document.querySelector("#placeButton");
const modelPicker = document.querySelector("#modelPicker");

const state = {
  hand: null,
  cameraOn: false,
  scanning: false,
  lastScanAt: 0,
  target: new THREE.Vector3(0, -0.08, -1.35),
  foundAt: null
};

const renderer = new THREE.WebGLRenderer({
  canvas: sceneCanvas,
  alpha: true,
  antialias: true
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(58, 1, 0.01, 100);
camera.position.set(0, 0, 0);

const keyLight = new THREE.DirectionalLight(0xfff2d1, 2.6);
keyLight.position.set(0.8, 1.5, 1.2);
scene.add(keyLight);
scene.add(new THREE.HemisphereLight(0xb8ffe0, 0x40352d, 1.5));

const runeRing = makeRuneRing();
scene.add(runeRing);

function setStatus(text, ready = false) {
  statusText.textContent = text;
  signal.classList.toggle("ready", ready);
}

function makeRuneRing() {
  const group = new THREE.Group();
  const ring = new THREE.Mesh(
    new THREE.TorusGeometry(0.16, 0.005, 10, 72),
    new THREE.MeshBasicMaterial({ color: 0x89ffc5, transparent: true, opacity: 0.82 })
  );
  const mark = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.035, 0),
    new THREE.MeshBasicMaterial({ color: 0xffcf6a, transparent: true, opacity: 0.94 })
  );
  mark.position.y = 0.16;
  group.add(ring, mark);
  group.visible = false;
  group.position.copy(state.target);
  return group;
}

function makeFallbackHand() {
  const group = new THREE.Group();
  const material = new THREE.MeshStandardMaterial({
    color: 0xd7a47b,
    roughness: 0.62,
    metalness: 0.04
  });

  const palm = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.28, 0.08), material);
  palm.position.y = -0.04;
  group.add(palm);

  for (let i = 0; i < 5; i += 1) {
    const finger = new THREE.Mesh(new THREE.CapsuleGeometry(0.022, i === 0 ? 0.16 : 0.22, 8, 14), material);
    finger.rotation.z = i === 0 ? 0.92 : 0;
    finger.position.set(-0.088 + i * 0.044, i === 0 ? 0.02 : 0.15, 0.005);
    group.add(finger);
  }

  group.scale.setScalar(1.25);
  return group;
}

function prepareHand(object) {
  const box = new THREE.Box3().setFromObject(object);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const maxSide = Math.max(size.x, size.y, size.z) || 1;

  object.position.sub(center);
  object.scale.multiplyScalar(0.44 / maxSide);
  object.rotation.set(-0.42, 0.24, -0.16);

  const holder = new THREE.Group();
  holder.add(object);
  holder.position.copy(state.target);
  holder.visible = false;
  scene.add(holder);
  state.hand = holder;
}

async function loadModel(url) {
  const loader = new GLTFLoader();
  const gltf = await loader.loadAsync(url);
  if (state.hand) {
    scene.remove(state.hand);
  }
  prepareHand(gltf.scene);
  state.hand.visible = true;
  setStatus("Hand geladen", true);
}

async function loadDefaultHand() {
  try {
    await loadModel("./models/hand.glb");
  } catch {
    prepareHand(makeFallbackHand());
    setStatus("Plaats hand.glb in DP12/models", false);
  }
}

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: "environment" }, width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false
    });
    cameraVideo.srcObject = stream;
    await cameraVideo.play();
    state.cameraOn = true;
    scanButton.disabled = false;
    placeButton.disabled = false;
    cameraButton.textContent = "Camera aan";
    cameraButton.disabled = true;
    setStatus("Camera actief", true);
  } catch (error) {
    setStatus("Camera toegang geweigerd", false);
    console.error(error);
  }
}

function screenToWorld(x, y) {
  const rect = sceneCanvas.getBoundingClientRect();
  const ndc = new THREE.Vector2(
    ((x - rect.left) / rect.width) * 2 - 1,
    -(((y - rect.top) / rect.height) * 2 - 1)
  );
  const world = new THREE.Vector3(ndc.x, ndc.y, -1).unproject(camera);
  return world.normalize().multiplyScalar(1.35);
}

function placeHandAt(x, y) {
  state.target.copy(screenToWorld(x, y));
  state.foundAt = performance.now();
  runeRing.visible = true;
  if (state.hand) {
    state.hand.visible = true;
  }
  setStatus("Rune gevonden", true);
}

function scanForRune(now) {
  if (!state.scanning || !state.cameraOn || now - state.lastScanAt < 520) {
    return;
  }

  state.lastScanAt = now;
  const ctx = scanCanvas.getContext("2d", { willReadFrequently: true });
  ctx.drawImage(cameraVideo, 0, 0, scanCanvas.width, scanCanvas.height);
  const { data, width, height } = ctx.getImageData(0, 0, scanCanvas.width, scanCanvas.height);

  let totalX = 0;
  let totalY = 0;
  let hits = 0;

  for (let y = 4; y < height - 4; y += 2) {
    for (let x = 4; x < width - 4; x += 2) {
      const i = (y * width + x) * 4;
      const left = (y * width + x - 3) * 4;
      const right = (y * width + x + 3) * 4;
      const up = ((y - 3) * width + x) * 4;
      const down = ((y + 3) * width + x) * 4;
      const light = data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114;
      const contrast =
        Math.abs(light - (data[left] * 0.299 + data[left + 1] * 0.587 + data[left + 2] * 0.114)) +
        Math.abs(light - (data[right] * 0.299 + data[right + 1] * 0.587 + data[right + 2] * 0.114)) +
        Math.abs(light - (data[up] * 0.299 + data[up + 1] * 0.587 + data[up + 2] * 0.114)) +
        Math.abs(light - (data[down] * 0.299 + data[down + 1] * 0.587 + data[down + 2] * 0.114));

      if (contrast > 260 && light < 168) {
        totalX += x;
        totalY += y;
        hits += 1;
      }
    }
  }

  if (hits > 16) {
    const rect = sceneCanvas.getBoundingClientRect();
    const x = rect.left + (totalX / hits / width) * rect.width;
    const y = rect.top + (totalY / hits / height) * rect.height;
    placeHandAt(x, y);
  } else {
    setStatus("Runes zoeken...", true);
  }
}

function resize() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function animate(now = 0) {
  requestAnimationFrame(animate);
  scanForRune(now);

  const pulse = 1 + Math.sin(now * 0.006) * 0.04;
  runeRing.scale.setScalar(pulse);
  runeRing.rotation.z += 0.012;
  runeRing.position.lerp(state.target, 0.12);

  if (state.hand) {
    state.hand.position.lerp(state.target, 0.08);
    state.hand.rotation.y += 0.004;
    state.hand.visible = Boolean(state.foundAt) || !state.cameraOn;
  }

  renderer.render(scene, camera);
}

cameraButton.addEventListener("click", startCamera);

scanButton.addEventListener("click", () => {
  state.scanning = !state.scanning;
  scanButton.textContent = state.scanning ? "Stop zoeken" : "Zoek runes";
  setStatus(state.scanning ? "Runes zoeken..." : "Scanner uit", true);
});

placeButton.addEventListener("click", () => {
  const rect = sceneCanvas.getBoundingClientRect();
  placeHandAt(rect.left + rect.width / 2, rect.top + rect.height / 2);
});

sceneCanvas.addEventListener("pointerdown", (event) => {
  if (state.cameraOn) {
    placeHandAt(event.clientX, event.clientY);
  }
});

modelPicker.addEventListener("change", async () => {
  const [file] = modelPicker.files;
  if (!file) {
    return;
  }
  const url = URL.createObjectURL(file);
  try {
    await loadModel(url);
  } finally {
    URL.revokeObjectURL(url);
  }
});

scanButton.disabled = true;
placeButton.disabled = true;
window.addEventListener("resize", resize);
resize();
loadDefaultHand();
animate();
