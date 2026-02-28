const API_BASE = "http://127.0.0.1:5000";
const REGISTER_URL = "<placeholder_url_for_now>";

const statusEl = document.getElementById("status");
const loginBox = document.getElementById("loginBox");
const loggedBox = document.getElementById("loggedBox");
const consentBox = document.getElementById("consentBox");
const consentCheck = document.getElementById("telemetryConsent");

const usernameEl = document.getElementById("username");
const passEl = document.getElementById("password");

document.getElementById("registerLink").addEventListener("click", () => {
    // If he doesnt have account, then redirect to <placeholder_url_for_now>
    const targetUrl = REGISTER_URL === "<placeholder_url_for_now>" ? `${API_BASE}/register` : REGISTER_URL;
    chrome.tabs.create({ url: targetUrl });
});

async function render() {
    const { accessToken, username, telemetryConsent } = await chrome.storage.local.get(["accessToken", "username", "telemetryConsent"]);

    if (telemetryConsent) {
        consentCheck.checked = true;
    }

    const logged = !!accessToken;
    statusEl.textContent = logged ? `Logged in as ${username}` : "Not logged in";
    loginBox.style.display = logged ? "none" : "block";
    consentBox.style.display = logged ? "none" : "block";
    loggedBox.style.display = logged ? "block" : "none";
}

consentCheck.addEventListener("change", async () => {
    await chrome.storage.local.set({ telemetryConsent: consentCheck.checked });
});

document.getElementById("loginBtn").addEventListener("click", async () => {
    if (!consentCheck.checked) {
        statusEl.textContent = "You must consent to telemetry to continue.";
        return;
    }

    const username = (usernameEl.value || "").trim();
    const password = passEl.value || "";

    if (!username || !password) {
        statusEl.textContent = "Username and password required.";
        return;
    }

    statusEl.textContent = "Logging in...";
    try {
        const res = await fetch(`${API_BASE}/api/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (!res.ok) {
            statusEl.textContent = data.error || "Login failed";
            return;
        }

        await chrome.storage.local.set({
            username: username,
            accessToken: data.access_token,
            telemetryConsent: true
        });

        statusEl.textContent = "✅ Login successful";
        await render();
    } catch (e) {
        statusEl.textContent = "Backend not reachable.";
    }
});

document.getElementById("logoutBtn").addEventListener("click", async () => {
    await chrome.storage.local.remove(["accessToken", "username"]);
    statusEl.textContent = "Logged out.";
    await render();
});

render();
