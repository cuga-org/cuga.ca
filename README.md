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
    *   Select a membership type (Adult, Youth, New Player).
    *   View dynamically calculated membership fees, including logic for early bird pricing (before March 1st) versus regular season pricing.
    *   Electronically agree to the CUGA Code of Conduct and the terms of the applicable waiver.
    *   **Fully Bilingual Interface**: The entire page, including form labels, dynamic messages, and buttons, is available in English and French, with a language switcher and auto-detection based on browser preference.
    *   **Simulated Google Pay Integration**: The form features a "Pay with Google Pay" button. This is a **front-end simulation only** and does **not** process any real financial transactions or connect to Google Pay services.
    *   **Enhanced Simulated Data Submission & Confirmation**:
        *   Upon completing the form and "payment" (or for $0 fee memberships), an on-page confirmation message is displayed bilingually, indicating success and outlining fictional next steps (e.g., "You will receive a confirmation email shortly").
        *   The form area is hidden, and options are provided to "Start a new application" (which resets the form and view) or "Go to Homepage".
        *   Member data is **not** actually sent to a Google Drive sheet. Instead, the collected data (including member details, calculated fee, and a timestamp) is logged to the browser's developer console for demonstration and testing purposes. The form is then reset.

**Important Note on Simulations:** The payment and data submission functionalities on `waiver.html` are currently client-side simulations. No real payments are processed, and no data is transmitted to a live backend or cloud storage. These features are implemented to showcase the intended user workflow.
