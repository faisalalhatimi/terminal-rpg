#!/bin/bash
set -e

echo "training-01" > /etc/hostname

mkdir -p /root/case
chmod 755 /root/case

mkdir -p /root/training

cat > /root/training/orientation.txt <<'TXT'
HATI SECURITY OPERATIONS
New analyst orientation

Welcome to the desk.

Your shift is 08:00 to 16:00, Monday to Friday, plus one weekend every four weeks.
Your desk is D-14, second row, under the AC that does not work.
Your badge opens the operations floor and nothing else. Do not lose it.

The kitchen is next to the entrance. The coffee machine is a lie. No ice cream too.

Escalation is simple. If you cannot close it in an hour, hand it up. Nobody
here is impressed by an analyst who sat on a live incident for a shift because
they wanted to solve it alone.
TXT

{
  echo "2026-07-11 22:04:11 shift start . zelda . night"
  for i in $(seq 1 23); do
    printf '2026-07-11 %02d:%02d:%02d alert . ids . signature %04d . low\n' \
      $((22 + i / 30)) $(( (i * 7) % 60 )) $(( (i * 13) % 60 )) $((3000 + i))
  done
  echo "2026-07-12 02:14:07 alert . ids . authenticated session . web-03 . HIGH"
  for i in $(seq 24 46); do
    printf '2026-07-12 %02d:%02d:%02d alert . ids . signature %04d . low\n' \
      $(( (i / 12) + 2 )) $(( (i * 11) % 60 )) $(( (i * 3) % 60 )) $((3000 + i))
  done
  echo "2026-07-12 05:50:02 note . zelda . quiet night apart from web-03, handing to the day desk"
  echo "2026-07-12 06:00:00 handover . zelda . day shift . see note above"
  echo "2026-07-12 06:00:01 shift end . zelda . night"
} > /root/training/shift.log

cat > /root/scratch.tmp <<'TXT'
dont delete this
- previous trainee, faisal
TXT

printf 'n7pi-NUFH-DS1\n' > /root/training/.evidence

touch /root/.bash_history

fail() { echo "SEED FAILED: $1" >&2; exit 1; }

grep -q 'D-14' /root/training/orientation.txt || fail "orientation is missing D-14"
grep -qi 'zelda' /root/training/shift.log || fail "shift log is missing zelda"
grep -qi 'handover' /root/training/shift.log || fail "shift log is missing a handover line"

alerts=$(grep -c 'alert' /root/training/shift.log)
[ "$alerts" -eq 47 ] || fail "alert count is $alerts, the objective says 47"

[ -d /root/case ] || fail "case directory missing"
[ "$(stat -c %a /root/case)" = "755" ] || fail "case directory should start at 755"
[ -f /root/scratch.tmp ] || fail "scratch.tmp missing"
[ -f /root/training/.evidence ] || fail "hidden evidence file missing"
grep -q 'n7pi-NUFH-DS1' /root/training/.evidence || fail "tutorial cipher does not match"
