// Envoie des analytics sur le serveur
function sendAnalyticsData(data) {
    fetch("/collect", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => console.log("Analytics data sent:", data))
      .catch(error => console.error("Error sending analytics data:", error));
}

// Suivi des pages vues
function trackPageView() {
    const last_time = sessionStorage.getItem('last_page_at');
    const duration = last_time ? Math.round((Date.now() - last_time) / 1000) : 0; // Durée en secondes ou 0 si première visite
    return {
        url: window.location.href,  // URL de la page vue
        duration: duration
    };

}

// Suivre le type d’appareil et d'autres infos techniques
function getDeviceInfo() {
    const deviceType = /Mobi|Android/i.test(navigator.userAgent) ? "mobile" : "desktop";
    const os = navigator.platform;
    const browser = navigator.userAgent;
    return {
        deviceType: deviceType,
        os: os,
        browser: browser
    };
}

// Suivre l'événement de chargement de la page
window.addEventListener("load", () => {
    const analyticsData = {
        eventType: "page",
        time: Date.now(),
        deviceInfo: getDeviceInfo(),
        pageInfo: trackPageView()
    };
    sendAnalyticsData(analyticsData);
    sessionStorage.setItem('last_page_at', Date.now());
});
