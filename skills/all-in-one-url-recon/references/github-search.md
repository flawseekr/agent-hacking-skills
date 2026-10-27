## Objective

Perform reconnaissance using GitHub Code Search through the authenticated GitHub CLI (`gh`).

## Prerequisites

- Check whether the `gh` command is installed and verify that the user is authenticated.

- If `gh` is installed but the user is not authenticated:
  1. Instruct the user to log in using `gh auth login`.
  2. Verify authentication before proceeding.

- If `gh` is not installed:
  1. Open `https://api.github.com/repos/cli/cli/releases/latest`.
  2. List the available `browser_download_url` values from the response.
  3. Filter the download links and select the appropriate binary for the user's operating system and architecture.
  4. Provide the user with the download link.
  5. Provide installation instructions appropriate for the user's environment.
  6. Guide the user through authentication using `gh auth login`.
  7. Verify installation and authentication before proceeding.

## Workflow

1. Search GitHub code for TARGET using the following command:

```bash
gh search code "<TARGET>" --limit 1000 --json url,textMatches --jq '.[] | "\(.url)"'
```

2. Inspect every returned repository URL and identify the relevant source files and file context.

3. Extract relevant URLs, endpoints, and other security-relevant information from the available evidence.

4. If source code is available, reconstruct endpoints and related behavior by correlating actual code evidence across files, treating the process like solving a puzzle. **Never guess or invent missing details. Evidence takes precedence over assumptions.**

- Record the discovered repository URLs, relevant source files, extracted endpoints, and security-relevant information.
- Include evidence for each finding, such as source snippets, file URLs, and line numbers where available.
- Clearly distinguish confirmed findings from plausible leads and unresolved items.
- Do not report unverified assumptions as facts.

## Output

Save the temporary results to `github-output.txt`, containing one URL per line.

Example:

```text
https://example.com
https://example.com/test
https://example.com/signup
https://example.com/signup?param=value
https://example.com/assets/some.pdf
```

If any non-GET requests are identified, record them in the following format:

```text
POST https://example.com/submit (headers={}) (data=data)
PUT https://api.example.com/v1/some-api (headers={}) (data={"data":"value"})
```
