// Initialise les variables de suivi
const sessionStartTime = Date.now();
let pageViews = 0;

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
            pageViews++;
            const pageData = {
                eventType: "page_view",
                url: window.location.href,
                timestamp: new Date().toISOString(),
                pageViews: pageViews,
                sessionDuration: Math.round((Date.now() - sessionStartTime) / 1000) // Durée en secondes
            };
            sendAnalyticsData(pageData);
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
                eventType: "session_start",
                sessionStartTime: new Date(sessionStartTime).toISOString(),
                deviceInfo: getDeviceInfo()
            };
            sendAnalyticsData(analyticsData);
        });

        // Suivre l’événement de déchargement de la page (fin de session)
        window.addEventListener("beforeunload", () => {
            const sessionDuration = Math.round((Date.now() - sessionStartTime) / 1000); // Durée en secondes
            const endData = {
                eventType: "session_end",
                sessionDuration: sessionDuration,
                pageViews: pageViews
            };
            sendAnalyticsData(endData);
        });

        // Suivi des changements de pages (pour les SPA)
        window.addEventListener("popstate", trackPageView);