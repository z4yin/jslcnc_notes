# JSLC and Conquer — game design

## 1. Authority, scope, and reading key

This document defines the intended game and separates that design from the current browser implementation.
It accompanies [the player manual](HOW_TO_PLAY.md) and [the ordered build gaps](GAPS.md).

`N:` means the notes repository at `8a1a2e3cdf117ab4ecc98345c980fbdb00b7426d`.
`G:` means the game repository at `e7a97c5356bd7697a1105ae7b06ed79129713788`.
References use repository-relative `file:line` coordinates.
The game pin includes aircraft, production, AoI-label, player-controlled laser, and mission-opening updates.

Authority follows this order: notes contracts; other notes design; owner messages; game source; planning documents; recent torch briefs; owner-intent extraction.
`N:CONTRACTS.md` wins when sources conflict.
Source code proves present behavior, not approval of that behavior.
No new balance proposal in this document overrides a contract.

**IMPLEMENTED** means the inspected main source reaches the stated behavior within its named scope.
**PARTIAL** means part exists, but integration, scope, or design agreement remains incomplete.
**DESIGNED-ONLY** means the required behavior has no established path in the active main match.
Code in a separate beta or SAGE tree does not establish active-match implementation.
None of these labels certifies live play, visual quality, deployment, or deterministic parity.
Section 26 contains the sole counted status ledger.

## 2. Premise and tone — PARTIAL

Three military machines contest territory, resources, and public legitimacy.
JSLC brings combined arms and orbital bureaucracy.
AoI brings cheap pressure, concealment, and a tunnel network.
The Directorate of the Penguins brings Antarctic imperial ambition, ancient technology, and extremely questionable claims to all fishies.

The joke must change a decision on the battlefield.
A press conference does not stop a shell in flight.
A protected ship can obstruct a harbor without firing a weapon.
An orbital laser escapes terrestrial jurisdiction, but not the consequences of its target choice.

Satire targets institutions, propaganda, military excess, and fictional antagonists.
It does not turn a people or religion into a unit category.
Named real-world public-role references use the contract's optional fictional display mode.
Invented private misconduct has no place in that system.
Sources: `N:CONTRACTS.md:323`; `G:src/explainer/data/factions.ts:8`; `G:session-transcripts/transcript_full.jsonl:585`.

## 3. Factions and identities — PARTIAL

| Side | Intended play | Strengths | Weaknesses and counterplay |
|---|---|---|---|
| JSLC / JCOM Coalition | Build a defended combined-arms network, then project power by air, sea, and orbit. | Layered defense, reconnaissance, precision fire, repair, carriers, amphibious logistics. | Expensive losses, supply routes, power demand, protected-target incidents. |
| AoI | Apply cheap, mobile pressure through concealed positions and tunnel exits. | Numbers, raids, rockets, infiltration, convoy exploitation, distributed production. | Fragile units, exposed networks, interdicted routes, confirmed evidence. |
| Directorate of the Penguins | Field fewer, expensive, durable units from powered deployment fields. | Shields, polar adaptation, ancient technology, powerful specialist units. | Power dependency, expensive replacement, rescue of the captive chickies. |

The public faction label remains **AoI**.
The brief's “Axis of Iran” and older “Khamas” do not authorize a rename.
Current text also uses “Axis of Intifada”; the owner explicitly protected the abbreviation, not a new long-form expansion.
The latest main replaces the “Free Network” roster label with AoI.
Sources: `G:session-transcripts/transcript.jsonl:2471`; `G:src/content/classicRoster.ts:52`; `G:src/guide/content.ts:181`.

JSLC's roster includes rifle infantry, Merkava armor, D9 support, layered missile defense, aircraft, and distinct naval hulls.
AoI's core roster includes infantry, vehicles, paragliders, boats, drones, rocket teams, and harvesters.
Penguin lore adds Emperor melee troops, Beanie Elephant workers, Dragoon walkers, Puddle Jumpers, and the Space Dreidel.
Beanie Elephants repair and build; their warmth and polar upgrades belong to the authored technology design.
The live catalogue does not prove each named unit has its promised specialist behavior.
Sources: `G:src/guide/content.ts:55`; `G:src/content/classicRoster.ts`; `N:design/PENGUIN_AND_CHICKIE_LORE.md`.

Current production still shares core unit classes and faction multipliers.
Local faction bonuses include AoI tunnel emergence, a JSLC spawn-health bonus, and a temporary Penguin shield marker.
These do not complete powered warp production or the full asymmetric roster.
Source: `G:src/main.ts:2046`.

Protected civilians, UN actors, patrons, and the flotilla are not ordinary playable factions.
Lawfare antagonists operate off-map through events, not targetable civilian characters.
Source: `N:CONTRACTS.md:246`.

## 4. Core loop and victory — PARTIAL

The loop is reconnaissance, income, production, territorial expansion, force projection, and recovery.
The player must protect both the supply route and the political consequences of force.
Reconnaissance can reveal an enemy advantage without removing the protected status of its cover.
Repair and resupply preserve expensive units between engagements.

Current skirmish victory centers on enemy command assets.
AoI can retain command through completed core Tunnel Nodes after headquarters loss.
Team matches retain separate ownership and end when only one team survives.
Campaign objectives can replace the ordinary headquarters finish.
Zero legitimacy is not a universal, approved defeat rule for every mode.
The chickie surrender is a specific authored exception.
Sources: `G:src/guide/content.ts`; `G:src/gameplay/CAMPAIGN.md:22`; `N:design/PENGUIN_AND_CHICKIE_LORE.md:54`.

## 5. Economy, resources, and sustainment — PARTIAL

Finite deposits create reasons to expand and expose supply routes.
Workers collect supplies and return them to a compatible drop-off.
Core workers carry up to 40 supplies.
The current local game also retains income outside direct collection, including a reduced-income state after nearby depletion.
Do not describe the current economy as entirely deposit-funded.
Sources: `G:vendor/cnc2d/game/src/core/sim.ts:2049`; `G:src/main.ts:1879`.

