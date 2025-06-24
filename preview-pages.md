# Reusable Workflow: Deploy Static Preview Pages

This document describes how to use the `preview-pages.yml` reusable workflow to deploy static content (like HTML/CSS/JS sites, Storybooks, etc.) to GitHub Pages. It's designed to deploy the default branch of your repository to the root of the GitHub Pages site and individual Pull Request previews into subdirectories.

## Features

*   Deploys the content of your default branch (e.g., `main`) to the root of your GitHub Pages site.
*   For every open Pull Request, it deploys its content to a subdirectory: `/previews/PR_NUMBER/`.
*   Generates a `version.json` at the site root, listing the commit SHA of the default branch and details of all included PR previews.
*   Generates a `version.json` within each PR's preview directory, listing its specific commit SHA, branch name, and PR number.
*   Optionally lints an HTML file in the PR's content.
*   Optionally runs a build command for the PR's content (and for each subsequent PR preview) if your site requires a build step.
*   Posts a comment on the active Pull Request with a direct link to its preview and a list of other PRs included in the deployment.

## How to Use

To use this reusable workflow, you'll call it from a workflow in your own repository.

### 1. Prerequisites in Your Repository

*   **Enable GitHub Pages**: In your repository settings, under "Pages", ensure GitHub Pages is enabled. The source should be set to "GitHub Actions".
*   **Repository Secrets**: You must create a repository secret named `CALLING_REPO_WORKFLOW_TOKEN` (or whatever name you choose to pass to the `secrets` block in the job calling the reusable workflow). This token needs specific permissions to allow the reusable workflow to:
    *   Read your repository content (`contents: read`)
    *   Write to GitHub Pages (`pages: write`)
    *   Write comments on Pull Requests (`pull-requests: write`)
    *   Obtain an OIDC token for GitHub Pages deployment (`id-token: write`)
    A Personal Access Token (PAT) with `repo` and `workflow` scopes can be used, or a GitHub App with the granular permissions mentioned. For security, prefer a token with the minimum necessary permissions.

### 2. Example Calling Workflow

Create a new workflow file in your repository (e.g., `.github/workflows/deploy-previews.yml`):

```yaml
name: Deploy Previews using Reusable Workflow

on:
  pull_request:
    types: [opened, synchronize, reopened, closed] # Trigger on PR changes and closure to update/remove previews

jobs:
  deploy_all_previews:
    # Only run on open, synchronize, reopened.
    # For 'closed' PRs, the reusable workflow logic will naturally exclude it from 'get_open_prs',
    # effectively removing its preview from the *next* deployment triggered by another PR event.
    # A dedicated cleanup on PR close might be more immediate but adds complexity.
    # This setup ensures previews are for currently open PRs.
    if: github.event.action != 'closed' && github.event.pull_request.draft == false

    # Use the path to the reusable workflow: {owner}/{repo}/.github/workflows/{filename}@{ref}
    # Replace {owner}, {repo}, {filename}, and {ref} with the actual values for the repository
    # hosting the preview-pages.yml workflow.
    uses: <OWNER>/<REPO>/.github/workflows/preview-pages.yml@main # Or specific tag/SHA
    with:
      calling_repo_owner: ${{ github.repository_owner }}
      calling_repo_name: ${{ github.event.repository.name }}
      pr_number: ${{ github.event.pull_request.number }}
      pr_head_ref: ${{ github.event.pull_request.head.ref }}
      default_branch: ${{ github.event.repository.default_branch || 'main' }} # Or your specific default branch
      cname_domain: 'your.custom.domain.com' # Optional: Your custom domain for GitHub Pages
      lint_file_path: 'index.html' # Optional: Path to HTML file to lint, or '' to disable
      build_command: 'npm install && npm run build' # Optional: Command to build your site
      static_site_path: 'dist' # Optional: Path to built static files, relative to PR root (e.g., 'dist', 'build', '_site')

    secrets:
      CALLING_REPO_TOKEN: ${{ secrets.CALLING_REPO_WORKFLOW_TOKEN }} # Name of the secret you created in your repo
```

**Important**:
*   Replace `<OWNER>/<REPO>` in the `uses:` line with the actual owner and repository name where this `preview-pages.yml` reusable workflow is located.
*   Adjust `default_branch` if your repository's default branch is not `main`.
*   If your project doesn't require a build step, you can omit `build_command` and `static_site_path` (or set `build_command: ''` and `static_site_path: '.'`).
*   If you don't use a custom domain for GitHub Pages, omit the `cname_domain` input.
*   The `CALLING_REPO_WORKFLOW_TOKEN` secret name in the calling workflow must match the name you created in your repository's secrets settings.

### Inputs for the Reusable Workflow

The reusable workflow (`preview-pages.yml`) accepts the following inputs:

