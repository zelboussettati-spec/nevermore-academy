let runesFound = 0;
let animationId = null;
let huntStarted = false;
let orientationActive = false;
let dragStart = null;
let visibleTarget = null;

const view = {
  yaw: 0,
  pitch: 0
};

const runes = [
  {
    symbol: "\u263e",
    name: "NOCTIS",
    text: "Waar de nacht geheimen bewaart.",
    yaw: -80,
    pitch: -4,
    depth: 0.85,
    found: false
  },
  {
    symbol: "\u25c9",
    name: "VISIO",
    text: "Waar verborgen waarheden zichtbaar worden.",
    yaw: 35,
    pitch: 8,
    depth: 0.72,
    found: false
  },
  {
    symbol: "\u2726",
    name: "UMBRA",
    text: "Waar schaduwen oude kennis beschermen.",
    yaw: 120,
    pitch: -10,
    depth: 0.95,
    found: false
  }
];

function showPage(pageId) {
  document.querySelectorAll(".page").forEach(page => {
    page.classList.remove("active");
  });

  document.getElementById(pageId).classList.add("active");
  document.getElementById("mobileMenu").classList.remove("active");
  window.scrollTo(0, 0);

  if (pageId === "game" && huntStarted) {
    renderRunes();
  }
}

function toggleMenu() {
  document.getElementById("mobileMenu").classList.toggle("active");
}

function showInfo(location) {
  const infoBox = document.getElementById("infoBox");

  if (location === "The Quad") {
    infoBox.innerHTML = `
      <div class="info-icon">O</div>
      <h3>The Quad</h3>
      <p>Central gathering space surrounded by gothic architecture.</p>
      <button class="btn" onclick="showPage('profile')">Explore Location</button>
    `;
  }

  if (location === "Library") {
    infoBox.innerHTML = `
      <div class="info-icon">B</div>
      <h3>Library</h3>
      <p>Ancient books reveal forbidden Nevermore knowledge.</p>
      <button class="btn" onclick="showPage('profile')">View Student Profile</button>
    `;
  }

  if (location === "Dorms") {
    infoBox.innerHTML = `
      <div class="info-icon">N</div>
      <h3>Dorms</h3>
      <p>Students whisper about strange sounds moving through the halls.</p>
      <button class="btn" onclick="showPage('profile')">View Student Profile</button>
    `;
  }

  if (location === "Secret Hall") {
    infoBox.innerHTML = `
      <div class="info-icon">*</div>
      <h3>Secret Hall</h3>
      <p>A hidden passage unlocks the AR Rune Hunt.</p>
      <button class="btn" onclick="showPage('game')">Start AR Game</button>
    `;
  }
}

async function startCamera() {
  const video = document.getElementById("camera");

  resetGame();
  huntStarted = true;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false
    });

    video.srcObject = stream;
    await enableOrientation();
    buildRuneLayer();
    window.Nevermore3D?.init();
    startRenderLoop();
    setScanText(
      orientationActive
        ? "Draai langzaam rond. Een rune licht op als hij in het vizier staat."
        : "Sleep over het camerabeeld om rond te kijken. Pak een rune als hij in het vizier staat."
    );
  } catch (error) {
    alert("Camera kon niet geopend worden. Geef toestemming of open de website via HTTPS.");
  }
}

async function enableOrientation() {
  orientationActive = false;

  if (!("DeviceOrientationEvent" in window)) {
    addDragControls();
    return;
  }

  try {
    if (typeof DeviceOrientationEvent.requestPermission === "function") {
      const permission = await DeviceOrientationEvent.requestPermission();

      if (permission !== "granted") {
        addDragControls();
        return;
      }
    }

    window.addEventListener("deviceorientation", handleOrientation, true);
    orientationActive = true;
  } catch (error) {
    addDragControls();
  }
}

function handleOrientation(event) {
  if (typeof event.alpha === "number") {
    view.yaw = normalizeAngle(360 - event.alpha);
  }

  if (typeof event.beta === "number") {
    view.pitch = clamp(event.beta - 55, -35, 35);
  }
}

function addDragControls() {
  const area = document.querySelector(".camera-area");

  area.addEventListener("pointerdown", event => {
    dragStart = {
      x: event.clientX,
      y: event.clientY,
      yaw: view.yaw,
      pitch: view.pitch
    };
    area.setPointerCapture(event.pointerId);
  });

  area.addEventListener("pointermove", event => {
    if (!dragStart) {
      return;
    }

    const dx = event.clientX - dragStart.x;
    const dy = event.clientY - dragStart.y;

    view.yaw = normalizeAngle(dragStart.yaw - dx * 0.28);
    view.pitch = clamp(dragStart.pitch + dy * 0.18, -35, 35);
  });

  area.addEventListener("pointerup", () => {
    dragStart = null;
  });

  area.addEventListener("pointercancel", () => {
    dragStart = null;
  });
}

function buildRuneLayer() {
  const layer = document.getElementById("runeLayer");
  layer.innerHTML = "";

  runes.forEach((rune, index) => {
    const button = document.createElement("button");
    button.className = "world-rune hidden";
    button.type = "button";
    button.dataset.index = index;
    button.innerHTML = `
      <span class="world-rune-symbol">${rune.symbol}</span>
      <span class="world-rune-name">${rune.name}</span>
    `;
    button.addEventListener("click", () => collectRune(index));
    layer.appendChild(button);
  });
}

function startRenderLoop() {
  if (animationId) {
    cancelAnimationFrame(animationId);
  }

  const tick = () => {
    renderRunes();
    animationId = requestAnimationFrame(tick);
  };

  tick();
}

