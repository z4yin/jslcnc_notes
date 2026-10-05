# HUD Overlay Layouts (Cobalt Design)

## 1. Two-Sided PR Meter (Legitimacy vs. Popular Support)
**Location:** Top Center
**Layout:**
- A wide, split progress bar. Left side: JSLC Legitimacy (Cobalt-500 to Emerald-500). Right side: AoI Popular Support (Crimson-500).
- **Scale:** `0` to `100`.
- **Threshold Marker:** A distinct white tick mark at `40` on the JSLC side indicating the ROE Restriction Threshold.
- **Values:** Displayed in `Roboto Mono`, e.g., `JSLC: 72 | AOI: 45`.
- **Gain-Cap Indicator:** Small text or icon next to JSLC value: `+25 / min cap reached` (when active).
- **Delta Ticker:** Below the meter, a 3-second temporary label pops up on PR changes: `[-28] UN_SITE_STRIKE_UNVERIFIED` (Amber-500 or Crimson-500).
- **Wipeout State:** On `FLOTILLA_LETHAL_INCIDENT`, the meter flashes red, drops JSLC side to `0` instantly, and displays a full-width alert banner: `CRITICAL: FLOTILLA CASUALTY - LEGITIMACY COLLAPSE`.

## 2. UN Lawfare & Albanese Cable Warning Ticker
**Location:** Right Side (below minimap or upper right quadrant)
**Layout:**
- **Panel:** A sleek, semi-transparent (`Cobalt-900`, 85% opacity) feed window.
- **Portrait:** Left-aligned 64x64 portrait frame. Displays "Francesca Albanese" (real mode) or generic UN Official (fictional mode).
- **Ticker/Feed:**
  - `LAWFARE_WARNING`: `[WARNING] UN Condemnation in T-20s` (Amber text, counting down).
  - `LAWFARE_CONDEMNATION`: `[CONDEMNATION] Excessive force cited.` with a prompt button `[Rebut with ISR Release]` (Visible for 30s).
- **Styling:** Header uses `Header 2`. Body text uses `Micro/Labels` for timestamps.

## 3. Conventional ROE Freeze Indicator with Orbital Laser Immunity Badge
**Location:** Bottom Center (Command Bar / Power Bar)
**Layout:**
- **Command Bar Overlay:** When `ROE_FREEZE_BEGIN` triggers, all terrestrial offensive powers (air strikes, artillery) receive a Slate-400 tint and a lock icon overlay (`Amber-500`).
- **Freeze Timer:** A prominent countdown over the locked abilities: `ROE FREEZE: 00:45`.
- **Orbital Immunity Badge:**
  - Powers with `Jurisdiction = ORBITAL` (like the Space Laser) remain fully lit.
  - They feature a pulsing `Neon-Cyan-400` border.
  - **Badge Tag:** A label floating above the orbital powers reads: `JCOM ORBITAL — OUTSIDE UN JURISDICTION` (using `Micro/Labels`, `Neon-Cyan-400` text).
- **Attempted Use:** If the player attempts to use a locked power, it flashes red with `STRATEGIC_POWER_BLOCKED`.

## 4. Flotilla Blockade & Dredging Depth Status
**Location:** In-World (On Water) & Dredging UI
**Layout:**
- **Blockade Ring:** A `UN-Blue-500` glowing dashed line radius (60 units) around the anchored flotilla.
- **Label:** Floating world-space text above the flagship: `[BLOCKADE]` in `Amber-500`.
- **Vessel Resolve Bars:** Small progress bars above each vessel.
- **Flagship Marker:** The central flagship has an icon and text: `Greta Thunberg's Vessel` (real) or `Eco-Flotilla Flagship` (fictional) with `Must be boarded`.
- **Dredging Depth Status (Sidebar or world-space near job):**
  - Normal: Progress bar filling up.
  - **Halted:** When blockaded, the progress bar turns `Slate-400` (frozen), and an overlay says `PAUSED: FLOTILLA BLOCKADE`. The progress does not reset.