Supply pays for construction, units, and applicable support actions.
Command resources and rank gate strategic actions separately.
Arms caches and convoy cargo follow their own contract accounting.
An upgrade cannot silently spend another resource because its label resembles supply.

Ships and forward units need replenishment where their active systems consume fuel, ammunition, missiles, or parts.
Logistics vessels make distant operations sustainable; they are not decorative escorts.
Current operational logistics exists, but the separate supply/morale model lacks an observed active caller.
The guide must identify which platform and mode actually support each service.
Sources: `G:src/gameplay/operationalLogistics.ts`; `G:src/gameplay/supplyMoraleSystem.ts:88`; `G:session-transcripts/transcript.jsonl:2452`.

## 6. Construction and production — PARTIAL

Builders place valid foundations and complete prerequisites before advanced production.
Land buildings require a complete dry foundation away from crossings.
Naval production requires compatible water access.
Expanded producers reject incompatible unit classes and advance one job at a time.
The current expanded queue limit is eight jobs per producer.
Low power slows progress; blocked naval launches retain their queue job.
Sources: `G:src/gameplay/buildPlacement.ts:21`; `G:src/gameplay/expandedMechanics.ts:205`; `G:src/gameplay/expandedMechanics.ts:528`.

| Faction | Core technology route |
|---|---|
| JSLC | Fusion Plant → Ground Command and Supply Works → Research Directorate → layered defenses. |
| AoI | Generator Shed → Training Courtyard and Resource Plot → Covered Workshop, Concealed Block, and Tunnel Node. |
| Penguins | Fish Reactor → Waddle Academy and Fish Depot; the wider shield and warp tree remains incomplete. |

Source: `G:vendor/cnc2d/game/src/core/techTree.ts:46`.
The current Build panel calls these Penguin structures Khaydarin Pylon, Gateway Warp Conduit, and ZPM Subspace Siphon respectively.
Those display names do not establish full warp mechanics.
Source: `G:src/gameplay/buildCatalog.ts:63`.

The required production sidebar has seven tabs: Structures, Defences, Infantry, Vehicles, Aircraft, Naval, and Support.
Each item shows a cameo, cost, duration, prerequisites, queue count, and a specific blocked reason.
The first eligible producer becomes primary.
Desktop double-click or phone long-press selects another primary.
Each factory retains its own queue and rally point.
Shift-click queues five; right-click cancels under the defined refund rule.
Tab cycling and production shortcuts require an explicit conflict-free keyboard layout.
The latest main adds these seven tabs, primary selection, queue badges, costs, durations, and several blocked reasons.
Selecting another compatible factory overrides the primary for that purchase.
An optional Split queues mode chooses the least-queued eligible factory.
Sources: `G:src/ui/productionDesk.ts:193`; `G:src/ui/productionSidebar.ts:281`.

The complete workflow remains **PARTIAL**.
Cards contain text rather than the requested platform cameos.
Unknown blocked reasons fall back to a generic factory requirement.
Rally routing is local-only, and global production shortcuts intercept E and R before escort and repair handlers.
Desktop double-click and phone long-press paths exist but lack live acceptance here.
Sources: `G:src/ui/productionSidebar.ts:176`, `:349`, `:474`, `:557`; `G:src/ui/productionDesk.ts:291`.
Authority: torch `briefs/pu01.md`.

## 7. Power — PARTIAL

Power output and demand affect the base before a blackout becomes a tactical disaster.
Current core headquarters provide 50 power; plants provide 100.
Research, supply infrastructure, and layered defenses consume power.
Core and expanded production can fall to half speed under low power.
Sources: `G:vendor/cnc2d/game/src/core/sim.ts:1866`; `G:src/gameplay/expandedMechanics.ts:528`.

The intended Penguin field network must make shield support and warp deployment depend on functioning power.
Weather and lawfare effects must enter the same power and production accounting.
Current isolated effects do not establish that common model.
The HUD must state the shortage and its actual effect, not merely change a number's color.

## 8. Combat, damage, veterancy, and command rank — PARTIAL

Ordinary combat resolves movement, range, cooldowns, projectiles, and health.
Expanded definitions add armor, footprint, weapons, and selected special actions.
Tags and names alone do not create a damage type or counter relationship.
The catalogue must distinguish a functioning action from a reference design.
Sources: `G:src/gameplay/expandedRoster.ts:153`; `G:src/gameplay/expandedMechanics.ts`; `G:src/guide/content.ts:31`.

Area attacks can damage friendly and allied units.
Hostile-only automatic targeting does not confer immunity inside a blast.
Protected actors require a separate exclusion and incident path.
Source: `G:src/gameplay/friendlyFire.ts`.

Every damaging weapon and power requires `LETHAL` or `NONLETHAL` and terrestrial or orbital jurisdiction.
Nonlethal effects preserve protected health at one or higher and use resolve, disable, displacement, or capture instead.
The loader must reject missing tags.
The active strategic definition currently lacks those required fields.
Sources: `N:CONTRACTS.md:68`; `G:src/gameplay/superweaponRuntime.ts:29`.

Core projectile kills award veteran status at three kills and elite status at ten.
Each threshold multiplies health, maximum health, and damage by 1.2; both thresholds yield a cumulative 1.44 multiplier.
Veterans also receive core regeneration.
Expanded direct-damage paths need the same kill credit and rank effects.
Sources: `G:vendor/cnc2d/game/src/core/sim.ts:1968`; `G:vendor/cnc2d/game/src/core/sim.ts:2688`.

Commander XP thresholds currently include 0, 300, 800, 1600, and 2600.
Rank and a point counter exist; an observed point-spending faction menu does not.
Earned promotion choices remain a build requirement, not an available manual instruction.
Source: `G:src/main.ts:168`.

## 9. Public relations and legitimacy — PARTIAL

