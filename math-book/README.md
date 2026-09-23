# رياضيات التكميلية المهنية — Arabic math book

By teachers **Houssein Zaaror** (حسين زعرور) and **Mohamad Abdallah** (محمد عبدالله).

An Arabic math book built from the official exam questions of 2015, 2016 and 2017 (التكميلية المهنية, first session).
It uses English digits and `x`, `y` throughout.

- `index.html`: the book. It is fully self-contained (fonts and math are embedded) and works offline.
- `كتاب-الرياضيات.pdf`: an A4 print version for students (no answers).
- `answers.html` / `دليل-الإجابات-للمعلم.pdf`: the teacher answer key, kept separate from the book.

## Contents
Six lessons. Each lesson opens with an introduction (a real situation, a prior-knowledge check and the lesson idea) and has hands-on activities with teaching aids, tasks at three levels (support, core, enrichment), an explanation, rule cards, common mistakes, worked examples, kitchen and restaurant
applications, exercises at four levels (easy, medium, hard, challenge ★), a "Skills Builder" (problem-solving steps: understand, plan, solve, check), social-emotional learning activities (cooperation, reflection, self-awareness & self-management…), extra assessment (multiple choice + an open question), a research question, a lesson exam with a full solution at the end of every lesson, a "True or False?" set on common
mistakes and a "Rate yourself" checklist. The cover carries the Al-Mabarrat Association logo (`assets/mabarrat-logo.jpg`).
The book also has 36 cut-out MCQ review cards, with the answer printed upside down. It ends with:
- the 3 official exams
- 6 mock exams in the same format
- a formula sheet
- (the answer key is a separate teacher file)

## Build
```
npm install          # KaTeX
pip install sympy
python3 build.py     # verifies every answer with sympy, then writes index.html
python3 make_pdf.py  # builds both PDFs: cover + framed, page-numbered pages, filled-in index, bookmarks
```
The content lives in `content.py`. `verify.py` checks every exercise and exam answer. The build stops if any answer is wrong.
