---
name: "paper-explainer-video"
description: "Make a 16:9 animated dashboard explainer video (mp4 + Python script + narration) for a section or result of a research paper, with a parameter sweep and live plots."
---

# Paper explainer video (dashboard style)

Use this when the user asks for an explainer video, animation or "video like the FAS one" for a paper, a section (system model, a theorem, a result figure) or a concept for teaching.

## What the output looks like
One 16:9 frame (1920x1080, 30 fps, white background, colorful):
- Top: a small grey credit line, a bold title, and a one-line purple summary of the setup.
- Left (about 40% width): an animated physical scene (waves, antennas, nodes, users, circuits). It moves every frame, with markers that show the decisions or outcomes.
- Right: a 2x2 grid of live panels. Static curves are drawn once; a dotted vertical line and dots move along them. One panel may be fully redrawn each frame (for example a bar chart of one realization).
- Bottom: a yellow rounded caption box. It changes 4-6 times as the swept parameter crosses thresholds, then shows a summary with the key numbers during a final hold.
- An optional inset in the scene (for example a complex-plane arrow) for the key quantity.

## Procedure
1. Read the paper section. Pick ONE swept parameter that tells the story (horizon, SNR, speed, tilt, number of blocks, and so on). Write the one-sentence message the video must show.
2. Re-implement the model in numpy/scipy, using the paper's own equations and parameter values. Verify the key numbers (closed forms vs. numerical integration, table values, limits) before drawing anything. Tell the user if something does not match.
3. Precompute the expensive parts: Monte Carlo curves on a fine grid (around 21 points, about 20k draws), and cache them.
4. For realization panels, use ONE fixed random draw that varies smoothly with the parameter (for example a finite plane-wave sum with fixed paths, and noise drawn once). Scan seeds and choose one that tells the story clearly; say this in the narration notes.
5. Timeline: intro hold (about 2 s), an eased sweep (0.5 - 0.5 cos(pi x)), and a final hold (about 3 s). Default 17 s; for voice-over make it about 60 s (for example 8 / 42 / 10 s).
6. Write the script with argparse: `--out`, `--preview` (writes 3 PNG frames), `--dpi`. Put the parameters at the top (CREDIT, model values, SEED, timings). Render with matplotlib FFMpegWriter (libx264, yuv420p, bitrate 6000), using a grab_frame loop.
7. ALWAYS render the previews first and look at them. Fix overlaps, then render the full video. Afterwards, extract 4 frames with ffmpeg and check them.
8. Deliver the .mp4, the .py and a narration .md (time | caption | what to say in simple English | panel guide | settings | easy edits). Number versions v1, v2, ....

## Layout lessons (avoid these bugs)
- For the scene axes use `set_aspect('equal', adjustable='datalim')` and centre the xlim on the content, or the scene shrinks and gets clipped.
- Put long scene labels where nothing moves; check that inset axes do not cover labels.
- Legends: put them in empty regions (often `lower right` for outage-type curves). Use `ncol=2` for bar panels and leave headroom in ylim for markers.
- Keep the gridspec top at about 0.86, so the subtitle does not hit the panel titles, and the bottom at about 0.155, so a two-line caption does not hit the x-labels.
- Formula text goes inside the axes in an empty area, not over a curve.
- Full redraws (cla) are only for the scene and one realization panel; the others use set_data. About 4 minutes for 510 frames at 1080p is normal.

## Style constants
Blue #1c7ed6, orange #e8590c, green #2f9e44, red #e03131, teal #0c8599, purple #7048e8, gray #868e96, ink #212529, gold #f59f00. Bold titles at 11.5 pt, base font 10 pt, top/right spines off.

## Language
Captions and narration use simple English (B2 or below), with short sentences and numbered caption steps ("1 ·", "2 ·", ...).