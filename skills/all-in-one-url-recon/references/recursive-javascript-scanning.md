## Objective

Perform comprehensive, recursive resource discovery across the target application and relevant public sources. Identify, collect, and validate JavaScript, HTML, source maps, manifests, configuration files, API-related resources, and other observeable assets. Follow resource references recursively until no new resources are discovered. Base all results on actual observations and verifiable evidence, without relying solely on file extensions, URL patterns, or assumptions.

## Workflow

### HTML Discovery

Extract observable resource references from the target application, including:

- External, inline, module, and dynamically loaded JavaScript.
- HTML documents, linked application pages, and embedded frames.
- API endpoints and relevant JSON or XML resources.
- Source maps, build manifests, and application configuration files.
- Resource URLs referenced in HTML attributes, scripts, and configuration data.

Do not restrict discovery by file extension. Include resources identified through actual references, regardless of their URL suffix.

### Runtime Network Capture

Use Playwright to record network requests and responses observed during browser execution.

- Visit discovered application routes and explore interactive features that may trigger lazy loading or additional resource requests.
- Capture JavaScript, HTML documents, API requests, source maps, manifests, and relevant structured-data resources.
- Record request URLs, methods, response status codes, content types, and supporting evidence.
- Include resources loaded through redirects or dynamically generated URLs.
- Verify resource content before classifying it. A request or HTTP status code alone does not establish validity.

### Source Map Discovery

Discover accessible source maps using:

- `.map` URLs referenced by JavaScript.
- `sourceMappingURL` directives in JavaScript files.
- Source map references observed in HTML, build artifacts, or runtime network traffic.
- Additional source map URLs established through actual references.

Validate each candidate using its response and content. Do not assume a URL is a valid source map based on its extension alone.

### Manifest Discovery

Identify and collect available build manifests and resource mapping files associated with Vite, Webpack, Next.js, and other relevant frameworks.

Discover manifests through HTML, runtime network traffic, application configuration, and public references.

Collect and record verified manifests without analyzing their contents.

### Recursive Resource Crawling

Recursively inspect discovered resources for additional observable resource references, regardless of file extension.

- Extract references from JavaScript imports, dynamic `import()`, module dependencies, chunk mappings, and runtime loaders.
- Inspect HTML links, embedded frames, scripts, and relevant configuration or structured-data resources.
- Follow source map and build-manifest references to discover additional resources.
- Add newly discovered resources to the crawling queue, including extensionless and dynamically generated URLs.
- Validate resources and deduplicate by normalized URL while preserving relevant HTTP methods and discovery evidence.
- Continue processing the queue sequentially until no new resources are discovered.

**Main rule:** Do not include CSS, images, fonts, or other purely visual assets in the output. Do not assume a referenced URL is valid or belongs to a particular resource type without supporting evidence.

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
