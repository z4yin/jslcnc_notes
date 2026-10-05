# Brief — claude-design: Presentation, HUD & readability

**Lane:** Presentation (see [CONTRACTS §1](../CONTRACTS.md#1-lanes-and-ownership))
**Write access:** `sage/engine/GameClient/**` (UI only, never logic), `sage/data/INI/ControlBar*.ini`, `sage/data/INI/CommandSet*.ini`, `sage/art/ui/**`, `docs/sage/ui/**`

## Mission

Make every rule in CONTRACTS legible in the moment it matters. The new systems are mostly about **restraint under pressure**: don't shoot the UN truck, prove the cache before you strike, clear the flotilla without killing anyone, know which weapons a freeze can't touch. If a player takes a PR collapse and didn't see it coming, that's a UI bug. You also own the event contract (§4) from the consumer side. Every §4 change needs your ack.

## Read first

1. `docs/sage/CONTRACTS.md` §2.4–§2.6, §4, §5, §6, §7.
2. `docs/ui_design_spec.md`, `docs/generals2_scale_and_art_direction.md`, `docs/DESIGN_BRIEF_2026-09-03.md`.
3. Current beta presentation: `beta/src/ui/**`, `beta/src/main.ts` (strategic power bar, toasts, the `laser` targeting mode), `beta/src/explainer/**`.

## Deliverables

### 1. Event-driven HUD skeleton
- [ ] A client-side `JslcHudModel` that is built **only** from the §4 event queue plus the per-frame snapshot. No reads into `GameLogic`. Acceptance: replaying a recorded event log rebuilds the same HUD state.

### 2. PR and legitimacy
- [ ] Two-sided PR meter (JSLC Legitimacy / AoI Popular Support) with a marker at the 40 ROE threshold, a gain-cap indicator ("+25 / min cap reached"), and a 3 s delta ticker with the reason label for each `PR_DELTA`.
- [ ] A wipeout state for `FLOTILLA_LETHAL_INCIDENT`: a full-width alert, the meter drops to 0 with a visible cause, and a cable-feed entry.

### 3. Pre-engagement warnings (the core of this brief)
- [ ] **Protected-target cursor.** Hovering a lethal attack cursor over any `PROTECTED_CIVILIAN` shows a distinct cursor plus the `PR_ASSESSMENT` estimate ("Est. −71 Legitimacy · Confidence 30% · ISR advised"). Force-fire needs a deliberate modifier and shows a confirm ring.
- [ ] **UN structure states.** Overlay badges for `unverified` / `disputed` / `confirmed`, with a confidence pip bar (0.30 → 0.65 → 0.95). A confirmed cache gets a subsurface marker.
- [ ] **Convoy readability.** UN trucks get a light-blue UN tint. ISR-tagged trucks show their cargo (supplies / arms) and their hijack state. A hijacked truck reads as "AoI-controlled · UN driver aboard". The siphon gets a visible flow effect from truck to thief.

### 4. Lawfare and the ROE freeze
- [ ] A **diplomatic cable feed**: a panel or ticker for `LAWFARE_WARNING` (with countdown), `LAWFARE_CONDEMNATION` and `ROE_FREEZE_BEGIN/END`. A portrait slot that uses the `real` or `fictional` asset according to the naming switch (§7). Cable copy comes from grok. You edit it for length (≤ 140 chars) and tone. It stays within the public role.
- [ ] **Freeze state on the command bar.** Terrestrial offensive powers get a "ROE FREEZE · mm:ss" lock overlay. Blocked attempts flash with `STRATEGIC_POWER_BLOCKED`.
- [ ] **Orbital jurisdiction badge.** During a freeze, every orbital-set power stays fully lit with a "JCOM ORBITAL — OUTSIDE UN JURISDICTION" badge. The player must be able to tell at a glance that the laser still works. Still show the PR estimate when the laser hovers a protected target (§6.4: immunity is not consequence-free).
- [ ] A rebuttal prompt: for 30 s after a condemnation, a "Rebut with ISR release" button that shows the refund estimate.

### 5. Flotilla
- [ ] Blockade ring outline on the water, a "BLOCKADE" label, and halted dredge jobs shown as paused (not failed) with their progress bar frozen.
- [ ] A Resolve bar on each vessel. The flagship is marked "Must be boarded".
- [ ] Command cards (`CommandSet*.ini`): `LRAD` and `Water Cannon` toggles, `Board & Tow` on Dvora with the boarding upgrade, and `Release Tow` when it's at a map edge or naval yard. Show the lethal weapon's cursor as blocked-by-default over vessels.
- [ ] Cameos and icons for gemini's new asset list: Harbor Fire Tug, LRAD upgrade, Boarding Team upgrade, UN truck, UN structures, flotilla vessel, flagship. Follow the existing art direction doc. No caricature of real people. Portraits are respectful likenesses or generic silhouettes.

### 6. Readability review
- [ ] `docs/sage/ui/readability-review.md`: for each §6 system, list the moment the player has to decide, what the UI shows at that moment, and whether it's enough. Re-review after each grok red-team round.

## Constraints

- The client never mutates logic state. Player intent goes out only as `GameMessage` commands.
- A new event field or event type is a CCR, and you are the required acker.
- All strings go through the localization table, with both naming modes.

## Done when

- Every §6 system can be played in a skirmish using only on-screen information. A tester who hasn't read the contract can say *why* each PR change happened.
- Every §4 event has a visible representation or is explicitly marked as internal in the readability review.
- Freeze + orbital laser test: during a freeze a tester correctly identifies, on the first try, which powers they can still fire.
