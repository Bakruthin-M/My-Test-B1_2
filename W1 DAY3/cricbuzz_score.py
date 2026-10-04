"""
Week 1 - Day 3 - Task 1
Capture a live cricket score from Cricbuzz with Playwright (sync API).

How the selectors were found (Inspect on cricbuzz.com, verified in the console):
    document.querySelector("a.bg-cbWhite[href*='/live-cricket-scores/']")
Each match card on the home page is an <a> with class "bg-cbWhite" that links to
/live-cricket-scores/... Inside a card:
    - every team row is a div.justify-between with the team name and a
      span.font-medium holding the score, e.g. "242-5 (20)"
    - the last <span> of the card is the status line, and its colour class tells
      the match state:  text-cbLive  /  text-cbComplete  /  text-cbPreview

Usage:
    python cricbuzz_score.py            # headless
    python cricbuzz_score.py --headed   # watch the browser do it
"""

import sys

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

URL = "https://www.cricbuzz.com/"
SCREENSHOT = "score.png"

# Cricbuzz serves an "Access Denied" page to the bare headless browser.
# Sending a normal desktop user agent is enough to be treated like a real visitor.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

CARD = "a.bg-cbWhite[href*='/live-cricket-scores/']"  # one match card
LIVE_STATUS = "span.text-cbLive"                         # red status line = match in progress
SCORE_ROW = "div.justify-between:has(span.font-medium)"  # team-name + score row


def read_card(card):
    """Return (team_lines, status) for one match card."""
    team_lines = []
    for row in card.locator(SCORE_ROW).all():
        name = row.locator("span").first.inner_text().strip()
        score = row.locator("span.font-medium").inner_text().strip()
        if score:
            team_lines.append(f"{name} {score}")
    status = card.locator("span").last.inner_text().strip()
    return team_lines, status


def main(headless):
    with sync_playwright() as p:
        # channel="chromium" uses the full Chromium build; the slim
        # "headless shell" that Playwright uses by default gets blocked.
        browser = p.chromium.launch(headless=headless, channel="chromium")
        page = browser.new_page(user_agent=USER_AGENT, viewport={"width": 1400, "height": 900})
        page.goto(URL, wait_until="domcontentloaded")

        # Wait for the thing we actually need: the first match card.
        # No fixed sleep - this returns the moment the card is rendered,
        # and raises a clear TimeoutError if it never shows up.
        page.wait_for_selector(CARD, timeout=30_000)

        cards = page.locator(CARD)
        live_cards = cards.filter(has=page.locator(LIVE_STATUS))

        if live_cards.count() == 0:
            # Do not crash - say so, and still leave the screenshot behind.
            print("No match is live on Cricbuzz right now.")
            latest = cards.first
            team_lines, status = read_card(latest)
            print(f"Latest result: {latest.get_attribute('title').strip()} - {status}")
        else:
            card = live_cards.first
            team_lines, status = read_card(card)
            title = card.get_attribute("title").strip()   # e.g. "India vs West Indies, 3rd ODI"
            teams = title.split(",")[0]
            for line in team_lines:
                print(line)
            print(f"{teams} - {status}")

        page.screenshot(path=SCREENSHOT)
        print(f"\nsaved {SCREENSHOT}")
        browser.close()


if __name__ == "__main__":
    headed = "--headed" in sys.argv
    try:
        main(headless=not headed)
    except PlaywrightTimeout:
        print("Cricbuzz did not show any match cards in time. Check your connection and try again.")
        sys.exit(1)
