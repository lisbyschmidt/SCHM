# SCHM

Source for [www.schm.dk](https://www.schm.dk/) — the site for SCHM, the freelance
practice of Søren Lisby Schmidt.

One static page. No build step, no dependencies: everything the page needs is in
`index.html`, styles and script included. Open the file in a browser to preview it.

| File | Purpose |
| --- | --- |
| `index.html` | The whole site |
| `soren.jpg` | Portrait used in the hero |
| `social-banner.png` | 1200×630 Open Graph image for link previews |
| `branding/` | Not used by the page: `make_images.py` generates `social-banner.png` and `branding/linkedin-cover.png` (LinkedIn cover) from `branding/foto.png` |
| `CNAME` | Custom domain for GitHub Pages |

Pushing to `main` deploys to GitHub Pages.
