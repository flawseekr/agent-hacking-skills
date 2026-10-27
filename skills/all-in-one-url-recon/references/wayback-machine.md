## Objective

Perform Wayback Machine reconnaissance. Verify that the Wayback Machine service is operational before proceeding, and keep the scope limited to the target.

## How To

1. Execute the following commands, replacing `<TARGET>` with the target domain **without the HTTP/HTTPS scheme**:

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=<TARGET>/*&output=text&fl=original&collapse=urlkey"
curl -s "https://web.archive.org/cdx/search/cdx?url=*.<TARGET>/*&output=text&fl=original&collapse=urlkey"
```

2. Preserve the raw output without filtering or curating the results.

3. Combine both command outputs into a single output file.

4. Extract lines beginning with `http`, then sort and deduplicate the results.

```bash
grep '^http' <RAW_OUTPUT> | sort -u
```

## Output

Save the temporary results to `wayback-output.txt`, containing one URL per line.

Example:

```text
https://example.com
https://example.com/test
https://example.com/signup
https://example.com/signup?param=value
https://example.com/assets/some.pdf
```
