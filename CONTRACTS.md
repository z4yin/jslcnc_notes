# SAGE Migration Contracts

Status: **v1.0 — normative.** Baseline: tag `spec-baseline-ts` (commit `90a40fe`, 311 passing tests).
Agent briefs: [`briefs/codex.md`](briefs/codex.md) · [`briefs/gemini.md`](briefs/gemini.md) · [`briefs/grok.md`](briefs/grok.md) · [`briefs/claude-design.md`](briefs/claude-design.md)

This file is the single source of truth for the port of the JSLCnC beta (TypeScript, `beta/`) to a C++ SAGE-architecture engine (Generals / Zero Hour module model: `Object` + `Body` + `Update` + `Weapon` + INI templates). If a brief and this file disagree, this file wins. Words in capitals (MUST, MUST NOT, SHOULD, MAY) are used as in RFC 2119.

---

## 0. Ground rules

1. **The frozen TS is the oracle.** `beta/src/gameplay/*.ts` at `spec-baseline-ts` defines correct behavior for every system that already exists. A C++ port is correct when it reproduces that module's golden vectors (§3). Nobody edits `beta/src/gameplay/` or `beta/test/` on the migration branch. Fixes to the oracle go in a separate commit on `v0c-alpha`, add a new tag (`spec-baseline-ts.N`), and regenerate the vectors.
2. **New systems are spec-first.** The five systems in §6 do not exist in the TS baseline. This document is their oracle. Their golden vectors are written by hand from §6 (owner: grok) and reviewed by codex before any C++ is written.
3. **No regressions across the boundary.** New systems MUST NOT change the output of any existing `spec-baseline-ts` vector. They only add new event types and new state.
4. **One lane per agent** (§1). You may read anything. You may write only in your own lane's paths. Cross-lane changes go through a contract change request (§8).
5. **Determinism above everything.** Logic runs at a fixed step. All randomness comes from the seeded RNG (§2.2). No wall clock, no `rand()`, no iteration over unordered containers inside the logic step.

---

## 1. Lanes and ownership

| Lane | Agent | Owns (write access) | Delivers |
|---|---|---|---|
| **Sim core** | codex | `sage/engine/GameLogic/**`, `sage/tests/golden/**` (harness, not vectors), `beta/scripts/emit-golden.mjs` | C++ ports of the existing TS gameplay modules, the golden-vector harness, and the C++ for the §6 systems |
| **Data & world** | gemini | `sage/data/INI/**`, `sage/data/maps/**`, `docs/sage/data-map.md` | INI templates for every roster asset, the CSV→INI pipeline, map waypoints/areas for convoys and flotilla anchorages, and the tunables tables lifted out of TS into INI |
| **Antagonist systems & adversarial QA** | grok | `docs/sage/golden/new/**`, `sage/data/INI/Scripts/Lawfare*.ini`, `sage/tests/adversarial/**` | Hand-authored golden vectors for §6, the Albanese lawfare director script, skirmish-AI behavior for AoI hijack/shielding, and exploit hunting |
| **Presentation** | claude-design | `sage/engine/GameClient/**` (UI only), `sage/data/INI/ControlBar*.ini`, `sage/data/INI/CommandSet*.ini`, `sage/art/ui/**`, `docs/sage/ui/**` | HUD, PR meters, the EVA/diplomatic cable feed, ROE-freeze and jurisdiction indicators, command cards for non-lethal options, and the readability review of every new system |

Shared, read-only for everyone: `docs/sage/CONTRACTS.md` (this file), `beta/**`, `docs/*.csv`.

---

## 2. Engine-level invariants

### 2.1 Time

- One logic frame is **1/30 s** (SAGE `LOGICFRAMES_PER_SECOND = 30`).
- TS tunables are in seconds. Convert them **once**, at INI load, with `frames = round(seconds * 30)`. Logic code MUST NOT multiply by a floating `dt`.
- Golden vectors from TS drive the module with `dt = 1/30` so that both sides step the same way.

### 2.2 Randomness

- PRNG: **Mulberry32**, bit-exact with `beta/src/gameplay/seededRng.ts` (`MULBERRY_INCREMENT = 0x6d2b79f5`).
- String seeds: **FNV-1a 32-bit** (`0x811c9dc5`, prime `0x01000193`), applied to UTF-16 code units the way `hashSeed` does.
- Each subsystem owns a **named stream**: `seed = hashSeed(matchSeed + ":" + streamName)`. Stream names are fixed: `pr`, `logistics`, `weather`, `capture`, `patron`, `gunship`, `convoy`, `lawfare`, `flotilla`, `shield`. One subsystem MUST NOT draw from another's stream.
- `prWar.ts` embeds its own Mulberry32. The port MUST reproduce it exactly, including the draw order.

