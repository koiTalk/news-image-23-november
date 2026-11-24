# The World in One Day — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/koiTalk/news-image-23-november/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/koiTalk/news-image-23-november/reward.svg)](https://make.fun/c/news-image-20261123)

A single 1024×1024 image summing up the world news of Monday 23 November 2026:
**60 stories** — 3 lead stories, 12 more news items, 45 also-today items — plus the
final US market closes.

## Top stories

- **COP31 collapses: "worst COP ever"** — the UN chief voices deep disappointment
  as 190 nations fail in Antalya; COP32 is set for Addis Ababa in 2027.
- **Kyiv region: at least 14 dead** — a boy, 7, is pulled alive from the Dymer
  flats as the toll there hits 11; 23 Nov is a day of mourning.
- **Russian warship sinks at Benghazi** — corvette Merkury burns after a suspected
  drone blast; the UN demands a swift, independent probe.

## Markets (US close, final)

S&P 500 7,237.17 (+4.73%), Nasdaq 24,089.56 (+6.51%), Dow 49,595.31 (+3.01%);
Nvidia +31.48% to $165.05; Kospi −3.31%; gold $3,671.80; Brent $89.10.

## How it is built

`main.py` (Python 3.13, standard library only, no network) draws the broadsheet
with a hand-written 5×7 bitmap font and a hand-written PNG encoder
(`zlib` + `struct`, no PIL). It is fully deterministic: two runs produce
byte-identical output.

```sh
MAKEFUN_OUTPUT_DIR=/output python3 main.py
# writes /output/entry.png (1024x1024, ~32 KB)
```

All stories happened or were first reported on 23 November 2026.
