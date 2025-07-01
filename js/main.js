// General JavaScript for the site (e.g., language switcher, animations)
document.addEventListener('DOMContentLoaded', () => {
    console.log("main.js loaded");

    // Language Switcher Logic (adapted from index.html)
    const langButtons = document.querySelectorAll('.lang-button');
    const langSections = document.querySelectorAll('.lang-fr, .lang-en'); // Will target all elements with these classes

    const setLanguage = (lang) => {
        // Hide all language-specific sections first
        document.querySelectorAll('.lang-fr, .lang-en').forEach(section => {
            section.style.display = 'none';
        });

        // Show sections for the selected language
        // This needs to be smart if a page doesn't have both fr/en for all its content blocks
        // For now, this assumes top-level containers like <div class="lang-fr">...</div> in each page's main content area
        document.querySelectorAll(`.lang-${lang}`).forEach(section => {
            section.style.display = 'block'; // Or appropriate display type
        });

        langButtons.forEach(button => {
            const isSelected = button.dataset.lang === lang;
            button.classList.toggle('bg-blue-600', isSelected); // Tailwind active state
            button.classList.toggle('text-white', isSelected);
            button.classList.toggle('bg-gray-400', !isSelected); // Tailwind inactive state
            button.classList.toggle('text-gray-800', !isSelected);
        });
        document.documentElement.lang = lang;
        localStorage.setItem('language', lang);

        // Dispatch custom event
        console.log(`main.js: dispatching languageChanged event for ${lang}`);
        document.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: lang } }));
    };

    // Initialize language
    const storedLang = localStorage.getItem('language');
    if (storedLang) {
        setLanguage(storedLang);
    } else {
        const browserLang = (navigator.language || navigator.userLanguage || 'fr').slice(0, 2);
        setLanguage(browserLang === 'en' ? 'en' : 'fr');
    }

    langButtons.forEach(button => {
        button.addEventListener('click', () => setLanguage(button.dataset.lang));
    });

    // AOS Initialization (already in individual HTML files, but can be centralized if preferred)
    // AOS.init({
    //     duration: 1000,
    //     once: true,
    // });

    // Bubble animation (from index.html - might need adjustment for multiple pages if fixed positioning is an issue)
    const bubblesContainer = document.querySelector('.bubbles'); // Assumes one .bubbles container per page or a global one
    if (bubblesContainer) {
        function createBubble() {
            const bubble = document.createElement('div');
            bubble.classList.add('bubble');
            const size = Math.random() * 40 + 10;
            bubble.style.width = `${size}px`;
            bubble.style.height = `${size}px`;
            bubble.style.left = `${Math.random() * 100}%`;
            const animationDuration = Math.random() * 10 + 5;
            bubble.style.animationDuration = `${animationDuration}s`;
            bubblesContainer.appendChild(bubble);
            setTimeout(() => {
                bubble.remove();
            }, animationDuration * 1000);
        }
        setInterval(createBubble, 500);
    }

    // Version info (from index.html) - this can be part of a shared footer loading script
    function appendVersionInfoToFooters(element) {
        // This function will be called for each page.
        // It assumes footers will have a specific structure or a common class to append to.
        // For now, let's assume the shared footer (when implemented) will have a known structure.
        // If using placeholder <footer id="shared-footer">, this needs to be more robust or run after footer is populated.
      const footerContainerFr = document.querySelector('#shared-footer.lang-fr .container:last-of-type'); // Placeholder
      const footerContainerEn = document.querySelector('#shared-footer.lang-en .container:last-of-type'); // Placeholder

      if (footerContainerFr) footerContainerFr.appendChild(element.cloneNode(true));
      if (footerContainerEn) footerContainerEn.appendChild(element.cloneNode(true));
      // If footers are not language specific at this point, a single query is enough
      // const footerContainer = document.querySelector('#shared-footer .container:last-of-type');
      // if (footerContainer) footerContainer.appendChild(element.cloneNode(true));
    }

    function createVersionElement(text, isError) {
      const versionP = document.createElement('p');
      versionP.classList.add('text-xs', 'text-center', 'mt-4', 'pt-2', 'border-t', 'border-gray-600');
      versionP.textContent = text;
      if (isError) {
        versionP.classList.add('text-red-600');
      } else {
        versionP.classList.add('text-gray-500');
      }
      return versionP;
    }

    // Version info injection - now waits for footerLoaded event
    document.addEventListener('footerLoaded', () => {
        console.log("main.js: footerLoaded event received, attempting to inject version info.");
        fetch('version.json')
          .then(response => {
            if (!response.ok) {
              throw new Error('version.json not found or invalid');
            }
            return response.json();
          })
          .then(data => {
            const versionText = `Version: Branch: ${data.branch || 'main'} | Commit: ${data.commit ? data.commit.substring(0, 7) : 'N/A'}`;
            const versionElement = createVersionElement(versionText, false); // Assuming createVersionElement is defined above
            const versionContainer = document.getElementById('version-info-container');
            if (versionContainer) {
                versionContainer.innerHTML = ''; // Clear previous content if any
                versionContainer.appendChild(versionElement);
                console.log("main.js: Version info injected.");
            } else {
                console.warn("main.js: version-info-container not found after footerLoaded.");
            }
          })
          .catch(error => {
            console.warn('Could not load version information:', error);
            const errorText = 'Version info not available';
            const errorElement = createVersionElement(errorText, true);
            const versionContainer = document.getElementById('version-info-container');
            if (versionContainer) {
                versionContainer.innerHTML = ''; // Clear previous content
                versionContainer.appendChild(errorElement);
            }
          });
    });

    // BF Cache handling for language
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            const lang = localStorage.getItem('language');
            if (lang) {
                setLanguage(lang);
            } else {
                const browserLang = (navigator.language || navigator.userLanguage || 'fr').slice(0, 2);
                setLanguage(browserLang === 'en' ? 'en' : 'fr');
            }
        }
    });
});
