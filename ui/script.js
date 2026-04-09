const API = "http://127.0.0.1:8000";
let itemsMap = {}, allItems = [], activeFilters = new Set();

function rgb(r, g, b) {
  return `rgb(${Math.round(r || 0)},${Math.round(g || 0)},${Math.round(b || 0)})`;
}

function applyLayers(outfit) {
  const tops = ["shirt", "polo", "tshirt"];
  const bottoms = ["pants"];
  const shoes = ["shoes", "sneakers", "boots", "loafers", "oxford"];

  const find = types => outfit.find(n => {
    const t = itemsMap[n]?.type?.toLowerCase() || "";
    return types.some(x => t.includes(x));
  });

  const setLayer = (id, item, label) => {
    const el = document.getElementById(id);
    if (!el) return;

    if (!item) {
      el.style.background = "var(--mq-empty)";
      el.style.borderColor = "var(--mq-border)";
      el.textContent = "";
      return;
    }

    const c = rgb(item.reds, item.green, item.blue);
    el.style.background = c;
    el.style.borderColor = c;
    el.textContent = label;
  };

  const topItem = itemsMap[find(tops)];
  const bottomItem = itemsMap[find(bottoms)];
  const shoeItem = itemsMap[find(shoes)];
  const watchItemName = outfit.find(n => itemsMap[n]?.type === "watch");
  const watchItem = itemsMap[watchItemName];

  setLayer("layer-top", topItem, topItem?.type?.toUpperCase() || "TOP");
  setLayer("layer-bottom", bottomItem, bottomItem?.type?.toUpperCase() || "BOTTOM");
  setLayer("layer-shoes", shoeItem, shoeItem?.type?.toUpperCase() || "SHOES");

  const watchEl = document.getElementById("watch-preview");
  if (watchEl) {
    if (watchItem) {
      const sc = rgb(
        watchItem.strap_reds ?? watchItem.reds,
        watchItem.strap_green ?? watchItem.green,
        watchItem.strap_blue ?? watchItem.blue
      );

      const dc = rgb(
        watchItem.dial_reds ?? watchItem.reds,
        watchItem.dial_green ?? watchItem.green,
        watchItem.dial_blue ?? watchItem.blue
      );

      watchEl.innerHTML = `
        <div class="watch-piece strap" style="background:${sc}; border-color:${sc}">
          <span>strap</span>
        </div>
        <div class="watch-piece dial" style="background:${dc}; border-color:${dc}">
          <span>dial</span>
        </div>
        <div class="watch-piece strap" style="background:${sc}; border-color:${sc}">
          <span>strap</span>
        </div>
      `;
    } else {
      watchEl.innerHTML = "";
    }
  }
}

function renderCards(outfitList, scores = {}) {
  const el = document.getElementById("cards");

  if (!outfitList || outfitList.length === 0) {
    el.innerHTML = `<div class="empty-state"><p>No outfit found</p></div>`;
    return;
  }

  el.innerHTML = "";
  outfitList.forEach(name => {
    const item = itemsMap[name];
    if (!item) return;

    const card = document.createElement("div");
    card.className = "item-card";

    let swatchHTML = "";
    if (item.type === "watch") {
      const sc = rgb(item.strap_reds ?? item.reds, item.strap_green ?? item.green, item.strap_blue ?? item.blue);
      const dc = rgb(item.dial_reds ?? item.reds, item.dial_green ?? item.green, item.dial_blue ?? item.blue);
      swatchHTML = `
        <div class="watch-sw">
          <div style="background:${sc}">
            <span>strap</span>
          </div>
          <div style="background:${dc}">
            <span>dial</span>
          </div>
        </div>`;
    } else {
      swatchHTML = `<div class="swatch-sm" style="background:${rgb(item.reds, item.green, item.blue)}"></div>`;
    }

    const vibes = Array.isArray(item.vibe) ? item.vibe : [];
    const vibeHTML = vibes.map(v => `<span class="vibe">${v}</span>`).join("");

    const s = scores[name];
    const scoreHTML = s !== undefined ? `
      <div class="score-wrap">
        <div class="score-track">
          <div class="score-fill" style="width:${Math.round(s * 100)}%"></div>
        </div>
        <span class="score-num">${s.toFixed(2)}</span>
      </div>` : "";

    card.innerHTML = `
      ${swatchHTML}
      <div class="card-info">
        <div class="card-type">${item.type}</div>
        <div class="card-name">${name}</div>
        <div class="vibes">${vibeHTML}</div>
      </div>
      ${scoreHTML}
    `;

    el.appendChild(card);
  });

  applyLayers(outfitList);
}

function setMeta(text, score) {
  const el = document.getElementById("meta");
  el.innerHTML = "";

  if (text) {
    const b = document.createElement("span");
    b.className = "meta-badge type";
    b.textContent = text;
    el.appendChild(b);
  }

  if (score !== undefined) {
    const s = document.createElement("span");
    s.className = "meta-badge score";
    s.textContent = `Score ${score.toFixed(2)}`;
    el.appendChild(s);
  }
}

async function suggest() {
  const item = document.getElementById("itemSelect").value;
  try {
    const res = await fetch(`${API}/suggest/${encodeURIComponent(item)}`);
    const data = await res.json();
    setMeta(`Suggested from ${item}`);
    renderCards(data.outfit || []);
  } catch (e) {
    renderCards([]);
  }
}

async function shuffleOutfit() {
  const item = document.getElementById("itemSelect").value;
  try {
    const res = await fetch(`${API}/random/${encodeURIComponent(item)}`);
    const data = await res.json();
    setMeta(`Shuffled from ${item}`);
    renderCards(data.outfit || []);
  } catch (e) {
    renderCards([]);
  }
}

async function bestOutfit() {
  try {
    const res = await fetch(`${API}/best`);
    const data = await res.json();
    setMeta("Best outfit", data.score);
    renderCards(data.outfit ? [...data.outfit] : []);
  } catch (e) {
    renderCards([]);
  }
}

function refreshDropdown() {
  const sel = document.getElementById("itemSelect");
  const cur = sel.value;
  sel.innerHTML = "";

  const filtered = activeFilters.size === 0
    ? allItems
    : allItems.filter(i => activeFilters.has(i.type));

  filtered.forEach(item => {
    const o = document.createElement("option");
    o.value = item.item_name;
    o.textContent = item.item_name;
    if (item.item_name === cur) o.selected = true;
    sel.appendChild(o);
  });
}

async function loadItems() {
  try {
    const res = await fetch(`${API}/items`);
    const data = await res.json();
    allItems = data;

    data.forEach(i => {
      itemsMap[i.item_name] = i;
    });

    const types = [...new Set(data.map(i => i.type))].sort();
    const chipsEl = document.getElementById("filterChips");

    types.forEach(t => {
      const chip = document.createElement("button");
      chip.className = "chip";
      chip.textContent = t;
      chip.onclick = () => {
        chip.classList.toggle("on");
        activeFilters.has(t) ? activeFilters.delete(t) : activeFilters.add(t);
        refreshDropdown();
      };
      chipsEl.appendChild(chip);
    });

    refreshDropdown();
  } catch (e) {
    document.getElementById("cards").innerHTML =
      `<div class="empty-state"><p>Could not connect to API at ${API}</p></div>`;
  }
}

loadItems();