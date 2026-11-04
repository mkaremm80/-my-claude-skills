---
name: "paper-equation-guide"
description: "Explain every equation of a research paper in a colored PDF guide: labeled equation terms, plain meaning, worked numeric examples, helper drawings and simulation checks. Use when asked to explain a paper's math."
---

# Paper Equation Guide

Turn the mathematics of any research paper (PDF or LaTeX) into a colored, easy-to-read PDF guide. Every equation is shown with each term highlighted in color and labeled with an arrow, then explained in plain words, derived briefly, illustrated with real numbers and (when useful) a drawing, and checked by simulation.

Writing style: English, short sentences, simple words (B2 level), professional. Numbers quoted from the paper must match the paper. Numbers from your own worked example must be clearly labeled as an illustration (state the parameters and that one example realization or fixed seed is used).

## Step 1 - Read and map the math
1. Read the whole paper. List every numbered equation, proposition/lemma/theorem, the key unnumbered formulas (cost/complexity, metrics such as reduction %, confidence intervals, normalized quantities), and every symbol with its meaning and nominal value.
2. Build the equation map: which equation feeds which (e.g., model -> estimator -> score -> decision; geometry -> dimension -> rule). Note what each proposition explains.
3. Note notation problems for the authors (same symbol used for two things, undefined symbols, inconsistent figure vs. text notation). Report them in a small "notation point" box.

## Step 2 - Compute worked examples and verify
- Pick one small, representative operating point from the paper (its nominal parameters). Write a Python script (numpy/scipy) that computes, for each equation, concrete example values (e.g., matrix entries, posterior mean/variance at a few indices, scores, probabilities, eigenvalues and cumulative energy, cost counts).
- Look for a teaching example that shows WHY an equation is needed (e.g., two cases with the same mean but different outage; an adjacent next choice showing clustering).
- Verify every closed-form result by Monte Carlo (about 1e6 samples) or direct computation, and record formula vs. simulation in a table.
- Do NOT name a Python script `numbers.py` (it shadows the standard library module and breaks numpy). Use names like `eq_numbers.py`.

## Step 3 - Helper drawings
With matplotlib (STIXGeneral font, mathtext stix, `pdf.fonttype=42`, about 6.6 x 3.3 in, 10-11 pt):
- a plot that shows the meaning of a model equation (e.g., correlation vs. distance),
- what the estimator believes after a few measurements (true value vs. predicted, and uncertainty),
- how a probability formula depends on its inputs (with the teaching example marked),
- spectrum / cumulative energy for a dimension definition.
Add notes with `ax.annotate(..., arrowprops=dict(arrowstyle='-|>', color='#C0392B'), bbox=dict(boxstyle='round,pad=0.3', fc='#FFF8E1', ec='#E09F3E'))`. Put notes in empty areas, increase `ylim` to create headroom, move legends away from data. Render each plot to PNG (`pdftoppm -r 70`) and check for overlaps before using it.
For rank/size arguments, draw simple TikZ matrix shapes (wide vs. tall rectangle) instead of a plot.

## Step 4 - Labeled equations (annotate-equations)
Use the LaTeX package `annotate-equations` (needs two or more pdflatex runs):
```latex
\usepackage{annotate-equations}
\renewcommand{\eqnhighlightheight}{\mathstrut}
\renewcommand{\eqnannotationfont}{\bfseries\small}
...
\vspace*{2.2em}
\begin{equation*}
\eqnmarkbox[teal]{mu}{\bm\mu}=\eqnmarkbox[blue]{c}{\mathbf C}\,\eqnmarkbox[orange]{a}{\mathbf A^{-1}}\,\eqnmarkbox[red]{y}{\mathbf y}
\end{equation*}
\annotate[yshift=1.2em]{above,left}{mu}{best guess}
\annotate[yshift=-1.2em]{below,right}{y}{measured data}
\vspace*{2.0em}
```
Rules that avoid collisions:
- Wrap each labeled equation in a titled tcolorbox and reserve space with `\vspace*{2.2em}` before and `\vspace*{2.0em}` after (more if labels are stacked).
- Alternate labels above/below and left/right; never put two labels on the same side at the same height next to each other. When needed, stack them with a larger `yshift` (e.g., 2.6em).
- Keep labels short (3-6 words). Long equations: split into two displayed lines (e.g., mean on one line, covariance on the next), each with its own labels.
- Labels must not cross the box edge: use left labels for left terms and right labels for right terms, and shorten text if needed.

## Step 5 - Build the colored PDF
LaTeX `article`, A4, `helvet` sans, `xcolor[table]`, `tcolorbox[most]`, `tikz` (arrows.meta, positioning, calc, fit, backgrounds), `booktabs`, `tabularx`, `xltabular`, `enumitem`, `titlesec`, `fancyhdr`, `float`, `caption`, `needspace`, `bm`, `annotate-equations`. Colors: navy #1B3A5C, teal #00798C, rosered #D1495B, amber #E09F3E, leaf #2E8B57, plum #6A4C93. Boxes: `verdict` (teal), `goodbox` (green, small example), `notebox` (amber, where it comes from / notes), `eqbox` (navy title, the labeled equation). Define `\newcolumntype{P}[1]{>{\raggedright\arraybackslash}p{#1}}` and pass box titles as `title={#1}`.

Structure:
1. Cover banner (navy band): "How to Read Every Equation in the Paper", paper title, date.
2. **Equation map** (TikZ grid, absolute positions such as `\def\dx{33mm}\def\dy{21mm}`, boxes about 26 mm wide, straight arrows only, no crossings, short arrow labels) + one-line story + "how each section is built" note.
3. **All symbols in one table** (symbol | simple meaning | value in paper) + notation-point box.
4. **One section per equation / proposition**: labeled equation box -> "In plain words" -> "Where it comes from" (2-3 lines, when a derivation exists) -> helper drawing -> "Small example" with real numbers -> "Why the paper needs it".
5. Cost/complexity formulas with an operation-count example.
6. Table of the formulas behind the reported numbers (reduction %, CI with the t value, normalized metrics) with one example each from the paper.
7. **Checked by simulation** table (formula vs. simulation) and a short statement of correctness; report any error found.
8. **Summary: one line per equation.**
Use `\clearpage` before major sections that hold big boxes and `\Needspace{12\baselineskip}` before smaller headings to avoid orphan headings.

Compile 3 times (`pdflatex -interaction=nonstopmode`). Missing packages: `apt-get update && apt-get install -y texlive-latex-extra texlive-fonts-extra texlive-science texlive-pictures`. If `newtxmath` fails with `binhex.tex not found`, use `mathptmx`.

## Step 6 - Check before sending
- Crop every equation box from the PDF (PyMuPDF `page.search_for(title)` then `get_pixmap(clip=...)`) and look at them stacked: no overlapping labels, no label outside the box, no text hidden.
- Render all pages into a montage and check the equation map and page breaks.
- Confirm all paper numbers match the paper and all example numbers match the script output.
- Deliver the PDF with SendUserFile and summarize what each section contains, plus any notation issue or error found. Number new versions (v2, v3, ...) when the user asks for changes.