### 2.3 Numbers

- Ported TS modules use `double` inside the logic. Do not switch to fixed point until the golden suite is green, and only then with a contract change.
- Golden comparison: integers and enums match exactly. Doubles match within `|a-b| <= 1e-9 * max(1, |a|, |b|)`.
- Display rounding (`Math.round`, `toFixed`) is part of the contract wherever the TS stores the rounded value (for example `prPenalty = Math.round(...)` in `prWar.ts`). Round in the same place.

### 2.4 The PR sink

Every legitimacy or popular-support change goes through **one function**:

```cpp
// Mirrors applyPrDelta(teamOrFaction, delta, reason, sim) in prWar.ts
Real PrWar::applyDelta(PrFaction who, Real delta, PrReason reason, const PrSource& src);
```

- `PrFaction` is `JSLC` (Coalition Legitimacy) or `AOI` (Popular Support). Both meters are clamped to `[0, 100]`.
- Gains are subject to `PR_GAIN_CAP_PER_MINUTE = 25` (rolling 60 s window) and to diminishing returns, exactly as in TS. **Penalties are never capped.**
- `PrReason` is an enum. The §6 systems add these values: `UN_CONVOY_LETHAL`, `UN_CONVOY_RECOVERED`, `UN_CONVOY_ISR_EXPOSE`, `UN_SITE_STRIKE_UNVERIFIED`, `UN_SITE_STRIKE_VERIFIED`, `UN_SITE_CACHE_EXPOSED`, `LAWFARE_CONDEMNATION`, `LAWFARE_CONDEMNATION_REBUTTED`, `FLOTILLA_LETHAL_WIPEOUT`, `FLOTILLA_TOWED`, `FLOTILLA_DISPERSED`.
- Every call emits a `PR_DELTA` event (§4). The UI reads PR only from events and snapshots. It never reads it directly.

### 2.5 Lethality and jurisdiction

These two tags are new and cut across every system. Every `WeaponTemplate` and every strategic power MUST declare both:

```ini
Weapon LRAD_AcousticBeam
  Lethality      = NONLETHAL   ; LETHAL | NONLETHAL
  Jurisdiction   = TERRESTRIAL ; TERRESTRIAL | ORBITAL
  ...
End
```

- **Lethality** decides whether damage to a protected object (UN asset, civilian vessel, human shield) counts as a lethal engagement. `NONLETHAL` weapons never reduce a protected object's health below 1. They act through the object's `Resolve` meter or through displacement instead (§6.5).
- **Jurisdiction** decides whether terrestrial legal authority can gate the weapon. `ORBITAL` is reserved for weapons fired from the JCOM orbital platform (§6.4). Data defaults: `Lethality = LETHAL`, `Jurisdiction = TERRESTRIAL`. A load-time check fails the build if any orbital power listed in §6.4 lacks `Jurisdiction = ORBITAL`.

### 2.6 Protected objects

An object is **protected** if it has the KindOf `PROTECTED_CIVILIAN` (UN trucks, UN structures, flotilla vessels, existing human-shield sites). Engaging a protected object always goes through `PrWar::assessEngagement()`. That function generalizes `assessSite`/`confirmStrike` in `prWar.ts` and uses the same recon-confidence model:

- Initial confidence `0.30`, `+0.35` per ISR pass, capped at `0.95` (never 1.0).
- Base penalty formula, unchanged: `round((STRIKE_BASE_PR_PENALTY + STRIKE_CONFIDENCE_SCALING) * (2.0 - conf))`.
- §6 systems MAY multiply that base by a per-class `ProtectedClassMultiplier`. They MUST NOT replace the formula. Round **once**, at the end: `round(28 * (2.0 - conf) * mult)`. Do not round the base first and then multiply. All worked numbers in §6 use this order.

---

## 3. Golden vectors

### 3.1 Layout

```
docs/sage/golden/
  ts/<module>/<case>.jsonl     # emitted from the frozen TS (owner: codex, via emit-golden.mjs)
  new/<system>/<case>.jsonl    # hand-authored from §6 (owner: grok)
  MANIFEST.json                # case list + sha256 of each file + oracle tag
```

