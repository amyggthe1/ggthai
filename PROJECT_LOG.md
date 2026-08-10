# Project log — Thai Language site

Running record of what changed and why, so the work can be picked up on another
machine. For *how the stroke animations work*, read
`glyph_project/HANDOVER.md`. For *how the site is laid out and published*, read
`README.md`. This file is the history and the to-do list.

**Live:** http://gerardlam.free.fr/kie/ · entry point `home.html`
**Last session:** 10 August 2026

---

## Resuming on another computer

1. Copy the whole `Website TH GG` folder. It is self-contained — no database, no
   accounts, no API keys.
2. Only needed if you intend to regenerate stroke artwork:

   ```bash
   pip install pillow numpy scipy scikit-image
   ```

   Editing pages or content needs nothing installed. `ffmpeg` is only required by
   `extract_numeral_strokes.py`, which you are unlikely to run again.
3. Sanity check after copying:

   ```bash
   python check_links.py          # expect: 22 pages, 286 refs, all resolve
   ```
4. Open `index.html` (root) — it redirects to `kie/home.html`.

### Publishing

FTP the contents of `kie/` to the `kie` directory on free.fr. **Never upload the
root `index.html` to the site root** — `gerardlam.free.fr/` is a different
personal site and would be overwritten. That file is a local shortcut only.

`glyph_project/` and `graphie/` are build source and an unrelated project. They
are excluded by `.gitignore` and must not be uploaded.

---

## Current state

| Area | State |
|---|---|
| 16 lesson pages | Done. Each links back to `lessons.html` and deep-links into the quiz filtered to itself. |
| Vocabulary quiz (`kie/index.html`) | ~598 items, 7 modes. Uses speech synthesis. |
| Consonants | 44 letters: stroke animation, tracing canvas, **recorded** pronunciation. |
| Numerals ๐–๙ | 10 numerals: stroke animation from hand-traced paths. Synthesised audio. |
| Vowels / tone marks | Reference tables only. No stroke data exists — see HANDOVER §5. |
| Alphabet quiz | `kie/glyph/alphabet.html` (renamed from `game.html`). Covers the 44 consonants **and** the 10 numerals. |
| Landing page | `kie/home.html` + `manifest.webmanifest` for Add to Home Screen. |

Published payload is roughly 22 MB, dominated by the stroke GIFs.

---

## Routine tasks

**Regenerate the stroke-practice page** (`kie/glyph.html` is a build artifact —
never hand-edit it):

```bash
cd glyph_project
python scripts/build_index.py      # writes output/index.html
python scripts/deploy_to_site.py   # writes ../kie/glyph.html
```

**Regenerate numeral artwork** (only if the traces or metrics change):

```bash
python scripts/generate_gifs.py numeral_strokes.txt output/thai_numeral_stroke_order
cp output/thai_numeral_stroke_order/* ../kie/glyph/thai_numeral_stroke_order/
```

**Retrace a numeral:** open `glyph_project/tools/trace_numerals.html` in a
browser, drag along the stroke, download. Save as
`data/numeral_strokes_raw.txt`, apply the centring step, write the result to
`data/numeral_strokes.txt`. HANDOVER §4b explains why, and why centring twice
breaks it.

**Check links after any edit:** `python check_links.py` from the root.

---

## History

### Session 2 — 10 August 2026

**Published to GitHub.** The site now also lives at
https://github.com/amyggthe1/ggthai, public, with GitHub Pages serving
https://amyggthe1.github.io/ggthai/. free.fr is unchanged and still live; this is
an addition, not a migration. The repository root is the project folder, so the
root `index.html` redirect is what makes the Pages address land on
`kie/home.html`. `.nojekyll` must stay committed or the IPA-named stroke images
404. Day-to-day updates are now GitHub Desktop: commit, then push.

**Numerals added to the alphabet quiz** (`kie/glyph/alphabet.html` — hand-written,
not generated, unlike `glyph.html`):
- New `NUMS` array of ๐–๙ in the same shape as `CHARS`, so all three question
  modes work without special-casing: `rom` holds the Arabic digit, `phon` the
  spoken name, `mean` the value in English, `word` the number spelled out in Thai.
  Values mirror `REF.numerals` in `glyph.html` — keep the two in step.
- Two new sets on the start screen: **Numerals ๐–๙** (10) and **Everything** (54).
  The existing "All consonants" still means the 44 consonants only.
- In the mixed set, distractors are drawn from the same family as the question.
  Offering consonants against a numeral gave the answer away.
- Numerals speak their spelled-out word (สาม), not the glyph — speech engines read
  a bare numeral inconsistently.