function renderRunes() {
  const compass = document.getElementById("compass");
  const reticle = document.getElementById("reticle");
  const nodes = document.querySelectorAll(".world-rune");
  const horizontalFov = 72;
  const verticalFov = 48;
  let bestTarget = null;
  let bestScore = Infinity;

  compass.textContent = Math.round(view.yaw) + " graden";

  nodes.forEach((node, index) => {
    const rune = runes[index];

    if (rune.found) {
      node.classList.add("hidden");
      node.classList.remove("locked");
      return;
    }

    const yawDiff = shortestAngle(rune.yaw - view.yaw);
    const pitchDiff = rune.pitch - view.pitch;
    const inView = Math.abs(yawDiff) <= horizontalFov / 2 && Math.abs(pitchDiff) <= verticalFov / 2;

    if (!inView) {
      node.classList.add("hidden");
      node.classList.remove("locked");
      return;
    }

    const x = 50 + (yawDiff / (horizontalFov / 2)) * 46;
    const y = 50 - (pitchDiff / (verticalFov / 2)) * 39;
    const score = Math.hypot(yawDiff, pitchDiff);
    const scale = 0.68 + (1 - rune.depth) * 0.7 + Math.max(0, 1 - score / 42) * 0.45;
    const opacity = clamp(1 - score / 52, 0.35, 1);

    node.classList.remove("hidden");
    node.style.left = x + "%";
    node.style.top = y + "%";
    node.style.opacity = opacity;
    node.style.transform = `translate(-50%, -50%) scale(${scale}) rotateY(${yawDiff * -0.7}deg)`;

    if (score < bestScore) {
      bestScore = score;
      bestTarget = { index, score };
    }
  });

  visibleTarget = bestTarget && bestTarget.score <= 10 ? bestTarget.index : null;

  nodes.forEach((node, index) => {
    node.classList.toggle("locked", index === visibleTarget);
  });

  reticle.classList.toggle("locked", visibleTarget !== null);

  if (visibleTarget !== null) {
    setScanText("Rune in vizier. Tik op Pak rune in vizier.");
  } else if (huntStarted && runesFound < runes.length) {
    setScanText(orientationActive ? "Draai langzaam verder. Luister naar de richting." : "Sleep links of rechts om verder rond te kijken.");
  }

  window.Nevermore3D?.update({
    view,
    runes,
    visibleTarget,
    huntStarted
  });
}

function scanRune() {
  if (!huntStarted) {
    setScanText("Start eerst de AR Hunt met camera toestemming.");
    return;
  }

  if (visibleTarget === null) {
    pulseReticle();
    setScanText("Nog niet dichtbij genoeg. Zet een rune precies in het vizier.");
    return;
  }

  collectRune(visibleTarget);
}

function collectRune(index) {
  const rune = runes[index];

  if (!rune || rune.found) {
    return;
  }

  const aimDistance = Math.hypot(shortestAngle(rune.yaw - view.yaw), rune.pitch - view.pitch);

  if (aimDistance > 14) {
    pulseReticle();
    setScanText("Deze rune is zichtbaar, maar nog niet goed genoeg gericht.");
    return;
  }

  rune.found = true;
  runesFound++;
  window.Nevermore3D?.flashRune(index);

  document.getElementById("currentRune").textContent = rune.symbol;
  document.getElementById("runeName").textContent = rune.name;
  document.getElementById("runeText").textContent = rune.text;
  document.getElementById("foundCard").classList.remove("hidden");
  document.getElementById("runeCount").textContent = runesFound;
  document.getElementById("progressFill").style.width = (runesFound / runes.length) * 100 + "%";

  setTimeout(() => {
    document.getElementById("foundCard").classList.add("hidden");
  }, 1800);

  if (runesFound === runes.length) {
    document.getElementById("artefact").classList.remove("hidden");
    setScanText("Alle runes gevonden. Artefact ontgrendeld.");
  } else {
    setScanText("Rune verzameld. Draai verder om de volgende te vinden.");
  }
}

function resetGame() {
  runesFound = 0;
  visibleTarget = null;

  runes.forEach(rune => {
    rune.found = false;
  });

  document.getElementById("runeCount").textContent = "0";
  document.getElementById("progressFill").style.width = "0%";
  document.getElementById("artefact").classList.add("hidden");
  document.getElementById("foundCard").classList.add("hidden");
  setScanText("Start de camera en draai rond om de eerste rune te vinden.");
  buildRuneLayer();
  window.Nevermore3D?.update({
    view,
    runes,
    visibleTarget,
    huntStarted
  });
}

function pulseReticle() {
  const reticle = document.getElementById("reticle");
  reticle.classList.remove("miss");
  void reticle.offsetWidth;
  reticle.classList.add("miss");
}

function setScanText(text) {
  document.getElementById("scanText").textContent = text;
}

function normalizeAngle(angle) {
  return ((angle % 360) + 360) % 360;
}

function shortestAngle(angle) {
  return ((angle + 540) % 360) - 180;
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

if (new URLSearchParams(window.location.search).has("preview3d")) {
  window.addEventListener("load", () => {
    setTimeout(() => {
      showPage("game");
      resetGame();
      huntStarted = true;
      orientationActive = false;
      view.yaw = 35;
      view.pitch = 8;
      buildRuneLayer();
      window.Nevermore3D?.init();
      startRenderLoop();
      setScanText("3D preview actief.");
    }, 250);
  });
}