### 3.2 Record schema (one JSON object per line)

```jsonc
{ "v": 1, "kind": "init",   "module": "prWar", "seed": 1337, "tunables": { /* overrides or {} */ }, "state": { /* initial */ } }
{ "v": 1, "kind": "input",  "frame": 0,  "op": "confirmStrike", "args": { "siteId": "s1" } }
{ "v": 1, "kind": "step",   "frame": 0,  "frames": 30 }
{ "v": 1, "kind": "expect", "frame": 30, "state": { "jslcLegitimacy": 72 }, "events": [ { "type": "PR_DELTA", "who": "JSLC", "delta": -28, "reason": "UN_SITE_STRIKE_UNVERIFIED" } ] }
```

- `expect.state` is a **partial** match: only the listed keys are compared, using dotted paths for nested values.
- `expect.events` is the **exact, ordered** list of events emitted since the previous `expect`.

### 3.3 Coverage gate

- Every `node --test` case in `beta/test/**` and `beta/tests/**` that exercises a gameplay module MUST map to at least one golden case. `MANIFEST.json` records the mapping (`testFile#testName → case`).
- **Done for a module** = 100% of its golden cases pass in `sage/tests/golden` on Windows x64 Release and Debug, and replaying the same seed twice gives the same CRC per frame.

### 3.4 Module port table

| TS module (`beta/src/gameplay/`) | C++ target (SAGE module type) | Priority |
|---|---|---|
| `seededRng.ts` | `GameLogic/Random/JslcRng` | P0 |
| `spatialGrid.ts` | `GameLogic/Partition/JslcSpatialHash` (wraps PartitionManager) | P0 |
| `prWar.ts` | `GameLogic/Jslc/PrWar` (singleton, `SubsystemInterface`) | P0 |
| `fogOfWar.ts` | adapter onto `PartitionManager` shroud plus `JslcFogRules` | P1 |
| `pathfinding.ts` | `AIPathfind` locomotor surface rules (`UnitLocomotion` → `LocomotorSurfaceType`) | P1 |
| `operationalLogistics.ts` | `JslcLogisticsUpdate` (UpdateModule) | P1 |
| `supplyMoraleSystem.ts` | `JslcSupplyMoraleUpdate` | P1 |
| `weatherAndFording.ts` | `JslcWeatherSubsystem` + `DredgeUpdate` + `TacticalBridgeBody` | P1 |
| `weatherForecast.ts` | `JslcForecastSubsystem` (the Open-Meteo fetch stays in the client, never in the logic) | P2 |
| `superweaponRuntime.ts` | `SpecialPowerModule` subclasses + `JslcStrategicPowerGate` | P1 |
| `airDefenseLayers.ts` | `JslcAirDefenseUpdate` | P2 |
| `altitudeCombat.ts` | `WeaponTemplate` altitude modifiers | P2 |
| `captureOperations.ts` | `JslcCaptureUpdate` | P2 |
| `undergroundLogistics.ts` | `TunnelContain` extension `JslcTunnelNetwork` | P1 (§6.2 depends on it) |
| `patronTrade.ts` | `JslcPatronSubsystem` | P2 |
| `gunshipOverwatch.ts` | `JslcGunshipUpdate` | P2 |
| `rosterBehaviors.ts` | per-asset modules (split by asset) | P2 |
| `factionSpecialSystems.ts` | per-asset modules | P2 |
| `auroraElevator.ts` | `JslcElevatorUpdate` | P3 |
| `campaignDirector.ts` / `towerDefenseDirector.ts` | `ScriptEngine` actions + `JslcDirector` | P3 |
| `mapLoader.ts` / `battlefieldMap.ts` | map converter (gemini) + `TerrainLogic` queries | P1 |

---

## 4. Event contract (logic → client)

Logic publishes typed events into a per-frame queue. The client consumes them, and nothing flows back except player commands (`GameMessage`). Every event carries `frame`, `type` and `seq` (monotonic per frame).

