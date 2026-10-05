# Brief — gemini: Data, INI & world

**Lane:** Data & world (see [CONTRACTS §1](../CONTRACTS.md#1-lanes-and-ownership))
**Write access:** `sage/data/INI/**` (except `ControlBar*.ini`, `CommandSet*.ini`, `Scripts/Lawfare*.ini`), `sage/data/maps/**`, `docs/sage/data-map.md`

## Mission

Turn the JSLCnC content corpus into SAGE data: INI object, weapon, locomotor and upgrade templates for every roster asset; tunables lifted out of TS constants; and maps with the waypoints and areas the §6 systems need. You are the large-context lane. You read the CSVs, the 80k-line map manifest and the TS tunables blocks all at once and keep them consistent.

## Read first

1. `docs/sage/CONTRACTS.md`, especially §2.1 (seconds → frames at load), §2.5 (Lethality / Jurisdiction), §6 (all tunables and new objects).
2. `docs/JSLC_Master_RTS_Arsenal.csv`, `docs/JSLC_AoI_Faction_Roster.csv`, `docs/JSLC_Morale_and_Supply_Mechanics.csv`, `docs/JSLC_Wasp_Hovercraft_and_Ford_Carrier_Air_Wing.csv`.
3. Every `*_TUNABLES` const in `beta/src/gameplay/*.ts`, plus `beta/config/gameConstants.ts`.
4. `beta/src/content/classicRoster.ts`, `beta/src/content/superweapons.ts`, `beta/src/content/maps/mapManifest.ts`.
5. `docs/openra_conformance_spec.md` §3 (SAGE world units and scale).

## Deliverables

### 1. Pipeline
- [ ] `sage/tools/csv2ini` (any language, but it must be committed and deterministic). It generates `Object`, `Weapon`, `Locomotor` and `Upgrade` blocks from the CSVs plus `classicRoster.ts`. Hand edits go in `*.override.ini`, never in generated files.
- [ ] `docs/sage/data-map.md`: one row per asset with its TS id, CSV name, INI object name and any fields you had to invent. Mark invented values with ⚠.

### 2. Tunables
- [ ] `sage/data/INI/JslcTunables.ini`: every `*_TUNABLES` value at `spec-baseline-ts`, with the same names, in seconds. codex's loader converts seconds to frames.
- [ ] A §6 block with every default from CONTRACTS §6 (`CONVOY_*`, `DIG_BENEATH_*`, `UN_SITE_MULT`, `UN_CONVOY_MULT`, `LAWFARE_*`, `ROE_FREEZE_SEC`, `FLOTILLA_*`, …).
- [ ] A check script that diffs the INI against the TS constants and fails on any mismatch for baseline values.

### 3. Weapon tags (§2.5)
- [ ] Every `Weapon` carries `Lethality` and `Jurisdiction`.
- [ ] The **orbital set** in CONTRACTS §6.4 is tagged `Jurisdiction = ORBITAL`. Nothing else is.
- [ ] New `NONLETHAL` weapons: `LRAD_AcousticBeam` (range 180, Resolve drain 12/s), `WaterCannon_Jet` (range 110, drain 8/s, push 6/s), `SpikeStrip_Deploy`, `EMP_VehicleDisable`. Leave damage at 0 and put the effect in `NonLethalEffect` fields, which codex parses.

### 4. New objects and upgrades (§6)
- [ ] `UN_AidTruck`, `UN_AidDepot`, `UN_Structure_School`, `UN_Structure_Clinic`, `UN_Structure_Warehouse`, `UN_Structure_HQ`: team `Neutral_UN`, with the KindOf from §6.1 and §6.2.
- [ ] `Civ_EcoFlotillaVessel`, `Civ_EcoFlotillaFlagship`: team `Neutral_Civilian`, `Resolve 100`, unarmed.
- [ ] `JSLC_HarborFireTug` (water cannon). `Upgrade_LRAD` and `Upgrade_BoardingTeam` for the Super Dvora Mk III. `Upgrade_LRAD` and the water-cannon upgrade for the Sa'ar 6.
- [ ] AoI abilities: a `Hijacker` flag and `Steal` (siphon) on the AoI infantry roster entries that fit the role, and `DigBeneath` on the AoI worker. List your picks in `data-map.md` for grok to sign off.

### 5. Maps
- [ ] Converter from `mapManifest.ts` / `beta/maps/**` to SAGE map data (heightmap, passability, water, bridges), consistent with `mapLoader.ts` (`DEFAULT_TILE_SIZE = 40`, tile center offset 0.5).
- [ ] Per map, where the terrain allows: `UNCorridor_<n>_Start/_End` waypoint pairs, map-placed `UN_Structure_*`, and `FlotillaAnchorage_<n>` waypoints at canal mouths, river mouths and harbor approaches. Priority maps: Great Bitter Lake, Strait of Fire, Litani Gorge, and every map whose tactics text mentions a canal.
- [ ] A per-map table in `data-map.md` listing which §6 features each map supports. The lawfare director uses it to know whether the flotilla is eligible.

## Constraints

- Baseline numbers MUST match TS exactly. Only the §6 values are new.
- Display names honor the `real | fictional` naming switch (CONTRACTS §7). Put both strings in the localization table (`Data/English/Generals.str` style), keyed by one id.
- Don't invent mechanics. If an asset needs behavior the contract doesn't describe, file a CCR.

## Done when

- `csv2ini` regenerates cleanly with no diff.
- The tunables check passes.
- The orbital-set load check (codex) passes.
- Every §6 object loads in an empty skirmish without errors.
- At least 3 maps carry a full §6 waypoint set.

## Handoffs

- **To codex:** INI field names and units, plus `NonLethalEffect` fields, before they write the parsers.
- **To grok:** the `Hijacker`/`Steal`/`DigBeneath` roster picks and the per-map §6 table.
- **To claude-design:** the asset list for new cameos and icons (§6 objects and upgrades).
