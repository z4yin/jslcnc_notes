# UI Readability Review

**Owner:** claude-design (Presentation Lane)
**Target:** SAGE C++ Migration, §6 New Systems

This document tracks the moment a player has to decide on an action, what the UI shows at that moment, and verifies whether it's enough to inform their decision according to the `CONTRACTS.md` rules.

## 1. UN Aid Convoys and Hijacking (§6.1)

*   **Decision Moment:** Player sees a UN truck and must decide whether to attack it, tag it with ISR, or use non-lethal means.
*   **UI State:**
    *   UN trucks have a distinct light-blue UN tint.
    *   Hovering a lethal cursor over the truck shows a blocked-by-default warning and a `PR_ASSESSMENT` estimate (e.g., "Est. −71 Legitimacy · Confidence 30% · ISR advised").
    *   If tagged by ISR, cargo (supplies/arms) is revealed.
    *   If hijacked, status changes to "AoI-controlled · UN driver aboard".
    *   Siphoning displays a visible flow effect from the truck to the AoI thief.
*   **Assessment:** Legible. The player is explicitly warned about the steep PR cost of a blind lethal strike.

## 2. UN Building Shielding (§6.2)

*   **Decision Moment:** Player wants to strike a UN structure (school/clinic) that might have an AoI cache.
*   **UI State:**
    *   Structure displays a verification state overlay badge: `unverified`, `disputed`, or `confirmed`.
    *   Confidence pip bar fills as ISR passes occur (0.30 → 0.65 → 0.95).
    *   Hovering lethal cursor shows the estimated PR cost (e.g., Massive collapse for `unverified`).
    *   Proven caches get a subsurface marker.
*   **Assessment:** Legible. Player knows exactly what state the building is in before ordering a strike.

## 3. Diplomatic Lawfare & ROE Freeze (§6.3)

*   **Decision Moment:** Francesca Albanese initiates a lawfare action (Condemnation or ROE Freeze).
*   **UI State:**
    *   **Diplomatic Cable Feed:** Displays `LAWFARE_WARNING` countdowns, condemnations, and freeze announcements.
    *   **Rebuttal Prompt:** A "Rebut with ISR release" button appears for 30s after a condemnation, showing the estimated PR refund.
    *   **Command Bar (ROE Freeze):** Terrestrial offensive powers receive a lock overlay and "ROE FREEZE · mm:ss" text. Blocked attempts flash `STRATEGIC_POWER_BLOCKED`.
*   **Assessment:** Legible. The lock overlay directly communicates restrictions, and the cable feed explains why.

## 4. Orbital Laser Immunity (§6.4)

*   **Decision Moment:** Player needs to use an orbital power during an active ROE freeze.
*   **UI State:**
    *   Unlike terrestrial powers, orbital powers remain fully lit during a freeze.
    *   They display a "JCOM ORBITAL — OUTSIDE UN JURISDICTION" badge.
    *   Hovering the laser over a protected target *still* shows the PR assessment estimate (immunity is from the freeze, not the PR consequences).
*   **Assessment:** Legible. The contrast between locked terrestrial powers and lit orbital powers makes the rule immediately understandable.

## 5. Civilian Eco-Flotilla (§6.5)

*   **Decision Moment:** Flotilla arrives, blockading a waterway and halting dredge jobs. Player must clear them.
*   **UI State:**
    *   A visible blockade ring outline with a "BLOCKADE" label appears on the water.
    *   Affected dredge jobs show as paused (progress bar frozen), not failed.
    *   Vessels have a `Resolve` bar.
    *   The flagship is explicitly marked "Must be boarded".
    *   Command cards offer non-lethal toggles (LRAD, Water Cannon, Board & Tow).
    *   Lethal weapons hover shows blocked-by-default to prevent accidental wipeout.
    *   If a wipeout occurs, a full-width alert flashes, legitimacy drops to 0, and the cable feed updates.
*   **Assessment:** Legible. The non-lethal intended path is pushed via command cards and blocked default cursors.

---
*Note: This document must be re-reviewed after each adversarial QA red-team round by grok.*
