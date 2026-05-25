After completing the data analysis task, produce a single browser-ready HTML report named `report.html`.

The report must be a polished, self-contained deliverable that opens directly in a modern browser. Think like a pragmatic web developer: reuse mature UI, charting, and table libraries instead of building custom components from scratch.

Deliverable requirements:
- Output exactly one HTML file: `report.html`.
- Embed all report text, analysis results, chart data, table data, configuration, and custom CSS/JavaScript in that file.
- Do not require a build step, package install, backend, notebook, local server, or separate asset folder.
- Stable CDN dependencies are allowed unless offline-only output is explicitly required.
- Pin CDN library versions where practical.
- Do not fetch local files or private APIs at runtime.

Preferred libraries:
- UI/layout: Bootstrap 5, Pico CSS, or Web Awesome.
- Charts: Plotly.js or Apache ECharts.
- Tables: DataTables or an equivalent mature table library.
- Utilities: Day.js, Lodash, PapaParse, Arquero, or similar focused libraries when they reduce custom code.
- Avoid React, Vue, Svelte, or other app frameworks unless the report genuinely needs them.
- Do not use Tailwind Play CDN for production-style output.

Report structure:
Include the following sections when relevant:
- Title
- Date generated
- Executive summary
- Key findings
- Methodology
- Data sources
- Data quality notes
- Main charts
- Main tables
- Interpretation
- Caveats and limitations
- Appendix with technical details, if useful

Design requirements:
- Use a responsive layout.
- Use library-provided components such as cards, alerts, tabs, accordions, badges, and navigation where appropriate.
- Include a table of contents for long reports.
- Use consistent spacing, typography, and visual hierarchy.
- Avoid raw, unstyled HTML.

Chart requirements:
- Use Plotly.js or Apache ECharts.
- Each chart must have a clear title, labeled axes, units where applicable, and a short interpretation.
- Use interactive features such as tooltips, hover labels, zoom, or legends when useful.
- Choose chart types based on the analytical question:
  - Bar charts for comparisons
  - Line charts for trends
  - Scatterplots for relationships
  - Histograms or box plots for distributions
  - Heatmaps for matrices
- Avoid pie charts unless they are clearly the best fit.

Table requirements:
- Use semantic HTML tables.
- Use DataTables or an equivalent library for large or interactive tables.
- Enable search, sorting, pagination, and copy/export controls where useful.
- Include clear column names, units, captions, and formatting.
- Use `<thead>`, `<tbody>`, `<th>`, `<td>`, captions, and scoped headers where appropriate.

Accessibility requirements:
- Use semantic HTML.
- Maintain good color contrast.
- Do not rely on color alone to communicate meaning.
- Add accessible labels or text summaries for meaningful charts and visuals.
- Ensure interactive elements remain usable with keyboard navigation where possible.

Analysis transparency:
- State data sources.
- Explain filters, joins, assumptions, derived metrics, and exclusions.
- Include row counts before and after major cleaning or filtering steps.
- Identify missing data, duplicates, outliers, and other data quality issues.
- Distinguish facts, estimates, and interpretations.
- Do not overstate confidence.

Code quality:
- Keep custom JavaScript and CSS minimal.
- Prefer library configuration over custom implementations.
- Use small helper functions only when they reduce repetition.
- Avoid unnecessary dependencies.
- Comment only non-obvious logic.

Large data handling:
- If the full dataset is too large to embed, include aggregated data in the report.
- Explain what was omitted and why.
- Preserve enough detail for the report’s conclusions to be auditable.

Final self-check before delivery:
- There is exactly one file named `report.html`.
- The file opens in a browser without a build step.
- UI, charts, and tables use mature libraries instead of custom reinvention.
- Charts render correctly.
- Tables initialize correctly.
- Navigation works.
- Data needed by the report is embedded.
- Findings are clear and supported by the analysis.
- Assumptions and limitations are visible.
- Tables and charts are labeled and accessible.

Do not create a custom design system, charting engine, table widget, router, state framework, or export system. Use established browser-ready libraries. Custom code should be limited to report-specific data preparation, chart configuration, table configuration, and small interaction glue.