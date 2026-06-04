import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const state = {
  ready: false,
  renderer: null,
  scene: null,
  camera: null,
  hand: null,
  handRoot: null,
  handGlow: null,
  runeGroups: [],
  canvas: null,
  area: null,
  lastTarget: null,
  sweep: 0
};

const horizontalFov = 72;
const verticalFov = 48;

window.Nevermore3D = {
  init,
  update,
  flashRune
};

function init() {
  if (state.ready) {
    return;
  }

  state.canvas = document.getElementById("threeScene");
  state.area = document.querySelector(".camera-area");

  if (!state.canvas || !state.area) {
    return;
  }

  state.scene = new THREE.Scene();
  state.camera = new THREE.PerspectiveCamera(52, 1, 0.1, 100);
  state.camera.position.set(0, 0.2, 6);

  state.renderer = new THREE.WebGLRenderer({
    canvas: state.canvas,
    alpha: true,
    antialias: true
  });
  state.renderer.setClearColor(0x000000, 0);
  state.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  addLights();
  buildHandAnchor();
  buildRuneMeshes();
  loadHandModel();
  resize();

  window.addEventListener("resize", resize);
  state.ready = true;
  animate();
}

function addLights() {
  const ambient = new THREE.HemisphereLight(0xd7c5ff, 0x080611, 1.7);
  const key = new THREE.DirectionalLight(0xffffff, 2.4);
  const fill = new THREE.PointLight(0x9d20ff, 13, 12);

  key.position.set(2.4, 3, 4.8);
  fill.position.set(-2.8, 0.8, 3.4);

  state.scene.add(ambient, key, fill);
}

function buildHandAnchor() {
  state.handRoot = new THREE.Group();
  state.handRoot.position.set(0.25, -1.0, 1.52);
  state.handRoot.rotation.set(-0.34, -0.12, 0.06);
  state.handRoot.scale.setScalar(0.68);

  state.handGlow = new THREE.Sprite(
    new THREE.SpriteMaterial({
      map: makeGlowTexture(0xd6b4ff),
      color: 0xd6b4ff,
      transparent: true,
      opacity: 0.18,
      depthWrite: false
    })
  );
  state.handGlow.position.set(0, 0.35, -0.25);
  state.handGlow.scale.set(1.3, 1.3, 1);
  state.handRoot.add(state.handGlow);
  state.scene.add(state.handRoot);
}

function loadHandModel() {
  const loader = new GLTFLoader();

  loader.load(
    "models/hand_wednesday_addams.glb",
    gltf => {
      state.hand = gltf.scene;
      state.hand.traverse(child => {
        if (child.isMesh) {
          child.castShadow = false;
          child.receiveShadow = false;
          child.material = child.material.clone();
          child.material.emissive = new THREE.Color(0x12051f);
          child.material.emissiveIntensity = 0.14;
        }
      });

      state.hand.rotation.set(-0.85, 0.2, -0.22);
      state.hand.scale.setScalar(1);
      centerModel(state.hand);
      state.handRoot.add(state.hand);
    },
    undefined,
    () => {
      state.handRoot.add(makeFallbackHand());
    }
  );
}

function centerModel(model) {
  const box = new THREE.Box3().setFromObject(model);
  const size = new THREE.Vector3();
  const center = new THREE.Vector3();

  box.getSize(size);
  box.getCenter(center);
  model.position.sub(center);

  const biggest = Math.max(size.x, size.y, size.z) || 1;
  model.scale.multiplyScalar(1.8 / biggest);
}

function makeFallbackHand() {
  const group = new THREE.Group();
  const palm = new THREE.Mesh(
    new THREE.SphereGeometry(0.42, 24, 16),
    new THREE.MeshStandardMaterial({ color: 0xd9c2af, roughness: 0.7 })
  );
  palm.scale.set(1, 0.72, 1.25);
  group.add(palm);

  for (let i = 0; i < 5; i++) {
    const finger = new THREE.Mesh(
      new THREE.CapsuleGeometry(0.085, 0.7, 8, 16),
      new THREE.MeshStandardMaterial({ color: 0xe2c8b6, roughness: 0.65 })
    );
    finger.position.set((i - 2) * 0.16, 0.42, -0.05 + Math.abs(i - 2) * 0.035);
    finger.rotation.z = (i - 2) * -0.12;
    group.add(finger);
  }

  return group;
}

function buildRuneMeshes() {
  ["NOCTIS", "VISIO", "UMBRA"].forEach((name, index) => {
    const group = new THREE.Group();
    const color = [0xa77cff, 0xd6b4ff, 0x9d20ff][index];
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(0.42, 0.035, 16, 96),
      new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: 1.7,
        metalness: 0.25,
        roughness: 0.28
      })
    );
    const core = new THREE.Mesh(
      new THREE.IcosahedronGeometry(0.18, 1),
      new THREE.MeshStandardMaterial({
        color: 0xffffff,
        emissive: color,
        emissiveIntensity: 2.2,
        transparent: true,
        opacity: 0.92
      })
    );
    const glow = new THREE.Sprite(
      new THREE.SpriteMaterial({
        map: makeGlowTexture(color),
        color,
        transparent: true,
        opacity: 0.48,
        depthWrite: false
      })
    );
    const label = new THREE.Sprite(
      new THREE.SpriteMaterial({
        map: makeLabelTexture(name),
        transparent: true,
        depthWrite: false
      })
    );

    glow.scale.set(1.55, 1.55, 1);
    label.position.set(0, -0.74, 0);
    label.scale.set(1.02, 0.28, 1);

    group.add(glow, ring, core, label);
    group.visible = false;
    group.userData.baseColor = color;
    state.runeGroups.push(group);
    state.scene.add(group);
  });
}

