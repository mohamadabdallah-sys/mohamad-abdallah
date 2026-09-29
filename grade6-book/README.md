# رياضيات الصفّ السادس — Grade 6 math book (2026–2027)

By teachers **Houssein Zaaror** (حسين زعرور) and **Mohamad Abdallah** (محمد عبدالله).

An Arabic grade-6 math book that follows the 2026–2027 teaching plan (6 units, 21 lessons) and the grade-6 worksheet booklet.
It has the same design as the grade-7 book (`../grade7-book`), with a burgundy cover. It uses English digits and `x`, `y` throughout.

- `index.html`: the book. It is self-contained and works offline.
- `كتاب-رياضيات-الصف-السادس.pdf`: the A4 print version for students (no answers).
- `answers.html` / `دليل-المعلم-الصف-السادس.pdf`: the teacher answer key.

## Contents
- An index (units → lessons → page), a table of the page where each lesson section starts, and a review test (ردم الفاقد).
- Six unit openers from the plan: lessons, sessions and dates, essential questions, SEL, Skills Builder and the unit activity.
  1. Natural numbers: place value and expanded form, order of operations.
  2. Multiples and divisors: divisibility and primes, powers, GCD/LCM, irreducible fractions.
  3. Fractions and decimals: decimal fractions, expanded form with rounding and truncating, multiplying and dividing fractions.
  4. Signed numbers: the number line and opposites, comparing, adding and subtracting.
  5. Geometry: lines and circles, angles, triangles, areas.
  6. Proportionality and statistics: ratio, algebraic expressions, percentages, proportional tables, statistics.
- Every lesson has the parts of the previous books, plus a new **«ببساطة»** box: the idea in simple words, step by step, and a memory tip.
- Figures:
  - A drawn illustration for each lesson (`illustrations.py`).
  - Question figures drawn to scale (`qfigs.py`), added with markers such as `[[fig:nl|-5|5|1|A@-3]]`. They cover number lines, factor trees, fraction bars, percent grids, circles, angles, triangles, area shapes, bar and line charts, dot plots and a place-value table.
- Question types include "spot the mistake", "complete the table", "read the chart", "odd one out", "insert brackets", "create your own", matching exercises and word problems.
- The back of the book has 84 MCQ cards, 6 unit exams, 2 term exams and a summary sheet.

Every answer (more than 1 000) is checked with sympy by `verify.py`, and the build fails if any answer is wrong.

## Build
```
python3 make_pdf.py   # verify → build → render → PDF (page numbers, index, frame, bookmarks)
```
`node_modules` is a symlink to `../math-book/node_modules`.
