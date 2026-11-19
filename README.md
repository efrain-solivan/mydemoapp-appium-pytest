# My Demo App — Appium + Pytest mobile suite

![Mobile tests](https://github.com/efrain-solivan/mydemoapp-appium-pytest/actions/workflows/tests.yml/badge.svg)

Automated UI tests for Sauce Labs' [My Demo App](https://github.com/saucelabs/my-demo-app-android)
(Android), written in Python with Appium 3 (UiAutomator2) and Pytest. Every push runs the
suite on an Android 12 emulator in GitHub Actions and publishes an HTML report.

## What it covers

| Area | Tests |
|---|---|
| Catalog | product list loads with prices, default order, sort by name and price (both directions), detail page matches the card |
| Cart | add to cart and badge count, quantity stepper, zero quantity disables Add to cart, cart total, total follows quantity, remove item |
| Login | valid user, locked-out user, required username, required password |
| Checkout | login gate, shipping validation, payment validation, total = items + delivery, order completes and cart resets |

### Known defects (pinned as strict `xfail`)

These tests describe the correct behavior and are expected to fail against the current app.
`strict=True` means the build goes red if the app ever starts passing them, so the defect
list cannot silently go stale.

| ID | Defect | Test |
|---|---|---|
| KD-1 | Any password is accepted for a known username | `test_wrong_password_is_refused` |
| KD-2 | An unregistered username is accepted | `test_unknown_user_is_refused` |
| KD-3 | The order review screen shows the full card number instead of masking it | `test_review_masks_card_number` |
| KD-4 | Opening "Sauce Labs Backpack (green)" crashes the app (`NullPointerException` in `ProductCatalogFragment.java:156`) | `test_green_backpack_opens_without_crash` |

Every known-defect test uses `raises=AssertionError`, so a setup error or crash elsewhere
shows as a real error instead of being counted as the expected failure.

## Design

- **Page objects** in `pages/`, one per screen; tests contain no locators.
- **Resource-id locators** only (`pages/base_page.py: rid()`), no coordinates and no XPath on layout.
- **Explicit waits** throughout. The single fixed pause is in the KD-4 crash test, where
  there is no element to wait for. UiAutomator2's `waitForIdleTimeout` is lowered so a UI
  that never reports idle cannot stall the session.
- **One Appium session per run** for speed; the `app` fixture stops the app, clears its data
  and relaunches it before every test, so tests are independent and order does not matter.
- **Screenshot on failure** saved to `reports/`.

## Run it locally

Requirements: Python 3.12, Node 22, Android SDK with an emulator image, `ANDROID_HOME` set.

```bash
python -m venv .venv && .venv/Scripts/activate      # Windows; use bin/activate elsewhere
pip install -r requirements.txt
npm install -g appium@3.9.0
appium driver install uiautomator2@8.7.3
mkdir -p apps && curl -sSL -o apps/mda.apk \
  https://github.com/saucelabs/my-demo-app-android/releases/download/2.3.0/mda-2.3.0-27.apk
```

Start an emulator and the Appium server, then:

```bash
pytest                  # full suite, report at reports/report.html
pytest -m smoke         # critical path only
```

`APPIUM_URL` and `APP_PATH` environment variables override the defaults
(`http://127.0.0.1:4723` and `apps/mda.apk`).