| Event | Payload | Emitted by |
|---|---|---|
| `PR_DELTA` | `who, delta, reason, newValue, capped:boolean` | PrWar |
| `PR_ASSESSMENT` | `targetId, conf, estPrCost, recommendation: confirm\|abort\|gather_recon` | PrWar |
| `CONVOY_SPAWNED` / `CONVOY_ARRIVED` | `convoyId, routeId, cargo` | UnConvoy |
| `CONVOY_HIJACKED` | `convoyId, truckId, byObjectId` | UnConvoy |
| `CONVOY_SIPHON_TICK` | `truckId, supplies, arms` | UnConvoy |
| `CONVOY_RECOVERED` / `CONVOY_DESTROYED` | `truckId, by, lethality` | UnConvoy |
| `SHIELD_CACHE_BUILT` | `structureId, cacheId` (AoI-visible only) | UnShield |
| `SHIELD_CACHE_EXPOSED` | `structureId, cacheId, method` | UnShield |
| `LAWFARE_WARNING` | `action, etaFrames` | Lawfare |
| `LAWFARE_CONDEMNATION` | `jslcDelta, aoiDelta, cableText` | Lawfare |
| `ROE_FREEZE_BEGIN` / `ROE_FREEZE_END` | `freezeId, durationFrames, scope` | Lawfare |
| `STRATEGIC_POWER_BLOCKED` | `powerId, reason: ROE_FREEZE` | StrategicPowerGate |
| `FLOTILLA_DEPLOYED` | `flotillaId, anchorageId, vesselIds[]` | Flotilla |
| `FLOTILLA_BLOCKADE_ACTIVE` / `_LIFTED` | `flotillaId, cells[], haltedDredgeJobs[]` | Flotilla |
| `FLOTILLA_VESSEL_BOARDED` / `_TOWED` / `_DISPERSED` | `vesselId, by` | Flotilla |
| `FLOTILLA_LETHAL_INCIDENT` | `vesselId, attackerId, weapon` | Flotilla |
| `DREDGE_HALTED` / `DREDGE_RESUMED` | `sectorId, jobId, cause` | Dredge |

The UI MUST be able to render every system in §6 from events plus the per-frame snapshot alone. That is claude-design's acceptance test.

---

## 5. Existing behavior that §6 touches (do not change)

- `ROE_RESTRICTION_THRESHOLD = 40`. When legitimacy is below it, `roeRestricted = true` and the **orbital strike cooldown multiplier** scales from 1.0 to 2.5. That is a *public-opinion* effect, and it stays as baselined. The new **ROE freeze** (§6.3) is a separate *legal* effect. §6.4 makes orbital assets immune to the freeze, not to the baselined cooldown multiplier. See open question Q1.
- Human-shield dispersal (`SHIELD_DISPERSE_PR_GAIN_BASE`, `SHIELD_DISPERSE_PR_CAP_PER_MINUTE`) keeps its numbers. UN shielding (§6.2) is a new site class on the same model.
- Dredging (`DredgingJob`, `DREDGE_MAX_CURRENT = 5.0 ft/s`) keeps its numbers. The flotilla adds a `halted` state that **pauses** a job and keeps its progress (§6.5).

---

## 6. New systems (spec-first)

All tunables below are defaults. They live in INI (`sage/data/INI/JslcTunables.ini`, owner gemini) and get mirrored into golden `init.tunables` for each case.

### 6.1 UN aid convoys and hijacking

**Fiction.** Neutral UN aid trucks cross the map on fixed humanitarian corridors. AoI can hijack them to siphon supplies and smuggled arms. JSLC has to deal with this without becoming the side that shot up a UN convoy.

**Objects.**
- `UN_AidTruck`: team `Neutral_UN`, KindOf `VEHICLE PROTECTED_CIVILIAN UN_ASSET CAN_BE_HIJACKED`, HP 400, speed matching the TS truck class. Carries `Cargo { supplies, arms }`.
- `UN_AidDepot`: corridor endpoints placed by the map (waypoint pair `UNCorridor_<n>_Start` / `_End`, owner gemini).

**Spawning.** Every `CONVOY_INTERVAL_SEC = 150` (±`CONVOY_JITTER_SEC = 30`, from the `convoy` stream), one convoy of `CONVOY_SIZE = 3` trucks spawns on a corridor chosen uniformly from the stream. Cargo per truck: `supplies = 300`, and `arms = 0` or `120` with `ARMS_SMUGGLE_CHANCE = 0.35`, rolled per truck. **Arms cargo is hidden.** JSLC sees it only once the truck is ISR-tagged.

