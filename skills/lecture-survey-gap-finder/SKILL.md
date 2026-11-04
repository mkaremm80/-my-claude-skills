---
name: "lecture-survey-gap-finder"
description: "Turn any research topic, in any field, into a colorful PDF lecture survey of recent papers with figures, research gaps and a table of Q1 paper ideas."
---

# Lecture Survey and Gap Finder

Use this skill when a student or researcher gives a topic (any field: engineering, medicine, education, business, physics, social science...) and asks for a literature survey, a "lecture survey", research gaps, or paper ideas for a Q1 journal.

The output is one colorful A4 PDF (LaTeX), about 8-12 pages, named `<Short_Topic>_Survey_Gaps_Ideas_v1.pdf`. It contains: the papers at a glance, a survey written like a lecture, figures, a gap table, an ideas table, and a starting plan for the best three ideas.

Writing style: English, short sentences, simple words (B2 level), professional. Every number must come from a paper. Anything that is your own estimate or classification must be labeled as such.

## Step 0 - Ask (one short message, or AskUserQuestion)
Ask only what you cannot guess. Use defaults if the person does not answer.
1. Topic and field (required).
2. Year range (default: the last 2-3 years until today) and number of papers (default 20).
3. The student's background and skills (e.g., coding, statistics, lab access, clinical data). This fills the "Fit" column of the ideas table. If unknown, write "Fit" from general feasibility instead.
4. Any target journal or venue (optional).

## Step 1 - Find the papers
1. Use SciSpace `search-papers` if it is available (load it with ToolSearch). Otherwise use WebSearch on Google Scholar, Semantic Scholar, arXiv, PubMed (medicine), ERIC (education), SSRN (business), etc.
2. Run 5-7 searches, each a full natural-language question, each covering one sub-area of the topic (methods, applications, experiments, reviews, emerging directions). Run them in parallel.
3. Keep papers inside the year range. Remove: duplicates (same title on arXiv and journal - keep the journal version), papers outside the range, and unreliable uploads (repositories with extraordinary claims, AI tools listed as authors, no affiliation, no method). Say in the PDF what you removed and why.
4. Mark preprints (arXiv, medRxiv, SSRN, Preprints.org) as "not yet peer reviewed".
5. For each kept paper record: ID, short title, authors, venue, date, DOI/URL, type (Experiment / Theory-Method / Review / Dataset / Clinical trial / Case study ...), theme, and every number in the abstract (results, sizes, distances, accuracy, sample size, p-values...).

## Step 2 - Analyse
1. Group the papers into 4-6 themes. Each theme gets one color.
2. For each theme find: the trend over time, the best reported numbers, and the open problem the authors admit.
3. Choose 6-9 aspects that matter in this field for the coverage matrix (examples: engineering - experiment, hardware, channel model, coding, ML, network, security; medicine - RCT, sample size >1000, low-income setting, long follow-up, AI model, cost analysis; education - K-12, higher ed, randomized design, long-term effect, AI tool, teacher training). Tag each paper only when its abstract clearly reports that aspect.
4. Find 6-10 gaps. Every gap needs evidence: paper IDs and numbers. A column with 0-2 papers in the coverage matrix is a gap candidate, but explain why it matters.
5. Turn gaps into 6-8 paper ideas. Each idea: title, gaps it fills, main method, key result to show, fit with the student, target Q1 journal, effort.

## Step 3 - Novelty check (required)
For the 3 strongest ideas, run one search each ("Has X been done for Y?"). Record the closest papers found (N1, N2, ...). In the PDF say for each idea: "not found in our search", "partly done by [Nk]", or "already done - drop or change". Always warn that a quick search is not a full novelty check.

## Step 4 - Figures (matplotlib, STIX font, pdf.fonttype=42, about 6.8 x 4 in, 10-11 pt)
Make as many as the data allows; never invent data.
1. Timeline: x = date, y = theme, marker shape = type, paper ID written inside the marker.
2. Key-metric plot: the main number of the field vs the main condition (rate vs distance, accuracy vs dataset size, effect size vs sample size, cost vs year...). Only numbers from abstracts. Use filled vs empty markers when two regimes exist (e.g., finite vs asymptotic, internal vs external validation). Annotate the trend with an arrow and a note box.
3. Records / benchmark bar chart: best result per approach, with the trade-off written next to each bar.
4. Field pipeline diagram (TikZ): the generic chain of the field (e.g., data -> model -> evaluation -> deployment; patient -> diagnosis -> treatment -> follow-up). Put red gap badges G1, G2... on the blocks where each gap sits.
5. Coverage matrix: rows = papers grouped by theme color, columns = aspects, check marks, bottom row = totals, red totals for columns with <= 2 papers. Caption: "our classification from the abstracts".
6. Idea map: x = effort/risk, y = expected impact, color = fit with the student; shade the "start here" box. Caption: "our estimate, not a measured value".
7. Novelty map for the best idea: the closest existing works on a timeline by category, plus a star for the empty spot the idea fills.

