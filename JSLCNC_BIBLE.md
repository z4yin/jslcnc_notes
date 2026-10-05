# JSLCNC: THE UNIFIED ARCHITECTURE & GAME BIBLE

## 1. CORE VISION & DESIGN PHILOSOPHY
JSLCNC is an asymmetric, satirical military-techno RTS. The game operates on two distinct but interlocking victory axes: **Kinetic Warfare** (destroying the enemy) and the **Information/Lawfare War** (managing Public Legitimacy and international PR). The game is designed to reflect the brutal, bureaucratic realities of modern asymmetric conflict.

**Golden Rule:** The UI should get out of the way. We rely on the physical 3D battlefield to communicate game state (e.g., visual vehicle damage, smoking rigs) whenever possible, though classic RTS UI elements remain available.

## 2. ENGINE ARCHITECTURE (SAGE WASM)
We are leveraging the recently open-sourced **SAGE Engine** (GPLv3), compiling the C++ Simulation Core into WebAssembly (Wasm) to run inside the web browser. 
*   **Networking:** Lockstep Multiplayer protocol. Fixed-point deterministic math with a stagger-handshake (Ready -> Lock -> Start) and rollback buffer to prevent desyncs.
*   **Rendering:** SAGE WebGL Viewport running at 60 FPS, with the Sim Loop operating at a strict 30 Hz.

## 3. FACTIONS & ASYMMETRY
1.  **JSLC (Joint Special Logistics Coalition):** High-tech, bureaucratically shackled, heavily reliant on complex supply chains.
    *   *Visual Language:* Pristine mechanical states degrading to dead, sparking pods. 
    *   *Mechanics:* Must maintain Ammo, Fuel, and Spare Parts. Bound by strict Rules of Engagement (ROE).
2.  **AoI (Axis of Intifada):** Low-tech, highly adaptable, operates using civilian shielding and subterranean networks.
    *   *Visual Language:* Catastrophic visual junk, wobbling suspensions, mobile scrap fires.
    *   *Mechanics:* Uses hijacked UN convoys, PR exploitation, and cheap drone swarms.
3.  **Penguins (The Directorate):** Advanced black-ops/crypto faction.
    *   *Mechanics:* High-tier cyber warfare, EMPs, Fulgurite strikes, and heavy stealth (Ghost infiltrators).

## 4. LAWFARE & PUBLIC LEGITIMACY (PR WAR)
*   **The PR Meter:** A tug-of-war meter representing Legitimacy. Falling too low triggers international embargoes, ROE freezes (blocking heavy ordnance), and spawns flotilla blockades.
*   **The Diplomatic Distractor:** An adversarial AI (e.g., Francesca Albanese) issues condemnations, draining PR when kinetic tempo in UN zones is too high.
*   **Counter-Play:** Releasing ISR drone footage, capturing HVTs for tribunal dossiers, and surgical strikes.

## 5. LOGISTICS & THE LIFEBLOOD SYSTEM
Every JSLC unit is bound to a logistics tether.
*   **Fuel & Ammo:** Consumed during movement and combat. Empty units are suppressed or stalled.
*   **Mechanical Reliability:** Degrades over time. Requires D9/SCV triage repair.
*   **Supply Lines:** C-130 drops, Naval UNREP (Underway Replenishment), and Mega-HAS (Hardened Aircraft Shelters) are required to keep the war machine running.

## 6. ASSET PIPELINE
*   **3D Models:** W3D hierarchy. Damage states are baked directly into the bone structure to minimize UI clutter. 
*   **Textures & Maps:** High-res texture packs upscaled from vanilla SAGE assets using World Builder. Key maps include the Diego Garcia undersea base and dense Urban Centers (Mosul/Raqqa layout).

## 7. UI/UX DIRECTIVE
The original UI has been condemned. We are pursuing a complete tear-down and rebuild.
*   **Inspiration:** The new UI will heavily borrow from modern open-source RTS projects (OpenRA, Beyond All Reason, OpenSAGE) to ensure clean affordances, minimal screen clutter, and logical user flows. 
*   **Classic C&C Fundamentals:** While we use visual damage telegraphs, **UI unit health bars MUST remain available as a toggleable option.** Additionally, clicking on a unit must immediately identify it and display its stats/status in the UI, exactly as it functioned in classic Command & Conquer.
*   **Presentation:** Dark, modern military-HUD aesthetic (Cobalt Palette). Minimalist, data-driven, and intuitive.

## 8. CAMPAIGNS & STORYLINES
*   **JSLC Campaign:** A multi-stage operational tour dealing with restrictive ROEs, logistical nightmares, and international lawfare while dismantling subterranean networks and defending key assets (like the Diego Garcia undersea base).
*   **AoI Campaign:** Consists of exactly one level. One minute after the mission starts, JSLC air drops weapons into the region. A massive popular rebellion immediately breaks out, and the people—deciding to overthrow the rulers that haven't allowed them to vote for 20 years—completely wipe out the player's base. Campaign over.
*   **Penguins (The Directorate) Campaign:** A full, conventional RTS campaign spanning global black-ops, cyber-warfare, and stealth strikes. *Note: This campaign is fully laid out in the lore but is scheduled to be built last.*

---
*This document serves as the absolute source of truth for all engineering, design, and art decisions moving forward. Any deviation requires a formal amendment to this Bible.*


## 9. EXPLOIT PATCHES & BALANCING (RED-TEAM AMENDMENTS)
Based on Astra's formal Red-Team audit, the following mechanical patches are integrated to prevent competitive griefing:
*   **"Splash-Bait" Invincibility Fix:** If an AoI unit fires kinetic weapons from within a Flotilla's radius, the `PROTECTED_CIVILIAN` PR-wipeout shield is immediately stripped from those vessels, rendering them legal collateral. 
*   **"Parasite" Siphon Fix:** AoI units attempting to siphon a neutral UN truck must deploy a stationary tether, halting the truck. Additionally, a JSLC unit within 60 units of the truck projects an "Escort Aura" that disables siphoning entirely.
*   **SAGE Engine Pathfinding Fix (Flotilla Anchoring):** To prevent SAGE pathfinding soft-locks when a flotilla anchors, a 2-second displacement phase forces any overlapping JSLC naval units to slide outside the boundary before the impassable `FLOTILLA_BLOCK` mesh is enforced.
*   **Orbital Jurisdiction Loophole Fix:** Orbital strikes are no longer a free late-game win condition. While immune to standard ROE freezes, excessive orbital strikes during lawfare escalations incur severe, escalating PR drain multipliers.