**AoI actions.**
1. **Hijack** (Generals `HijackerUpdate` semantics). An AoI unit with the `Hijacker` ability boards an adjacent truck over a `HIJACK_CHANNEL_SEC = 3` channel. The truck changes team to AoI but keeps KindOf `PROTECTED_CIVILIAN`, because the UN driver is still aboard as a hostage. AoI can then drive it anywhere. Delivering it to an AoI supply depot transfers the full cargo.
2. **Steal** (siphon, no takeover). An AoI unit with `Steal` parked within 40 world units of a moving or stopped truck siphons `SIPHON_RATE_PER_SEC = 10` supplies and, when arms are present, `4` arms per second into the AoI stockpile. Each tick emits `CONVOY_SIPHON_TICK`. The truck stays neutral and keeps moving.
3. Siphoned or delivered **arms** grant AoI a temporary `+10%` recruit-rate multiplier per 120 arms, stacking to `+30%` and decaying over 180 s. Siphoned **supplies** go into the AoI resource pool 1:1.

**JSLC options.**

| Option | Requirement | Effect | PR |
|---|---|---|---|
| ISR tag | Hermes 900 or any ISR unit keeps the truck in sight for `ISR_TAG_SEC = 4` | Reveals cargo and hijack state. Raises that truck's engagement confidence by +0.35 per pass (§2.6) | Exposing a hijacked truck that carries arms: `UN_CONVOY_ISR_EXPOSE` +6 to JSLC, −8 to AoI |
| Non-lethal disable | Any `NONLETHAL` weapon (LRAD, spike strip, EMP) | Truck immobilized for 20 s. A hijacker aboard is ejected after the full 20 s | None |
| Recovery | JSLC infantry boards an immobilized hijacked truck (3 s) | Truck returns to `Neutral_UN` and resumes its corridor. Arms cargo is confiscated | `UN_CONVOY_RECOVERED` +8 (gain-capped) |
| Lethal fire | Any `LETHAL` weapon that damages a truck | Normal damage | `UN_CONVOY_LETHAL` = base formula × `UN_CONVOY_MULT = 1.5`, charged once per truck, on first lethal damage, at the truck's confidence at that moment |

So a blind lethal shot at a truck costs about `round(28 × 1.7 × 1.5) = 71`. An ISR-tagged hijacked truck (conf 0.65) still costs `round(28 × 1.35 × 1.5) = 57`. Lethal fire is never "free". Non-lethal play is the intended answer.

**Acceptance (golden `new/convoy/`):** spawn timing for a fixed seed; hijack channel interrupted by damage; siphon totals over 10 s; recovery restores the team and corridor; lethal penalty charged exactly once per truck; arms visibility before and after the ISR tag.

### 6.2 UN building shielding (tunnels and caches under UN structures)

**Fiction.** AoI digs tunnel nodes and weapons caches under UN schools, clinics and warehouses. Striking such a structure without verified proof collapses JSLC's PR. Striking it *with* verified proof is survivable.

**Objects.** `UN_Structure_*` (school, clinic, warehouse, HQ): team `Neutral_UN`, KindOf `STRUCTURE PROTECTED_CIVILIAN UN_ASSET`. Map-placed by gemini.

**AoI action: Dig Beneath.** An AoI worker next to a UN structure spends `DIG_BENEATH_COST = 400` and `DIG_BENEATH_SEC = 40` to create a hidden **cache** linked to the structure. A cache MAY also register as an `undergroundLogistics` node (tunnel portal), which reuses `JslcTunnelNetwork`. While a cache exists:
- AoI units garrisoned in the network can pop out at that structure.
- The structure gives AoI `+15%` armor to units within 60 world units of it (they hug the shield).
- Max `MAX_CACHES_PER_STRUCTURE = 1`. Max `MAX_SHIELDED_STRUCTURES = 4` per AoI player.

**Verification states** (per structure, mirroring `VerificationState` in `prWar.ts`): `unverified → disputed → confirmed`.
- ISR passes raise confidence (+0.35 per pass, cap 0.95) and move the state to `disputed` at conf ≥ 0.40.
- **Proof** moves it to `confirmed`. Proof is either an **Orbital Subsurface Scan** (`jslc-orbital-subsurface-scan`) covering the structure, or a ground team (combat engineers) entering an exposed tunnel portal. Proof emits `SHIELD_CACHE_EXPOSED` and `UN_SITE_CACHE_EXPOSED` (+10 JSLC, −12 AoI, gain-capped).

**Striking a UN structure.**

