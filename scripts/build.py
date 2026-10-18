"""Build the site using Python's standard library; no packages to install."""
from pathlib import Path
from urllib.parse import urlsplit
from html import escape
import argparse
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--base-url', default='http://127.0.0.1:8767')
args = parser.parse_args()
base_url = args.base_url.rstrip('/')
base_path = urlsplit(base_url).path.rstrip('/')
indexable = urlsplit(base_url).hostname in ('www.alexkarner.com', 'alexkarner.com')
out = ROOT / 'dist'
if out.exists():
    shutil.rmtree(out)
out.mkdir()
shutil.copytree(ROOT / 'assets', out / 'assets')

def links(html):
    return re.sub(r'(href|src)="/(?!/)', lambda m: m[1]+'="'+base_path+'/', html)

header = links((ROOT / 'templates/header.html').read_text())
footer = links((ROOT / 'templates/footer.html').read_text())
pages = [
    ('home', '/', 'Alex Karner', 'Teaching, research, and practice aimed at creating places where everyone can thrive.'),
    ('cv', '/publications/', 'Curriculum vitae — Alex Karner', 'Scholarship, teaching, funded research, and service.'),
    ('contact', '/contact/', 'Contact — Alex Karner', 'Contact Alex Karner, Associate Professor at The University of Texas at Austin.'),
]

def document(content, path, title, description, extra=''):
    canonical = base_url + path
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{escape(canonical, quote=True)}">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:type" content="website"><meta property="og:url" content="{escape(canonical, quote=True)}">
{'' if indexable else '<meta name="robots" content="noindex, follow">'}
<link rel="icon" href="{base_path}/assets/alex-karner-site-icon.svg" type="image/svg+xml">
<link rel="icon" href="{base_path}/assets/alex-karner-site-icon.png" type="image/png">
<link rel="stylesheet" href="{base_path}/assets/style.css">
<script defer src="{base_path}/assets/legacy-links.js" data-base-path="{base_path}"></script>
{extra}</head><body class="ak-site">
<a class="ak-skip" href="#main-content">Skip to content</a>
<header class="ak-header">{header}</header>
<main class="ak-main" id="main-content">{content}</main>
<footer class="ak-footer">{footer}</footer>
<script defer src="{base_path}/assets/navigation.js"></script>
</body></html>'''

for name, path, title, description in pages:
    destination = out / path.strip('/') / 'index.html'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(document(links((ROOT / 'content' / (name+'.html')).read_text()), path, title, description))

for alias in ('previous-updates', 'main-page'):
    target = base_path + '/'
    destination = out / alias / 'index.html'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(document(f'<div class="ak-wrap ak-fallback"><h1>Page moved</h1><p><a href="{target}">Continue to the homepage</a>.</p></div>', '/', 'Page moved — Alex Karner', '', f'<meta http-equiv="refresh" content="0;url={target}">'))

(out / '404.html').write_text(document(links('<div class="ak-wrap ak-fallback"><h1>Page not found</h1><p><a href="/">Return to the homepage</a> or <a href="/publications/">browse the CV</a>.</p></div>'), '/404.html', 'Page not found — Alex Karner', ''))
(out / '.nojekyll').touch()
(out / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base_url+'/sitemap.xml\n')
(out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(base_url+p[1])+'</loc></url>' for p in pages)+'</urlset>\n')
# Keep the public portrait and icon URLs used by the previous WordPress site.
uploads = out / 'wp-content/uploads'
uploads.mkdir(parents=True)
for name in ('AlexKarner-11437-300x200-1.jpg', 'AlexKarner-11437-300x200.jpg'):
    shutil.copy(ROOT / 'assets/portrait.jpg', uploads / name)
for name in ('alex-karner-site-icon-150x150.png', 'alex-karner-site-icon-300x300.png'):
    shutil.copy(ROOT / 'assets/alex-karner-site-icon.png', uploads / name)
print(f'Built {len(pages)} pages, legacy links, and assets at {base_url}')
