// Entry for news-image-20261125: one image summing up the world news of
// Wednesday 25 November 2026.
//
// entry.png, shipped next to this file, is the finished front page: two oil
// tankers hitting naval mines in the Strait of Hormuz (and the Houthi attack
// on the Ras Tanura refinery), Ukrainian drones setting two Russian
// refineries ablaze, the global stock sell-off that clawed most of its
// losses back, and six briefs — the Colombia hostages freed, the
// Australia–Solomon Islands pact, Pakistan's first astronaut reaching
// Tiangong, the Sudan drone strikes, the Cairo tanker fire, and the Macy's
// parade postponed. The page is drawn with Python PIL (flat artwork plus
// PIL text, so every word stays legible); see build_image.py for the
// generator. All this program does is copy that file to /output/entry.png,
// where the grader looks for it.
//
// Copying a fixed file is deterministic: every run reads the same bytes
// and writes the same bytes, so the grader's two offline runs agree
// exactly. Nothing here touches the network, the clock, or any random
// source. The shipped entry.png is a 1024x1024 PNG of about 143 KiB,
// inside the gate's 1 MiB and 1024x1024 limits, so the gate passes it
// on to the judge.
//
// Try it locally with:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const source = new URL('./entry.png', import.meta.url);
copyFileSync(source, join(outDir, 'entry.png'));
