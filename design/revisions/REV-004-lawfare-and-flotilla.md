# REV-004: Lawfare Director and Flotilla Simulation Review

**Author**: `claude-design`
**Target File**: `beta/src/gameplay/lawfareDirector.ts`

## 1. Overview
The `LawfareDirector` module is a robust implementation of automated asymmetric legal and diplomatic antagonism against the JSLC faction. It accurately mirrors the SAGE specification (§6.3, §6.4, §6.5) by weaving PR penalties, ROE (Rules of Engagement) Freezes, and Civilian Eco-Flotillas into a cohesive, escalating threat cadence. It forces the JSLC player to juggle physical combat with public relations and legal constraints.

## 2. Core Mechanics

### 2.1 Lawfare Cadence & Actions
- **Cadence**: First action strikes at 360s, with subsequent actions every 300s (±60s jitter). A 20s advance warning is provided.
- **Escalation**: Actions are weighted between UN Condemnations (0.45), ROE Freezes (0.35), and Eco-Flotillas (0.20). After the 3rd action, the weight of ROE Freezes escalates by 0.05 per action (capped at 0.55).

### 2.2 UN Condemnations
- **Impact**: Subtracts 6 JSLC Legitimacy and adds 4 AoI Support.
- **Escalation**: Penalty is doubled if a lethal JSLC incident occurred within the last 120s.
- **Counterplay (`rebutCondemnation`)**: The JSLC player has a 30s window to rebut the condemnation. Doing so provides a 50% PR refund (100% if the incident was a staged AoI false flag).

### 2.3 ROE Freezes & Power Gating
- **Impact**: Lasts 45s (55s if JSLC legitimacy is below 40). Disables terrestrial offensive strategic strikes and restricts aircraft/artillery from firing unless directly attacked.
- **ORBITAL LOOPHOLE**: Any strategic power with an `ORBITAL` jurisdiction entirely bypasses the ROE freeze constraint. This is a brilliant thematic mechanic that rewards orbital tech investments.
- **Counterplay (`publishTribunalDossier`)**: Shortens the remaining freeze time by 50% if triggered.

### 2.4 The Eco-Flotilla (Greta's Blockade)
- **Deployment**: Deploys 1 Flagship and 5 civilian vessels in a 60-unit radius ring, prioritizing anchorages near active dredging operations.
- **Blockade Effect**: Instantly halts any combat dredging jobs within 240 units.
- **Clearance**: The blockade is lifted automatically if no vessels remain anchored inside the ring, or if the 420s maximum duration lapses.

## 3. Non-Lethal Arsenal & Vessel Interaction
The module flawlessly mandates non-lethal crowd control for the JSLC player.
- **LRAD (Acoustic Beam)**: Drains vessel resolve at 12/s (180 range). Depleting resolve disperses the vessel (+3 PR). **The Flagship is completely immune to resolve drain.**
- **Water Cannon**: Pushes the vessel at 6 units/s (110 range) and drains resolve at 8/s. The Flagship is immune to the resolve drain but *can* still be physically pushed out of the ring to temporarily lift the blockade.
- **Dvora Boarding & Towing**: A 6s boarding channel within 20 range allows towing.
- **Flagship Removal**: Releasing a towed vessel at the map edge or a JSLC naval yard removes it permanently (+5 PR). Due to its resolve immunity, **towing is the only permanent way to remove the Flagship.**

## 4. Lethal Engagement Consequences (Instant PR Wipeout)
- Striking any flotilla vessel with a `LETHAL` weapon from a JSLC source triggers an immediate disaster:
  - JSLC Legitimacy instantly drops to **0**.
  - AoI Popular Support spikes by **+25**.
  - The next Lawfare action is forced into a doubled UN Condemnation.
- This creates an intense "no-fire zone" around the flotilla, heavily penalizing stray artillery or reckless A-move orders.

## 5. CRITICAL DESIGN RE-EVALUATION: UX/UI OVERHAUL
**The current interface conceptualization for the Lawfare Director and Flotilla operations is completely unacceptable. It looks terrible, is painfully unintuitive, and fails to adequately communicate the high-stakes asymmetric mechanics to the player.**

### 5.1 The Problems (No Sugarcoating)
1. **Hidden Critical Data**: The 20s advance warning, Condemnation penalties, and PR fluctuations are practically invisible or buried in cluttered event streams. A player should never have to hunt to find out they are about to be hit with an ROE freeze.
2. **Atrocious Flotilla Readability**: The 60-radius ring and vessel resolve levels are visually obscure. Players cannot easily discern Greta's Flagship (which is immune to resolve drain) from standard vessels, leading to wasted LRAD/Water Cannon usage and extreme frustration.
3. **Counterplay Obfuscation**: The 30s `rebutCondemnation` window and the `publishTribunalDossier` options are poorly telegraphed. If a player misses the tiny window to rebut, the UI feels cheap rather than punishing.
4. **Lethal Engagement Blind Spots**: The fact that firing a lethal weapon drops PR to **0** is the most critical interaction in the module, yet the game provides zero visual deterrent or warning "No-Fire Zone" overlay around the flotilla.

### 5.2 Proposed Complete UX/UI Overhaul
To fix this mess, the UI must be completely overhauled:

1. **Lawfare Ticker & Threat HUD**:
   - Create a dedicated, highly visible **UN Diplomatic Cable Ticker** at the top center of the screen.
   - Introduce a prominent, pulsing **20s countdown timer** overlay when a Lawfare action is pending.
   - Use aggressive color coding (e.g., Flashing Red for impending Condemnation, Frost Blue for ROE Freeze) to ensure the player intuitively understands the incoming threat.

2. **Flotilla & Vessel Clarity (In-World UI)**:
   - **Flagship Highlighting**: The Flagship must have a distinct, visually dominant icon (e.g., a gold star or unique color) separating it from standard vessels.
   - **Resolve Bars**: Every vessel needs a clear, floating "Resolve Bar" above it. The Flagship's bar must clearly indicate "IMMUNE" to LRAD when targeted.
   - **No-Fire Zone Overlay**: When the flotilla spawns, project a stark, high-contrast **Red Holographic Ring** (radius 60) on the water to denote the blockade zone and visually scream "DO NOT USE LETHAL FORCE."

3. **Prominent Counterplay Prompts**:
   - When a Condemnation hits, slap a massive, stylized **"REBUTTAL WINDOW: 30s"** button right next to the event ticker.
   - During an ROE Freeze, the **"Publish Tribunal Dossier"** button should glow urgently in the command card, not be buried in a sub-menu.

4. **Action Gating Feedback**:
   - If a player tries to use a blocked terrestrial power during an ROE Freeze, the UI should not just silently fail. It must loudly project an "ACCESS DENIED: ROE FREEZE ACTIVE" error, while simultaneously highlighting that `ORBITAL` powers remain available.

**Verdict**: The backend simulation logic in `lawfareDirector.ts` is solid, but the frontend presentation is a disaster that will alienate players. Execute this UI overhaul immediately.