JSLC legitimacy and AoI support range from zero to 100.
The normative PR sink receives every gain and penalty and emits `PR_DELTA` events.
Gains share a rolling ceiling of 25 per 60 seconds, with the specified diminishing returns.
Penalties have no matching gain-style cap.
No weather, crash, rescue, or campaign subsystem may write around the sink.
Source: `N:CONTRACTS.md:54`.

The protected-incident penalty is `round(28 × (2 − confidence) × classMultiplier)`.
Confidence begins at 0.30, increases by 0.35 per qualifying ISR pass, and caps at 0.95.
Evidence reduces uncertainty; it does not erase protection or authorize cost-free lethal force.
Source: `N:CONTRACTS.md:83`.

REV-001 intends declining legitimacy to create production, rearm, patron, and protest friction.
It explicitly rejects weapon lockout.
CONTRACTS §6.3 still prescribes a terrestrial offensive freeze.
CONTRACTS Q1 also retains an opinion-based cooldown multiplier below 40.
These are unresolved policy conflicts.
Until a contract change lands, the contract remains the conformance baseline.
Do not substitute jpd1's proposed PR bands or invented exact friction percentages.
Sources: `N:design/revisions/REV-001-survival-over-reputation.md`; `N:CONTRACTS.md:246`; `N:CONTRACTS.md:328`.

Current main still contains direct legitimacy writes and an unseeded embargo roll.
Its visible PR meter does not establish sink conformance.
Sources: `G:src/main.ts:2016`; `G:src/gameplay/operationalLogistics.ts:578`; `G:src/gameplay/weatherAndFording.ts:1511`.

## 10. Protected actors, convoys, structures, and flotilla — DESIGNED-ONLY

This status applies to the complete contract behavior in the active match.
Separate candidate implementations and art do not close it.

**Convoys.** Three protected trucks arrive every 150 seconds, with seeded variation of ±30 seconds.
Each truck carries 300 supplies and either zero or 120 arms; armed probability is 0.35.
Hijack takes three seconds and retains a protected hostage driver.
Siphoning within 40 range transfers ten supplies and four arms per second.
Each 120 arms adds ten percent recruitment benefit, up to thirty percent, with 180-second decay.
A four-second ISR pass increases confidence by 0.35.
Exposing an armed hijack awards JSLC +6 and AoI −8 through the sink.
Nonlethal disable lasts twenty seconds; boarding an immobilized truck takes three seconds and recovery awards +8.
The first lethal damage triggers the truck penalty once; its multiplier is 1.5.
Blind fire costs about 71; one ISR pass reduces that example to 57.
Source: `N:CONTRACTS.md:189`.

**Protected structures.** Dig Beneath costs 400 supplies and forty seconds.
Limits are one cache per site and four per player.
A cache grants fifteen percent armor within sixty range.
ISR can make a site disputed at confidence 0.40 or greater.
Confirmation requires the specified proof scan or an engineer at the portal.
Confirmation awards JSLC +10 and AoI −12.
Unverified and disputed sites retain a 2.5 multiplier; confirmed sites use 0.35.
A blind penalty can be 119, which clamps legitimacy at zero.
A confirmed site at 0.95 confidence still costs ten.
A site without a cache cannot become confirmed.
Source: `N:CONTRACTS.md:217`.

**Flotilla.** Five normal boats and one flagship arrive as protected, unarmed actors.
Each has 300 health and 100 resolve.
The group blocks JSLC naval traffic and can halt nearby dredging for 240 seconds without deleting progress.
Existing dredging resumes after the obstruction; new jobs cannot start while blocked.
A 420-second timeout clears the event without a PR reward.
Source: `N:CONTRACTS.md:285`.

LRAD reaches 180 and drains twelve resolve per second from ordinary boats.
Water cannon reaches 110, drains eight resolve per second, and pushes six units per second.
The flagship ignores resolve drain; water cannon only displaces it.
A Dvora boards within twenty range over six uninterrupted seconds.
It tows at half speed and releases at the map edge or yard for +5.
Ordinary dispersal awards +3.
Only towing permanently clears the flagship before timeout.
Source: `N:CONTRACTS.md:298`.

The first JSLC lethal hit sets legitimacy to zero and gives AoI +25, once per flotilla.
Splash and accidental friendly fire count.
AoI damage is not attributed to JSLC.
The next condemnation is forced and doubled.
Automatic weapons must exclude protected boats; explicit force-fire remains deliberate and consequential.
Sources: `N:CONTRACTS.md:309`; `N:golden/new/flotilla/lethal_wipeout.jsonl:1`.

## 11. Lawfare — DESIGNED-ONLY

The contract director schedules its first event at 360 seconds and later events every 300 ±60 seconds.
A twenty-second warning precedes the event.
Base weights are condemnation 0.45, freeze 0.35, and eligible flotilla 0.20.
A flotilla requires an anchorage and no active flotilla.
Source: `N:CONTRACTS.md:246`.

Condemnation applies JSLC −6 and AoI +4; a recent protected incident doubles those values.
The rebuttal window lasts thirty seconds.
A staged incident permits full rebuttal; other eligible cases permit the specified partial response.
A terrestrial freeze lasts forty-five seconds, plus ten at legitimacy below forty.
After the third event, freeze weight rises by 0.05 to a maximum of 0.55.
A qualifying dossier halves the remaining freeze once.
Movement and nonlethal responses remain available.
Return fire has the contract's explicit exemption.
Source: `N:CONTRACTS.md:246`.

The HUD needs a warning, countdown, reason, affected actions, rebuttal availability, and dossier feedback.
A disabled button without that explanation fails the design.
REV-004 specifically treats this visibility as unfinished.
Sources: `N:design/revisions/REV-004-lawfare-and-flotilla.md`; `N:ui/hud_layouts.md`.

## 12. Superweapons and orbital jurisdiction — PARTIAL

