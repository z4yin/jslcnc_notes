# Brief — codex: Sim core & golden harness

**Lane:** Sim core (see [CONTRACTS §1](../CONTRACTS.md#1-lanes-and-ownership))
**Write access:** `sage/engine/GameLogic/**`, `sage/tests/golden/**` (harness only), `beta/scripts/emit-golden.mjs`
**Oracle:** tag `spec-baseline-ts`, plus CONTRACTS §6 for the new systems

## Mission

Port the frozen TypeScript gameplay modules to C++ inside the SAGE module model so that they reproduce the TS bit-for-bit (within §2.3 tolerance). Then implement the five spec-first systems in §6 against grok's hand-authored vectors. You own determinism. If replay CRCs drift, that's yours.

## Read first

1. `docs/sage/CONTRACTS.md`, all of it. §2 (invariants) and §3 (golden vectors) are your daily reference.
2. `beta/src/gameplay/seededRng.ts`, `prWar.ts`, `spatialGrid.ts` (the P0 modules).
3. `beta/package.json` → `npm test` runs `node --import tsx --test test/**/*.test.ts tests/**/*.test.ts`. That is the 311-test oracle.
4. The `@core/*` alias in `beta/tsconfig.json` resolves into the upstream mainframe repo (`jcom_v0bb_mainframe_cnc2d/game/src/core`). The `Sim` and `Entity` types come from there. Golden emission needs a minimal stub `Sim`, not the upstream one.

## Deliverables, in order

### Phase A — Harness (blocks everyone)
- [ ] `beta/scripts/emit-golden.mjs`: loads each TS module under `tsx`, drives it with `dt = 1/30`, and writes `docs/sage/golden/ts/<module>/<case>.jsonl` in the §3.2 schema. It also writes `MANIFEST.json` with sha256 per file, the oracle tag, and the `testFile#testName → case` mapping. Running it twice MUST produce byte-identical output.
- [ ] `sage/tests/golden/GoldenRunner.cpp`: reads a jsonl file, applies `init`/`input`/`step`, checks each `expect` with partial-state matching and exact ordered events, and reports the first divergence with frame, path, expected and actual.
- [ ] CI target `golden` (Release + Debug, Windows x64). It also runs a double replay of each case and compares per-frame CRCs.

### Phase B — P0 ports
- [ ] `JslcRng`: Mulberry32 + FNV-1a, with named streams (§2.2). Include a test that hashes the 10 stream names and draws 1,000 values per stream against TS output.
- [ ] `JslcSpatialHash` over `PartitionManager`.
- [ ] `PrWar` singleton with `applyDelta()` as the **only** PR mutation path (§2.4), `assessEngagement()` (§2.6), the embedded PRNG draw order from `prWar.ts`, and the gain cap and diminishing returns. Add the new `PrReason` values now, even before their systems exist.

### Phase C — P1 ports
Work through the §3.4 table by priority. For each module: get its vectors green, then open a PR. Don't batch modules into a single PR.

### Phase D — §6 systems (after grok's vectors for that system land)
- [ ] `Lethality` / `Jurisdiction` fields on `WeaponTemplate` and `SpecialPowerTemplate`, with the INI parse and the load-time orbital check (§2.5).
- [ ] `JslcStrategicPowerGate`: checks jurisdiction **before** the freeze (§6.4). Write this one first, since §6.3 and §6.4 both depend on it.
- [ ] `UnConvoySubsystem` + `HijackerUpdate` reuse + `StealUpdate` (siphon) (§6.1).
- [ ] `UnShieldSubsystem` on top of `JslcTunnelNetwork` (§6.2).
- [ ] `LawfareDirector` logic hooks. grok writes the director's script and weights. You provide the actions it calls (§6.3).
- [ ] `FlotillaSubsystem`: the `FLOTILLA_BLOCK` locomotor surface flag, ring anchoring, the `Resolve` body, displacement, boarding and towing (a `ContainModule`-style tow link), the dredge `halted` state, and the one-shot wipeout (§6.5).
- [ ] Targeting rule: attack-move and guard never auto-acquire `PROTECTED_CIVILIAN` with lethal weapons. Only force-fire can.

## Constraints

- Do not edit `beta/src/gameplay/**` or `beta/test/**`. If the oracle looks wrong, write it up as a CCR (§8). Don't "fix" it in C++.
- No `float` in ported logic until the suite is green (§2.3). No `dt` multiplication (§2.1).
- No iteration over `std::unordered_*` inside the logic step. Use ordered containers or sorted ids.
- Every event in §4 has a C++ struct with exactly the listed fields. If you need a new field, that's a CCR acked by claude-design.

## Done when

- 100% of `golden/ts/**` cases pass in Release and Debug, and double-replay CRCs match.
- 100% of `golden/new/**` cases pass for each §6 system you've shipped.
- `MANIFEST.json` `ts/**` hashes are unchanged from the tagged emission.

## Handoffs

- **To gemini:** the INI field list for each module (tunable names, types, units), so the tables can come out of TS constants.
- **To grok:** a stub `Sim` + event recorder they can use to dry-run hand-authored vectors.
- **To claude-design:** a stable event queue + snapshot API (§4) before any HUD work starts.
