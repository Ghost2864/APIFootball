const STAT_TRANSLATION = {
    "goals.total": "Голы",
    "goals.assists": "Ассисты",
    "cards.yellow": "Жёлтые",
    "cards.red": "Красные",
    "games.lineups": "Матчи",
    "games.rating" : "Рейтинг",
    "games.minutes": "Минуты",
    "dribbles.success": "Удачных обводок",
    "dribbles.attempts": "Попыток обводок",
    "passes.total" : "Количество передач",
    "passes.key" : "Точные передачи",
    "goals.saves" : "Отбитые удары",
    "goals.conceded" : "Пропущенные голы",
    "duels.total" : "Количество единоборств",
    "duels.won" : "Выйграно единоборств",
    "penalty.saved" : "Отбито пенальти"

};

async function loadPlayerProfile() {
    const params = new URLSearchParams(window.location.search);
    const player_id = params.get("player");
    if (!player_id) return alert("Игрок не указан!");

    const container = document.getElementById("profileContainer");
    container.innerHTML = '<p>Загрузка...</p>';

    try {
        const response = await fetch(`/api/profile/${player_id}`);
        const data = await response.json();

        const player = data.player ?? data[0];
        const stats = data.stats ?? data[1];

        container.innerHTML = `
            <div class="profile-card">
                <img class="profile-photo" src="${player.photo}" alt="Фото">
                <div class="profile-info">
                    <div><b>${player.firstname} ${player.lastname}</b></div>
                    <div>Возраст: ${player.age}</div>
                    <div>Страна: ${player.nationality}</div>
                    <div>Место рождения: ${player.birth.place ?? '-'}</div>
                </div>
            </div>

            <div class="stats-block">
                <img class="team-logo" src="${stats['team.logo']}" alt="Эмблема">

                <div class="stats-title">Статистика</div>
                <div class="stats-grid" id="statsGrid"></div>
            </div>
        `;

        const statsGrid = document.getElementById("statsGrid");

        for (const [key, label] of Object.entries(STAT_TRANSLATION)) {
            if (stats[key] !== undefined && stats[key] !== null) {
                statsGrid.innerHTML += `
                    <div class="stat-item">
                        <div>${label}</div>
                        <div><b>${stats[key]}</b></div>
                    </div>
                `;
            }
        }

    } catch (err) {
        console.error(err);
        container.innerHTML = "<p>Ошибка загрузки данных</p>";
    }
}

loadPlayerProfile();
