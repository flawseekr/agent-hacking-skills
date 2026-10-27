## Objective

Perform comprehensive, recursive resource discovery across the target application and relevant public sources. Identify, collect, and validate JavaScript, HTML, source maps, manifests, configuration files, API-related resources, and other observeable assets. Follow resource references recursively until no new resources are discovered. Base all results on actual observations and verifiable evidence, without relying solely on file extensions, URL patterns, or assumptions.

## Workflow

### HTML Discovery

Extract all resource references from the target application, including:

- External and inline JavaScript, module scripts, and dynamically loaded scripts.
- HTML documents, linked pages, and embedded frames.
- Static assets, including JSON, XML, and other application resources.
- Resource URLs referenced in HTML attributes, inline code, and configuration data.

Do not restrict discovery to file extensions. Include resources identified through actual references, regardless of their URL suffix.

### Runtime Network Capture

Use Playwright to record network requests and responses observed during browser execution.

- Visit discovered application routes and explore interactive features that may trigger lazy loading or additional resource requests.
- Capture scripts, stylesheets, API responses, documents, fonts, images, WebAssembly, and other relevant resources.
- Record request URLs, methods, response status codes, content types, and relevant evidence.
- Include resources loaded through redirects or dynamically generated URLs.
- Avoid treating a requested URL as a valid resource until its response and DOM or content has been appropriately verified.

### Source Map Discovery

Discover accessible source maps and related debugging artifacts using:

- `.map` URLs referenced by scripts or stylesheets.
- `sourceMappingURL` directives in JavaScript and CSS.
- Source map references found in HTML, build output, or runtime network traffic.
- Alternative URL patterns supported by observed application references.

Validate discovered resources and retain their evidence. Do not assume that a `.map` URL is a valid source map based on its extension alone.

### Manifest Discovery

Identify and collect available build manifests and resource mapping files for Vite, Webpack, Next.js, and other relevant frameworks.

Include manifests discovered through HTML, network traffic, configuration references, or publicly accessible build artifacts. Do not analyze their contents; only collect and record verified resources.

### OSINT

Search Google, GitHub, the Wayback Machine, and other relevant public sources for application resources that are not exposed through the current application interface.

- Search for scripts, stylesheets, source maps, manifests, configuration files, API-related resources, and other relevant assets.
- Validate each result by inspecting its actual response and content.
- Exclude invalid results and deduplicate resources across discovery sources.
- Preserve the source and evidence for each discovered resource.
- Do not classify a resource based solely on its filename, extension, or search result snippet.

### Recursive Resource Crawling

Recursively inspect discovered resources for additional resource references, regardless of file extension.

- Extract references from JavaScript imports, dynamic `import()`, module dependencies, chunk mappings, and runtime loaders.
- Extract references from CSS `@import` and `url()` declarations.
- Inspect HTML links, frames, embedded resources, and relevant configuration or data files for further resource URLs.
- Follow references found in source maps and build artifacts when they reveal additional resources.
- Add newly discovered resources to the crawling queue, including resources served from extensionless or dynamically generated URLs.
- Validate each resource and deduplicate by normalized URL while preserving relevant request methods and discovery evidence.
- Continue processing the queue until no new resources are discovered.

Do not assume every referenced URL is a source file or valid resource. Confirm its type using observed responses and content.

## Output

Save the temporary results to `javascript-analysis-output.txt`, containing one URL per line.

Example:

```text
https://example.com
https://example.com/asset-manifest.json
https://example.com/login
```

If any non-GET requests are identified, record them in the following format:

```text
POST https://example.com/submit (headers={}) (data=data)
PUT https://api.example.com/v1/some-api (headers={}) (data={"data":"value"})
```
