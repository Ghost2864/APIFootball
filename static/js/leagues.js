async function loadLeagues() {
    const params = new URLSearchParams(window.location.search);
    const country = params.get("country");

    if (!country) {
        alert("Страна не указана!");
        return;
    }

    

    const response = await fetch(`/api/leagues/${country}`);
    const data = await response.json();

    const container = document.getElementById("leaguesContainer");
    container.innerHTML = "";

    if (!data || data.length === 0) {
        container.innerHTML = "<p>Лиги не найдены</p>";
        return;
    }

    data.forEach(league => {
        const card = document.createElement("div");
        card.className = "league-card";

        card.onclick = () => {
            window.location.href = `/teams?league=${league.id}&league_id=${league.id}`;
        };

        const logo = document.createElement("img");
        logo.className = "league-logo";
        logo.src = league.logo;

        const title = document.createElement("div");
        title.className = "league-title";
        title.innerText = league.name;

        const id = document.createElement("div");
        id.className = "league-id";
        id.innerText = `Id: ${league.id}`;

        card.appendChild(logo);
        card.appendChild(title);
        card.appendChild(id);
        container.appendChild(card);
    });
}

loadLeagues();
