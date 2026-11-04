# Paper Understanding Skills for Claude

Six Claude skills that help students and researchers work with research papers.
Give Claude a paper (PDF or LaTeX) and ask for one of the outputs below, or give Claude a topic for a lecture survey.

| Skill | What you get | Ask Claude like this |
|---|---|---|
| [paper-figure-guide](skills/paper-figure-guide/SKILL.md) | A colored PDF guide. Every figure is redrawn with numbered callouts, arrows and shaded regions, then "How to read it" and "What it tells us" boxes. | "Explain the figures of this paper." |
| [paper-equation-guide](skills/paper-equation-guide/SKILL.md) | A colored PDF guide. Every equation has labeled terms, plain meaning, a worked numeric example, helper drawings and a simulation check. | "Explain the math of this paper." |
| [paper-explainer-video](skills/paper-explainer-video/SKILL.md) | A 16:9 animated dashboard video (mp4) with a parameter sweep and live plots, plus the Python script and a narration file. | "Make an explainer video for Section III." |
| [paper-comic](skills/paper-comic/SKILL.md) | A comic-magazine PDF (A4, about 8 pages) that tells the paper as a story with characters, panels and speech bubbles. | "Turn this paper into a comic." |
| [lecture-survey-gap-finder](skills/lecture-survey-gap-finder/SKILL.md) | A colorful PDF lecture survey (A4, about 8-12 pages) of recent papers on any topic, with figures, a research-gap table and a table of Q1 paper ideas. | "Make a lecture survey on [topic] with gaps and Q1 ideas." |
| [paper-from-zero-guide](skills/paper-from-zero-guide/SKILL.md) | A colorful PDF guide (A4, about 20-30 pages) that explains a paper from zero: background, every equation with labels, full proofs, examples, results, and simulation checks. | "Explain this paper from zero." |

All skills follow the same rules: simple English (B2 level), every number comes from the paper,
illustrative examples are clearly labeled, and each output is checked visually before delivery.

## Install

### Claude app (claude.ai / desktop)
1. Download a skill zip from the [`dist/`](dist) folder (one zip per paper skill; lecture-survey-gap-finder and paper-from-zero-guide have no dist zips yet, install them via Claude Code below).
2. Go to **Settings → Capabilities → Skills** and upload the zip.
3. Turn the skill on, then ask Claude as shown in the table above.

### Claude Code
Copy the skill folders into your skills directory:

```bash
git clone https://github.com/mkaremm80/-my-claude-skills.git
mkdir -p ~/.claude/skills
cp -r -my-claude-skills/skills/* ~/.claude/skills/
```

## Requirements
The skills run code in Claude's workspace. They use:
- Python: `numpy`, `scipy`, `matplotlib`, `pymupdf`, `Pillow`, `playwright` (Chromium)
- LaTeX: `pdflatex` with `texlive-latex-extra`, `texlive-fonts-extra`, `texlive-science`, `texlive-pictures`, and the `annotate-equations` package
- Tools: `ffmpeg` (video), `poppler-utils` (`pdftoppm`, `pdfimages`)

Each SKILL.md says how to install anything missing.

## Repository layout
```
skills/
  paper-figure-guide/SKILL.md
  paper-equation-guide/SKILL.md
  paper-explainer-video/SKILL.md
  paper-comic/SKILL.md
  paper-comic/scripts/comic_engine.py   # same engine as in SKILL.md, ready to import
  lecture-survey-gap-finder/SKILL.md
  paper-from-zero-guide/SKILL.md
dist/                                   # zips for the four paper skills, for upload to the Claude app
```

## Author
Prof. Mahmoud Abdelaziz, Military Technical College (MTC), Cairo, Egypt
[Google Scholar](https://scholar.google.com/citations?user=vwLQ_4UAAAAJ) · [GitHub](https://github.com/mkaremm80)

## License
MIT. See [LICENSE](LICENSE).
