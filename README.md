# Alex Karner's website

The public site at **alexkarner.com**, preserving its paper background, green palette, Source Serif 4 / DM Sans typography, responsive navigation, and expandable CV. The initial content was copied from the published WordPress site on October 18, 2026, after removing the completed ACSP announcement.

## Update content

- `content/home.html`: introduction, research, projects, selected scholarship, and announcements.
- `content/cv.html`: full public CV, including past ACSP presentations.
- `content/contact.html`: contact text and email link.
- `templates/header.html` and `templates/footer.html`: shared navigation.
- `assets/style.css`: the existing design; bundled fonts retain their licenses.

Edit a content file in GitHub (or locally), review the change, and commit to `main`. The **Publish website** workflow builds, checks, and publishes automatically. No hosting dashboard or WordPress login is needed for content updates. Content is HTML so its existing formatting is preserved; this is not a visual page editor.

The CV is a public snapshot. Updating the Overleaf master does not automatically publish it here. Review and replace the public CV content deliberately, excluding private account identifiers and personal contact details.

## Preview locally

Python 3.10 or later is sufficient; no dependencies are needed.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8767 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8767. To check project hosting, build with `--base-url https://aakarner.github.io/alexkarner.com`. To check the final domain, build with `--base-url https://www.alexkarner.com`.

## Publishing and domain transition

GitHub Pages uses **GitHub Actions** as the publishing source. The build obtains the host and path from Pages settings, so the same files work at the temporary project address or the final custom domain. Temporary GitHub and localhost builds carry a `noindex` directive; production-domain builds are indexable.

1. Verify the GitHub Pages version, including desktop and mobile layouts, links, images, and CV disclosures.
2. Verify domain ownership in GitHub and configure `www.alexkarner.com` as the repository's custom domain.
3. Change only the website's DNS records at the existing DNS provider, following current GitHub Pages instructions. Preserve email and unrelated records. Record the previous values for rollback.
4. Run **Publish website** again so links, canonical URLs, and sitemap use the custom domain. Enable HTTPS when its certificate is ready.
5. Verify both apex and www HTTPS addresses, then retain the old hosting and backups until the migration is confirmed stable.

The existing `aakarner.github.io` transportation blog belongs to a separate repository and is not replaced by this site.

## Compatibility

The homepage, `/publications/`, and `/contact/` keep their paths and CV fragment IDs. Portrait and favicon upload URLs are retained. `/main-page/` and `/previous-updates/` use HTML redirects, and old `?page_id=` links use a small browser script. GitHub Pages does not provide configurable HTTP 301 redirects, so these legacy redirects differ from WordPress's server redirects.

Only public website content is included. WordPress deployment scripts, credentials, databases, private backups, and the Overleaf master are not part of this repository. WordPress administrative, REST API, feed and login endpoints are not reproduced.

## Rollback

Revert a content commit to republish its previous version. During domain migration, restore the recorded web DNS values to return to the retained WordPress host; DNS propagation may take time.
