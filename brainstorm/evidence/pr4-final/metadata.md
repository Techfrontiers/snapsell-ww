# Screenshot metadata (Section 5)

- Audited commit (snapsell-ai, branch webapp-tailwind): cbc4c4afa3a43851a93ac1a12177f81d95deeb3a
- PR: https://github.com/Techfrontiers/snapsell-ai/pull/4 (draft)
- Date: 2026-10-29 Bangkok (~08:53)
- Tool: Playwright chromium_headless_shell-1248 (headless-shell binary),
  flags: --no-sandbox --disable-gpu --hide-scrollbars
  --window-size=<W>,<H> --virtual-time-budget=15000 --screenshot=<file> file://...
- Method: staged files were fetched FRESH from the branch in this audit and
  verified byte-identical to the branch files (cmp) before screenshotting.
  The EN shot uses a screenshot-only variant with the default language forced
  to 'en' (one line changed); the committed file is unchanged and language
  switching is proven by the lang-switch harness (40 elements, 0 mismatches).
- Files:
  - desktop-1440.png: viewport 1440x1000, TH default
  - mobile-390.png: viewport 390x844, TH default
  - desktop-en-1440.png: viewport 1440x1000, EN default (variant)
  - full-page-1440.png: viewport 1440x4600, TH default (full page)
- Checks from these shots (eyeballed): no horizontal overflow at 1440 or 390;
  all images present (10/10 staged, all rendered in full-page shot);
  TH/EN translation complete in EN shot; studio panel + gallery render;
  footer present. NOT covered by screenshots: anchor click-scroll behavior
  (targets verified statically), reduced-motion behavior (media query present
  in code, behavior not exercised), Swal modal/toast appearance (logic proven
  by harness; no modal was open during screenshots).
