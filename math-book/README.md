# رياضيات التكميلية المهنية — Arabic math book

An Arabic math book built from the official exam questions of 2015, 2016 and 2017 (التكميلية المهنية, first session).
It uses English digits and `x`, `y` throughout.

- `index.html`: the book. It is fully self-contained (fonts and math are embedded) and works offline.
- `كتاب-الرياضيات.pdf`: an A4 print version.

## Contents
Six lessons. Each lesson has an explanation, rule cards, common mistakes, worked examples, kitchen and restaurant
applications, and exercises at three levels (easy, medium, hard). The book ends with:
- the 3 official exams
- 2 mock exams in the same format
- a formula sheet
- a full answer key

## Build
```
npm install          # KaTeX
pip install sympy
python3 build.py     # verifies every answer with sympy, then writes index.html
node pdf.js          # writes the PDF (Playwright / Chromium)
```
The content lives in `content.py`. `verify.py` checks every exercise and exam answer. The build stops if any answer is wrong.
