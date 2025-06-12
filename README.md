# CUGA.ca Website

This repository contains the source code for the Canadian Underwater Games Association (CUGA) website, hosted at [cuga.ca](https://www.cuga.ca).

The site provides information about underwater sports in Canada, primarily focusing on:
*   Underwater Hockey
*   Underwater Rugby
*   Underwater Football

It also features a directory of underwater sports clubs across Canada.

This website is a fork and modification of the original camosub.ca codebase.

## Website Pages and Features

This website includes the following key pages:

*   **`index.html`**: The main landing page with information about CUGA, its sports disciplines (Underwater Hockey, Rugby, and Football), club listings, and contact information. It features a language switcher for English and French content.
*   **`cuga.html`**: Lists CUGA affiliated clubs across Canada. (Note: This page might be integrated or superseded by dynamic club listings on `index.html` in future updates).
*   **`join.html`**: Provides detailed information about CUGA membership options, benefits, and the process for joining.
    *   **Fully Bilingual**: Content is available in English and French, with a language switcher and auto-detection.
    *   **Streamlined Process**: The previous placeholder PayPal button has been removed. Instead, a clear call-to-action button directs users to the `waiver.html` page to start their application.
*   **`waiver.html`**: An interactive membership application and waiver form that allows users to:
    *   Enter their personal and emergency contact details.
    *   Provide their club name (optional) and select sports played (Underwater Hockey, Rugby, Football) via checkboxes.
    *   Select a membership type (Adult, Youth, New Player).
    *   View dynamically calculated membership fees, including logic for early bird pricing (before March 1st) versus regular season pricing.
    *   View the full official CUGA waiver text within a scrollable area on the page.
    *   Provide their initials in a dedicated input field, as required by the waiver text.
    *   Sign digitally using an interactive signature pad (implemented with `signature_pad.js` library via CDN). Functionality includes a "Clear Signature" button and a fallback to a typed signature input if the library fails to load.
    *   Electronically agree to the CUGA Code of Conduct and the terms of the waiver via checkboxes.
    *   **Fully Bilingual Interface**: The entire page, including form labels, dynamic messages, and buttons, is available in English and French, with a language switcher and auto-detection based on browser preference.
    *   **Simulated Google Pay Integration**: The form features a "Pay with Google Pay" button. This is a **front-end simulation only** and does **not** process any real financial transactions or connect to Google Pay services.
    *   **Enhanced Simulated Data Submission & Confirmation**:
        *   Upon completing the form and "payment" (or for $0 fee memberships), an on-page confirmation message is displayed bilingually, indicating success and outlining fictional next steps (e.g., "You will receive a confirmation email shortly").
        *   The main form sections are hidden, and options are provided to "Start a new application" (which resets the form and view) or "Go to Homepage".
        *   Member data is **not** actually sent to a Google Drive sheet. Instead, the collected data is logged to the browser's developer console. This data includes all form fields: personal details, club name, selected sports (as a comma-separated string if multiple), membership type, calculated fee, waiver initials, the signature (as a Base64 data URL from the canvas, or typed text if fallback was used), the printed name for the signature, and a timestamp of the submission. The form is then reset.
    *   *Note on Waiver Presentation*: The signature is captured against the waiver text displayed as HTML content within a scrollable section. The stretch goal to render the full waiver text onto a single, combined image canvas with the signature for download was not implemented due to its complexity.

**Common Elements:**
*   **Language Selector**: All main pages (`index.html`, `join.html`, `waiver.html`) feature a language selector for switching between English and French. The user's manual language selection now persists across pages and sessions by using `localStorage`. If no preference is stored, language is auto-detected from the browser on the first visit, and this auto-detected choice also becomes persistent until manually changed.
*   **Prototype Disclaimer**: The prototype disclaimer banner, providing a link to the official `cuga.org` website, is consistently displayed at the top of `index.html`, `join.html`, and `waiver.html`. It is positioned after the language selector and before the main page header for site-wide visibility.

**Important Note on Simulations:** The payment and data submission functionalities on `waiver.html` are currently client-side simulations. No real payments are processed, and no data is transmitted to a live backend or cloud storage. These features are implemented to showcase the intended user workflow.