Plotting rules: render each figure to PNG (`pdftoppm -r 70`) and look at it. Fix overlapping labels, clipped text, and legends that cover data (use explicit text positions; put annotation boxes in empty areas).

## Step 5 - Build the PDF (LaTeX)
Preamble: `article`, a4paper, margin 18 mm, `helvet` sans, `xcolor[table]`, `tcolorbox[most]`, `tikz` (arrows.meta, positioning, calc, fit, backgrounds), `booktabs`, `tabularx`, `xltabular`, `array`, `enumitem`, `titlesec`, `fancyhdr`, `float`, `caption`, `needspace`, `graphicx`, `amsmath`, `hyperref[hidelinks]`.
Colors: navy #1B3A5C, teal #00798C, rosered #D1495B, amber #E09F3E, leaf #2E8B57, plum #6A4C93.
Boxes (`\newtcolorbox{name}[1]{...title={#1}}`): `verdict` (teal, main message), `stepbox` (navy, "How to read it"), `goodbox` (green, "What it tells us"), `notebox` (amber, abbreviations/notes), `critical` (red, "Before you start writing"), `ideabox[2]` (color as 2nd argument, breakable).
Macros: citation `\newcommand{\cit}[1]{\textcolor{navy}{[#1]}}` - NEVER redefine `\ref` (it breaks section references). Gap badge `\gap{G1}` and idea badge `\idea{I1}` as small colored TikZ nodes.

Structure:
1. Cover band (navy TikZ band + teal strip): topic, "Literature survey, research gaps and Q1 paper ideas", number of papers, date range, version, date, prepared for.
2. `verdict` box: the main message in three sentences. `stepbox`: how to use the guide. `notebox`: abbreviations table (define every abbreviation once).
3. How the papers were selected (searches, filters, what was removed).
4. The papers at a glance: table (ID, short title, venue, date, type; zebra rows; navy header) + timeline figure + `goodbox`.
5. Literature survey (lecture style): one subsection per theme, 6-10 sentences, story order (oldest to newest), numbers with citations, end with "Message:" and the gap badge. Put the key-metric figure in its theme with `stepbox` + `goodbox`. Then the records figure + `goodbox`. This section can be reused as the "Related Work" of a paper.
6. Where the gaps sit: pipeline diagram + `goodbox`.
7. Coverage matrix + `stepbox` + `goodbox`.
8. Research gaps table: Gap | Short name | Evidence from the papers | Why it matters.
9. Paper ideas table (`xltabular`): ID | Idea | Gaps | Main method and key result | Fit | Target journal. Add a gray note: "check the current journal quartile (JCR or Scimago) before you submit". Then the idea map + `goodbox`.
10. Best three ideas: one `ideabox` each with Problem, Possible contributions (numbered, no bold), First simulation/experiment, Risk. Put the novelty map next to idea 1.
11. `critical` box: before you start writing (repeat novelty search on 2-3 databases, read full texts, update preprints).
12. References: the surveyed papers [1..n] and the novelty-check papers [N1..]. Use `\sloppy` before the list. Gray footnote: data source and date, which figures are exact data and which are estimates.

Layout: do not put `\clearpage` before every section (it leaves half-empty pages). Use `\Needspace{12-30\baselineskip}` before headings that are followed by a big table or figure, so a heading is never alone at the bottom of a page. Compile twice with `pdflatex -interaction=nonstopmode`. Missing packages: `apt-get install -y texlive-latex-extra texlive-fonts-extra texlive-science texlive-pictures`.

## Step 6 - Check before sending
- Render all pages (`pdftoppm -r 55`) into 4-page sheets and look at every sheet: no orphan headings, no half-empty pages, no overlaps, tables inside margins (fix Overfull hbox warnings above ~10pt).
- Zoom (`-r 110`) on the pipeline diagram and the idea table.
- Check every number in the text and figures against the abstracts; check ratios you state (e.g., "about 4 orders of magnitude").
- Make sure every estimate (coverage tags, idea map, fit) is labeled as an estimate.

## Step 7 - Deliver
Send the PDF with SendUserFile. Reply in a few short lines: the main finding, the list of figures, the best three ideas with one line each, and the limits (estimates, quick novelty check). Give a "Sources:" list. Any revision keeps the name with a new version number (v2, v3, ...).

## Adapting to other fields (quick guide)
- Medicine / health: key metric = effect size, AUC, mortality, sample size; pipeline = population -> screening -> diagnosis -> treatment -> follow-up; targets like The Lancet Digital Health, JAMA Netw Open, BMJ Open (check quartile).
- Education: key metric = learning gain / effect size vs sample size or duration; pipeline = learner -> content -> teaching method -> assessment -> outcome.
- Business / economics: key metric = return, cost, adoption rate vs time or firm size; pipeline = input -> process -> market -> performance.
- Computer science / AI: key metric = accuracy vs model size or data size; pipeline = data -> model -> training -> evaluation -> deployment.
- Physical sciences / engineering: key metric = main performance vs distance, power, temperature or size; pipeline = the physical system chain.