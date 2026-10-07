# ثرائد التقوى — محمد عبدالله

The typeset edition of the book «ثرائد التقوى» by Mohamad Abdallah (محمد عبدالله), built from the author's Word manuscript.

## Files
- `ثرائد-التقوى.pdf` — the complete book: front cover, 363 pages, back cover, with PDF bookmarks for every topic.
- `للطباعة-المتن.pdf` — the interior only (17 × 24 cm), for the printing house.
- `للطباعة-الغلاف.pdf` — front and back cover (17 × 24 cm each).
- `غلاف-أمامي.png`, `غلاف-خلفي.png` — cover images (200 dpi) for stores and social media.

## What was done
- Language corrections and removal of duplicated passages (`src/fixes.txt`, `src/structure.txt`).
- Every Qur'an quotation is matched in the Mushaf, printed in Uthmani script and referenced (sura and verse) in a footnote; wrong references were corrected from the matched text.
- Every source (inline brackets, end-of-topic source lists, Word footnotes) is a footnote at the bottom of its page, numbered from ١ on each page: the number in the text, `١: المصدر` in the footnote.
- Each topic starts on a new page with its number and an ornamental title; page numbers at the bottom; running head with the topic title; table of contents at the end.

## Build
```
python3 make_pdf.py
```
Needs Python 3 with `pymupdf`, and Node with Playwright (Chromium).

1. `prep.py` applies the corrections to `src/original.txt` (the text extracted from `src/manuscript.docx`) → `build/edited.txt`
2. `build.py` turns it into HTML: footnotes, Qur'an matching (`quran.py`, `src/quran-uthmani.json`), topics → `build/book.html`
3. `paginate.js` lays the book out in Chromium (pages, per-page footnotes, table of contents), `render.js` prints it
4. `cover.py` draws the covers; `make_pdf.py` joins everything and adds bookmarks

Fonts (in `fonts/`): Amiri, Amiri Quran, Aref Ruqaa; cover: Reem Kufi, IBM Plex Sans Arabic (SIL Open Font License).
