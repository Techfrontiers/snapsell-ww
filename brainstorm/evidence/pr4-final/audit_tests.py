"""Audit-only tests for GPT's 7 product-data cases (NOT part of snapsell-ai).
Run against the AUDITED server.py (fresh branch copy, SHA-locked).
Usage: python3 audit_tests.py   (cwd must contain server.py, or set path below)
"""
import sys, os
sys.path.insert(0, "/tmp/audit")
import server

PASS, FAIL = 0, 0
def check(name, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"PASS | {name} | {detail}")
    else: FAIL += 1; print(f"FAIL | {name} | {detail}")

# Case 2: unclear label / incomplete info -> fail-closed, never invent
desc, needs, diag = server.parse_copy("สินค้าดูไม่ชัด ไม่รู้ว่าคืออะไร", "th")
check("case2-vague-no-marker-fail-closed", desc == server.MIN_DESC["th"] and len(needs) == 1 and diag is not None, f"desc={desc!r} needs={needs}")
desc, needs, diag = server.parse_copy("", "th")
check("case2-empty-output-fail-closed", desc == server.MIN_DESC["th"] and diag == "empty model output", f"diag={diag!r}")
desc, needs, diag = server.parse_copy("NEEDS_CONFIRMATION:\n- ราคา?", "th")
check("case2-marker-empty-desc-fallback", desc == server.MIN_DESC["th"] and needs == ["ราคา?"], f"desc={desc!r} needs={needs}")

# Case 4: malformed response -> fail-closed (marker variants)
desc, needs, diag = server.parse_copy("garbage {{{ no structure at all", "th")
check("case4-garbage-fail-closed", desc == server.MIN_DESC["th"] and diag == "garbage {{{ no structure at all", "raw kept only as diagnostic")
desc, needs, diag = server.parse_copy("ชื่อสินค้า\nรายละเอียดดีมาก\nNEEDS_CONFIRMATION:\n- ยืนยันราคา", "th")
check("case4-wellformed-parses", desc == "ชื่อสินค้า\nรายละเอียดดีมาก" and needs == ["ยืนยันราคา"], f"desc={desc!r}")

# Case 5: invented claims stripped (price / place / nutrition / availability)
d, removed = server.enforce_claims("อร่อยมาก ซื้อได้ที่ 7-Eleven ราคา 999 บาท", "", "th")
check("case5-invented-place-price-stripped", d == server.MIN_DESC["th"] and len(removed) >= 1, f"desc={d!r} removed={removed}")
d, removed = server.enforce_claims("มีวิตามินซีสูง ช่วยต้านอนุมูลอิสระ", "", "th")
check("case5-invented-nutrition-stripped", d == server.MIN_DESC["th"] and len(removed) >= 1, f"desc={d!r} removed={removed}")
d, removed = server.enforce_claims("พร้อมส่งวันนี้ มีของในสต็อก", "", "th")
check("case5-invented-availability-stripped", d == server.MIN_DESC["th"] and len(removed) >= 1, f"desc={d!r} removed={removed}")
# ...but a matching seller value exempts (value-based, not keyword-only)
d, removed = server.enforce_claims("ราคา 35 บาท", "ราคา 35 บาท", "th")
check("case5-matching-seller-value-kept", d == "ราคา 35 บาท" and not removed, f"desc={d!r}")

# Case 6: seller facts CONFLICT with image/copy -> safe direction = strip, never publish
d, removed = server.enforce_claims("ราคา 50 บาท", "ราคา 100 บาท", "th")
check("case6-conflict-price-stripped", d == server.MIN_DESC["th"] and len(removed) >= 1, f"desc={d!r} removed={removed}")
d, removed = server.enforce_claims("ขนาด 500 มล.", "ขนาด 600 มล.", "th")
check("case6-conflict-size-stripped", d == "" and len(removed) >= 1, f"desc={d!r} removed={removed}")
d, removed = server.enforce_claims("ขนาด 500 มล.", "ขนาด 500 มล.", "th")
check("case6-matching-size-kept", d == "ขนาด 500 มล." and not removed, f"desc={d!r}")

print(f"\nAUDIT TESTS: {PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
