"""
Link checker for the Thai Language site.

Walks every published HTML file, resolves each local reference — href, src,
CSS url(), and the asset paths embedded in the stroke-practice JSON blob — and
reports anything that does not exist on disk.

    python check_links.py

Exits 1 if anything is broken, so it can be used in a pre-publish check.
Skips glyph_project/ and graphie/, which are not published (see .gitignore).
"""
import os, re, sys, unicodedata, urllib.parse

ROOT    = os.path.dirname(os.path.abspath(__file__))
SKIP    = {'glyph_project', 'graphie', '.git'}
EXTERNAL = ('http://', 'https://', '//', 'mailto:', 'tel:', 'data:', '#')

# href/src, CSS url('...'), and "glyph/thai_stroke_order/..." inside JSON.
PATTERNS = [
    r'(?:href|src)="([^"]+)"',
    r"(?:href|src)='([^']+)'",
    r"url\(['\"]?([^'\")]+)['\"]?\)",
    r'"((?:glyph/)?thai_stroke_order/[^"]+)"',
    r'"((?:glyph/)?thai_numeral_stroke_order/[^"]+)"',
    r'"((?:glyph/)?audio/[^"]+)"',
]


def html_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP and d != 'thai_stroke_order']
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(base, f)


def main():
    broken, checked, pages = [], 0, 0

    for path in sorted(html_files()):
        pages += 1
        text = open(path, encoding='utf-8').read()
        rel  = os.path.relpath(path, ROOT)

        if '\x00' in text:
            broken.append((rel, '<file contains NUL bytes>'))

        refs = set()
        for pat in PATTERNS:
            refs |= set(re.findall(pat, text))

        for ref in sorted(refs):
            # Skip external links and unresolved JS template placeholders.
            if ref.startswith(EXTERNAL) or '${' in ref:
                continue
            target = urllib.parse.unquote(ref.split('?')[0].split('#')[0])
            if not target:
                continue
            checked += 1
            full = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(full):
                # Unicode normalisation drift is the likely cause on macOS.
                alt = unicodedata.normalize('NFC', full)
                if os.path.exists(alt):
                    broken.append((rel, f'{ref}  [normalisation mismatch]'))
                else:
                    broken.append((rel, ref))

    print(f'{pages} pages, {checked} local references checked')
    if broken:
        print(f'\n{len(broken)} BROKEN:')
        for page, ref in broken:
            print(f'  {page}  ->  {ref}')
        sys.exit(1)
    print('all links resolve')


if __name__ == '__main__':
    main()