| State at strike | PR to JSLC |
|---|---|
| `unverified` or `disputed`, cache present or not | `UN_SITE_STRIKE_UNVERIFIED` = base formula × `UN_SITE_MULT = 2.5`. At conf 0.30 that is `round(28 × 1.7 × 2.5) = 119`, which clamps to 0. **Massive collapse.** |
| `confirmed` (cache proven) | `UN_SITE_STRIKE_VERIFIED` = base formula × `0.35`. At conf 0.95 that is `round(28 × 1.05 × 0.35) = 10` |
| No cache, but JSLC believed `confirmed` | Cannot happen. `confirmed` requires proof of an actual cache |

Abort at the assessment prompt pays `ABORT_RESTRAINT_PR_BONUS` exactly as baselined.

The strike penalty is about **what was hit and what was proven**. It does not depend on jurisdiction, so an orbital weapon striking an unverified UN structure still takes the collapse. See §6.4.

**Acceptance (golden `new/shield/`):** cache build timing; armor aura; state transitions per ISR pass; subsurface scan confirms only structures that really have a cache; unverified strike clamps legitimacy to 0; verified strike costs ≤ 10; abort bonus.

### 6.3 Francesca Albanese — diplomatic lawfare director

**Fiction.** Francesca Albanese, UN Special Rapporteur, is the off-map diplomatic antagonist. She is never a unit and never on the map, and there is no mechanic that targets her. She shows up through EVA cables, a portrait, and periodic lawfare actions that distract JSLC and constrain conventional force.

**Cadence.** A director on the `lawfare` stream. First action at `LAWFARE_FIRST_SEC = 360`, then every `LAWFARE_INTERVAL_SEC = 300` ± `LAWFARE_JITTER_SEC = 60`. Each action is announced `LAWFARE_WARNING_SEC = 20` ahead with `LAWFARE_WARNING`. Action weights:

| Action | Weight | Effect |
|---|---|---|
| **UN Condemnation** | 0.45 | `LAWFARE_CONDEMNATION`: −6 JSLC, +4 AoI. Doubled if JSLC caused a lethal protected-object incident in the last 120 s. JSLC can **rebut** within 30 s by spending a `Release ISR` info-op that covers the cited incident: refunds 100% when the incident was AoI-staged and 50% otherwise (`LAWFARE_CONDEMNATION_REBUTTED`) |
| **Conventional ROE Freeze** | 0.35 | `ROE_FREEZE_BEGIN` for `ROE_FREEZE_SEC = 45` (see scope below) |
| **Deploy Eco-Flotilla** | 0.20 | Spawns the flotilla (§6.5). Only eligible if the map defines at least one `FlotillaAnchorage_*` waypoint and no flotilla is active. Otherwise its weight goes to the other two actions |

**Escalation.** Each action after the third raises the freeze weight by +0.05, capped at 0.55. Legitimacy below `ROE_RESTRICTION_THRESHOLD` (40) adds +10 s to freeze duration.

**ROE freeze scope.** While a freeze is active, the `JslcStrategicPowerGate` blocks:
- Activation of every JSLC strategic power with `Jurisdiction = TERRESTRIAL` and an offensive category (air strike, artillery, missile, bunker-buster). Each attempt emits `STRATEGIC_POWER_BLOCKED`.
- Attack orders from JSLC aircraft and artillery (KindOf `AIRCRAFT` or `ARTILLERY`) on targets that are not currently attacking JSLC. Self-defense and return fire are always allowed. Ground direct-fire units are not frozen.
- **Not blocked:** non-lethal weapons, ISR, info-ops, movement, construction, and everything with `Jurisdiction = ORBITAL` (§6.4).

**Counterplay.** `Publish Tribunal Dossier` during a freeze shortens the remaining freeze by 50%, once per freeze.

**Acceptance (golden `new/lawfare/`):** action schedule for a fixed seed; warning lead time; freeze blocks terrestrial powers and leaves orbital ones untouched; self-defense still fires; rebuttal refund math; escalation weights.

### 6.4 Orbital laser immunity (JCOM orbital jurisdiction)

**Fiction.** The JCOM space station operates outside UN terrestrial authority. Neither Albanese nor the UN has any jurisdiction over orbital assets.