Strategic powers need real effects, costs, prerequisites, cooldowns, ownership, and targeting feedback.
The current runtime supports several damage, reveal, jam, and field effects.
It does not establish full catalogue coverage or typed jurisdiction.
Source: `G:src/gameplay/superweaponRuntime.ts:105`.

Orbital jurisdiction is checked before terrestrial lawfare gates.
The orbital laser, pinpoint, containment, defense strike, spectrum, subsurface, and C4I set remain outside that freeze.
Activation, charging, and cooldown progress all retain that immunity.
The badge reads `JCOM ORBITAL — OUTSIDE UN JURISDICTION`.
Protected-target PR consequences still apply in full.
The separate opinion cooldown rule remains pending the contract's Q1 resolution.
Sources: `N:CONTRACTS.md:269`; `N:golden/new/orbital/immunity.jsonl:1`.

Current local JSLC skirmish uses a player-controlled laser charge instead of automatic map strikes.
The base charge is fifteen seconds and ignores terrestrial freeze state.
Its opinion multiplier rises from 1.0 at legitimacy forty to 2.5 at zero.
The charge tick neither fires nor grants command resources, and a player strike restarts it.
The dedicated HUD path excludes authored missions and remote matches.
This closes the automatic-fire defect while leaving catalogue-wide jurisdiction and protected consequences incomplete.
Sources: `G:src/gameplay/laserCharge.ts:25`; `G:src/gameplay/laserCharge.ts:45`; `G:src/main.ts:1863`.

## 13. Naval operations and amphibious warfare — PARTIAL

Ford, Wasp, Burke, Seawolf, and Sa'ar hulls require distinct silhouettes and roles.
Ford supplies CATOBAR aviation.
Wasp combines compatible aviation with a stern well deck.
Burke supports fleet defense and helicopters; Seawolf serves the submarine role.
Sa'ar offers a smaller naval combat and aviation platform.
Platform names do not establish every real-world weapon as a functioning game action.
Sources: `G:src/content/classicRoster.ts:341`; `G:src/gameplay/expandedRoster.ts:175`.

Ships carry actual craft and cargo, with explicit deck and well-deck limits.
Current complements are compressed gameplay groups, not full real-world air wings.
The inspected Ford offers sixteen deck slots and eight default aircraft.
Wasp offers eight flight slots, five default aircraft, and two LCACs.
Auto complement buys replacements for lost default craft; it does not duplicate aircraft still on a mission.
Sources: `G:src/gameplay/expandedRoster.ts:175`; `G:src/gameplay/navalAmphibious.ts:413`.

Well-deck launch and recovery use the stern.
An LCAC must leave the ship, reach the beach, and deploy its actual cargo.
Recovery reverses that physical sequence.
Wasp-class LHD-6 has a well deck; America-class LHA-6 does not.
Do not relabel one hull to grant the other's capability.
Sources: torch `briefs/wd01.md`; `G:src/gameplay/navalAmphibious.ts:172`; `G:src/gameplay/navalAmphibious.ts:326`.

**Deep-water sinking is IMPLEMENTED and protected.**
Non-embarked ground units that enter deep water die and leave a wreck.
Air, naval, and embarked units are exempt while those conditions hold.
Cargo from a lost transport faces the same water hazard after release.
The current deep-water threshold is one gameplay metre.
The separate shallow-water hazard grace does not grant deep-water immunity.
Do not replace sinking with a shore stop, refund, or harmless deletion.
Sources: `G:vendor/cnc2d/game/src/world/water.ts:7`; `G:vendor/cnc2d/game/src/core/sim.ts:828`; `G:src/gameplay/battlefieldSystems.ts:129`.

## 14. Diego Garcia undersea base — PARTIAL

The fictional base is a fleet yard beneath Diego Garcia, not a small cave containing a shrunken carrier.
Its architectural envelope is 7,200 by 4,800 metres.
The main basin is 6,500 by 3,200 metres, with a waterline at −820 and twenty-two metres of water depth.
The design provides one hundred metres of overhead clearance.
Source: `G:docs/design/DIEGO_GARCIA_UNDERSEA_BASE.md:41`.

The berth plan holds eight capital, twelve escort, twelve submarine, eight auxiliary, and sixteen patrol positions.
Those 56 wet berths are distinct from four dry-dock allocations.
The lift shaft is 500 metres across, with a 420-by-120-metre admission envelope.
Each end has twelve staging positions of 420 by 120 metres.
The 400-metre fairway cannot become queue parking.
Sources: `G:docs/design/DIEGO_GARCIA_UNDERSEA_BASE.md:69`; `G:docs/design/DIEGO_GARCIA_UNDERSEA_BASE.md:86`.

The current exercise reserves destinations and serves deterministic queue tickets.
One transfer takes 720 simulation seconds: enclosure sixty, transit six hundred, and equalization sixty.
That gives five theoretical transfers per hour before approach delays.
The harbor source uses internal 100-millisecond steps; this does not prove contract-wide 30 Hz integration.
Sources: `G:docs/design/DIEGO_GARCIA_UNDERSEA_BASE.md:92`; `G:src/gameplay/diegoGarcia.ts`.

Damage halts the lift.
Flooding and failed pumping can stop transfer and berth services.
The lower layer conceals ships from surface attack while berth systems repair and replenish them.
The separate `diego-garcia.html` exercise exposes surface and underground views.
Expanded harbor production can stage ships below, but ordinary online matches do not provision the full exercise.
Some architectural districts remain allocations rather than simulated services.
Source: `G:docs/design/DIEGO_GARCIA_UNDERSEA_BASE.md:111`.

The older Aurora elevator uses four short phases and a different clearance model.
Its 22-second sequence must not silently replace the 720-second harbor transfer.
Campaign integration needs an explicit crosswalk between those systems and the normative Blue Aurora mission.
Sources: `G:beta/src/gameplay/auroraElevator.ts:8`; `N:CAMPAIGN.md:9`.

