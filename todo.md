# Styling TODOs & Observations

This document lists items related to the application of `styles.css` that require further attention, decisions, or were out of scope for the initial pass.

## General Observations

*   **Hybrid Styling Approach:** Several pages (`index.html`, `cuga.html`, `docs/financial-governance.html`, `join.html`, `waiver.html`) now use a hybrid approach, with `styles.css` for global elements (header, footer) and Tailwind CSS (plus some local `<style>` blocks) for the main content. This was done to preserve complex existing layouts and JavaScript interactions. A future task could be to progressively refactor these main content areas to use the global style system if desired, or to formalize the hybrid approach.
*   **Font Consistency:** "Kumbh Sans" has been set as the primary font via `styles.css`. Pages that heavily use Tailwind might still have "Inter" or other Tailwind default fonts in their main content areas. Review for full font consistency if required.
*   **Tailwind Conflicts:** There's a potential for conflicts between `styles.css` and Tailwind CSS. While efforts were made to apply `styles.css` to distinct global areas, a thorough review of style overrides might be needed, especially on hybrid pages. For example, `index.html` had a `bg-blue-700` on the body which was removed as `styles.css` sets a default body background.

## Page-Specific TODOs

### `index.html`
*   **Page Subtitle/Tagline:** The main page subtitle and tagline (below the global CUGA header) are currently styled with inline styles and old Tailwind classes. These should ideally be refactored to use classes from `styles.css` or have dedicated classes added to `styles.css`.
*   **Side Navigation:** The floating side navigation (for in-page scrolling) is functional but uses Tailwind. Its styling could be integrated into `styles.css`. The FR/EN versions are duplicated in the HTML; this could be refactored to a single nav updated by JS.
*   **Button Styling:** Buttons within the main content (e.g., "Voir la liste des clubs CUGA", video tab buttons) use Tailwind. Consider migrating them to `.btn` classes from `styles.css` for consistency.
*   **Main Content Sections:** All main content sections (sports disciplines, nationals, about us, executive, contact) use Tailwind extensively.
*   **Footer Version Info:** The `version.json` script appends version info. Its styling is basic. This could be formalized in `styles.css`.

### `cuga.html` (Club Listings)
*   **Header Subtitle/Tagline:** Similar to `index.html`, the subtitle/tagline below the main logo needs proper styling via `styles.css`.
*   **Language Buttons:** The language toggle buttons are styled with Tailwind.
*   **Experimental Banner:** Styled with Tailwind.
*   **Filter Controls & Club Table:** The entire main content (filters, club listings table) is heavily reliant on Tailwind and JavaScript for its dynamic nature. Untouched by `styles.css`.
*   **Icon Links in Table:** Links for email, website, Facebook, etc., in the clubs table use FontAwesome icons and Tailwind.
*   **No Hamburger Menu:** This page doesn't have the global hamburger menu implemented in its header, as its primary navigation is the FR/EN language buttons and the content is very specific. Consider if global nav is needed here.

### `docs/financial-governance.html`
*   **Secondary Navigation Bar:** The sticky bar containing in-page navigation links and the language selector uses Tailwind and inline styles. This could be componentized in `styles.css`.
*   **Page Title in Secondary Nav:** The "Nonprofit Governance Guide" title in the secondary nav uses `text-primary-color` (from `styles.css` variables) but other styling is Tailwind.
*   **Main Content:** The entire interactive guide (introduction, access rights chart, legal framework accordions, restrictions cards, risks section, best practices checklist) uses Tailwind, custom CSS in `<style>`, and JavaScript.
*   **Font:** The page uses 'Inter' via its own `<style>` block, which is different from the global 'Kumbh Sans'. This should be reconciled. The Kumbh Sans link was added, but Inter is still declared in the local style block.

### `join.html`
*   **Page Subtitle:** The "Adhésion à CUGA / CUGA Membership" subtitle below the global header needs proper styling (currently `text-xl md:text-2xl font-bold`).
*   **Main Content Form:** The membership form is styled with Tailwind. Consider if form elements should adopt styles from `styles.css` (`.form-control`, `.form-label`, `.btn`).
*   **Button "Apply for Membership / Sign Waiver":** Uses Tailwind.

### `waiver.html`
*   **Page Subtitle:** "Décharge d'adhésion CUGA / CUGA Membership Waiver" subtitle needs styling.
*   **Main Content Form:** The waiver form is complex and styled with Tailwind. Similar to `join.html`, consider standardizing form elements with `styles.css`.
*   **Signature Pad:** Styling for the signature pad and related buttons is custom/Tailwind.
*   **Google Pay Button:** Custom/Tailwind styled.
*   **Modal/Success Message:** The submission result message uses Tailwind.

### `privacy-policy.html` & `terms-of-use.html`
*   **Content Styling:** These pages are simpler and now use `.container`. Headings (h1, h2) and paragraphs (p) should largely pick up global styles. A review to ensure all Tailwind utility classes for typography, color, and spacing have been appropriately replaced by global styles in the content areas would be good.
*   **Language Buttons:** Styled with Tailwind.

## General Next Steps / To Discuss
*   **Review Hybrid Pages:** Decide on a long-term strategy for pages using both `styles.css` and Tailwind.
*   **Component Prioritization:** Which common elements (beyond header/footer) should be prioritized for global styling next? (e.g., buttons, form elements, cards).
*   **JavaScript for Language Switching:** The JS for language switching has been adapted for global elements on each relevant page. This leads to some duplication of logic (e.g., `siteContent` objects, `setLanguage` structure). Consider refactoring into a shared JS module if possible, though page-specific element IDs might make this complex.
*   **Testing:** Thoroughly test all pages across different screen sizes and browsers to ensure layout and functionality are as expected after these changes. Pay special attention to the hybrid pages.
*   **Accessibility:** Review color contrast and focus states, especially for elements where Tailwind styling was retained or where new global styles were applied.
*   **AGENTS.md:** Ensure all changes comply with any instructions in `AGENTS.md` files if they exist in the repository (none were explicitly mentioned for this task).
*   **Favicon and Manifest:** The `site.webmanifest` and various favicon files (`favicon.ico`, `apple-touch-icon.png`, etc.) are present. Ensure they are correctly linked in the head of all HTML pages if not already. This was not part of the current task but is a general best practice. (Added `styles.css` link, but not these).
