[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/iqbalbeladaz/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/iqbalbeladaz/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World in One Day — Wednesday 25 November 2026

My entry for the make.fun bounty `news-image-20261125` ("Sum up
25 November's world news in one image", $100 pool). The whole of
Wednesday 25 November 2026, set as a single 1024×1024 broadsheet page.

## How it is put together

- `generate.py` — an original Pillow renderer. It paints the page
  from nothing: navy masthead with the date, one lead story, seven
  story cards in two columns, a markets panel, and a dark "also today"
  band of one-line briefs. Run it and it writes `entry.png`.
- `entry.png` — the finished picture, 1024×1024, regenerated
  byte-for-byte by the script above.
- `main.ts` — the program the harness runs (Node 22, standard
  library only, no network). It simply delivers the picture to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, defaulting to `/output`.

## The day it covers

Eight lead stories, each first reported on Wednesday 25 November 2026:

1. Yemen's Houthis say they attacked Saudi Arabia's Ras Tanura oil
   refinery and Riyadh's financial district; 11 wounded in a tower
   strike on Tuesday.
2. Vladimir Putin vows "inevitable" retaliation for Ukraine's strikes
   on Russian refineries.
3. Volodymyr Zelensky confirms Ukraine hit the Russian cargo ship
   Sparta II in the Gulf of Finland; Norway urges caution.
4. Nvidia falls about 6% as US lawmakers question Trump's role in
   Jensen Huang's return; Asian tech stocks tumble, Nikkei down 2.8%.
5. All hostages are freed as Colombian forces storm a supermarket in
   Cartagena after a day-long siege; one captor killed.
6. China investigates Shanghai party chief Chen Jining — the fourth
   Politburo member probed in the graft crackdown since 2025.
7. Israeli strikes in Gaza kill seven, including a Hamas security chief.
8. Pakistan's first astronaut reaches China's Tiangong station as
   Shenzhou-24 launches from Jiuquan.

Briefs along the bottom: the US shelves proposals to use business
deals to end the Ukraine war (FT); Trump warns Iran of a "very
traumatic" outcome if the nuclear deal fails; rescuers search for
dozens trapped in a flooded gold mine in West Java; Senegal regains
its Africa Cup of Nations title after a CAS ruling; Thanksgiving
travel builds across the US as core inflation data lands.

Every headline was cross-checked across the day's sources (Reuters,
AP copy, BBC, Al Jazeera, the Kyiv Independent and the 25 November
roundups) before it was set on the page.

## License

MIT — see `LICENSE`.
