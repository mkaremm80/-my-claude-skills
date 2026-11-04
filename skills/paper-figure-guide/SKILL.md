---
name: "paper-figure-guide"
description: "Explain every figure of a research paper in a colored PDF guide with annotated figures (callouts, arrows, shaded regions) and helper drawings. Use when asked to explain or understand a paper's figures."
---

# Paper Figure Guide

Turn the figures of any research paper (PDF or LaTeX) into a colored, easy-to-read PDF guide. Every figure is shown again with explanations drawn on it (numbered red circles, arrows, notes, shaded regions), followed by "How to read it" and "What it tells us" boxes. Add one or two helper drawings for the key ideas the figures assume.

Writing style: English, short sentences, simple words (B2 level), professional. Numbers must come from the paper, never invented. If you illustrate with your own example (e.g., one simulated realization), say so clearly next to it.

## Step 1 - Read the paper and plan
1. Read the whole paper first. List every figure (and panel), its caption, the section that discusses it, and the numbers the text quotes about it.
2. Find the paper's main message and write the story chain: which figure shows HOW the system works, which shows WHEN/WHERE the method helps, which shows HOW MUCH it gains. This chain goes on the cover.
3. Decide which concepts a reader needs to understand the figures (e.g., a dimension, a threshold, a mechanism). Each one becomes a helper drawing.

## Step 2 - Get the figure content
Use the best source available, in this order:
1. **LaTeX source / TikZ / data files** given by the user: reuse them directly.
2. **Vector plots inside the PDF** (MATLAB/matplotlib exports): extract the real data with PyMuPDF (`pip install --break-system-packages pymupdf`; `import pymupdf as fitz`).
   - `page.get_drawings()` gives paths with color, width and items. A curve is usually one path with many `'l'` (line) items; markers are small closed paths; error bars are short vertical lines plus caps.
   - Group by stroke color to separate series; split panels by x-range.
   - Calibrate axes from tick labels: take text spans from `page.get_text('dict')`, keep numeric spans of the tick font size inside the axis region, and fit pixel-to-value with `np.polyfit`. Check the calibration against a number quoted in the text or a printed value (e.g., heat-map cell labels can be read directly as text spans).
   - If an x-calibration looks wrong (picked up nearby labels), use the known discrete x values (e.g., budgets 3..8) by order.
3. **Raster images** (`pdfimages -list`, then `pdfimages -png`): keep the image and draw annotations on top (TikZ overlay or matplotlib `imshow` + `annotate`). Read values from the figure only when the text confirms them.
4. Always verify extracted data with at least one number from the text (e.g., recompute a reported percentage).

## Step 3 - Make the annotated figures
- **Block diagrams / system figures:** if TikZ source exists, add numbered badges at node anchors, e.g.
  `\tikzset{badge/.style={circle, fill=red!75!black, text=white, font=\footnotesize\bfseries, inner sep=1.2pt, minimum size=4.2mm}}` then `\node[badge] at (tx.north west) {1};`. Compile as a `standalone` PDF. For raster diagrams, overlay badges with TikZ `\begin{scope}[x={(img.south east)},y={(img.north west)}]`. Explain each number in a table (No. | Part | What it means).
- **Plots:** redraw with matplotlib from the extracted data at readable size (about 6.8 x 4.2 in, fonts 10-11 pt, `font.family='STIXGeneral'`, `mathtext.fontset='stix'`, `pdf.fonttype=42`). Then add:
  - `ax.annotate(text, xy=point, xytext=box_position, arrowprops=dict(arrowstyle='-|>', color='#C0392B', lw=1.4), bbox=dict(boxstyle='round,pad=0.3', fc='#FFF8E1', ec='#E09F3E'))` for notes.
  - `ax.fill_between` (green for gain, red for loss) and `ax.axvspan` for regimes.
  - boundary lines (e.g., a red staircase on a heat map), reference lines, and the key numbers (max gain, crossing points).
  - Put long explanations in the title or in the guide text instead of inside the plot.
- **Helper drawings:** small plots that make the hidden concept visible (e.g., eigenvalue bars + cumulative energy to show an effective dimension; one example realization showing where probes or samples go). Label them "Helper drawing A/B" and say what is an illustration.
- Render every figure to PNG (`pdftoppm -r 70`) and look at it. Fix any label that overlaps data, colorbars, legends or axis labels before moving on.

## Step 4 - Build the colored PDF (LaTeX)
Use `article`, A4, `helvet` sans font, `xcolor[table]`, `tcolorbox[most]`, `tikz`, `booktabs`, `tabularx`, `enumitem`, `titlesec`, `fancyhdr`, `float`, `caption`, `needspace`, `bm`. Define colors navy #1B3A5C, teal #00798C, rosered #D1495B, amber #E09F3E, leaf #2E8B57 and boxes: `verdict` (teal), `goodbox` (green, "What it tells us"), `notebox` (amber), `critical` (red), `stepbox` (navy, "How to read it"). Define `\newcolumntype{P}[1]{>{\raggedright\arraybackslash}p{#1}}`. Pass box titles as `title={#1}` (an `=` inside a title breaks otherwise).

Structure:
1. **Cover banner** (navy TikZ band): "How to Read Every Figure in the Paper", paper title, date.
2. **Story box:** a 3-box TikZ chain (Fig. X - HOW -> Fig. Y - WHEN -> Fig. Z - HOW MUCH) and the main message in 2-3 sentences.
3. **Words used in this guide:** table of symbols and terms in simple words.
4. **One section per figure** (start big sections with `\clearpage` or `\Needspace{14\baselineskip}` so headings are not left alone at a page bottom). For each panel: annotated figure, "How to read it" (numbered steps: axes, units, colors, what each marker/line is), a small table of the key values when useful, and "What it tells us" (trends, crossing points, best/worst cases, why).
5. **Helper drawings** placed right after the figure that needs them.
6. **Summary table:** one sentence of meaning per figure.
7. A gray footnote stating the data source (exact paper data vs. illustrative example).

Compile twice with `pdflatex -interaction=nonstopmode`. If TeX packages are missing: `apt-get update && apt-get install -y texlive-latex-extra texlive-fonts-extra texlive-publishers texlive-science`. If `newtxmath` fails with `binhex.tex not found`, use `mathptmx` instead.

## Step 5 - Check before sending
- Render all pages (`pdftoppm -r 50`) into a montage and look at every page: no overlaps, no orphan headings, figures readable, badges not covering text.
- Every number in the guide matches the paper (or is clearly labeled as an illustration).
- Deliver the PDF with SendUserFile and give a short summary of what each figure section contains.
- If the user asks for changes, keep the same file name with a new version number (v2, v3, ...).