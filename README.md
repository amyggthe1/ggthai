# Thai Language site

Personal Thai lesson notes, a vocabulary quiz and consonant handwriting drills.
Plain static HTML — no build step, no framework, no server required. Every page
is self-contained (inline CSS and JS) so it works from the filesystem or from
any static host.

Open `index.html` to enter the site.

**Picking this up after a break?** Read `PROJECT_LOG.md` first — it has the
history, the current state and the open items. This file covers layout and
publishing; `glyph_project/HANDOVER.md` covers how the stroke animations work.

---

## Layout

```
PROJECT_LOG.md          history, current state, open items — start here
README.md               this file: layout and publishing
check_links.py          link checker, run after any edit
index.html              local shortcut — redirects to kie/home.html (not uploaded)
kie/                    the site (~18 MB)
  home.html               landing page — the entry point
  manifest.webmanifest    lets phones "Add to Home Screen" as an app
  lessons.html            directory of all 16 lesson pages
  index.html              the vocabulary quiz
  glyph.html              consonant stroke practice  (generated — see below)
  <lesson>.html           16 lesson pages
  glyph/
    alphabet.html         script recognition game
    Sarabun.ttf           font used by glyph.html
    thai_stroke_order/          132 consonant GIFs / posters / outlines
    thai_numeral_stroke_order/  30 numeral GIFs / posters / outlines
    audio/                      44 recorded consonant names (mp3)

glyph_project/          build source for the stroke artwork — NOT published
graphie/                separate, unfinished project — NOT published
```

`glyph_project/` and `graphie/` are excluded by `.gitignore`. **Only `kie/`
should reach the web host** — see "Publishing" below for why the root
`index.html` stays local.

## How the pages connect

- Every lesson page links back to `lessons.html` and deep-links into the quiz
  filtered to itself, via `index.html?source=<Lesson>`. The quiz reads that
  query parameter and narrows its pool; an unknown value falls back to the full
  set rather than showing an empty quiz.
- The quiz holds its own copy of the vocabulary (~598 items tagged by source
  lesson). **Adding a word to a lesson page does not add it to the quiz** — the
  `VOCAB` array in `kie/index.html` has to be updated too.
- `kie/glyph.html` is generated. See the next section.

## Regenerating the stroke-practice page

`kie/glyph.html` is a build artifact — **do not edit it by hand**, your changes
will be overwritten. It is produced from `glyph_project/`:

```bash
cd glyph_project
python scripts/build_index.py      # writes output/index.html
python scripts/deploy_to_site.py   # writes ../kie/glyph.html
```

The deploy step rewrites asset paths (the page sits one level above its assets
on the site) and injects the site navigation. Full details, including how the
animations are produced, are in `glyph_project/HANDOVER.md`.

If you regenerate the artwork itself, copy `glyph_project/output/Sarabun.ttf`
and `glyph_project/output/thai_stroke_order/` into `kie/glyph/` as well — the
deploy script only handles the HTML.

## Publishing

Currently live at **http://gerardlam.free.fr/kie/** — upload the contents of
`kie/` by FTP to the `kie` directory. Entry point:
http://gerardlam.free.fr/kie/home.html

> **Do not upload the root `index.html` to the site root.**
> `gerardlam.free.fr/` already serves a different personal site; overwriting its
> `index.html` would destroy it. That is why the landing page lives at
> `kie/home.html` and the root file is only a local redirect.

Any static host works. The site is entirely relative-linked, so it can live at a
domain root or in a subdirectory.

**GitHub Pages.** Push the repository and enable Pages on the default branch,
root folder. `.nojekyll` is present and must stay — without it Jekyll skips
files it does not recognise, and the stroke images have non-ASCII names.

**Netlify / Cloudflare Pages.** Drag the folder in, or connect the repository.
No build command; publish directory is the repository root.

### Things to know before you host

- **Non-ASCII filenames.** The 132 stroke images are named with IPA characters
  (`01_kɔɔ_kài.gif`). All are NFC-normalised and match their HTML references
  exactly, which is what Linux hosts and Git expect. macOS stores filenames as
  NFD, so if these files are ever added to the repository from a Mac the names
  can drift and the images 404. Check on a case- and Unicode-sensitive host
  after any large file move.
- **Size.** `kie/` is ~18 MB, almost all of it the stroke GIFs. Comfortably
  within free-tier limits, but the stroke page is the heavy one on mobile data.
- **Audio.** The 44 consonants play a real recording from `kie/glyph/audio/`,
  paired to each letter by the `NN_` filename prefix. Everything else — the
  numerals and the vocabulary quiz — falls back to the browser's Web Speech API
  with `lang="th-TH"`, which needs a Thai voice installed on the device. The app
  says so plainly when one is missing. Recordings are fetched on click, never
  preloaded, so they cost nothing until used.
- **HTTPS.** Speech synthesis and "Add to Home Screen" both want a secure
  context. All three hosts above give you HTTPS by default.

## Checking links after edits

```bash
python check_links.py
```

Walks every HTML file, resolves each local `href`, `src`, `url()` and embedded
asset path, and reports anything that does not exist on disk.
