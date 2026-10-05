# STRICT AGENT INSTRUCTIONS FOR JSLCNC

**READ THIS IMMEDIATELY BEFORE EXECUTING ANY CODE, DESIGN, OR ARCHITECTURE TASKS ON THIS REPOSITORY.**

## 1. ABSOLUTE COMPLIANCE
You are reading the master constraints for the JSLCNC (Joint Special Logistics Command and Conquer) project. You are **FORBIDDEN** from hallucinating new features, shifting the tone, breaking the asymmetric balance, or implementing classic "health-bar RTS" tropes that violate the game's core design.

## 2. THE HOLY TEXTS
You must read and strictly adhere to the following two documents before proceeding with any work:
1. `JSLCNC_BIBLE.md`: Contains the engine schema (SAGE C++ Wasm), faction asymmetry (JSLC, AoI, Penguins), the logistics system, the PR/Lawfare tug-of-war, and the visual damage states.
2. `CAMPAIGN_INSTRUCTIONS.md`: Details the rigid 18-map progression for JSLC, the 1-minute wipeout campaign for AoI, and the branching logic.

## 3. ENGINE REALITIES
- **DO NOT** attempt to write TypeScript simulation logic. We have officially pivoted to the C++ SAGE Engine compiled to WebAssembly. The engine is driven entirely by `sage/data/INI/` configurations.
- **DO NOT** break SAGE pathfinding. (Read the "Flotilla Anchoring" displacement phase fix in the Bible).
- **DO NOT** implement traditional UI health bars as the primary visual. They are an *optional toggle*. The primary health indicator is 3D visual damage (e.g., sparkling mechanical pods vs. mobile scrap fires).

## 4. TONE & LORE
- This is a satirical, asymmetric military-techno RTS. Do not soften the tone, but do not cross the line into ethnic/religious stereotypes.
- The mechanics *must* reflect the bureaucratic and PR nightmares of modern asymmetric warfare (e.g., UN truck escorts, Diplomatic Distractor AI freezing ROEs, "Splash-Bait" flotilla shielding).

## 5. FUCKING UP IS IMPOSSIBLE IF YOU FOLLOW THIS
If you attempt to deviate from the `JSLCNC_BIBLE.md` or soften the mechanics, your changes will be rejected. Execute the vision exactly as it is laid out in the documentation.
