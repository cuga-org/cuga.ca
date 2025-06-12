# CUGA.ca Website

This repository contains the source code for the Canadian Underwater Games Association (CUGA) website, hosted at [cuga.ca](https://www.cuga.ca).

The site provides information about underwater sports in Canada, primarily focusing on:
*   Underwater Hockey
*   Underwater Rugby
*   Underwater Football

It also features a directory of underwater sports clubs across Canada.

This website is a fork and modification of the original camosub.ca codebase.


## Automated iCalendar Event Generation

This repository includes a system for automatically generating iCalendar (`.ics`) event files from a designated Google Sheet. This system utilizes the Google Gemini API to interpret event data and create structured calendar entries.

### Components

*   **`event_generator.py`**: A Python script responsible for:
    *   Fetching data from the public Google Sheet.
    *   Generating prompts for each event.
    *   Interacting with the Google Gemini API to obtain iCalendar VEVENT components.
    *   Consolidating generated events into a single `.ics` file.
    *   Tracking processed events to prevent duplicates.
*   **`.github/workflows/generate_calendar.yml`**: A GitHub Actions workflow that:
    *   Automates the execution of `event_generator.py` on a daily schedule.
    *   Can also be triggered manually.
    *   Commits the updated `generated_events.ics` and `processed_prompts.txt` files back to the repository if changes are detected.
*   **`requirements.txt`**: Lists the necessary Python dependencies for the `event_generator.py` script (e.g., `requests`, `icalendar`, `google-generativeai`).
*   **`processed_prompts.txt`**: This file stores a unique fingerprint for each event that has been successfully processed by the Gemini API. The `event_generator.py` script uses this file to avoid reprocessing the same event and making redundant API calls. It is automatically created and managed by the script.
*   **`generated_events.ics`**: The main output iCalendar file containing all the generated events. This file can be imported into most calendar applications.

### Google Sheet Data Source

The script currently fetches data from the following public Google Sheet:
[https://docs.google.com/spreadsheets/d/1Lk8Lq5gu-nI1dwZjWZqYM05-x4E-5kD_huPsW-28AMo/gviz/tq](https://docs.google.com/spreadsheets/d/1Lk8Lq5gu-nI1dwZjWZqYM05-x4E-5kD_huPsW-28AMo/gviz/tq)

The script is designed to parse specific columns from this sheet, including but not limited to:
*   `Club Name` (and `Club Name FR` for French)
*   `Province` (and `Province FR`)
*   `City` (and `City FR`)
*   `Practice Location` (and `Practice Location FR`)
*   `Practice Times` (and `Practice Times FR`)
*   `Notes` (and `Notes FR`)
*   `RRULE` (for recurrence information)

### Gemini API Key Setup

To enable the generation of calendar events using the Gemini API, a valid API key is required.

1.  Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  In your GitHub repository, navigate to `Settings` > `Secrets and variables` > `Actions`.
3.  Create a new repository secret named `GEMINI_API_KEY` and paste your API key as the value.

The GitHub Actions workflow (`generate_calendar.yml`) is configured to use this secret to authenticate with the Gemini API. If the `GEMINI_API_KEY` is not provided, the script will skip live API calls and use mock data, resulting in placeholder calendar events.

### Workflow Operation

*   **Triggers**: The workflow runs automatically every day at midnight UTC. It can also be manually triggered from the Actions tab in the GitHub repository.
*   **Process**:
    1.  Checks out the latest code.
    2.  Sets up a Python environment and installs dependencies.
    3.  Executes `event_generator.py` (using the `GEMINI_API_KEY`).
    4.  If `generated_events.ics` or `processed_prompts.txt` have been modified by the script, the workflow commits these changes back to the main branch of the repository.

### Output

The primary output of this system is the `generated_events.ics` file located in the root of the repository. This file is updated automatically by the workflow.
