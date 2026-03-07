#!/bin/bash
# Regression test: Verify security warning exists after obsidian eval example
# This test ensures the eval command has a prominent security warning

FILE="skills/obsidian-cli/SKILL.md"
PASS=0
FAIL=0

# Test 1: Security warning callout exists after eval example
if grep -A5 'obsidian eval' "$FILE" | grep -qi 'security warning'; then
  echo "PASS: Security warning callout found after eval example"
  ((PASS++))
else
  echo "FAIL: No security warning after eval example"
  ((FAIL++))
fi

# Test 2: Warning mentions arbitrary JS execution
if grep -i 'arbitrary javascript' "$FILE" | grep -qi 'eval\|warning\|access'; then
  echo "PASS: Warning mentions arbitrary JavaScript execution"
  ((PASS++))
else
  echo "FAIL: Warning does not mention arbitrary JavaScript execution"
  ((FAIL++))
fi

# Test 3: Warning mentions filesystem access risk
if grep -i 'filesystem' "$FILE" | grep -qi 'eval\|warning\|access'; then
  echo "PASS: Warning mentions filesystem access risk"
  ((PASS++))
else
  echo "FAIL: Warning does not mention filesystem access"
  ((FAIL++))
fi

# Test 4: Warning mentions untrusted input
if grep -qi 'untrusted' "$FILE"; then
  echo "PASS: Warning mentions untrusted input"
  ((PASS++))
else
  echo "FAIL: Warning does not mention untrusted input"
  ((FAIL++))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
