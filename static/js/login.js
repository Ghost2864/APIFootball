import { saveToken } from "./auth.js";

document.getElementById("loginBtn").onclick = async () => {
    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login, password })
    });

    if (!response.ok) {
        document.getElementById("error").innerText = "Неверный логин или пароль";
        return;
    }

    const data = await response.json();

    saveToken(data.access_token);

    window.location.href = "/country";
};
