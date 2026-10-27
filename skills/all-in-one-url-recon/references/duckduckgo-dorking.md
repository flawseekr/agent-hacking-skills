## Objective

Perform duckduckgo dorking operation using a real browser through Playwright, MCP, or equivalent browser automation tools. Never force the use of curl, raw HTTP requests, or other non-browser methods as substitutes.

## Step by Step

1. Navigate to `https://html.duckduckgo.com/html/?q=site:<TARGET>`.
2. Extract results from each page using `browser_evaluate`, filtering all results to include only URLs hosted on the target domain.
3. Paginate through every results page. Continue looping while `hasNext` is `true` and stop only when `hasNext` is `false`.
4. Temporarily save ALL raw results without deduplication.

## Temporary Output

Save the temporary results to `duckduckgo-output.txt`, containing one URL per line.

```
https://example.com
https://example.com/test
https://example.com/signup
https://example.com/signup?param=value
https://example.com/assets/some.pdf
```
