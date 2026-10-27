---
name: browser-exploration-loop
description: Execute the browser-exploration skill using a real browser
---

## Objective

Capture all network traffic in a `.har` file for further analysis. Generate the HAR file from actual browser execution, including static page requests, DOM loading, state-changing requests, and all subsequent network activity throughout the entire exploration workflow.

## Precondition

- Ensure browser access is available through Playwright or MCP. If unavailable, do not fabricate requests using `curl`, raw HTTP requests, or similar tools; cancel skill execution and inform the user: "I cannot access the browser!"

- Before starting exploration, ensure the browser's Network Tools are enabled to capture and export the `.har` file throughout the entire workflow, starting from the beginning.

## Workflow

- Open the target, inspect its UI and DOM, explore every menu, fill out any forms using test data, and record all findings and interaction states in `browsing-state.json`.

- Always record every new finding, including menus or pages and forms. Set its state to `NEW`.

- Never mark a form or any input as `DONE` unless it has been filled in and submitted. Always fill in every discovered form and input whenever possible to ensure accurate exploration coverage. If submission is error, record the reason and keep its state incomplete.

- `DONE` statement is only allowed after actual execution and verified observation. Never mark any item as `DONE` based on assumptions, reasoning, intentions, or unverified results.

- Always review all items whose state is not `DONE` and execute the required actions until they are completed.

- Repeat this loop until all exploration tasks are exhausted. Prepare and execute a script to repeatedly run this skill, treating the script's execution state and output as the source of truth. Never rely on independent reasoning to override the script's results.
