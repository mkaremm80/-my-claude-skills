---
name: "paper-from-zero-guide"
description: "Turn any research paper (PDF or LaTeX) into a colorful PDF guide that explains it from zero: background, every equation with labels, full proofs, examples, results, and simulation checks."
---

# Paper From Zero Guide

Make one colorful A4 PDF (about 20-30 pages) that lets a reader with ZERO background understand a research paper fully: the field basics, every equation, every proof, every figure/table, and whether the paper's numbers are right.

Writing style: English, short sentences, simple words (B2 level), professional. Numbers quoted from the paper must match the paper exactly. Numbers from your own worked examples must be labeled "*Example*" with their parameters and seed. Deliver as `<Short_Paper_Name>_Guide_from_Zero_v1.pdf`; number later versions v2, v3, ...

Use a task list: (1) map the paper, (2) compute examples + verify, (3) helper drawings, (4) write + compile, (5) visual check + deliver.

## Step 1 - Read and map the paper
1. If a zip: unzip into its own folder; read `main.tex`, all `\input` files (tables, TikZ figures), `references.bib`, figure scripts and data files (e.g. `figdata.json`, `plots.py`). If a PDF: extract text and look at each figure page.
2. List: every numbered equation, every proposition/lemma/proof, key unnumbered formulas (scores, rules, complexity, metrics such as % reduction, confidence intervals, gap closed), every symbol with meaning and nominal value, all reported numbers in text/tables/figures.
3. Build the equation map: which equation feeds which (model -> estimator -> score -> decision; geometry -> dimension -> rule; theory -> the main rule -> results).
4. List the background concepts a beginner needs (e.g., for wireless: multipath fading, complex gain, SNR/dB, Gaussian/complex Gaussian, covariance/correlation, eigenvalues, rank/nullspace, singular values, pseudoinverse, projector, Bayesian prior/posterior, outage). Pick only what this paper uses.
5. Note notation problems and small errors for the authors: one symbol used for two things, undefined symbols, missing subscripts, conditions a proof silently needs (e.g., full column rank), examples in the text that do not match the stated rule, tie-breaking or other rules left unstated.