## 15. Aircraft, fuel, and basing — PARTIAL

Expanded aircraft require compatible basing and available slots before production.
Land airbases, CATOBAR decks, STOVL decks, and rotary-capable decks have different acceptance rules.
Aircraft receive a home base and divert when that base disappears, if another compatible slot exists.
Unrecoverable fuel exhaustion ends in a crash and an own-team PR penalty.
Sources: `G:src/gameplay/aircraftOps.ts:284`; `G:src/gameplay/aircraftOps.ts:353`; `G:src/gameplay/aircraftOps.ts:367`.

Airborne fixed-wing aircraft keep moving.
Idle orders produce loiter behavior; they do not stop the aircraft in mid-air.
Rotary aircraft may hover, but hover still burns fuel.
Bingo fuel overrides ordinary orders with return-to-base behavior.
Afterburner consumes fuel faster; parking at the assigned supply base restores fuel.
Sources: `G:src/gameplay/aircraftOps.ts:199`; `G:src/gameplay/aircraftOps.ts:411`.

The host's fuel setting offers 1×, 2×, 5×, 100×, and infinite endurance.
These values are fuel-capacity scales; larger finite values increase endurance rather than accelerate consumption.
Infinite disables fuel burn.
The lobby synchronizes the setting; the HUD presents fuel status.
Sources: `G:src/gameplay/aircraftOps.ts:9`; `G:src/match/launcher.ts:42`; `G:src/main.ts:133`.

The shared fuel arithmetic now reaches local and server paths.
However, home-base maintenance skips entities without an assigned home ID.
Coverage of every legacy aircraft and every spawn path remains incomplete evidence.
Other logistics PR writes still need ownership and sink review.
Sources: `G:src/gameplay/aircraftOps.ts:367`; `G:server/networkSimulation.ts:556`; `G:src/gameplay/operationalLogistics.ts:269`.

## 16. Real-world scale, terrain, and zoom — PARTIAL

One world unit represents one metre in the dimension catalogue.
Known platform dimensions and clearly labeled representative dimensions remain distinct.
A 333-metre carrier must dwarf a 1.8-metre soldier.
Large hulls cannot shrink to fit a convenient screenshot or harbor.
Sources: `G:src/content/unitDimensions.ts:1`; torch `briefs/_markings.md`, SCALE.

An optional far-zoom aid may enlarge small rendered units.
It must not alter collision, range, movement, cargo capacity, or simulation coordinates.
The camera must still allow navigation at genuine fleet scale.
Current render dimensions and the readability hook do not prove that every collision envelope uses the true footprint.
Source: `G:src/harness/GameHost.ts:153`.

Terrain needs finer subdivision than the older coarse blocks.
The owner requested at least sixteen sub-blocks, ideally sixty-four, and challenged the non-square subdivision.
A pathfinding cell size alone does not satisfy that visual and terrain requirement.
Source: `G:session-transcripts/transcript.jsonl:654`.

## 17. Patrol, escort, and repair — IMPLEMENTED within stated scope

Patrol can use a point or a friendly or neutral unit as its moving center.
Unit-bound patrol follows the target's updated position.
Escort keeps deterministic formation slots around a friendly target.
Aircraft, ships, and ground escorts use different offsets appropriate to their movement.
Ordinary move, attack, stop, and construction orders replace those assignments.
Blocked routes remain possible; an accepted order does not prove arrival.
Sources: `G:src/gameplay/tacticalOrders.ts:200`; `G:src/gameplay/tacticalOrders.ts:277`; `G:src/gameplay/aircraftOps.ts:127`.

Repair specialists can receive a repair assignment.
Eligible tank crews can perform a limited field patch after eight quiet seconds and three preparation seconds.
One order restores at most fifteen percent of maximum health at two percent per second.
Starting health determines a ninety-percent or seventy-percent ceiling; damage below thirty-five percent requires a specialist.
The crew action has a sixty-second cooldown and requires the tank to remain stationary and out of combat.
Sources: `G:src/gameplay/tacticalOrders.ts:54`; `G:src/gameplay/crewRepair.ts:8`.

## 18. Weather, water, and battlefield engineering — PARTIAL

Weather can alter laser efficiency, river danger, and engineering conditions.
Local weather and fording code has an active update path.
Hazard thresholds differ for infantry, wheeled vehicles, D9s, and heavy vehicles.
Its three-second exposure grace belongs to that hazard system, not the deep-water death rule.
Sources: `G:src/main.ts:1997`; `G:src/gameplay/weatherAndFording.ts:111`; `G:src/gameplay/weatherAndFording.ts:136`.

Dredging changes water access but must respect dangerous currents and protected flotilla obstruction.
Current current-limit cancellation does not implement the contract's separate pause-and-resume flotilla behavior.
Forecasts need deterministic, recorded inputs and a clear HUD forecast window.
Forecast files in another runtime do not prove active browser integration.
Sources: `G:src/gameplay/weatherAndFording.ts:1236`; `N:CONTRACTS.md:285`; `N:golden/baseline/ts/weatherForecast/`.

## 19. Capture, tribunals, and chickie rescue — PARTIAL

The intended detainee chain is surrender, securing, collection, airlift, carrier transfer, orbital transfer, and tribunal adjudication.
The beta design includes collection batches, V-22 transport, Sea Dragon orbital launch, and a separate Penguin cryogenic path.
Evidence comes from living captives and adjudication, not kills renamed as intelligence.
Rewards must occur once and preserve ownership and protected-person consequences.
This chain remains **DESIGNED-ONLY** in the active main match.
Ordinary damaged-structure capture is a separate implemented action.
Sources: `G:beta/src/gameplay/captureOperations.ts:58`; `G:beta/src/gameplay/captureOperations.ts:140`; `G:src/gameplay/expandedMechanics.ts:798`.

