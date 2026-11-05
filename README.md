# Tony Hoo — Personal Website

Multi-page static site (no Netlify build step). Netlify publishes the repo root; each page lives in its own folder, so URLs are clean (`/calculator/`, `/contact/` ...).

Pages: `/` Home · `/about/` · `/services/` (How I Help) · `/properties/` · `/calculator/` · `/stories/` · `/contact/` · `/privacy/`

## Editing
- Shared nav, footer, page titles/descriptions and page layouts: `build.py`
- Section content reused across pages: `src/*.html`
- Styles: `src/base.css` (+ `EXTRA_CSS` in `build.py`)
- Settings (WhatsApp number, featured project list) and page scripts: `src/site.js`

After editing, run `python3 build.py` and commit the regenerated `index.html` files and `assets/site.css` / `assets/site.js` together with the source.

`assets/` also holds the photos (skyline, Tony's portrait, buyer photos reused from the KL Projects Atlas).

Related sites: KL Projects Atlas (`kl-property-atlas-tonyhoo`), Home Loan Calculator (`tonyhoo-home-loan-calculator`).
