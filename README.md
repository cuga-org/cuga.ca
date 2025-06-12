# CUGA.ca Website

This repository contains the source code for the Canadian Underwater Games Association (CUGA) website, hosted at [cuga.ca](https://www.cuga.ca).

The site provides information about underwater sports in Canada, primarily focusing on:
*   Underwater Hockey
*   Underwater Rugby
*   Underwater Football

It also features a directory of underwater sports clubs across Canada.

This website is a fork and modification of the original camosub.ca codebase.

## Event Calendar (.ics) Generation

This repository includes an automated system for generating iCalendar (`.ics`) files for club events. These files can be imported into most calendar applications.

### Overview

-   **Script**: The `generate_ics.js` Node.js script located in the root directory is responsible for fetching club schedule data from the same Google Sheet used by `cuga.html`. It then processes this data and uses the Google Gemini API to generate iCalendar event information.
-   **Output**: Generated `.ics` files, typically one for each club or event series, are stored in the `/events` directory.
-   **Automation**: The process is automated by a GitHub Actions workflow defined in `.github/workflows/generate_events_ics.yml`. This workflow runs daily, executes the `generate_ics.js` script, and commits any new or updated `.ics` files back to the `events/` directory in the repository.

### Setup for Automation

For the automated workflow to successfully generate and update `.ics` files, a repository secret must be configured in your GitHub repository settings:

-   **`GEMINI_API_KEY`**: You must add your Google Gemini API key as a secret named `GEMINI_API_KEY`. This can be found under your repository's `Settings` > `Secrets and variables` > `Actions` > `New repository secret`.

Without this secret, the `generate_ics.js` script will fail when attempting to contact the Gemini API, and no `.ics` files will be generated or updated.