**Rule.** Every weapon and strategic power with `Jurisdiction = ORBITAL` is **100% immune** to ROE freezes and to every other lawfare gating effect. That covers activation, targeting, cooldown progression and charge. No lawfare action can delay, block, cancel or add cooldown to an orbital asset. The `JslcStrategicPowerGate` MUST check jurisdiction **before** checking the freeze, and immunity MUST be data-driven (the INI tag), not a hard-coded list.

**Orbital set (MUST carry `Jurisdiction = ORBITAL`):** the space laser (`laser` targeting mode in `beta/src/main.ts`), `jslc-orbital-pinpoint-beam`, `jslc-orbital-containment-grid`, `jslc-orbital-defense-platform-strike`, `jslc-orbital-spectrum-sweep`, `jslc-orbital-subsurface-scan`, and the C4I-uplink pinpoint strike in `rosterBehaviors.ts`.

**What immunity does not cover:**
- **Consequences of what you hit.** PR is public opinion, not jurisdiction. An orbital strike on an unverified UN structure (§6.2), a UN truck (§6.1) or a flotilla vessel (§6.5) pays the full penalty for that target class.
- **The baselined public-opinion cooldown multiplier** (§5), pending Q1.

**HUD.** Orbital powers show a distinct "JCOM ORBITAL — OUTSIDE UN JURISDICTION" state while a freeze is active (owner: claude-design).

**Acceptance (golden `new/orbital/`):** during an active freeze every orbital power activates, charges and cools down frame-identically to a no-freeze run with the same seed; every terrestrial offensive power is blocked; an orbital strike on an unverified UN site still triggers the §6.2 collapse.

### 6.5 Greta Thunberg's civilian eco-flotilla

**Fiction.** Albanese can call in Greta Thunberg's civilian eco-flotilla. It sails into a waterway or canal mouth and blockades it, physically blocking warships and halting combat dredging. Firing on it lethally wipes out JSLC's public standing. JSLC has to clear it non-lethally: LRAD, water cannons, or Dvora boarding teams that tow vessels away.

