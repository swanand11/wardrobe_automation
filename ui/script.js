const API = "http://127.0.0.1:5000";

async function loadItems(){
    try {
        const res = await fetch(`${API}/items`);
        if (!res.ok) throw new Error(`API /items returned ${res.status}`);
        const items = await res.json();

        const select = document.getElementById("itemSelect");
        select.innerHTML = "";

        if (!items.length) {
            select.innerHTML = `<option value="">No items available</option>`;
            return;
        }

        items.forEach(item => {
            const option = document.createElement("option");
            option.value = item.item_name;
            option.text = item.item_name + " (" + item.type + ")";
            select.appendChild(option);
        });
    } catch (err) {
        console.error("Failed to load items", err);
        document.getElementById("outfitContainer").innerHTML = "<p style='color:red'>Error loading items. Open browser console for details.</p>";
    }
}

async function generateOutfit(){

    const item = document.getElementById("itemSelect").value;

    const res = await fetch(`${API}/suggest/${item}`);

    const data = await res.json();

    displayOutfit(data.outfit);
}

function displayOutfit(outfit){

    const container = document.getElementById("outfitContainer");

    container.innerHTML = "";

    outfit.forEach(piece => {

        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <h3>${piece}</h3>
        `;

        container.appendChild(card);

    });
}

loadItems();