Chickies are captives in guarded sanctuaries.
Rescue removes the Directorate's borrowed authority and triggers surrender, golden effects, and a fanfare.
The lore requests JSLC +40 and lawfare refutation.
The gain cap still applies unless an approved contract change grants an exception.
Sources: `N:design/PENGUIN_AND_CHICKIE_LORE.md:54`; `N:CONTRACTS.md:54`; `G:session-transcripts/transcript_full.jsonl:585`.

Current local main spawns a sanctuary against Penguins and checks for any living player-zero entity within 130 range.
That proximity can trigger victory and zero Penguin legitimacy.
It does not establish a guarded infantry rescue, a +40 sink event, or dossier delivery.
No chickie-killing objective is permitted.
Source: `G:src/main.ts:1958`; `G:src/main.ts:2025`.

## 20. Campaign, chronology, and mission design — PARTIAL

The normative campaign has three acts and a late branch.
Its chapter sequence remains authoritative despite different authored map numbers.

| Canonical chapter | Purpose | Authored content relationship |
|---|---|---|
| Act I, Map 1: Diego Abyss | Learn the undersea base and fleet operation. | `camp-00a-diego-garcia-abyss` and `camp-00b-diego-garcia-ascension` split the tutorial. |
| Act I, Map 2: Shorehead | Execute a contested landing. | `operation-shorehead` currently depicts defense and repair; the landing beat needs reconciliation. |
| Act I, Map 3: Amphibious Thrust | Establish and hold a beachhead. | The authored amphibious mission supplies much of this lesson. |
| Act II, Map 4: Blue Aurora | Resolve four-phase mast and elevator locks. | The prequel elevator and new harbor exercise do not establish this chapter's placement. |
| Act II, Map 5: Kharg | Attack the resource network under lawfare pressure. | Kharg Island supplies the branch point; preceding naval maps can serve as supporting operations. |
| Act III: southern Iran or south Yemen | Choose a conventional inland campaign or a naval campaign. | Bushehr–Zagros–Shiraz or Socotra–Aden–Bab al-Mandeb. |

Source: `N:CAMPAIGN.md:3`.

The game catalogue contains eighteen campaign map assets with objectives and prebuilt forces.
The manual describes each asset without pretending that the whole sequence is playable.
Only the Shorehead procedural adaptation has an established current launch path.
Painted authored terrain remains unsupported by that ordinary runtime.
The campaign director handles bound objectives; persistent progression and save checkpoints remain unfinished.
Sources: `G:src/gameplay/CAMPAIGN.md:7`; `G:src/gameplay/campaignRuntime.ts:16`; `G:src/content/maps/mapManifest.ts:6`.

The latest Shorehead opening holds player combat units until a move or attack order releases them.
The raid starts farther away, and guards defend the relay.
The adaptation retains its authored objectives and incomplete terrain boundary.
Sources: `G:src/gameplay/missionEngagement.ts:13`; `G:src/gameplay/mapLoader.ts:171`.

Tutorials must introduce one operational dependency before combining several.
The fleet sequence must show why the player needs resupply ships, LCACs, air cover, and repair.
Mission bonuses can reward force preservation without replacing required objectives.
Sources: `G:session-transcripts/transcript.jsonl:2452`; `G:src/gameplay/CAMPAIGN.md:22`.

## 21. Skirmish, map catalogue, and tower defense — PARTIAL

The catalogue has nine faction-oriented 1v1 maps: three per faction.
It also has three four-player, three six-player, three eight-player, and three tower-defense maps.
Together with eighteen campaign maps, these make 39 canonical entries.
Two additional legacy files do not create two new canonical maps.
Catalogue counts do not establish launchability, expansion balance, or network capacity.
Sources: `G:src/content/maps/mapManifest.ts:6`; `G:session-transcripts/transcript.jsonl:2434`; `G:session-transcripts/transcript.jsonl:2444`.

Skirmish needs defensible starts, finite nearby deposits, contested expansion sites, readable crossings, and meaningful approach choices.
Difficulty should alter AI decisions and disclosed rules, not silently change the player's controls.
Tower defense needs a wave director, build periods, loss conditions, and its own mode entry.
The three map files and a beta director do not establish that mode in current main.
Source: `G:beta/src/main.ts:157`.

## 22. Multiplayer, replay, and simulation authority — PARTIAL

The present multiplayer implementation uses an HTTP authority with a nominal twenty updates per second.
Players own separate armies in free-for-all or team matches.
Static hosting alone does not supply the match service.
Rooms are in memory; restart and lost session credentials affect continuity.
No live multiplayer acceptance occurred in this review.
Source: `G:MATCHES.md:20`.

The normative simulation uses fixed thirty-Hz steps and seeded Mulberry32 streams.
String seeds use FNV-1a over UTF-16 code units.
The named streams include PR, logistics, weather, capture, patron, gunship, convoy, lawfare, flotilla, and shield.
Source: `N:CONTRACTS.md:37`.

The active local browser still uses a TypeScript Sim and an elapsed-time loop.
It is not the completed C++ migration described by `N:ENGINE.md`.
A common command order, complete saved state, seeded effects, and independent parity evidence remain necessary.
Frame-only checksums cannot prove matching future gameplay state.
Sources: `G:src/harness/GameHost.ts:43`; `jc/docs-jpd2:docs/planning/technical/DETERMINISM.md:8`.

## 23. UI, HUD, and input — PARTIAL

The game remains the main view.
Briefing gives the premise; Intel gives play instructions; Factions gives the roster and technology explorer.
Project implementation status belongs in the project area, not a public game instruction panel.
Navigation must use the current canonical game and hide retired variants.
Authority: torch `briefs/rl02.md`.

The HUD prioritizes selection, resources, power, orders, production, objective progress, and threats.
PR needs both meters, gain-cap feedback, incident reasons, and an explicit orbital jurisdiction badge.
Lawfare needs a warning and rebuttal timer.
Flotilla UI needs resolve, flagship immunity, tow state, and halted dredge progress.
Aircraft need fuel bars, home-base status, bingo warnings, and clear crash attribution.
Sources: `N:ui/hud_layouts.md`; `G:src/gameplay/aircraftOps.ts:230`.

