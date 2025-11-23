async function loadTeams() {
    const params = new URLSearchParams(window.location.search);
    const league_id = params.get("league");

    if (!league_id) {
        alert("Лига не указана!");
        return;
    }

    document.getElementById("pageTitle").innerText = `Команды лиги`;

    try {
        const response = await fetch(`/api/teams/${league_id}`);
        const data = await response.json();

        const container = document.getElementById("teamsContainer");
        container.innerHTML = "";

        if (!data || data.length === 0) {
            container.innerHTML = "<p>Команды не найдены</p>";
            return;
        }

        data.forEach(team => {
            const card = document.createElement("div");
            card.className = "team-card";


            card.onclick = () => {
                window.location.href = `/squad?team=${team.id}`;
            };

            const logo = document.createElement("img");
            logo.className = "team-logo";
            logo.src = team.logo;

            const name = document.createElement("div");
            name.className = "team-name";
            name.innerText = team.name;

            card.appendChild(logo);
            card.appendChild(name);
            container.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        alert("Ошибка загрузки команд");
    }
}

loadTeams();
