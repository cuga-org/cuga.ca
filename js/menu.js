// JavaScript for hamburger menu functionality

// Attempt to initialize right away if elements are already in the static DOM
// (e.g. for index.html which has its own header)
if (document.getElementById('hamburgerToggleButton') && document.getElementById('navMenu')) {
    //This check might be too early if navMenu is from nav-panel.html not yet loaded
    //initializeMenu();
}

// Listen for events indicating that parts of the DOM are ready
document.addEventListener('headerLoaded', () => {
    console.log("menu.js: headerLoaded event received.");
    tryInitializeMenu();
});
document.addEventListener('navPanelLoaded', () => {
    console.log("menu.js: navPanelLoaded event received.");
    tryInitializeMenu();
});
// Also try on DOMContentLoaded as a general fallback, especially if header/nav panel are static for some pages
document.addEventListener('DOMContentLoaded', () => {
    console.log("menu.js: DOMContentLoaded event received.");
    tryInitializeMenu();
});


function tryInitializeMenu() {
    if (window.menuInitialized) {
        // console.log("menu.js: Menu already initialized via another event.");
        return;
    }
    // Check if ALL required elements are now in the DOM
    const hamburgerToggle = document.getElementById('hamburgerToggleButton');
    const navMenu = document.getElementById('navMenu'); // This comes from nav-panel.html
    const navMenuOverlay = document.getElementById('navMenuOverlay'); // This also comes from nav-panel.html

    if (hamburgerToggle && navMenu && navMenuOverlay) {
        console.log("menu.js: All elements present, proceeding with initialization.");
        initializeMenu(hamburgerToggle, navMenu, navMenuOverlay);
        window.menuInitialized = true; // Set flag
    } else {
        // console.log("menu.js: Not all elements present yet. Hamburger:", !!hamburgerToggle, "NavMenu:", !!navMenu, "Overlay:", !!navMenuOverlay);
    }
}

