# رياضيات الصفّ السابع — Grade 7 math book (2026–2027)

By teachers **Houssein Zaaror** (حسين زعرور) and **Mohamad Abdallah** (محمد عبدالله).

An Arabic grade-7 math book that follows the 2026–2027 teaching plan and the grade-7 worksheets.
It has the same design as `../math-book`, with a royal-blue cover. It uses English digits and `x`, `y` throughout.

- `index.html`: the book. It is self-contained (fonts and math are embedded) and works offline.
- `كتاب-رياضيات-الصف-السابع.pdf`: the A4 print version for students (no answers).
- `answers.html` / `دليل-المعلم-الصف-السابع.pdf`: the teacher answer key.

## Contents
- A clear index (units → lessons → page) and a lesson-sections table, then a diagnostic test (ردم).
- Geometry questions carry figures drawn to scale from their data (`qfigs.py`, marker `[[fig:key]]`).
- Four units, one per term period, each with an opener page: the lessons, the number of sessions, the dates, the essential questions, SEL and Skills Builder.
  - Unit 1: numbers — powers, primes, fractions, decimals.
  - Unit 2: signed numbers and the coordinate plane.
  - Unit 3: algebra, equations, proportion.
  - Unit 4: geometry — congruent triangles, angles and parallel lines, bisectors.
- 13 lessons with the same parts as the previous book:
  - introduction, trilingual vocabulary (ar/en/fr), activities and teaching aids from the plan;
  - support, core and enrichment tasks;
  - explanation, rules, common mistakes, worked examples and real-life applications;
  - exercises from easy to challenge;
  - Skills Builder (problem solving), SEL activities, true or false, multiple choice and an open question, a research question and self-assessment;
  - a lesson exam with a full solution.
- 52 cut-out MCQ cards, 4 unit exams, 2 term exams and a summary sheet.

Every answer is checked with sympy by `verify.py`, and the build fails if any answer is wrong.

## Build
```
python3 make_pdf.py   # verify → build → render → PDF (page numbers, index, frame, bookmarks)
```
`node_modules` is a symlink to `../math-book/node_modules`, so run `npm install` in `../math-book` first.