**Objects.**
- `Civ_EcoFlotillaVessel` (×`FLOTILLA_SIZE = 5`): team `Neutral_Civilian`, KindOf `BOAT PROTECTED_CIVILIAN FLOTILLA`, HP 300, `Resolve` 100.
- `Civ_EcoFlotillaFlagship` (×1, Greta's vessel): same KindOf plus `FLOTILLA_FLAGSHIP`, `Resolve` 100, **cannot be dispersed** by LRAD or water cannon. It has to be boarded and towed.
- Neither type has weapons. They never attack.

**Deployment.** The flotilla spawns at the map edge nearest a chosen `FlotillaAnchorage_<n>` waypoint (canal mouths, river mouths, harbor approaches; placed by gemini). It sails there and anchors in a ring formation of radius 60. The anchorage is chosen by the `flotilla` stream, weighted ×3 toward anchorages within 300 world units of an **active dredging job** or a JSLC naval yard.

**Blockade (while ≥ 1 vessel is anchored inside the ring).**
- **Physical obstruction.** Anchored vessels occupy their pathfinding cells and mark the ring's water cells as impassable to JSLC `naval` locomotion (`FLOTILLA_BLOCK` surface flag). AoI and neutral boats ignore the flag. Emits `FLOTILLA_BLOCKADE_ACTIVE`.
- **Dredging halt.** Every `DredgingJob` whose sector lies within `FLOTILLA_DREDGE_HALT_RADIUS = 240` moves to `halted`. Progress is frozen, not lost, and `DREDGE_HALTED { cause: FLOTILLA }` is emitted. No new dredging job can start in that radius. The job resumes automatically (`DREDGE_RESUMED`) when the blockade lifts.
- The blockade lifts when no vessel is anchored inside the ring (`FLOTILLA_BLOCKADE_LIFTED`). The flotilla despawns after `FLOTILLA_MAX_SEC = 420` if it is never cleared. That counts as a lapse, with no PR change.

**JSLC non-lethal options.**

| Tool | Carrier | Effect on a vessel |
|---|---|---|
| **LRAD** (acoustic) | Upgrade on Super Dvora Mk III and Sa'ar 6 (`Upgrade_LRAD`) | Range 180. Drains `Resolve` at 12/s. At 0 Resolve a normal vessel **disperses**: it raises anchor and leaves by the nearest map edge (`FLOTILLA_VESSEL_DISPERSED`, `FLOTILLA_DISPERSED` +3, gain-capped). No effect on the flagship's Resolve |
| **Water cannon** | New unit `JSLC_HarborFireTug`, plus an upgrade on Sa'ar 6 | Range 110. Drains `Resolve` at 8/s and pushes the target 6 units/s away from the shooter, which can shove it out of the ring. Pushes the flagship but does not drain it |
| **Dvora boarding team** | Upgrade on Super Dvora Mk III (`Upgrade_BoardingTeam`) | Must be adjacent (≤ 20). Boarding channel `FLOTILLA_BOARD_SEC = 6`, cancelled if the Dvora takes damage or moves. Afterwards the Dvora **tows** the vessel at 50% of its own speed. Release at a map edge or JSLC naval yard → vessel removed (`FLOTILLA_VESSEL_TOWED`, `FLOTILLA_TOWED` +5, gain-capped). The **only** way to clear the flagship |

**Lethal fire = PR wipeout.** The first time any `LETHAL` weapon (including `ORBITAL` ones, §6.4) damages any flotilla vessel:
- JSLC legitimacy is set to **0** via `applyDelta(JSLC, -current, FLOTILLA_LETHAL_WIPEOUT)`, and AoI popular support gets +25.
- `FLOTILLA_LETHAL_INCIDENT` is emitted and the cable feed runs the incident. The next lawfare action is forced to Condemnation at doubled strength.
- This fires once per flotilla, not once per shot. Splash damage counts. Friendly-fire accidents count. Splash from AoI weapons does not.
- Weapons with `Lethality = NONLETHAL` never trigger it.

**AI.** Skirmish AI for JSLC MUST prefer the non-lethal tools and MUST NOT auto-target `PROTECTED_CIVILIAN` objects with lethal weapons. Units on attack-move or guard skip them automatically. Lethal engagement of a protected object requires an explicit force-fire order from the player.

**Acceptance (golden `new/flotilla/`):** anchorage weighting near dredging; blockade blocks JSLC naval pathing only; dredge job halts and later resumes with its progress intact; LRAD dispersal timing (100/12 ≈ 8.33 s → frame 250); water-cannon push; boarding cancel on damage; tow and release removal; flagship immune to dispersal; one lethal hit → legitimacy 0 exactly once; nonlethal weapons never trigger the wipeout; attack-move never auto-targets a vessel.

---

## 7. Content and naming notes

- Albanese and Thunberg appear as **off-map political antagonists, rendered through their public roles**: UN condemnations, legal pressure, a protest flotilla. The game never makes them targets. Every way to harm the flotilla is punished, and the designed answers are non-lethal. Copy and art MUST stay within that framing. Satire of public positions is fine. Invented personal misconduct is not.
- `PATRON_NAMING` in `patronTrade.ts` already supports `real | fictional` display modes. The lawfare director MUST honor the same switch. In `fictional` mode the antagonists are "the UN Special Rapporteur" and "the eco-flotilla" with generic portraits. The default comes from the same config key.

---

## 8. Change control

1. To change this contract, open `docs/sage/proposals/CCR-<nnn>-<slug>.md` with: the problem, the proposed text diff, the golden vectors it affects, and which lanes it touches.
2. The lane owners whose paths are affected must ack it. codex acks anything touching determinism (§2). claude-design acks anything touching events (§4).
3. Merge bumps the **Status** version at the top of this file. Minor = additive. Major = breaks an existing vector.
4. Every PR on the migration branch states which golden cases it turns green and confirms that `MANIFEST.json` hashes for `ts/**` are unchanged.

---

## 9. Open questions

| # | Question | Default until answered |
|---|---|---|
| Q1 | Should orbital assets also ignore the baselined *legitimacy* cooldown multiplier (1.0→2.5× below 40 PR), or only lawfare freezes? | Only lawfare freezes. The multiplier stays (conformance with `spec-baseline-ts`). |
| Q2 | Should the flotilla wipeout set legitimacy to 0, or apply a very large but finite penalty (for example −80)? | Set to 0. |
| Q3 | Can AoI deliberately steer a hijacked UN truck *into* the flotilla ring to bait JSLC splash damage? | Yes. It's emergent and allowed, and grok red-teams it. |
| Q4 | Does a UN structure cache survive the structure being destroyed? | No. The cache collapses with the structure, along with any tunnel node linked to it. |
| Q5 | Target engine: the EA GPL-3 Generals/ZH source tree, or an OpenSAGE (C#) fork? This contract assumes the **C++ Generals/ZH tree**. | C++ Generals/ZH. |
