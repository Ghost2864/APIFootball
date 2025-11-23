// Статические страны
const COUNTRIES = [
    { name: "England", code: "GB-ENG" },
    { name: "Spain",   code: "ES" },
    { name: "Germany", code: "DE" },
    { name: "Italy",   code: "IT" },
    { name: "France",  code: "FR" },
    { name: "Russia", code:"RU"}
];

function loadCountries() {
    const container = document.getElementById("countriesContainer");

    COUNTRIES.forEach(country => {
        const card = document.createElement("div");
        card.className = "card";
        card.onclick = () => {
            window.location.href = `/league?country=${country.code}`;
        };

        const name = document.createElement("div");
        name.className = "card-title";
        name.innerText = country.name;

        card.appendChild(name);
        container.appendChild(card);
    });
}

// function loadDropdown() {
//     const dropdown = document.getElementById("dropdownList");

//     COUNTRIES.forEach(country => {
//         const item = document.createElement("div");
//         item.className = "dropdown-item";
//         item.innerText = country.name;

//         item.onclick = () => {
//             window.location.href = `/league?country=${country.code}`;
//         };

//         dropdown.appendChild(item);
//     });
// }

loadCountries();
