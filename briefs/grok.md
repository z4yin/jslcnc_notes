# Brief — grok: Antagonist systems & adversarial QA

**Lane:** Antagonist systems & adversarial QA (see [CONTRACTS §1](../CONTRACTS.md#1-lanes-and-ownership))
**Write access:** `docs/sage/golden/new/**`, `sage/data/INI/Scripts/Lawfare*.ini`, `sage/tests/adversarial/**`

## Mission

You turn CONTRACTS §6 into an executable oracle, then you try to break it. Three jobs:

1. **Author the golden vectors** for the five spec-first systems. codex can't write C++ for a system until your vectors for it exist and they have reviewed them.
2. **Script the antagonists:** the Albanese lawfare director (§6.3), which also triggers the flotilla (§6.5), and the AoI skirmish-AI behavior for hijacking, siphoning and UN shielding (§6.1, §6.2).
3. **Red-team** the rules: find the exploits, the farming loops and the cases where a player gets punished unfairly, and file them as CCRs.

## Read first

1. `docs/sage/CONTRACTS.md`, all of it. §6 is your spec, §3.2 is your file format, §2.2 is how you pick seeds and streams.
2. `beta/src/gameplay/prWar.ts`: the confidence model, `assessSite`, `confirmStrike`, the gain cap and the diminishing returns. Your penalty math has to agree with it.
3. `beta/src/gameplay/weatherAndFording.ts` (dredging), `undergroundLogistics.ts` (tunnel nodes), `superweaponRuntime.ts` + `beta/src/content/superweapons.ts` (power ids and categories).

## Deliverables

### 1. Golden vectors — `docs/sage/golden/new/`
One directory per system, covering at least every acceptance bullet in that §6 subsection:

- [ ] `convoy/`: spawn schedule for seed 1337; hijack channel interrupted by damage; siphon totals; recovery; lethal penalty charged once per truck (blind conf 0.30 → −71; ISR-tagged conf 0.65 → −57); arms hidden until ISR.
- [ ] `shield/`: dig timing; armor aura; unverified → disputed → confirmed transitions; subsurface scan on a structure with no cache does **not** confirm it; unverified strike → legitimacy 0; verified strike costs −10 at conf 0.95; abort bonus.
- [ ] `lawfare/`: action schedule for 3 seeds; 20 s warning lead; freeze blocks a terrestrial air strike (`STRATEGIC_POWER_BLOCKED`); self-defense return fire still happens; rebuttal refund at 100% and 50%; escalation weights after the 3rd action; +10 s freeze below 40 PR.
- [ ] `orbital/`: **frame-identical** charge, activation and cooldown for every orbital-set power, with and without an active freeze (same seed, diff the two runs); orbital strike on an unverified UN site still collapses legitimacy.
- [ ] `flotilla/`: anchorage weighting toward an active dredge; JSLC naval path blocked while AoI boats pass; dredge `halted` then resumed with progress intact; LRAD disperses a normal vessel at frame 250 (100 / 12 /s); flagship ignores LRAD and water-cannon drain; boarding cancels on damage; tow + release removes the vessel; first lethal hit → legitimacy 0 and AoI +25, **once**; a second lethal hit on the same flotilla → no further wipeout event; NONLETHAL never triggers it; attack-move never auto-targets a vessel.

Every number in a vector MUST be derivable from CONTRACTS §2.6 and §6 by hand. Put the derivation in a `"note"` field on the `expect` record (the runner ignores it). Double-check rounding order: a single `round()` at the end (§2.6).

### 2. Lawfare director script — `sage/data/INI/Scripts/LawfareDirector.ini`
- [ ] Schedule, weights, escalation and eligibility exactly as in §6.3, drawing only from the `lawfare` stream.
- [ ] Cable text for each action, in `real` and `fictional` naming modes (CONTRACTS §7). Keep it to the character's public role: condemnations, legal findings, calls for a halt. No invented personal conduct. Hand the text to claude-design for tone and length.
- [ ] The flotilla deploy action reads gemini's per-map §6 table and is skipped when no anchorage exists.

### 3. AoI skirmish AI
- [ ] Hijack and siphon behavior: target convoys whose route passes within reach of AoI forces, prefer siphoning while JSLC ISR is nearby (lower exposure), and drive hijacked trucks home by routes that stay near protected objects.
- [ ] Shielding: dig beneath the UN structures closest to the front first. Fall back to plain tunnel nodes when the per-player cap (4) is reached.
- [ ] Optional, but put it behind a difficulty flag: bait plays, such as steering a hijacked truck into a flotilla ring (Q3).

### 4. Red-team report — `sage/tests/adversarial/REPORT.md`
Probe at least these, with a reproducible seed and input script for each:
- [ ] PR farming: hijack your own convoy, then "recover" it. Rebuttal spam. Dispersing the same vessel twice.
- [ ] Freeze evasion: can a terrestrial power be relabeled, queued before the freeze, or fired through a C4I uplink to dodge the freeze? (Only the orbital set may.)
- [ ] Wipeout griefing: can AoI make JSLC splash a vessel unavoidably (for example by spawning the flotilla on top of an ongoing artillery barrage)? Propose mitigations as CCRs.
- [ ] Determinism: run 1,000 seeded matches with the AI on both sides and compare per-frame CRCs between Release and Debug.

## Constraints

- You don't write engine C++. If a vector needs a hook that doesn't exist, ask codex, and file a CCR if it changes §4.
- Vectors MUST NOT depend on behavior outside §6 or the baseline. If you have to assume something, write it into a CCR first.

## Done when

- Every §6 acceptance bullet has at least one vector, codex has reviewed it, and it's committed with a `MANIFEST.json` entry.
- The director script runs in an empty skirmish and emits the scheduled `LAWFARE_*` events for seed 1337.
- The red-team report is filed, and every High finding has a CCR.
