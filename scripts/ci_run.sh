#!/usr/bin/env bash
# Runs inside android-emulator-runner, which executes each script line in its own shell,
# so the Appium server has to be started and the suite run from one script.
set -euo pipefail

adb shell settings put global hide_error_dialogs 1

appium --log appium.log --log-level info &
for _ in $(seq 1 30); do
  curl -sf http://127.0.0.1:4723/status >/dev/null && break
  sleep 2
done

pytest
