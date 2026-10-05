# JSLC and Conquer — ordered build gaps

## 1. Dispatch rules

This list turns the design review into bounded build tasks, ordered by player impact.
The source baseline is game `e7a97c5356bd7697a1105ae7b06ed79129713788` and notes `8a1a2e3cdf117ab4ecc98345c980fbdb00b7426d`.
`G:` and `N:` use the source coordinates defined in [GAME_DESIGN.md](GAME_DESIGN.md).
Status IDs refer to that document's counted ledger.

P0 blocks trustworthy rules or the central play experience.
P1 blocks a promised operational feature.
P2 blocks completeness, clarity, or visual acceptance.
These priorities are dispatch recommendations, not new gameplay rules.

Each row contains one build task and an observable completion condition.
The implementer must not self-certify completion.
No row authorizes this documentation lane to modify the game or run software test suites.

## 2. Highest-impact gaps

| Rank / ID | Priority | One-line build task | Completion condition | Evidence / design status |
|---|---|---|---|---|
| 1 — GAP-01 | P0 | Route every political change through the common PR sink with team ownership, gain limits, and incident events. | Crash, rescue, weather, combat, and campaign changes use one event path; no team-zero shortcut changes another team's score. | S14 PARTIAL; `N:CONTRACTS.md:54`; `G:src/main.ts:2016`; `G:src/gameplay/operationalLogistics.ts:578`. |
| 2 — GAP-02 | P0 | Integrate mandatory lethality tags and protected-target handling across direct fire, splash, automatic attacks, and strategic powers. | Missing tags fail loading; nonlethal effects preserve protected health; first-hit incidents occur once with correct attribution. | S10 DESIGNED-ONLY; `N:CONTRACTS.md:68`; `G:src/gameplay/superweaponRuntime.ts:29`. |
| 3 — GAP-03 | P0 | Resolve the freeze/friction conflict through a contract change, then implement the approved policy and visible timers. | CONTRACTS, REV-001, cooldown rules, button gates, and the manual agree; the change records explicit approval. | S15 PARTIAL and S18 DESIGNED-ONLY; `N:CONTRACTS.md:246`, `:328`. |
| 4 — GAP-04 | P0 | Extend the player-controlled laser's jurisdiction behavior across all orbital powers, authorities, and protected-target consequences. | Local and remote powers obey one approved policy; charge ticks never fire; orbital jurisdiction never erases PR penalties. | S20–S21 PARTIAL; `G:src/gameplay/laserCharge.ts:45`; `N:CONTRACTS.md:269`. |
| 5 — GAP-05 | P0 | Enable authored campaign terrain and progression with an approved crosswalk from the canonical acts to eighteen map assets. | Every advertised mission launches its terrain and objectives; Blue Aurora retains an explicit place; saves preserve valid progression. | S36 PARTIAL; `N:CAMPAIGN.md:3`; `G:src/gameplay/CAMPAIGN.md:7`. |
| 6 — GAP-06 | P1 | Complete production cameos, specific blocked reasons, remote rally routing, and conflict-free keyboard handling in the new sidebar. | Primary selection and queues work on desktop and phone; production keys do not silently replace tactical or logistics actions. | S07 PARTIAL; `G:src/ui/productionSidebar.ts:176`, `:349`, `:474`, `:557`; torch `briefs/pu01.md`. |
| 7 — GAP-07 | P1 | Apply compatible basing, capacity, bingo, diversion, fuel gauges, and crash ownership to every aircraft creation path. | Core, expanded, carrier, campaign, and remote aircraft behave consistently after base loss and fuel exhaustion. | S28 PARTIAL; `G:src/gameplay/aircraftOps.ts:367`; `G:server/networkSimulation.ts:556`. |
| 8 — GAP-08 | P1 | Complete faction-specific production and roster actions while preserving the AoI public label. | Tunnels, JSLC defense support, and powered Penguin deployment create distinct choices; catalogue entries disclose unavailable actions. | S02–S03 PARTIAL; `G:src/main.ts:2046`; `G:src/content/classicRoster.ts:52`. |
| 9 — GAP-09 | P1 | Replace proximity-only chickie victory with the guarded rescue and its approved PR and lawfare consequences. | Only the defined rescue completes the objective; chickies remain alive; rewards pass through the capped sink exactly once. | S35 PARTIAL; `G:src/main.ts:2025`; `N:design/PENGUIN_AND_CHICKIE_LORE.md:54`. |
| 10 — GAP-10 | P1 | Expose political, production, aircraft, and mission state through readable desktop and phone HUD panels. | Players can explain each refusal, fuel diversion, PR loss, rebuttal window, and blocked objective from visible state. | S42 PARTIAL; `N:ui/hud_layouts.md`; torch `briefs/rl02.md`. |

