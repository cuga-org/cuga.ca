// JavaScript for hamburger menu functionality
document.addEventListener('headerLoaded', initializeMenu);
// Fallback if headerLoaded is too late or doesn't fire (e.g. if menu.js loads after header is already in DOM)
// or if header is not dynamically loaded on a particular page (though current setup does load dynamically)
if (document.getElementById('hamburgerToggleButton')) {
    initializeMenu();
}


function initializeMenu() {
    // Prevent multiple initializations if headerLoaded fires and elements are already there
    if (window.menuInitialized) {
        console.log("menu.js: Menu already initialized.");
        return;
    }
    console.log("menu.js: Initializing menu...");

    const hamburgerToggle = document.getElementById('hamburgerToggleButton');
    const navMenu = document.getElementById('navMenu');
    const navMenuOverlay = document.getElementById('navMenuOverlay');

    // Check if essential menu elements exist
    if (!hamburgerToggle || !navMenu || !navMenuOverlay) {
        console.error("menu.js: Essential menu elements not found. Initialization aborted.");
        return;
    }

    const submenuToggles = navMenu.querySelectorAll('.submenu-toggle');
    const langFrLogo = document.querySelector('.lang-fr-logo'); // Assumes it's in the loaded header
    const langEnLogo = document.querySelector('.lang-en-logo'); // Assumes it's in the loaded header

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
