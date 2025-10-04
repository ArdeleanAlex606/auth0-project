const API_BASE_URL = "http://localhost:5000";

const loginButton = document.getElementById("login");
const logoutButton = document.getElementById("logout");
const discountsDiv = document.getElementById("discounts");
const discountList = document.getElementById("discount-list");

loginButton.addEventListener("click", () => {
    window.location.href = `${API_BASE_URL}/login`;
});

logoutButton.addEventListener("click", async () => {
    window.location.href = `${API_BASE_URL}/logout`;
    toggleUI(false);
});

async function fetchDiscounts() {
    try {
        const response = await fetch(`${API_BASE_URL}/discounts`, {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            const data = await response.json();
            displayDiscounts(data.discounts);
            toggleUI(true);
        } else {
            console.error("Failed to fetch discounts", response.status);
            toggleUI(false);
        }
    } catch (error) {
        console.error("Error fetching discounts", error);
        toggleUI(false);
    }
}

function displayDiscounts(discounts) {
    discountList.innerHTML = "";
    discounts.forEach(discount => {
        const li = document.createElement("li");
        li.textContent = `${discount.code} - ${discount.discount}% off at ${discount.store}`;
        discountList.appendChild(li);
    });
    discountsDiv.style.display = "block";
}

function toggleUI(isLoggedIn) {
    loginButton.style.display = isLoggedIn ? "none" : "block";
    logoutButton.style.display = isLoggedIn ? "block" : "none";
    discountsDiv.style.display = isLoggedIn ? "block" : "none";
}

// Check if the user is already logged in and fetch discounts
fetchDiscounts();