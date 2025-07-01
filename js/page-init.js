document.addEventListener('DOMContentLoaded', () => {
    console.log("page-init.js: DOMContentLoaded");

    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
        });
        console.log("page-init.js: AOS initialized");
    } else {
        console.error("page-init.js: AOS library not found.");
    }

    // Load shared header
    const headerPlaceholder = document.getElementById('header-placeholder');
    if (headerPlaceholder) {
        fetch('shared/header.html')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status} while fetching header.html`);
                }
                return response.text();
            })
            .then(data => {
                headerPlaceholder.innerHTML = data;
                console.log("page-init.js: Header loaded.");
                document.dispatchEvent(new CustomEvent('headerLoaded'));
            })
            .catch(error => {
                console.error('Error loading shared/header.html:', error);
                headerPlaceholder.innerHTML = '<p class="text-red-500 text-center">Error loading header.</p>';
            });
    } else {
        console.warn("page-init.js: header-placeholder not found on this page.");
    }

    // Load shared navigation panel (the menu itself)
    const navMenuPlaceholder = document.getElementById('nav-menu-placeholder');
    if (navMenuPlaceholder) {
        fetch('shared/nav-panel.html')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status} while fetching nav-panel.html`);
                }
                return response.text();
            })
            .then(data => {
                navMenuPlaceholder.innerHTML = data;
                console.log("page-init.js: Nav panel loaded.");
                document.dispatchEvent(new CustomEvent('navPanelLoaded')); // New event for menu.js
            })
            .catch(error => {
                console.error('Error loading shared/nav-panel.html:', error);
                navMenuPlaceholder.innerHTML = '<p class="text-red-500 text-center">Error loading navigation.</p>';
            });
    } else {
        console.warn("page-init.js: nav-menu-placeholder not found on this page.");
    }

    // Load shared footer
    const footerPlaceholder = document.getElementById('footer-placeholder');
    if (footerPlaceholder) {
        fetch('shared/footer.html')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status} while fetching footer.html`);
                }
                return response.text();
            })
            .then(data => {
                footerPlaceholder.innerHTML = data;
                console.log("page-init.js: Footer loaded.");
                document.dispatchEvent(new CustomEvent('footerLoaded'));
            })
            .catch(error => {
                console.error('Error loading shared/footer.html:', error);
                footerPlaceholder.innerHTML = '<p class="text-red-500 text-center">Error loading footer.</p>';
            });
    } else {
        console.warn("page-init.js: footer-placeholder not found on this page.");
    }
});
