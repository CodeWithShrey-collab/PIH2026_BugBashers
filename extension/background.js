let tabMap = {};

function websiteFromUrl(url) {
    try {
        if (!url) return null;
        if (url.startsWith("chrome://") || url.startsWith("edge://") || url.startsWith("about:")) return null;
        const u = new URL(url);
        return (u.hostname || "").toLowerCase();
    } catch {
        return null;
    }
}

// User required URL for export
const API_ENDPOINT = "<placeholder_url_for_now2>";
// Fallback local API
const FALLBACK_API = "http://127.0.0.1:5000/api/activity";

async function sendLog(payloadObj) {
    const { accessToken, telemetryConsent } = await chrome.storage.local.get(["accessToken", "telemetryConsent"]);

    if (!telemetryConsent || !accessToken) return false;

    const bodyString = JSON.stringify(payloadObj);

    const targetUrl = API_ENDPOINT === "<placeholder_url_for_now2>" ? FALLBACK_API : API_ENDPOINT;

    try {
        const res = await fetch(targetUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
            body: bodyString
        });
        return res.ok;
    } catch {
        return false;
    }
}

async function startTab(tabId, url) {
    const site = websiteFromUrl(url);
    if (!site) return;
    tabMap[tabId] = { website_name: site, st_time: Date.now() };
}

async function resetIfUrlChanged(tabId, url) {
    const site = websiteFromUrl(url);
    if (!site) return;

    const cur = tabMap[tabId];
    if (!cur || cur.website_name !== site) {
        if (cur) await endTab(tabId);
        tabMap[tabId] = { website_name: site, st_time: Date.now() };
    }
}

async function endTab(tabId) {
    const cur = tabMap[tabId];
    if (!cur) return;

    const payload = {
        website_name: cur.website_name,
        st_time: cur.st_time,
        end_time: Date.now()
    };

    delete tabMap[tabId];

    await sendLog(payload);
}

chrome.tabs.onCreated.addListener(async (tab) => {
    if (tab?.id && tab?.url) await startTab(tab.id, tab.url);
});

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo?.url) {
        await resetIfUrlChanged(tabId, changeInfo.url);
    } else if (tab?.url) {
        await resetIfUrlChanged(tabId, tab.url);
    }
});

chrome.tabs.onRemoved.addListener(async (tabId) => {
    await endTab(tabId);
});