Menus and sidebars use semitransparent overlays and grey general accents.
Semantic danger, faction, and jurisdiction colors remain meaningful.
Avoid node title bars and duplicate navigation chrome.
Phone targets need usable touch areas; desktop and phone layouts require separate observation.
Authority: torch `briefs/_rules.md:29`; `N:ui/tokens.md`.

Phone selection persists until an explicit selection or order-mode change or Unselect.
An enemy tap orders a formation attack at the slowest selected speed.
A friendly, neutral, or terrain tap orders movement.
Enemy hit regions extend twenty-five percent beyond the boundary unless overlap requires disambiguation.
Two-finger pan and pinch must not issue combat orders.
Sources: `G:session-transcripts/transcript.jsonl:2033`; `G:src/input/pointer.ts:267`; `G:src/input/pointer.ts:360`.

## 24. Art direction and markings — PARTIAL

Art must communicate platform identity at real relative scale.
Ford, Wasp, Burke, Seawolf, and Sa'ar cannot share a generic ship silhouette with different labels.
The requested acceptance includes outline comparison and perceptual distinctness.
No screenshot or silhouette acceptance was performed for this document.
Sources: `G:docs/generals2_scale_and_art_direction.md`; torch `briefs/_markings.md`, QUALITY.

The JSL aircraft roundel uses a blue `#0038B8` disc and a thin white ring.
Its white filled-band Magen David retains blue negative space.
Fixed-wing aircraft carry six positions: both fuselage sides and the upper and lower surfaces of both wings.
Helicopters carry both fuselage positions.
Ships, flags, structures, and appropriate UI use the JSL ensign, not a plain Israel flag.
Infantry use the prescribed patches.
The tracked marking masters are the source; do not redraw an approximation.
Authority: torch `briefs/_markings.md`; master family `eretz/yisrael/master/01_assets_markings`.

The present roster contains marking rules, but textual rules do not prove the rendered assets comply.
The asset pipeline must verify correct placement, contrast, and prohibited cross-faction use.
Source: `G:src/content/classicRoster.ts:42`.

## 25. Acceptance and source disagreements

The notes golden tree contains 326 JSONL files: 311 baseline files and fifteen new cases.
The baseline files use empty states, `noop`, and empty expectations.
Their names describe intended coverage; their count does not prove conformance.
The manifest lists ten new cases and omits `new/` from paths that require it.
Sources: `N:golden/MANIFEST.json`; `jc/docs-jpd2:docs/planning/technical/GOLDEN_VECTOR_PROTOCOL.md:6`.

The release needs meaningful immutable vectors, an identified oracle, complete state and event comparisons, and independent review.
Do not regenerate accepted fixtures from empty wrappers.
No suite ran in this documentation lane.

| Conflict | Required disposition |
|---|---|
| REV-001 forbids weapon locks; CONTRACTS §6.3 requires a freeze. | Preserve the contract baseline; obtain an explicit contract change before replacing it. |
| Lore awards +40; the common gain ceiling is +25 per sixty seconds. | Route rescue through the sink; require a contract exception for any bypass. |
| Notes ENGINE claims complete migration; browser imports TypeScript. | Describe the active runtime from source and the C++ line as a candidate. |
| New player-controlled laser charge versus incomplete common jurisdiction. | Preserve manual firing and extend immunity and PR consequences across the full power catalogue. |
| Five canonical campaign beats versus eighteen numbered assets. | Approve a chapter-to-map crosswalk without silently moving Blue Aurora. |
| Short Aurora lift versus fleet-scale harbor transfer. | Keep scenario contracts separate until an explicit integration decision. |
| Existing guide says routine fuel is absent. | Replace that stale claim with scoped aircraft fuel and basing instructions. |
| Guardian Carrier is described as both ship and ground transport. | Resolve the asset identity before teaching it as a naval platform. |

The parallel owner-intent ledger initially used the older `51e705d5` game snapshot.
This document retains its terrain and unresolved asset findings, while incorporating the later AoI-label fix, aircraft work, and production sidebar.
It also verifies the core veterancy damage and health multipliers directly.
It does not copy that ledger's unverified historical absences into current claims.

## 26. Implementation status ledger

Each row counts once. Section headings do not add counts.
Evidence points to the source or normative requirement that defines the row's scope.

