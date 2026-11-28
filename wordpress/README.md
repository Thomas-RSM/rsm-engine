# Relevant Search Media — WordPress theme

Two packages, both in `dist/`:

| File | What it is |
|---|---|
| `rsm-theme.zip` | The theme. Carries the design, fonts, film, import data and a copy of the companion plugin. |
| `rsm-elements.zip` | The companion plugin (19 Elementor widgets, editable header and footer, SEO output). Already bundled inside the theme; supplied separately only for manual installs and updates. |

Needs WordPress 6.5 or newer, PHP 7.4 or newer, and Elementor Free. Elementor Pro is not needed.

## Install (about three minutes)

1. **Appearance → Themes → Add New → Upload Theme.** Choose `rsm-theme.zip`, install, activate.
2. A notice appears: **Open RSM Setup.** (Or go to Appearance → RSM Setup.)
3. Press **Install and activate plugins.** This fetches Elementor Free from wordpress.org and installs RSM Elements from the theme.
4. Press **Import the website.** The home page, header, footer, menus, media, colours, fonts and settings are created, and the home page is set as the front page.

Open the site. It is finished.

Pressing Import again is safe: nothing is duplicated and your edits are kept. The separate **Reset and re-import** button replaces the imported pages, header, footer and menus with the originals.

## Editing

- **Pages:** Pages → Home → Edit with Elementor. Headings, paragraphs and buttons are Elementor's own widgets. The animated pieces (orbit, film, equation, lab, keyword console, map, cards, FAQ and so on) are RSM widgets under the **Relevant Search Media** category, each with Content, Style and Advanced tabs.
- **Header and footer:** Appearance → Header & Footer → Edit with Elementor.
- **Menus:** Appearance → Menus. The main menu's three levels become the mega menu. Add the CSS class `wide` to a top item for a wide panel, `right` to align it right.
- **Search title and description for a page:** the "Search appearance" box on the page edit screen.
- **Site colours and fonts:** Elementor → Site Settings → Global Colors / Global Fonts.

## Rebuilding the packages

`python3 build.py` reads `../site/index.html`, regenerates `rsm-theme/import/site.json`, syncs assets and rewrites both ZIPs in `dist/`.

## Known limits

- Only the **Home page** has been designed so far, so that is the only page imported. Menu and footer links to service, problem, about and contact pages lead to pages that do not exist yet.
- The keyword console's form posts to `/your-plan/`, which is not built yet.
- The orbit, film, equation, lab and console widgets are meant to be used once per page.
- If you run an SEO plugin (Yoast, Rank Math), turn off one of the two sources of meta tags to avoid doubles.
