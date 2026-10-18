"""Check local links, fragments, assets and migrated page structure."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parents[1] / 'dist'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.headings = set(), [], 0
        self.canonical = ''
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, 'Duplicate ID: '+a['id']
            self.ids.add(a['id'])
        if tag == 'h1': self.headings += 1
        if a.get('rel') == 'canonical': self.canonical = a['href']
        if tag in ('a', 'link', 'img', 'script'):
            self.links.append(a.get('href', a.get('src', '')))

pages = {p: Page(p.read_text()) for p in ROOT.rglob('*.html')}
base = urlsplit(pages[ROOT/'index.html'].canonical).path.rstrip('/')
for file, page in pages.items():
    assert page.headings == 1, f'{file}: expected one H1'
    for url in page.links:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc: continue
        path = unquote(parsed.path)
        if not path:
            target = file
        elif path.startswith('/'):
            assert not base or path.startswith(base+'/'), f'Wrong base path: {url}'
            target = ROOT / path[len(base):].lstrip('/')
        else:
            target = file.parent / path
        if target.is_dir(): target /= 'index.html'
        assert target.exists(), f'{file}: missing {url}'
        if parsed.fragment and target in pages:
            assert unquote(parsed.fragment) in pages[target].ids, f'{file}: missing fragment {url}'
for css in ROOT.rglob('*.css'):
    for url in re.findall(r'url\([\'"]?([^\)\'\"]+)', css.read_text()):
        assert (css.parent/url).exists(), f'Missing font: {url}'
home = (ROOT/'index.html').read_text()
cv = (ROOT/'publications/index.html').read_text()
assert 'At ACSP with our students' not in home
assert 'Upcoming: ACSP' not in cv
assert '<h3>ACSP, October 2026</h3>' in cv
assert cv.count('class="ak-cv-section"') == 12
assert cv.count('<table>') == 4
assert 'UT Account' not in cv
assert 'wp-admin' not in home+cv
print(f'Checked {len(pages)} HTML pages; all local links, fragments, fonts and content guards passed.')