| ID | Item and scope | Status | Evidence / remaining boundary |
|---|---|---|---|
| S01 | Premise and institutional satire | PARTIAL | `G:src/explainer/data/factions.ts:8`; mechanics do not yet carry every theme. |
| S02 | Distinct faction rosters and consistent AoI identity | PARTIAL | `G:src/content/classicRoster.ts:52`; AoI label fixed, full faction mechanics remain incomplete. |
| S03 | Asymmetric tunnel, defense, and powered warp production | PARTIAL | `G:src/main.ts:2046`; spawn bonuses do not complete the system. |
| S04 | Core loop and mode-specific victory | PARTIAL | `G:src/gameplay/CAMPAIGN.md:22`; mode contracts remain uneven. |
| S05 | Finite economy and expansion | PARTIAL | `G:vendor/cnc2d/game/src/core/sim.ts:2049`; passive income and map acceptance remain. |
| S06 | Construction prerequisites and expanded per-producer queues | IMPLEMENTED | `G:src/gameplay/expandedMechanics.ts:205`, `:528`; source scope only. |
| S07 | Seven-tab production sidebar and primary factories | PARTIAL | `G:src/ui/productionSidebar.ts:83`; cameos, specific errors, remote rallies, and shortcut conflicts remain. |
| S08 | Unified power and faction power dependencies | PARTIAL | `G:vendor/cnc2d/game/src/core/sim.ts:1866`; Penguin and weather integration remain. |
| S09 | Base combat, expanded actions, and damage coverage | PARTIAL | `G:src/gameplay/expandedMechanics.ts`; catalogue coverage is incomplete. |
| S10 | Mandatory lethality and jurisdiction tags | DESIGNED-ONLY | `N:CONTRACTS.md:68`; active power schema lacks the fields. |
| S11 | Friendly and allied area damage | IMPLEMENTED | `G:src/gameplay/friendlyFire.ts`; blast scope. |
| S12 | Veterancy across every damage path | PARTIAL | `G:vendor/cnc2d/game/src/core/sim.ts:1968`; expanded kill credit remains. |
| S13 | Earned commander promotion choices | PARTIAL | `G:src/main.ts:168`; rank and counter exist, spending menu unobserved. |
| S14 | Single PR sink, cap, and ownership | PARTIAL | `N:CONTRACTS.md:54`; direct writes remain in active main. |
| S15 | REV-001 friction under an approved common policy | PARTIAL | `N:CONTRACTS.md:246`; freeze and cooldown conflicts remain. |
| S16 | Protected UN convoy contract in active matches | DESIGNED-ONLY | `N:CONTRACTS.md:189`; candidate source is not active-match proof. |
| S17 | Protected structures, caches, and evidence contract | DESIGNED-ONLY | `N:CONTRACTS.md:217`; complete active path unobserved. |
| S18 | Lawfare director and rebuttal HUD | DESIGNED-ONLY | `N:CONTRACTS.md:246`; complete active path unobserved. |
| S19 | Flotilla, nonlethal clearance, and first-hit consequence | DESIGNED-ONLY | `N:CONTRACTS.md:285`; complete active path unobserved. |
| S20 | Strategic catalogue effects and gates | PARTIAL | `G:src/gameplay/superweaponRuntime.ts:105`; player-controlled laser fixed, full catalogue coverage remains. |
| S21 | Contract-wide orbital jurisdiction immunity | PARTIAL | `G:src/gameplay/laserCharge.ts:45`; local charge immunity exists, typed catalogue-wide integration remains. |
| S22 | Fleet roles, cargo, and replenishment | PARTIAL | `G:src/gameplay/expandedRoster.ts:175`; full complements and service coverage remain. |
| S23 | Stern well-deck launch and recovery | IMPLEMENTED | `G:src/gameplay/navalAmphibious.ts:326`; compatible actual craft. |
| S24 | Deep-water ground-unit sinking | IMPLEMENTED | `G:vendor/cnc2d/game/src/core/sim.ts:828`; protected mechanic. |
| S25 | Full undersea base and campaign integration | PARTIAL | `G:docs/design/DIEGO_GARCIA_UNDERSEA_BASE.md:111`; exercise and architectural limits. |
| S26 | Harbor lift tickets, staging, and reserved destination | IMPLEMENTED | `G:src/gameplay/diegoGarcia.ts`; separate exercise scope. |
| S27 | Fixed-wing motion and rotary hover fuel | IMPLEMENTED | `G:src/gameplay/aircraftOps.ts:411`; recognized airborne aircraft. |
| S28 | Basing, capacity, diversion, bingo, and crash ownership | PARTIAL | `G:src/gameplay/aircraftOps.ts:367`; legacy and spawn-path coverage remains. |
| S29 | Host-synchronized fuel-capacity options | IMPLEMENTED | `G:src/match/launcher.ts:42`; finite and infinite settings. |
| S30 | True scale, footprints, and optional readability aid | PARTIAL | `G:src/content/unitDimensions.ts:1`; collision and visual acceptance remain. |
| S31 | Unit-bound patrol and deterministic escort | IMPLEMENTED | `G:src/gameplay/tacticalOrders.ts:277`; source path includes local and server use. |
| S32 | Assigned specialists and limited tank crew repair | IMPLEMENTED | `G:src/gameplay/crewRepair.ts:8`; eligible units only. |
| S33 | Weather, fording, dredging, and forecast integration | PARTIAL | `G:src/gameplay/weatherAndFording.ts:111`; common event integration remains. |
| S34 | Full detainee transport and tribunal chain | DESIGNED-ONLY | `G:beta/src/gameplay/captureOperations.ts:58`; active main path unobserved. |
| S35 | Guarded chickie rescue and political consequences | PARTIAL | `G:src/main.ts:2025`; current proximity shortcut lacks the complete rescue. |
| S36 | Campaign acts, authored terrain, objectives, and progression | PARTIAL | `G:src/gameplay/CAMPAIGN.md:7`; only Shorehead adaptation has an established path. |
| S37 | Required skirmish map catalogue | IMPLEMENTED | `G:src/content/maps/mapManifest.ts:6`; file counts, not playability. |
| S38 | Tower-defense mode on active main | DESIGNED-ONLY | `G:beta/src/main.ts:157`; three map assets alone are insufficient. |
| S39 | Multiplayer rooms and release-grade continuity | PARTIAL | `G:MATCHES.md:20`; live service and recovery unverified. |
| S40 | Fixed-step determinism, replay, and C++ parity | PARTIAL | `N:CONTRACTS.md:37`; active TypeScript and twenty-Hz server differ. |
| S41 | Sticky phone selection and contextual orders | IMPLEMENTED | `G:src/input/pointer.ts:267`; source behavior, not device acceptance. |
| S42 | Complete HUD and current content navigation | PARTIAL | `N:ui/hud_layouts.md`; production and political state visibility remain. |
| S43 | Distinct platform art and prescribed markings | PARTIAL | Torch `briefs/_markings.md`; no visual acceptance performed. |
| S44 | Required finer terrain subdivision | DESIGNED-ONLY | `G:session-transcripts/transcript.jsonl:654`; requested subdivision not established. |
| S45 | Meaningful golden evidence and release acceptance | PARTIAL | `N:golden/MANIFEST.json`; empty baseline expectations cannot certify behavior. |
