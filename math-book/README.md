# رياضيات التكميلية المهنية — Arabic math book

By teachers **Houssein Zaaror** (حسين زعرور) and **Mohamad Abdallah** (محمد عبدالله).

An Arabic math book built from the official exam questions of 2015, 2016 and 2017 (التكميلية المهنية, first session).
It uses English digits and `x`, `y` throughout.

- `index.html`: the book. It is fully self-contained (fonts and math are embedded) and works offline.
- `كتاب-الرياضيات.pdf`: an A4 print version.

## Contents
Six lessons. Each lesson has an explanation, rule cards, common mistakes, worked examples, kitchen and restaurant
applications, exercises at four levels (easy, medium, hard, challenge ★), a "Skills Builder" (problem-solving steps: understand, plan, solve, check), a "True or False?" set on common
mistakes and a "Rate yourself" checklist. The cover carries the Al-Mabarrat Association logo (`assets/mabarrat-logo.jpg`).
The book ends with:
- the 3 official exams
- 3 mock exams in the same format
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