## Step 2 - Compute worked examples and verify (Python, numpy/scipy)
- Never name a script `numbers.py` (shadows a stdlib module). Use `eq_numbers.py`, save results to `numbers.json`.
- Use the paper's nominal operating point and one fixed-seed realization for examples. For each equation compute concrete values (matrix entries, posterior mean/variance at a few indices, scores, probabilities, eigenvalues and cumulative energy, singular values, bound values, operation counts).
- Find a teaching example that shows WHY an equation matters (e.g., same mean but different variance gives opposite outage behavior; greedy choice clustering).
- Verify every closed-form result: Monte Carlo (~1e6 samples) or direct computation. Recompute every number the paper reports that can be recomputed (eigenvalues, dimensions, condition numbers, errors) and record paper vs. ours.
- If the paper has a main simulation, write an independent small re-simulation of the key curve(s) (e.g., 20,000 trials, common random numbers). Run long jobs with `nohup python3 script.py args > log 2>&1 &` in the background and keep working; save results to JSON. Compare with the paper's figure data and plot ours (lines) vs paper (circles).
- Do the proofs yourself on paper first and check them numerically (e.g., bound >= true value for the paper's own configuration).

## Step 3 - Helper drawings (matplotlib)
Settings: `font.family STIXGeneral`, `mathtext.fontset stix`, `pdf.fonttype 42`, top/right spines off, light grid, about 6.6 x 3.0 in, 10-11 pt. Save each as PDF (for LaTeX) and PNG at 70 dpi (for checking).
Notes: `ax.annotate(text, xy, xytext, arrowprops=dict(arrowstyle='-|>', color='#C0392B'), bbox=dict(boxstyle='round,pad=0.3', fc='#FFF8E1', ec='#E09F3E'))`. Put notes in empty areas, raise `ylim` for headroom, keep legends off the data.
Typical set (adapt to the paper):
- what the raw phenomenon looks like for one realization (e.g., power across positions with a threshold),
- the model equation's meaning (e.g., correlation vs distance for several parameters),
- random variables as clouds in a plane with the failure region shaded (shows a probability formula visually),
- what the estimator believes after 1 measurement and after B measurements, for each policy (true vs estimate +- band, probed points marked, chosen item circled),
- the greedy/adaptive policy step by step (3 small panels),
- a probability formula vs its inputs with the teaching example marked,
- spectrum + cumulative energy (dimension definition), and mode shapes,
- our re-simulation vs the paper's values.
Make a vertical montage of all PNGs and LOOK at it; fix overlaps and wrong statements in notes before continuing.

## Step 4 - Labeled equations (annotate-equations)
```latex
\usepackage{annotate-equations}
\renewcommand{\eqnhighlightheight}{\mathstrut}
\renewcommand{\eqnannotationfont}{\bfseries\small}
\begin{eqbox}{Equation (3) -- best guess after t probes}
\vspace*{2.6em}
\begin{equation*}
\eqnmarkbox[teal]{q3mu}{\bm\mu}=\eqnmarkbox[navy]{q3G}{\mathbf G}\,\eqnmarkbox[amber]{q3A}{\mathbf A^{-1}}\,\eqnmarkbox[rosered]{q3y}{\mathbf y}
\end{equation*}
\annotate[yshift=1.3em]{above,left}{q3mu}{best guess}
\annotate[yshift=-1.3em]{below,right}{q3y}{measured data}
\vspace*{2.4em}
\end{eqbox}
```
Rules (learned the hard way):
- Mark names must be UNIQUE across the whole document: prefix them per box (q1..., q2...). Easiest: write plain names, then run a Python pass that prefixes names inside each `eqbox` block with `q<k>`.
- Alternate above/below and left/right. Two labels on the same side at the same height WILL collide: stack them (yshift 1.3em, 2.7em, 3.9em) and enlarge the `\vspace*` before/after accordingly (about 4-5em when stacked).
- Two-line boxes (e.g., mean then covariance): leave about 5em between the lines, or the lower labels of line 1 hit the upper labels of line 2.
- Labels near the box edge: use `left` labels for left terms and `right` labels for right terms, keep texts 2-5 words, shorten if they cross the frame.
- A label line should not pass through another label's text; if it does, move one label to the other side or another height.
- Needs at least 2-3 pdflatex runs.

## Step 5 - Build the PDF (LaTeX article)
Preamble: `[11pt,a4paper]article`, geometry margin 2cm, `helvet` sans as default family, `amsmath,amssymb,bm,mathtools`, `xcolor[table]`, `tcolorbox[most]`, `tikz` with libraries `arrows.meta,positioning,shapes.geometric,calc,fit,backgrounds,decorations.pathreplacing,decorations.pathmorphing` (pathmorphing is needed for `snake`), `booktabs,tabularx,xltabular,array,enumitem,titlesec,fancyhdr,float,caption,needspace,graphicx,annotate-equations,hyperref`.
Colors: navy #1B3A5C, teal #00798C, rosered #D1495B, amber #E09F3E, leaf #2E8B57, plum #6A4C93.
Boxes (all `enhanced,breakable`, title=`{#1}`): `eqbox` (white, navy frame: labeled equation), `verdict` (teal: key takeaways), `goodbox` (leaf: small example with numbers), `notebox` (amber: notes, cautions, notation points), `proofbox` (plum: full proofs, numbered steps, end with a black square), `zerobox` (rosered: everyday analogy).
Column types: `\newcolumntype{P}[1]{>{\raggedright\arraybackslash}p{#1}}` and `\newcolumntype{Y}{>{\raggedright\arraybackslash}X}`; use `Y` instead of `X` so narrow columns do not stretch.
Header: paper short title left, "Guide from zero -- v1" right; page number center. Section titles navy with a teal rule.

Structure:
1. **Cover**: navy band via TikZ overlay (title "Understanding the Paper from Zero", paper title, authors, version, date), then a `verdict` box "The whole paper in five sentences", a `notebox` "How to read this guide" (say which numbers are examples), and a small TikZ roadmap of the parts. Then table of contents.
2. **Part A - Background from zero**: one short section per needed concept, each with a picture or analogy (`zerobox`). Include a linear-algebra/probability tools table (tool | meaning in simple words | where used). End with the paper's problem as an analogy.
3. **Part B - Map and symbols**: TikZ equation map on an absolute grid (`\def\dx{40mm}\def\dy{25mm}`, nodes about 29 mm wide, straight arrows, no crossings, short arrow labels), one-line story, "how each section is built" note; all-symbols table (symbol | simple meaning | value in paper); notation-points `notebox`.
4. **Part C - Every equation, with proofs**: one section per equation/proposition: labeled `eqbox` -> **In plain words** -> `proofbox` with a full step-by-step proof (state every condition the proof needs) -> helper drawing -> `goodbox` small example with real numbers (and Monte Carlo check) -> **Why the paper needs it**. Also cover policy/score rules, the main proposed rule (re-use the paper's own TikZ system figure via `\resizebox{0.97\textwidth}{!}{\input{...}}` if it exists), and complexity with an operation count.
5. **Part D - Results explained**: experiment setup list; metrics table with formulas (e.g., % reduction, CI = mean +- t*s/sqrt(n) with the t value, gap closed) and one paper example each; rebuild the main tables as colored tables (`\rowcolors`) with "how to read it"; include the paper's figures (`\includegraphics` of the PDFs) each followed by a `notebox` "What to see"; the mechanism explanation; limitations stated by the authors.
6. **Part E - Checks and summary**: "Checked by our own simulation" table (item | formula/paper | ours | OK), our re-simulation figure, a `verdict` box on correctness listing any errors/notation points; summary table (one line per equation) using `tabularx` (NOT xltabular: an xltabular ending the document caused an `\cmrsideswitch` error); mini glossary.
Put `\Needspace{14\baselineskip}` before every `\section` (a regex pass is easiest) and `\clearpage` before each Part and before the summary, to avoid orphan headings.
Avoid long lists of numbers inside `$...$` in narrow table cells (they cannot break and overflow); write them as text with `$-$` for minus signs.

Compile 3 times: `pdflatex -interaction=nonstopmode`. Check the log for `^!` errors and `Overfull` lines and fix them. Missing packages: `apt-get install -y texlive-latex-extra texlive-fonts-extra texlive-science texlive-pictures`.

## Step 6 - Check before sending
- Render all pages with `pdftoppm -r 45 -png` and make a montage (7 per row); look at page breaks, empty areas, orphan headings.
- Render the equation pages at 75 dpi (4 pages side by side) and inspect EVERY eqbox: no overlapping labels, no label crossing the frame, no line crossing label text. Fix and recompile until clean. (`pdftoppm` is enough; installing PyMuPDF can be slow.)
- Confirm all paper numbers match the paper and all example numbers match `numbers.json`.
- Deliver the PDF with SendUserFile (display: render). In the reply, say in a few short lines what each part contains, what was verified (and how closely our re-simulation matches), and list the notation points/errors found for the authors.