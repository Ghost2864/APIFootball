const STAT_TRANSLATION = {
    "goals.total": "Голы",
    "goals.assists": "Ассисты",
    "cards.yellow": "Жёлтые",
    "cards.red": "Красные",
    "games.lineups": "Матчи",
    "games.rating": "Рейтинг",
    "games.minutes": "Минуты",
    "dribbles.success": "Удачных обводок",
    "dribbles.attempts": "Попыток обводок",
    "passes.total": "Количество передач",
    "passes.key": "Точные передачи",
    "goals.saves": "Отбитые удары",
    "goals.conceded": "Пропущенные голы",
    "duels.total": "Количество единоборств",
    "duels.won": "Выиграно единоборств",
    "penalty.saved": "Отбито пенальти"
};


async function loadPlayerProfile() {
    const params = new URLSearchParams(window.location.search);
    const player_id = params.get("player");
    const container = document.getElementById("profileContainer");

    if (!player_id) {
        container.innerHTML = "<p>Игрок не указан!</p>";
        return;
    }

    container.innerHTML = "<p>Загрузка...</p>";

    try {
        const response = await fetch(`/api/profile/${player_id}`);
        const data = await response.json();

        // главный профиль
        const player = data[0];

        // клуб (из первого турнира)
        const firstStats = data[1]?.stats;
        const clubName = firstStats?.["team.name"] ?? "Неизвестно";
        const clubLogo = firstStats?.["team.logo"] ?? "";

        container.innerHTML = `
            <div class="profile-card">
                
                <img class="profile-photo" src="${player.photo}" alt="Фото игрока">

                <div class="profile-info">
                    <div class="profile-header">
                        <div>
                            <div class="player-name"><b>${player.firstname} ${player.lastname}</b></div>
                            <div class="player-club">${clubName}</div>
                        </div>
                        <img class="club-logo" src="${clubLogo}">
                    </div>

                    <div>Возраст: ${player.age}</div>
                    <div>Страна: ${player.nationality}</div>
                    <div>Место рождения: ${player.birth?.place ?? "-"}</div>
                </div>

            </div>
        `;

        // турниры идут через один: игрок, турнир, игрок, турнир...
        const tournaments = [];
        for (let i = 1; i < data.length; i += 2) {
            tournaments.push(data[i]);
        }

        // вывод статистики по каждому турниру
        for (const comp of tournaments) {
            const stats = comp.stats;
            if (!stats) continue;

            const title = comp.league ?? "Турнир";

            let statsHtml = "";

            for (const [key, label] of Object.entries(STAT_TRANSLATION)) {
                if (stats[key] !== undefined && stats[key] !== null) {
                    statsHtml += `
                        <div class="stat-item">
                            <div>${label}</div>
                            <div><b>${stats[key]}</b></div>
                        </div>
                    `;
                }
            }

            container.innerHTML += `
                <div class="stats-block">
                    
                    <div class="tournament-header">
                        <img class="league-logo" src="${stats['league.logo'] ?? ''}">
                        <div class="stats-title">${title}</div>
                    </div>

                    <div class="stats-grid">
                        ${statsHtml}
                    </div>

                </div>
            `;
        }

    } catch (err) {
        console.error(err);
        container.innerHTML = "<p>Ошибка загрузки данных.</p>";
    }
}

loadPlayerProfile();