| Input Name           | Type   | Required | Default Value | Description                                                                                                |
|----------------------|--------|----------|---------------|------------------------------------------------------------------------------------------------------------|
| `calling_repo_owner` | string | Yes      |               | Owner of the calling repository (e.g., `github.repository_owner`).                                       |
| `calling_repo_name`  | string | Yes      |               | Name of the calling repository (e.g., `github.event.repository.name`).                                   |
| `pr_number`          | number | Yes      |               | Pull Request number from the calling repository that triggered the workflow.                               |
| `pr_head_ref`        | string | Yes      |               | Head ref (branch name) of the PR from the calling repository.                                              |
| `default_branch`     | string | Yes      |               | Default branch name of the calling repository (e.g., 'main', 'master').                                    |
| `cname_domain`       | string | No       | `''`          | Optional: Custom domain (CNAME) for GitHub Pages. If provided, used for constructing preview URLs.         |
| `lint_file_path`     | string | No       | `index.html`  | Optional: Path to the HTML file to lint in the PR content, relative to PR root. Set to `''` to disable. |
| `build_command`      | string | No       | `''`          | Optional: Command to build the static site (e.g., "npm install && npm run build"). Runs in PR content dir. |
| `static_site_path`   | string | No       | `.`           | Optional: Path to generated static files after build, relative to PR root (e.g. 'dist', 'build').          |

### Secrets for the Reusable Workflow

The reusable workflow requires the following secret to be passed from the calling workflow:

| Secret Name          | Required | Description                                                                                                                                                                                                                            |
|----------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `CALLING_REPO_TOKEN` | Yes      | A GitHub token (PAT or from a GitHub App) with permissions in the *calling repository*: `pages: write`, `contents: read`, `pull-requests: write`, `id-token: write`. This token is used to perform actions on behalf of your repository. |

## Site Structure

After a successful deployment, your GitHub Pages site will be structured as follows:

*   **Root (`/`)**: Contains the content from your repository's `default_branch`.
    *   `/version.json`: Contains the commit SHA of the `default_branch` and a list of all PRs currently being previewed.
*   **PR Previews (`/previews/PR_NUMBER/`)**: Each open PR gets its own subdirectory.
    *   `/previews/PR_NUMBER/version.json`: Contains the commit SHA, branch name, and PR number for that specific preview.

## How PR Preview Removal Works

When this workflow runs, it ensures that the deployed GitHub Pages site accurately reflects the current state of open Pull Requests. Here's how previews for closed or merged PRs are handled:

1.  **Fetching Open PRs**: At the beginning of each workflow run, the `Get open PRs` step fetches the list of all *currently open* Pull Requests in the calling repository.
2.  **Cleaning Previews Directory**: Before populating any PR previews, the `Populate All PR Previews` script completely removes and recreates the `previews` subdirectory (e.g., `MAIN_CONTENT_PATH/previews/` or `temp_deploy/previews/`) within the staging area for the site. This ensures a clean slate for each deployment.
3.  **Populating Active Previews**: The script then iterates *only* through the list of currently open PRs. For each open PR, it checks out the code, optionally builds it, and copies the content into its respective subdirectory (e.g., `previews/PR_NUMBER/`).
4.  **Deployment**: The entire staging area (including the newly populated `previews` directory which now only contains active PRs) is then uploaded as the GitHub Pages artifact and deployed.

**Effectively, if a Pull Request was previously open and had a preview, but is now closed or merged:**
*   It will not be in the list of open PRs.
*   The `previews` directory is wiped clean before new previews are generated.
*   The closed/merged PR's content will not be copied into the `previews` directory during the current run.
*   Therefore, its preview subdirectory will not exist in the artifact uploaded to GitHub Pages, and it will be removed from the live site upon deployment.

This mechanism ensures that the deployed site only contains previews for PRs that are currently open, providing an up-to-date view of ongoing changes.

## Troubleshooting

*   **Permissions Issues**: Double-check the permissions of the `CALLING_REPO_TOKEN`. Ensure it has all required scopes/permissions listed above.
*   **Workflow Not Triggering**: Verify the `on:` trigger in your calling workflow matches the events you expect (e.g., `pull_request` types).
*   **Build Failures**: If using `build_command`, check the logs of the "Build static site" step in the reusable workflow's run for errors. Ensure all necessary dependencies are installed by your build command.
*   **Incorrect URLs in PR Comment**: If `cname_domain` is used, ensure it's correctly set without `http://` or `https://`. If not used, ensure your repository name and owner are simple and don't cause issues with GitHub Pages URL generation.
*   **Content Not Updating**: Ensure the `ref` in your `uses:` line for the reusable workflow points to the latest/correct version (e.g., `@main` or a specific tag like `@v1.0.0`).
```