- Class pip reads "numeral" instead of "<class> class", in a neutral gold.

### Session 1 — 9 August 2026

**Repairs**
- `kie/emotions.html` was corrupted: valid HTML followed by 23,306 NUL bytes,
  47% of the file. Truncated to the real content.
- Quiz footer listed 15 of 16 lessons; Adverbs of Frequency was missing.

**Structure**
- `kie/glyph/index.html` → `kie/glyph.html`, so the stroke practice sits beside
  the rest of the site rather than being an orphan nobody linked to. Its assets
  stayed in `glyph/`, so the page now references them through a `glyph/` prefix —
  this is what `deploy_to_site.py` rewrites.
- Added `kie/home.html` landing page and `manifest.webmanifest`. Root
  `index.html` became a redirect, because the live site root is occupied.
- `kie/glyph/game.html` → `kie/glyph/alphabet.html`, updated in all four pages
  that link it, and added as a fifth tab in `glyph.html`.

**Tooling** — none of this existed before and all of it is worth keeping.
- `deploy_to_site.py`: turns the generated app into the site copy. Refuses to
  write if rewrite counts are wrong or a referenced asset is missing.
- `check_links.py`: walks every page, resolves every local reference.
- `README.md`, `.gitignore`, `.nojekyll`.

**Glyph page**
- Play button now hidden in Shadow practice — it sat dead centre over the
  outline you are meant to trace.
- Consonant-class colours: high class moved terracotta → navy `#1e3a6e`, tile
  tints to pale blue and lighter green. Letterform colour split into its own
  `--glyph-*` variables so tints and letters can change independently.
- Added tabs: Consonants / Vowels / Tone marks / Numbers / Alphabet quiz.
  Vowel, tone and numeral reference data lives in `scripts/reference_data.py`.
- 44 hand-drawn mnemonic icons were built, then switched off at the user's
  request. They survive in `scripts/mnemonic_icons.py`; set
  `SHOW_MNEMONIC_ICONS = True` to restore them.

**Numerals ๐–๙** — the long one. Four methods were tried; only the last worked.
Full detail in HANDOVER §4b, summarised here because the failures are
instructive:

1. Track the pen in the source video, map onto the font by bounding box —
   drifted off the letterform, because the video's typeface has different
   proportions from Sarabun.
2. Order the font's skeleton by when the video inked each pixel — still jumped
   between limbs; 23% of ๓ was unreachable, so whole regions appeared at once.
3. Walk the skeleton as a graph — scored perfectly on every metric and still
   looked wrong, because dead-end retracing makes the fill stall.
4. **Hand-traced by the user** in `tools/trace_numerals.html`, then centred on
   the stroke. This is what ships.

The lesson worth carrying forward: metrics said 2 and 3 were improving while the
result got visibly worse. When that happens, stop optimising and get a human to
specify the intent directly.

Numerals are also sized per character so each spans the guide band, animate 1.8×
slower than the consonants, and have no red pen dot. All three are set in
`data/numeral_strokes_metrics.txt`.

**Audio**
- 44 consonant recordings supplied by the user, linked by `NN_` filename prefix.
  Pronunciation plays the recording and falls back to speech synthesis when
  there is none.
- Fixed two Web Speech bugs that affected the quiz on every device: voice lookup
  ran before Chrome had loaded the voice list, and `speak()` fired in the same
  tick as `cancel()`, which silently drops the utterance.

---

## Open items

**Quiz audio is still synthesised.** Now that the consonants have recordings, the
same could be done for the ~640 vocabulary items — a far bigger recording
session. Alternative: generate with a neural TTS. Roughly 15,000 characters,
inside the free tier of Google Cloud TTS or Azure Speech, about 7 MB of mp3. The
playback code already prefers a file when one exists, so recordings can be added
in batches rather than all at once.

**Numeral stroke order is unverified.** It came from a children's handwriting
video plus the user's tracing. Reasonable, but no Thai teacher has checked it.
The consonants, by contrast, use RianThai's authored centrelines.

**Vowels, tone marks and numerals ๐–๙ have no verified stroke data** for the
vowels and tone marks specifically — they remain reference tables. HANDOVER §5
covers why and what the options are.

**Duplicated content.** `kie/index.html` holds its own copy of the vocabulary and
`kie/glyph.html` its own copy of the letter data. Adding a word in a lesson page
updates neither. Fine while content is stable; the most likely source of future
confusion.

**Mobile audio not yet tested.** Recordings were confirmed working on the
author's PC. iOS in particular blocks audio that is not triggered by a user
gesture — the Pronunciation button is fine, but the quiz's automatic playback in
listening mode may be silent on iPhone.
