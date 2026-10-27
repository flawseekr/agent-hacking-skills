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

Identify and collect publicly accessible manifests, asset mappings, configuration files, and framework-generated metadata that may provide useful information for application reconnaissance.

Discover resources through HTML references, runtime network traffic, application configuration, public references, and manual path checking. Include, but do not limit discovery to, the following filenames and paths:

- **Web manifests and source maps:** `manifest.json`, `manifest.webmanifest`, `site.webmanifest`, `*.js.map`, browser extension `manifest.json` (MV2/MV3).
- **`.well-known/` resources:** `.well-known/assetlinks.json`, `.well-known/apple-app-site-association`, `.well-known/openid-configuration`, `.well-known/oauth-authorization-server`, `.well-known/gpc.json`, `.well-known/nodeinfo`, `.well-known/security.txt`, `.well-known/mta-sts.txt`, `.well-known/dnt-policy.txt`, `.well-known/change-password`, `.well-known/ai-plugin.json`.
- **Vite:** `.vite/manifest.json`, `.vite/ssr-manifest.json`.
- **Webpack and Create React App:** `asset-manifest.json`, `manifest.json`, `precache-manifest.<hash>.js`, `webpack-stats.json`, `stats.json`.
- **Workbox and service workers:** `sw.js`, `service-worker.js`, `workbox-<hash>.js`, `firebase-messaging-sw.js`.
- **Angular:** `ngsw.json`, `ngsw-worker.js`, `3rdpartylicenses.txt`.
- **Nuxt:** `_nuxt/builds/meta/<uuid>.json`, `_nuxt/builds/latest.json`.
- **Gatsby:** `webpack.stats.json`, `chunk-map.json`, `page-data/**/page-data.json`, `app-data.json`.
- **Next.js:** `BUILD_ID`, `_buildManifest.js`, `_ssgManifest.js`, `routes-manifest.json`, `prerender-manifest.json`, `required-server-files.json`, `build/app-build-manifest.json`, `react-loadable-manifest.json`, `images-manifest.json`, `export-marker.json`, and `server/{pages,app-paths,middleware,next-font,functions-config,server-reference}-manifest.json`.
- **API specifications and configuration:** `openapi.json`, `swagger.json`, `v3/api-docs`, `package.json`, `composer.json`, `bower.json`, `firebase.json`, `vercel.json`, `now.json`, `netlify.toml`, `tsconfig.json`, `.babelrc`, `appsettings.json`, `config.json`, `env.json`.
- **Supporting XML and metadata:** `browserconfig.xml`, `opensearch.xml`.

Use these names as a starting point, adapting paths and filename patterns to the detected framework and application structure. Include relevant version-specific and hashed filenames where applicable.

Verify each discovered resource by inspecting its response and contents; do not assume a file is valid on its name or HTTP status alone.

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
