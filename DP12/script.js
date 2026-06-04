let runesFound = 0;
let animationId = null;
let huntStarted = false;
let orientationActive = false;
let dragStart = null;
let visibleTarget = null;
let sensorOrigin = null;
let sensorReadings = 0;
let dragControlsReady = false;

const view = {
  yaw: 0,
  pitch: 0
};

const runes = [
  {
    symbol: "\u263e",
    name: "NOCTIS",
    text: "Waar de nacht geheimen bewaart.",
    yaw: 82,
    pitch: -4,
    depth: 0.85,
    found: false
  },
  {
    symbol: "\u25c9",
    name: "VISIO",
    text: "Waar verborgen waarheden zichtbaar worden.",
    yaw: 188,
    pitch: 8,
    depth: 0.72,
    found: false
  },
  {
    symbol: "\u2726",
    name: "UMBRA",
    text: "Waar schaduwen oude kennis beschermen.",
    yaw: 286,
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
  sensorOrigin = null;
  sensorReadings = 0;

  try {
    await enableOrientation();

    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false
    });

    video.srcObject = stream;
    buildRuneLayer();
    window.Nevermore3D?.init();
    startRenderLoop();
    setScanText(
      orientationActive
        ? "Richt met de 3D-hand. Als de hand een rune vindt, licht hij op."
        : "Beweeg rond met je telefoon. Als dat niet werkt, sleep dan als fallback met de hand."
    );

    setTimeout(() => {
      if (huntStarted && orientationActive && sensorReadings < 2) {
        orientationActive = false;
        addDragControls();
    setScanText("Telefoonrichting reageert niet. Sleep als fallback om met de hand te zoeken.");
      }
    }, 1800);
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
  const rawYaw = getDeviceYaw(event);

  if (rawYaw !== null) {
    if (sensorOrigin === null) {
      sensorOrigin = rawYaw;
    }

    sensorReadings++;
    view.yaw = normalizeAngle(rawYaw - sensorOrigin);
  }

  if (typeof event.beta === "number") {
    view.pitch = clamp(event.beta - 55, -35, 35);
  }
}

function getDeviceYaw(event) {
  if (typeof event.webkitCompassHeading === "number") {
    return normalizeAngle(event.webkitCompassHeading);
  }

  if (typeof event.alpha === "number") {
    return normalizeAngle(360 - event.alpha);
  }

  return null;
}

function addDragControls() {
  if (dragControlsReady) {
    return;
  }

  dragControlsReady = true;
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
    setScanText("De hand heeft een rune gevonden. Tik om hem te pakken.");
  } else if (huntStarted && runesFound < runes.length) {
    setScanText(orientationActive ? "Richt met de hand door de ruimte. De runes zweven buiten beeld." : "Sleep links of rechts om de hand verder te richten.");
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
    setScanText("Nog niet dichtbij genoeg. Richt de hand precies op de rune.");
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
    setScanText("De hand is dichtbij, maar nog niet precies genoeg gericht.");
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
    revealSecretHall();
  } else {
    setScanText("Rune verzameld. Draai verder om de volgende te vinden.");
  }
}

function revealSecretHall() {
  const artefact = document.getElementById("artefact");
  const cameraArea = document.querySelector(".camera-area");

  artefact.classList.remove("hidden");
  artefact.classList.add("reward-active");
  cameraArea.classList.add("hall-open");
  setScanText("Secret Hall geopend. Je cadeau wacht onder het portaal.");

  setTimeout(() => {
    artefact.scrollIntoView({ behavior: "smooth", block: "center" });
  }, 550);
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
  document.getElementById("artefact").classList.remove("reward-active");
  document.querySelector(".camera-area").classList.remove("hall-open");
  document.getElementById("foundCard").classList.add("hidden");
  setScanText("Start de hunt en richt je telefoon door de ruimte.");
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
      const params = new URLSearchParams(window.location.search);
      showPage("game");
      resetGame();
      huntStarted = true;
      orientationActive = false;
      view.yaw = params.has("reward") ? 286 : 82;
      view.pitch = params.has("reward") ? -10 : -4;
      buildRuneLayer();
      window.Nevermore3D?.init();
      startRenderLoop();
      setScanText("3D preview actief.");

      if (params.has("reward")) {
        runes.forEach(rune => {
          rune.found = true;
        });
        runesFound = runes.length;
        document.getElementById("runeCount").textContent = runesFound;
        document.getElementById("progressFill").style.width = "100%";
        revealSecretHall();
      }
    }, 250);
  });
}
