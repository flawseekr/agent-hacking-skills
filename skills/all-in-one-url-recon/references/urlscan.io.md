## Objective

Perform urlscan.io reconnaissance. urlscan.io stores historical scans of web pages; each scan records the primary page URL plus every resource URL the page loaded. Query it to collect URLs and endpoints for the target, then keep the scope limited to the target.

## Prerequisites

- The public Search API needs no authentication but is rate-limited. For higher limits, send an `API-Key: <key>` header.
- Verify the service is reachable before proceeding (expect HTTP 200 from the search endpoint).

## How To

1. Search scans for the target. Use `page.domain:` to match scans whose primary page is on the target, and `domain:` to also match scans where the target appears as a subresource or link. Replace `<TARGET>` with the domain, no scheme.

```bash
curl -s "https://urlscan.io/api/v1/search/?q=page.domain:<TARGET>&size=100"
curl -s "https://urlscan.io/api/v1/search/?q=domain:<TARGET>&size=100"
```

2. Extract URLs from each result. Relevant fields per result: `page.url` (the scanned page), `task.url` (the submitted URL), `page.domain`, `_id` (scan UUID), `result` (result-API URL), `sort` (pagination cursor).

```bash
curl -s "https://urlscan.io/api/v1/search/?q=page.domain:<TARGET>&size=100" \
  | python3 -c "import sys,json;[print(r['page']['url']) for r in json.load(sys.stdin)['results']]"
```

3. Paginate while `has_more` is `true`. Pass the `sort` array of the last result as `search_after` (comma-joined). Continue until `has_more` is `false`.

```bash
curl -s "https://urlscan.io/api/v1/search/?q=page.domain:<TARGET>&size=100&search_after=<sort0>,<sort1>"
```

4. For each relevant scan, optionally pull the full resource list from the result API. `lists.urls` contains every resource URL loaded during the scan; `lists.linkDomains`, `lists.domains`, and `lists.ips` give related hosts. A private/unlisted scan returns HTTP 403 — skip it.

```bash
curl -s "https://urlscan.io/api/v1/result/<SCAN_UUID>/" \
  | python3 -c "import sys,json;[print(u) for u in json.load(sys.stdin).get('lists',{}).get('urls',[])]"
```

5. Filter all collected URLs to the target domain and preserve the raw results without curating. Record useful related hosts separately.

## Output

Save the temporary results to `urlscan-output.txt`, containing one URL per line.

```text
https://example.com
https://example.com/test
https://example.com/signup
https://example.com/signup?param=value
https://example.com/assets/some.pdf
```
