let runesFound = 0;
let autoScanTimer = null;

const runes = [
  {
    symbol: "☾",
    name: "NOCTIS",
    text: "Waar de nacht geheimen bewaart."
  },
  {
    symbol: "👁",
    name: "VISIO",
    text: "Waar verborgen waarheden zichtbaar worden."
  },
  {
    symbol: "✦",
    name: "UMBRA",
    text: "Waar schaduwen oude kennis beschermen."
  }
];

function showPage(pageId) {
  document.querySelectorAll(".page").forEach(page => {
    page.classList.remove("active");
  });

  document.getElementById(pageId).classList.add("active");
  document.getElementById("mobileMenu").classList.remove("active");
  window.scrollTo(0, 0);
}

function toggleMenu() {
  document.getElementById("mobileMenu").classList.toggle("active");
}

function showInfo(location) {
  const infoBox = document.getElementById("infoBox");

  if (location === "The Quad") {
    infoBox.innerHTML = `
      <div class="info-icon">👁</div>
      <h3>The Quad</h3>
      <p>Central gathering space surrounded by gothic architecture.</p>
      <button class="btn" onclick="showPage('profile')">Explore Location</button>
    `;
  }

  if (location === "Library") {
    infoBox.innerHTML = `
      <div class="info-icon">📖</div>
      <h3>Library</h3>
      <p>Ancient books reveal forbidden Nevermore knowledge.</p>
      <button class="btn" onclick="showPage('profile')">View Student Profile</button>
    `;
  }

  if (location === "Dorms") {
    infoBox.innerHTML = `
      <div class="info-icon">☾</div>
      <h3>Dorms</h3>
      <p>Students whisper about strange sounds moving through the halls.</p>
      <button class="btn" onclick="showPage('profile')">View Student Profile</button>
    `;
  }

  if (location === "Secret Hall") {
    infoBox.innerHTML = `
      <div class="info-icon">✦</div>
      <h3>Secret Hall</h3>
      <p>A hidden passage unlocks the AR Rune Hunt.</p>
      <button class="btn" onclick="showPage('game')">Start AR Game</button>
    `;
  }
}

async function startCamera() {
  const video = document.getElementById("camera");

  resetGame();

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false
    });

    video.srcObject = stream;
    document.getElementById("scanText").textContent =
      "Camera actief. Beweeg langzaam alsof je een verborgen symbool zoekt...";

    startAutoScan();

  } catch (error) {
    alert("Camera kon niet geopend worden. Geef toestemming of open de website via localhost/https.");
  }
}

function startAutoScan() {
  if (autoScanTimer) {
    clearInterval(autoScanTimer);
  }

  autoScanTimer = setInterval(() => {
    if (runesFound >= 3) {
      clearInterval(autoScanTimer);
      autoScanTimer = null;
      return;
    }

    revealNextRune();
  }, 3500);
}

function revealNextRune() {
  const rune = runes[runesFound];

  document.getElementById("currentRune").textContent = rune.symbol;
  document.getElementById("runeName").textContent = rune.name;
  document.getElementById("runeText").textContent = rune.text;
  document.getElementById("foundCard").classList.remove("hidden");

  runesFound++;

  document.getElementById("runeCount").textContent = runesFound;
  document.getElementById("progressFill").style.width = (runesFound / 3) * 100 + "%";

  document.getElementById("scanText").textContent =
    "Verborgen symbool gevonden: " + rune.name;

  if (runesFound === 3) {
    document.getElementById("artefact").classList.remove("hidden");
    document.getElementById("scanText").textContent =
      "Alle runes gevonden. Artefact ontgrendeld.";
  }
}

function scanRune() {
  revealNextRune();
}

function resetGame() {
  runesFound = 0;

  if (autoScanTimer) {
    clearInterval(autoScanTimer);
    autoScanTimer = null;
  }

  document.getElementById("runeCount").textContent = "0";
  document.getElementById("progressFill").style.width = "0%";
  document.getElementById("artefact").classList.add("hidden");
  document.getElementById("foundCard").classList.add("hidden");
  document.getElementById("scanText").textContent =
    "Zoek langzaam tot een rune oplicht...";
}