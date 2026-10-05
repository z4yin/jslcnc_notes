# JSLCNC: OFFICIAL CAMPAIGN & MAP BRANCHING INSTRUCTIONS

## Overview
This document serves as the master blueprint for the single-player campaign progression in JSLCNC. It details the 18-map progression, objective triggers, and branching logic.

## 1. The AoI Campaign
As mandated by the JSLCNC Bible, the AoI campaign is a single, one-minute level. 
*   **Map 1: The Uprising**
    *   *Trigger:* 60 seconds after mission start.
    *   *Event:* JSLC air drops weapons into the region. A massive popular rebellion triggers. The player's base is completely overrun by the local populace demanding voting rights.
    *   *Result:* Campaign over (Forced Defeat/Narrative Victory).

## 2. The JSLC Campaign (The 18-Map Progression)
The JSLC campaign is a sprawling 18-map progression focusing on dismantling the AoI network, managing logistics, and surviving international lawfare.

### Act I: The Kharg Island Incursion
*   **Map 1-3: Beachhead & Establishment**
    *   *Objectives:* Secure supply lines, establish Mega-HAS shelters, and defend against early AoI drone swarms.
    *   *Triggers:* "Rescue" - Escort downed pilots via CSAR before PR penalties apply.
*   **Map 4: The Kharg Island Nexus**
    *   *Objectives:* Dismantle the primary shipping hub.
    *   *Branching Point:* Depending on the player's PR score and kinetic collateral at the end of Map 4, the campaign branches into either the **Iran Offensive** (Aggressive/Low PR) or the **Yemen Interdiction** (Surgical/High PR).

### Act II (Branch A): The Iran Offensive
*   **Map 5A-9A: Deep Strike**
    *   *Objectives:* Heavy kinetic warfare. Destroy IRBM silos and underground tunnel networks.
    *   *Triggers:* "Disarm Timer" - Player has exactly 15 minutes to disarm WMDs before launch. The Diplomatic Distractor AI (Albanese) is highly active here, attempting to freeze ROE during critical strikes.

### Act II (Branch B): The Yemen Interdiction
*   **Map 5B-9B: Surgical Control**
    *   *Objectives:* Escort UN trucks (preventing AoI siphoning) and secure naval chokepoints.
    *   *Triggers:* "Escort" - Protect neutral convoys. If AoI successfully tethers to a truck for 60 seconds, the mission fails.

### Act III: The Blue Aurora Elevator
*   **Map 10-17: Convergence**
    *   *Objectives:* Both branches converge back for the final push towards the primary AoI stronghold.
*   **Map 18: The Blue Aurora Defense**
    *   *Objectives:* Defend the Blue Aurora Space Elevator (and the Diego Garcia undersea infrastructure) from a massive, coordinated AoI and Directorate (Penguin) assault.
    *   *Phases:* 
        *   Phase 1: Naval bombardment defense using Iron Dome/David's Sling.
        *   Phase 2: Counter-stealth operations against Directorate Ghost Infiltrators.
        *   Phase 3: Secure the orbital tether to call in the final JSLC Orbital Transport reinforcements for the decisive push.

## 3. The Directorate (Penguins) Campaign
*Note: Scheduled for later development.*
*   Focuses on manipulating the JSLC-AoI conflict, cyber-warfare, and securing Fulgurite EMP tech.

---
*This document works in tandem with `JSLCNC_BIBLE.md` to guide the mapping and scripting teams.*
