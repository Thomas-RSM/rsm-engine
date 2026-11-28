# Testing report

Tested 28 November 2026 on a fresh WordPress 7.1.5, PHP 8.3.6, Elementor Free 4.4.2, in headless Chromium driven by Playwright. Every line under "Passed" was actually run.

## Passed

| Test | Result |
|---|---|
| Theme installs from `rsm-theme.zip` on a site with no Elementor | Installed and activated |
| Setup screen installs Elementor Free from wordpress.org and RSM Elements from the bundle | Both active, returns to setup |
| One-click import | 1 page (set as front page), header, footer, 6 menus (103 items), 4 media files, global colours and fonts, permalinks |
| Import run three more times | Counts unchanged (1 page, 2 parts, 4 media, 6 menus, 103 items); earlier edits kept |
| Reset and re-import | Restores originals, no duplicates |
| Home opens in the Elementor editor | 249 elements, no unknown widget types, no empty or errored widgets |
| Editing a native heading, a stat, a button, a lab term; duplicating a card; saving | All saved; front end shows every change |
| Header and footer open in the Elementor editor, edit, save | Saved; front end shows the changes |
| Widget panel | Content, Style and Advanced tabs present |
| Front end at 1440, 1024 and 390 wide | No sideways scroll, no broken images, fonts load locally, no requests to outside hosts |
| Browser console | No JavaScript errors, front end or editor |
| PHP debug log (`WP_DEBUG` on) | No notices, warnings or errors from the theme or plugin |
| Animations and interactions | Orbit, sticky header, mega menu, mobile menu, film playback and chapter jumps, equation picture, lab, keyword console with real data, FAQ |
| Match with the original design | Section heights within 12 px at 1440; within 22 px at 1024 and 390. Side-by-side screenshots compared at 1440 |
| SEO output | Title, meta description, Open Graph, JSON-LD (Organization, WebSite, Person, DefinedTerm, WebPage, FAQPage, VideoObject), `robots.txt`, `/llms.txt`, sitemap |

## Not passed, not tested, or blocked

- **Internal links:** 69 of 72 lead to pages that have not been designed yet (services, problems, about, contact, your-plan). Only the Home page exists to convert.
- **Blog posts, forms, sliders:** none exist on the site, so there was nothing to convert or test. Post and archive templates are included but only lightly checked.
- **PHP 7.4 to 8.2:** not tested. Only 8.3 was available.
- **MySQL / MariaDB:** not tested. The test site ran on SQLite (the official SQLite integration plugin).
- **Apache / Nginx:** not tested. The test site ran on PHP's built-in server.
- **Tablet and phone:** checked by measurement and automated checks, not by side-by-side screenshots.
- **Real devices and Safari / Firefox:** not tested. Chromium only.
- **Other plugins** (caching, SEO, security): not tested alongside.
- **Sandbox-only setting:** the test machine reaches the internet through a proxy, so a small test-only file relaxed WordPress's download URL check and set the proxy certificate. It is not in the packages. On normal hosting the Elementor download uses WordPress's standard installer; that path was not exercised without the proxy.
