# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/fouZee/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/fouZee/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the make.fun bounty `news-image-20261125`: one image summing up the world news of Wednesday 25 November 2026.

A newspaper front page. The lead story is two oil tankers hitting naval mines in the Strait of Hormuz — both exploding and catching fire — with the Houthis saying they attacked the Ras Tanura refinery; below it, Ukrainian drones setting two Russian refineries ablaze and the global stock sell-off that clawed most of its losses back; six briefs cover the Colombia hostages freed, the Australia–Solomon Islands pact, Pakistan's first astronaut reaching Tiangong, the Sudan drone strikes, the Cairo tanker fire, and the Macy's parade postponed. The illustration is flat artwork drawn with PIL; all text is drawn with PIL so it stays legible.

`build_image.py` regenerates `entry.png` from scratch (Python 3 + Pillow, system DejaVu fonts).

`main.ts` (Node 22, standard library only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The copy is byte-identical on every run: no network, no clock, no randomness.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards
