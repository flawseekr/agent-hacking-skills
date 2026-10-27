---
name: all-in-one-url-recon
description: Perform comprehensive URL reconnaissance and validate findings against observed evidence.
---

## Objective

Perform comprehensive URL reconnaissance to discover, collect, and validate URLs, endpoints, and related resources from available sources. Base all findings on actual observations and verifiable evidence, without making hypotheses, prioritizing findings, or treating unverified results as confirmed.

## Workflow

Read the `Output` section to understand the objective.

1. Perform URL and endpoint discovery (reconnaissance) using any relevant methods necessary.

2. If references are needed, always check the skill's `references/` directory.

3. Research relevant techniques online to identify additional references and guidance.

4. If additional references are found, create separate documents in the working project directory, outside the skill's `references/` directory, following the Additional Reference Guide.

5. Perform reconnaissance sequentially in a continuous loop. Do not prioritize or rank URLs. Execute each action, observe the actual results, and use the collected evidence. Do not substitute assumptions or theoretical reasoning for actual execution. Base the final output exclusively on actions performed and results directly observed.

6. Work systematically and sequentially rather than in parallel. Coverage is more important than speed.

7. Once the URL and endpoint list has been collected, strictly validate each entry. Do not rely solely on HTTP status codes to determine whether a URL or endpoint is valid. Inspect the actual response content, headers, and behavior where relevant.

8. Clean up temporary files and unnecessary output. Keep only `FINDINGS.md`, output files, and relevant artifacts.

## Additional Reference Guide

Create additional reference documents in the working project directory, outside the skill's `references/` directory. Follow the existing reference format and conventions. Do not add reference content directly to the skill file.

Keep references simple, general, clear, and straight to the point.

## Validation

After all workflows are complete, consolidate the outputs from every technique into a single result. Normalize the output formats as necessary and ensure that all entries follow the required format.

Perform multi-step validation.

### First: HTTP Validation

For the first step, validate **GET requests only** using `tools/http-validator.py`.

Use the following default header:

```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36
```

- Ensure that the target does not return an SPA catch-all response. Observe and inspect the actual HTTP response.
- Compare the response against a nonexistent path appended to the end of the target path. **Do not use the root path as the comparison target.**
- Send the request to the actual target first, then perform the comparison. Never reverse this order.
- The goal is to identify and retain genuine pages rather than false positives caused by catch-all responses.

### Second: Browser Validation

Re-examine all entries flagged as potential SPA catch-all responses.

- Use a real browser to inspect the DOM and observe the rendered UI and functionality.
- Verify that the accessed page is genuinely distinct in its UI or behavior.
- Complete DOM observation **before including the entry in the final output**.
- Do not retain entries as valid pages without supporting browser-observed evidence.

### Third: Non-GET Request Validation

For non-GET requests, populate the required headers and request body based on the available evidence.

- Reconstruct the headers and request body using observed evidence whenever possible.
- If the request body cannot be fully reconstructed due to insufficient evidence, use `{}` only when appropriate for the endpoint and its content type.
- Preserve the correct HTTP method, URL, headers, and request body in the output.
- Do not treat an unverified request as confirmed merely because a response was received.

## Output

- Output must use JSONL format, with one valid JSON object per line.
- Each record must represent one observed URL and HTTP request.
- Follow the schema below. Include only evidence and values obtained from actual observations.
- Evidence must contain the raw response or DOM observation content, or a reference to the stored evidence.
- Set valid to true only when the resource has been verified using appropriate evidence. An HTTP status code of 200 alone is insufficient.

```json
{"url":"https://sub.example.com/dashboard","method":"GET","status_code":200,"response_content_type":"text/html","resource_type":"DIFFERENT-SPA","validation_method":"DOM_OBSERVATION","request":{"headers":{"User-Agent":"Mozilla/5.0"}},"evidence":{"raw_response":"String","dom_observation":"String"},"valid":true}

{"url":"https://sub.example.com/manifest.json","method":"GET","status_code":200,"response_content_type":"application/json","resource_type":"FILE","validation_method":"GET_ONLY","request":{"headers":{"User-Agent":"Mozilla/5.0"}},"evidence":{"raw_response":"String"},"valid":true}

{"url":"https://sub.example.com/hello","method":"GET","status_code":200,"response_content_type":"text/html","resource_type":"PAGE","validation_method":"GET_ONLY","request":{"headers":{"User-Agent":"Mozilla/5.0"}},"evidence":{"raw_response":"String"},"valid":true}

{"url":"https://sub.example.com/api/form","method":"POST","status_code":200,"response_content_type":"application/json","resource_type":"API","validation_method":"HTTP_REQUEST","request":{"headers":{"User-Agent":"Mozilla/5.0"},"body":{}},"evidence":{"raw_response":"String"},"valid":true}
```

## Evidence Guard

- There are four supported `resource_type` (values `DIFFERENT-SPA`, `PAGE`, `FILE`, and `API`. Use `DIFFERENT-SPA` only when DOM observation confirms that the resource is a distinct SPA experience.

- There are exactly 3 supported validation_method (values: `DOM_OBSERVATION`, `GET_ONLY` and `HTTP_REQUEST`). Use only these values.