function update(payload) {
  init();

  if (!state.ready) {
    return;
  }

  const { view, runes, visibleTarget, huntStarted } = payload;
  state.lastTarget = visibleTarget;

  state.runeGroups.forEach((group, index) => {
    const rune = runes[index];

    if (!huntStarted || !rune || rune.found) {
      group.visible = false;
      return;
    }

    const yawDiff = shortestAngle(rune.yaw - view.yaw);
    const pitchDiff = rune.pitch - view.pitch;
    const inView = Math.abs(yawDiff) <= horizontalFov / 2 && Math.abs(pitchDiff) <= verticalFov / 2;

    if (!inView) {
      group.visible = false;
      return;
    }

    const x = (yawDiff / (horizontalFov / 2)) * 3.15;
    const y = (pitchDiff / (verticalFov / 2)) * 2.05;
    const z = -0.45 - rune.depth * 0.85;
    const score = Math.hypot(yawDiff, pitchDiff);
    const scale = 0.75 + (1 - rune.depth) * 0.45 + Math.max(0, 1 - score / 36) * 0.35;

    group.visible = true;
    group.position.set(x, y, z);
    group.scale.setScalar(scale);
    group.rotation.y += 0.015 + index * 0.003;
    group.rotation.z += 0.008;
  });
}

function flashRune(index) {
  const group = state.runeGroups[index];

  if (!group) {
    return;
  }

  group.children.forEach(child => {
    if (child.material && "opacity" in child.material) {
      child.material.opacity = Math.min(child.material.opacity + 0.35, 1);
    }
  });
}

function animate() {
  requestAnimationFrame(animate);

  if (!state.ready) {
    return;
  }

  state.sweep += 0.018;
  animateHand();
  state.renderer.render(state.scene, state.camera);
}

function animateHand() {
  if (!state.handRoot) {
    return;
  }

  const targetGroup = state.lastTarget !== null ? state.runeGroups[state.lastTarget] : null;
  const targetX = targetGroup && targetGroup.visible ? targetGroup.position.x : Math.sin(state.sweep) * 0.38;
  const targetY = targetGroup && targetGroup.visible ? targetGroup.position.y : Math.cos(state.sweep * 0.8) * 0.2;
  const locked = targetGroup && targetGroup.visible;

  state.handRoot.rotation.y += ((-0.12 - targetX * 0.09) - state.handRoot.rotation.y) * 0.08;
  state.handRoot.rotation.x += ((-0.34 + targetY * 0.08) - state.handRoot.rotation.x) * 0.08;
  state.handRoot.position.x = 0.25 + targetX * 0.035;
  state.handRoot.position.y = -1.0 + Math.sin(state.sweep * 1.6) * 0.035;

  if (state.hand) {
    state.hand.rotation.z = -0.22 + Math.sin(state.sweep * 1.4) * 0.055;
  }

  if (state.handGlow) {
    state.handGlow.material.opacity += ((locked ? 0.58 : 0.18) - state.handGlow.material.opacity) * 0.12;
    const glowScale = locked ? 1.65 : 1.15;
    state.handGlow.scale.setScalar(glowScale + Math.sin(state.sweep * 3) * 0.05);
  }
}

function resize() {
  if (!state.renderer || !state.camera || !state.area) {
    return;
  }

  const rect = state.area.getBoundingClientRect();
  const width = Math.max(1, Math.floor(rect.width));
  const height = Math.max(1, Math.floor(rect.height));

  state.camera.aspect = width / height;
  state.camera.updateProjectionMatrix();
  state.renderer.setSize(width, height, false);
}

function makeGlowTexture(colorValue) {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 256;
  const ctx = canvas.getContext("2d");
  const color = "#" + colorValue.toString(16).padStart(6, "0");
  const gradient = ctx.createRadialGradient(128, 128, 8, 128, 128, 126);

  gradient.addColorStop(0, "rgba(255,255,255,0.92)");
  gradient.addColorStop(0.22, color);
  gradient.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 256, 256);

  return new THREE.CanvasTexture(canvas);
}

function makeLabelTexture(text) {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 160;
  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "rgba(9, 9, 18, 0.76)";
  roundRect(ctx, 54, 38, 404, 86, 40);
  ctx.fill();
  ctx.strokeStyle = "rgba(214, 180, 255, 0.72)";
  ctx.lineWidth = 3;
  ctx.stroke();
  ctx.fillStyle = "#f6edff";
  ctx.font = "700 44px Georgia, serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(text, 256, 82);

  return new THREE.CanvasTexture(canvas);
}

function roundRect(ctx, x, y, width, height, radius) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + width, y, x + width, y + height, radius);
  ctx.arcTo(x + width, y + height, x, y + height, radius);
  ctx.arcTo(x, y + height, x, y, radius);
  ctx.arcTo(x, y, x + width, y, radius);
  ctx.closePath();
}

function shortestAngle(angle) {
  return ((angle + 540) % 360) - 180;
}
