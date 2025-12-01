// === AUTH MODULE ===

// Сохраняем токен
export function saveToken(token) {
    localStorage.setItem("token", token);
}

// Получение токена
export function getToken() {
    return localStorage.getItem("token");
}

// Удаление токена (logout)
export function logout() {
    localStorage.removeItem("token");
    window.location.href = "/login.html";
}

// Проверка доступа для защищённых страниц
export function requireAuth() {
    if (!getToken()) {
        window.location.href = "/login.html";
    }
}

// Запрос с авторизацией
export async function authFetch(url, options = {}) {
    const token = getToken();

    const headers = options.headers || {};
    headers["Authorization"] = "Bearer " + token;

    return fetch(url, { ...options, headers });
}
