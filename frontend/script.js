document.getElementById("search-form").addEventListener("submit", function (e) {
    e.preventDefault();
    currentPage = 1;
    searchCards(1);
});

let currentPage = 1;

function getSelectValues(selectElement) {
    return Array.from(selectElement.selectedOptions).map(opt => opt.value);
}

async function searchCards(pageNumber) {
    const name = document.getElementById("searchName").value;
    const factions = getSelectValues(document.getElementById("factions"));
    const sortOrder = document.getElementById("sortOrder").value;
    const priceMax = document.getElementById("priceMax").value;

    const params = new URLSearchParams();
    if (name) params.append("name", name);
    params.append("page", currentPage);
    factions.forEach(f => f !== "" ? params.append("factions", f) : null);
    params.append("pageNumber", pageNumber);
    if (sortOrder) params.append("sortOrder", sortOrder);
    if (priceMax) params.append("priceMax", priceMax);

    const res = await fetch(`/api/cards?${params.toString()}`);
    const data = await res.json();

    const resultsDiv = document.getElementById("results");
    const paginationDiv = document.getElementById("pagination");
    resultsDiv.innerHTML = "";
    paginationDiv.innerHTML = "";

    if (data.error) {
        resultsDiv.innerHTML = `<p>Erreur : ${data.error}</p>`;
        return;
    }

    if (!data["hydra:member"] || data["hydra:member"].length === 0) {
        resultsDiv.innerHTML = "<p>Aucune carte trouvée.</p>";
        return;
    }

    data["hydra:member"].forEach(async card => {
        priceParams = new URLSearchParams();
        priceParams.append("reference", card.reference);
        const res = await fetch(`/api/cards/price?${priceParams.toString()}`);
        const price = await res.json();
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `
            <h3>${card.name}</h3>
            ${card.imagePath ? `<img class="cardImage" src="${card.imagePath}" alt="${card.name}" width="150">` : ""}
            <p>Reference :</p><a target="_blank" rel="noopener noreferrer" href="https://www.altered.gg/fr-fr/cards/${card.reference}">${card.reference}</a>
            <p></p><a target="_blank" rel="noopener noreferrer" href="https://www.altered.gg/fr-fr/cards/${card.reference}/offers">Offres disponibles</a>
            <p>${price["hydra:member"].length === 0 ? "Prix Indisponible" : price["hydra:member"][0].price + price["hydra:member"][0].currency }</p>
        `;
        resultsDiv.appendChild(div);
    });

    // Pagination
    const totalItems = data["hydra:totalItems"] || 0;
    const itemsPerPage = 30;
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    for (let i = 1; i < totalPages; i++) {
        const btn = document.createElement("button");
        btn.textContent = i;
        if (i === currentPage) btn.disabled = true;
        btn.addEventListener("click", () => {
            currentPage = i;
            searchCards(i);
        });
        paginationDiv.appendChild(btn);
    }
}
