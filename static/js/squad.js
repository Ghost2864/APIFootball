async function loadSquad() {
    const params = new URLSearchParams(window.location.search);
    const team_id = params.get("team");

    if (!team_id) {
        alert("Команда не указана!");
        return;
    }

    const container = document.getElementById("squadContainer");
    const teamHeader = document.getElementById("teamName");

    try {
        const response = await fetch(`/api/squad/${team_id}`);
        const data = await response.json();

        container.innerHTML = "";

        if (!data || data.length === 0) {
            container.innerHTML = "<p>Состав не найден</p>";
            return;
        }

        // Если backend добавляет team_name — выводим
        if (data[0].team_name) {
            teamHeader.innerText = `Состав: ${data[0].team_name}`;
        }

        data.forEach(player => {
            const card = document.createElement("div");
            card.className = "player-card";

            card.onclick = () => {
                window.location.href = `/profile?player=${player.id}`;
            };

            const photo = document.createElement("img");
            photo.className = "player-photo";
            photo.src = player.photo || "https://via.placeholder.com/90";

            const name = document.createElement("div");
            name.className = "player-name";
            name.innerText = player.name;

            const info = document.createElement("div");
            info.className = "player-info";
            info.innerHTML = `
                Возраст: ${player.age}
            `;

            card.appendChild(photo);
            card.appendChild(name);
            card.appendChild(info);

            container.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        alert("Ошибка загрузки состава");
    }
}

loadSquad();
