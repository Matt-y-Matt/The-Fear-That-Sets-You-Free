# The Fear That Sets You Free: handoff

A mobile-first scripture page on the fear of God, opened by scanning a QR code. It is finished and tested; it only needs deploying and a QR code.

## Files

- `index.html`: the complete page, one self-contained file. This is all that needs deploying.
- `data.py`: all content (segments, prayers, sub-themes, ESV verse text). Edit content here.
- `build.py` + `build2.py`: regenerate `index.html` from `data.py` with `python build2.py`.
- `make_qr.py`: makes the QR code once the page is live.

## Deploy (pick one)

1. **Vercel CLI.** In this folder run `npx vercel --prod`. Choose scope "cofounder-6147's projects", don't link to an existing project, name it `fear-that-sets-you-free`, directory `./`, and don't override settings.
2. **GitHub + Vercel.** Create a private repo `fear-that-sets-you-free`, add `index.html`, then on vercel.com/new import the repo and click Deploy. No build settings needed.

Note: Vercel's connector in Claude chat is not permitted to create projects (403), so do the first deploy from Claude Code or by hand.

## QR code

After deploying, run `python make_qr.py https://<live-address>`. It uses high error correction, navy on white, and outputs PNG and SVG. Test-scan it on both iPhone and Android before printing.

## What's in the page

- Cover: the title, a subtitle, and Exodus 20:20 as the cover verse.
- "Start here": the two kinds of fear.
- "Where are you right now?": three large tappable boxes that jump to each section.
- "How the links work": where the buttons go, what a commentary is, why to use one, and when to read it.
- Three sections, each with a "For you if…" intro, framing, a prayer (placed first), a contents list, sub-themes with verse cards, and "Back to the top" plus links to the other sections.
  - Bigger Than Your Fears
  - Bigger Than Your Sin
  - Back to Wonder
- Every verse card has two buttons:
  - "Read the whole chapter" goes to `https://www.bible.com/bible/59/{USFM}.{ch}.ESV` (59 = ESV).
  - "What does this mean?" goes to `https://enduringword.com/bible-commentary/{slug}-{ch}/` (David Guzik; slugs like `psalm`, `1-john`).
- A floating Top button, a Share button, automatic dark mode, and the Crossway ESV notice in the footer.

## Before printing

- ESV text was entered from memory and spot-checked. Have someone proofread the verses against the chapter links.
- The page quotes 203 verses across 114 cards, under the ESV's 500-verse quotation limit. Keep it under 500 if adding more.
- Enduring Word links were pattern-generated and checked on a sample. Tap through a few after deploying.
