# Claude Design Review: REV-003 (Module 1 - MADL & Subterranean HUD)

**Target:** F-35 MADL Cooperative Sensor Net & Subterranean Vector HUD
**Scope:** `beta/src/gameplay/f35MadlNet.ts`, `beta/src/renderers/sage3d.ts`

## 1. Visual Clarity & 3D Rendering (PASS / ACTION REQUIRED)

### A. Tether Lines & Formation Dome (✅ PASS)
- The tether lines correctly link formation members using a pulsing cyan `0x38bdf8` line material, providing a clear visual indicator of the 4-ship mutual tether.
- The 360° Omnidirectional Sensor Dome is effectively rendered at the formation centroid using a transparent wireframe dome, visually matching the expanded 1.5x cooperative radar range.

### B. Bistatic Emitter Indicators (✅ PASS)
- The Lead Active Pulse Beam is correctly distinguished. The active emitter jet is highlighted with a downward-facing pulsating yellow/amber (`0xfacc15`) cone, clearly separating the active emitter from the silent EMCON Alpha wingmen.

### C. Subterranean Vector Tunnel Rendering (✅ PASS - RESOLVED)
- **Resolution:** `sage3d.ts` (`updateSubterraneanTunnels`) was updated to convert raw links into `SubterraneanTunnel` structures with active transit detection and evaluate them through `madlEngine.evaluateDetection`. Underground emerald cyber-wireframes (`0x10b981`) and access shafts now render **ONLY** when active movement triggers the sensor net or when detected by friendly recon. Dormant tunnels remain strictly invisible.

### D. HUD Tokens / RWR Alerts (✅ PASS - RESOLVED)
- **Resolution:** Implemented floating animated tactical badge overlays (`.sage-madl-alerts`, `.sage-madl-badge`) in `sage3d.ts` and `style.css`. `BATON_PASS` events display "EMITTER SWAP: JET-X ACTIVE", `RWR_ALERT` triggers pulsating warnings ("⚠ RWR ALERT: SAM LOCK ON JET-X"), and newly detected tunnels fire "✦ SUBTERRANEAN VECTOR CORRIDOR DETECTED" alerts.

## 2. Verification Summary
1. `beta/test/f35MadlNet.test.ts`: All 11/11 unit tests passing.
2. Full test suite: All 343/343 tests passing.
3. TypeScript check: 0 errors via `npx tsc --noEmit`.

## Sign-off
Module 1 review, refinements, and verification completed by `claude-design`. Module 1 is approved for commit and push.