function initializeMenu(hamburgerToggle, navMenu, navMenuOverlay) {
    console.log("menu.js: Initializing menu event listeners and functions...");

    const submenuToggles = navMenu.querySelectorAll('.submenu-toggle');
    // Logo elements might be in a separate header component or specific to index.html
    // For menu.js, focus on menu panel specific elements first.
    // const langFrLogo = document.querySelector('.lang-fr-logo');
    // const langEnLogo = document.querySelector('.lang-en-logo');

    function toggleMenu() {
        const isOpen = navMenu.classList.toggle('is-open');
        hamburgerToggle.setAttribute('aria-expanded', isOpen.toString());
        navMenu.setAttribute('aria-hidden', (!isOpen).toString());
        navMenuOverlay.classList.toggle('is-visible', isOpen);
        navMenuOverlay.setAttribute('aria-hidden', (!isOpen).toString());
        document.body.style.overflow = isOpen ? 'hidden' : '';

        if (!isOpen) {
            if (window.getComputedStyle(hamburgerToggle).display !== 'none') {
                 hamburgerToggle.focus();
            }
            submenuToggles.forEach(subToggle => {
                const submenu = document.getElementById(subToggle.getAttribute('aria-controls'));
                if (submenu && submenu.classList.contains('is-open')) {
                    submenu.classList.remove('is-open');
                    subToggle.setAttribute('aria-expanded', 'false');
                }
            });
        }
    }

    hamburgerToggle.addEventListener('click', toggleMenu);
    navMenuOverlay.addEventListener('click', toggleMenu);

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && navMenu.classList.contains('is-open')) {
            toggleMenu();
        }
    });

    navMenu.querySelectorAll('.nav-link').forEach(link => {
        if (!link.closest('li').querySelector('.submenu-toggle')) {
             link.addEventListener('click', (e) => { // Added event argument e
                if (navMenu.classList.contains('is-open')) {
                    if (link.getAttribute('href').startsWith('#') && window.location.pathname === link.pathname) { // Check if it's an anchor on the same page
                        toggleMenu();
                    } else if (!link.getAttribute('href').startsWith('#')) {
                        // For actual navigation to a new page, allow default behavior.
                        // Menu will "close" on page load. If it needs to animate out, more complex logic is needed.
                    }
                }
            });
        }
    });

    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const submenuId = toggle.getAttribute('aria-controls');
            const submenu = document.getElementById(submenuId);
            if (submenu) {
                const isSubmenuOpen = submenu.classList.toggle('is-open');
                toggle.setAttribute('aria-expanded', isSubmenuOpen.toString());
            }
        });
    });

    function updateActiveNavLink() {
        if (!navMenu) return; // Ensure navMenu is available
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        const currentHash = window.location.hash;

        navMenu.querySelectorAll('.nav-link').forEach(link => {
            const linkHref = link.getAttribute('href');
            const linkPath = linkHref.split('/').pop().split('#')[0] || 'index.html'; // Handle cases like href="/"
            const linkHash = linkHref.includes('#') ? '#' + linkHref.split('#')[1] : '';

            let isActive = false;
            if (linkPath === currentPath) {
                if (linkHash && currentHash) { // If both link and URL have hashes, they must match
                    isActive = linkHash === currentHash;
                } else if (linkHash && !currentHash && linkPath === 'index.html') {
                    // Special case for index.html anchor links from other pages, or if hash is default
                    // This might need refinement based on exact desired behavior for index.html anchors
                    isActive = false; // Default to false unless hash matches or no hash
                } else if (!linkHash) { // If link has no hash, it's active if paths match
                    isActive = true;
                }
            }

            // Special handling for the "Home" link when on index.html without a hash
            if (currentPath === 'index.html' && !currentHash && (linkPath === 'index.html' && !linkHash)) {
                isActive = true;
            }


            if (isActive) {
                link.classList.add('active');
                const parentSubmenuToggle = link.closest('.submenu')?.previousElementSibling;
                if (parentSubmenuToggle && parentSubmenuToggle.classList.contains('submenu-toggle')) {
                    parentSubmenuToggle.setAttribute('aria-expanded', 'true');
                    link.closest('.submenu').classList.add('is-open');
                }
            } else {
                link.classList.remove('active');
            }
        });
    }


    function updateLogoForLanguage(lang) {
        if (langFrLogo && langEnLogo) {
            langFrLogo.style.display = (lang === 'fr') ? 'block' : 'none';
            langEnLogo.style.display = (lang === 'en') ? 'block' : 'none';
        }
    }

    function updateLangButtonStates(lang) {
        document.querySelectorAll('.lang-button').forEach(btn => { // Query all lang buttons on page
            const isActive = btn.dataset.lang === lang;
            btn.classList.toggle('active-lang', isActive); // General active class
            if (btn.closest('.main-lang-switcher')) { // Header desktop switcher
                btn.classList.toggle('bg-white', isActive);
                btn.classList.toggle('text-[var(--primary-color)]', isActive);
                btn.classList.toggle('bg-opacity-10', !isActive); // Tailwind specific
                btn.classList.toggle('text-white', !isActive);
            } else if (btn.closest('.nav-menu-utils')) { // Mobile menu switcher
                 btn.classList.toggle('bg-white', isActive);
                 btn.classList.toggle('text-[var(--primary-color)]', isActive);
                 btn.classList.toggle('border-white', !isActive);
                 btn.classList.toggle('bg-transparent', !isActive);
            }
        });
    }

    let menuTranslations = {}; // To be populated from JSON

    fetch('i18n/translations.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status} while fetching translations.json`);
            }
            return response.json();
        })
        .then(data => {
            menuTranslations = data;
            console.log("menu.js: Menu translations loaded.");
            // After loading translations, re-apply to menu items based on current language
            const currentLang = localStorage.getItem('language') || (navigator.language || navigator.userLanguage || 'fr').slice(0,2);
            translateMenuItems(currentLang);
        })
        .catch(error => {
            console.error('Error loading menu translations:', error);
            // Fallback or error message can be handled here
        });

    function translateMenuItems(lang) {
        if (!navMenu || Object.keys(menuTranslations).length === 0) {
            // console.log("menu.js: navMenu not found or translations not loaded yet for translateMenuItems.");
            return;
        }
        navMenu.querySelectorAll('[data-lang-key]').forEach(el => {
            const key = el.dataset.langKey;
            if (el.classList.contains('lang-fr-link')) {
                el.style.display = (lang === 'fr') ? 'block' : 'none';
            } else if (el.classList.contains('lang-en-link')) {
                el.style.display = (lang === 'en') ? 'block' : 'none';
            } else {
                if (menuTranslations[key] && menuTranslations[key][lang]) {
                    el.textContent = menuTranslations[key][lang];
                } else {
                    // console.warn(`menu.js: No translation found for key '${key}' and lang '${lang}'`);
                }
            }
        });
    }

    function handleLanguageChange(lang) {
        updateLogoForLanguage(lang);
        updateLangButtonStates(lang);
        translateMenuItems(lang);
        updateActiveNavLink(); // Re-check active link as URLs might change for language-specific anchors
    }

    // Listen for the global languageChanged event from main.js
    document.addEventListener('languageChanged', (event) => {
        console.log("menu.js: languageChanged event received.", event.detail.lang);
        handleLanguageChange(event.detail.lang);
    });

    // Initial setup
    const initialLang = localStorage.getItem('language') || (navigator.language || navigator.userLanguage || 'fr').slice(0,2);
    console.log("menu.js: Initial language determined as:", initialLang);
    handleLanguageChange(initialLang);
    updateActiveNavLink(); // Call on load

    window.menuInitialized = true;
    console.log("menu.js: Menu initialization complete.");
}