## 3. Remaining feature and integration gaps

| Rank / ID | Priority | One-line build task | Completion condition | Evidence / design status |
|---|---|---|---|---|
| 11 — GAP-11 | P1 | Connect convoy spawning, hijack, ISR, siphoning, nonlethal disable, boarding, and recovery to active matches. | The protected driver, hidden cargo, seeded timing, recruitment bonus, and once-per-truck penalty match the contract. | S16 DESIGNED-ONLY; `N:CONTRACTS.md:189`. |
| 12 — GAP-12 | P1 | Connect protected structures and caches to proof states, tunnel logistics, armor support, and incident accounting. | No-cache sites cannot become confirmed; evidence rewards and lethal multipliers use the common sink. | S17 DESIGNED-ONLY; `N:CONTRACTS.md:217`. |
| 13 — GAP-13 | P1 | Integrate flotilla traffic blocking, dredge pause, resolve, water cannon, boarding, towing, and first-hit consequences. | The flagship requires towing before timeout; paused work retains progress; AoI fire is not blamed on JSLC. | S19 DESIGNED-ONLY; `N:CONTRACTS.md:285`. |
| 14 — GAP-14 | P1 | Integrate the fleet-scale undersea base with campaign production, both staging areas, concealment, damage, flooding, and replenishment. | A full-size capital ship completes the reserved route; damage halts transfer; service limits are visible in both layers. | S25 PARTIAL; `G:docs/design/DIEGO_GARCIA_UNDERSEA_BASE.md:86`. |
| 15 — GAP-15 | P1 | Define the relationship between the Aurora four-phase mechanism and the harbor's twelve-minute ship lift. | Capacity, mast clearance, timing, mission placement, and failure rules have one explicit contract per scenario. | S25/S36 PARTIAL; `G:beta/src/gameplay/auroraElevator.ts:8`; `N:CAMPAIGN.md:9`. |
| 16 — GAP-16 | P1 | Unify supply, morale, fuel, ammunition, missiles, and repair services for forward forces and fleet support ships. | Each supported platform consumes and replenishes the advertised resource; the campaign teaches the active dependency. | S05/S22 PARTIAL; `G:src/gameplay/supplyMoraleSystem.ts:88`; `G:src/gameplay/operationalLogistics.ts`. |
| 17 — GAP-17 | P1 | Connect the complete detainee transport and tribunal chain to the active match with protected-person ownership and evidence events. | Surrendered units survive legitimate capture; transport losses and tribunal rewards resolve once for the correct team. | S34 DESIGNED-ONLY; `G:beta/src/gameplay/captureOperations.ts:58`. |
| 18 — GAP-18 | P1 | Add the faction promotion-point spending menu and route all combat kill credit through common veterancy handling. | Earned points buy visible choices; projectile and expanded damage paths award the same eligible ranks and effects. | S12–S13 PARTIAL; `G:src/main.ts:168`; `G:vendor/cnc2d/game/src/core/sim.ts:1968`. |
| 19 — GAP-19 | P1 | Complete tower defense as a selectable mode with waves, preparation periods, objectives, and restart behavior. | All three advertised tower-defense maps have a complete playable loop on the active runtime. | S38 DESIGNED-ONLY; `G:beta/src/main.ts:157`; `G:src/content/maps/mapManifest.ts:24`. |
| 20 — GAP-20 | P1 | Validate every advertised skirmish map for launch support, starts, expansion sites, water routes, and supported player counts. | The nine 1v1 and nine larger maps match their labels without inaccessible starts or unadvertised terrain substitution. | S37 IMPLEMENTED only for catalogue counts; `G:src/content/maps/mapManifest.ts:6`. |
| 21 — GAP-21 | P1 | Establish a common deterministic simulation schedule, command path, seeded effects, and complete replay state. | Equivalent inputs reproduce gameplay state across supported authorities; render timing and unseeded randomness do not change outcomes. | S40 PARTIAL; `N:CONTRACTS.md:37`; `G:src/harness/GameHost.ts:43`. |
| 22 — GAP-22 | P1 | Complete multiplayer service acceptance and document or implement reconnect, credential recovery, and room continuity. | Supported free-for-all and team sizes finish live matches; interruption behavior matches the published promise. | S39 PARTIAL; `G:MATCHES.md:20`. |
| 23 — GAP-23 | P1 | Replace empty golden coverage claims with meaningful immutable vectors, a pinned oracle, correct manifest paths, and independent parity evidence. | State and event changes are asserted; a deliberate mismatch fails; every referenced fixture resolves from the manifest. | S45 PARTIAL; `N:golden/MANIFEST.json`; jpd2 `GOLDEN_VECTOR_PROTOCOL.md:6`. |
| 24 — GAP-24 | P2 | Audit real dimensions, collision footprints, camera reach, and the optional small-unit enlargement across land, air, and naval assets. | Large hulls retain scale; enlargement changes rendering only; units can navigate their advertised physical envelopes. | S30 PARTIAL; `G:src/content/unitDimensions.ts:1`; torch `briefs/_markings.md`. |
| 25 — GAP-25 | P2 | Implement the requested finer terrain subdivision without substituting a pathfinding-cell setting for terrain detail. | The chosen subdivision meets the owner's minimum and preserves consistent depth, passability, and visual boundaries. | S44 DESIGNED-ONLY; `G:session-transcripts/transcript.jsonl:654`, `:678`. |
| 26 — GAP-26 | P2 | Replace ambiguous platform graphics with distinct silhouettes and apply the exact roundel, ensign, and patch masters. | Ford, Wasp, Burke, Seawolf, and Sa'ar pass visual comparison; markings use the prescribed positions and colors. | S43 PARTIAL; torch `briefs/_markings.md`; `G:docs/generals2_scale_and_art_direction.md`. |
| 27 — GAP-27 | P2 | Resolve Guardian Carrier and Redoubt Carrier identities and publish an explicit full-versus-compressed fleet-complement policy. | The roster, production categories, guide, and ship capacities agree without invented naval capability. | S02/S22 PARTIAL; `G:src/content/classicRoster.ts:158`; `G:src/gameplay/expandedRoster.ts:175`. |
| 28 — GAP-28 | P2 | Integrate weather forecasts, power effects, engineering hazards, and flotilla dredge pauses through recorded simulation events. | Forecast replay is stable; current cancellation and protected obstruction have distinct visible outcomes. | S08/S33 PARTIAL; `G:src/gameplay/weatherAndFording.ts:1236`; `N:CONTRACTS.md:285`. |
| 29 — GAP-29 | P2 | Reconcile the published guide and navigation with the current game, fuel rules, availability labels, and Briefing/Intel/Factions split. | Current play instructions exclude retired variants and clearly label future missions and catalogue-only actions. | S42 PARTIAL; `G:src/guide/content.ts:50`; torch `briefs/rl02.md`. |
| 30 — GAP-30 | P2 | Independently observe desktop and phone control, layout, and visual behavior after integration. | Sticky selection, expanded enemy hit areas, two-finger camera gestures, overlays, and touch targets work in actual play. | S41 source-IMPLEMENTED; S42–S43 PARTIAL; `G:src/input/pointer.ts:267`. |

## 4. Dependencies and protected regressions

GAP-01 and GAP-02 underpin convoys, structures, flotilla, capture, and orbital consequences.
GAP-03 requires an approved contract decision before an implementer changes freeze behavior.
GAP-05 and GAP-14 need a shared mission-to-runtime contract.
GAP-21 and GAP-23 underpin any C++ parity or cross-platform replay claim.

Keep these existing behaviors during later integration:

- Deep-water ground-unit sinking, wrecks, and transport-loss hazards.
- Stern-only well-deck routes with actual compatible craft.
- Fixed-wing motion and fuel use during rotary hover.
- Moving patrol centers and deterministic escort slots.
- Persistent phone selection and explicit Unselect.
- AoI's protected public label.
- Chickie rescue instead of chickie assassination.

The source review does not authorize deployment or declare these acceptance conditions passed.
