# UI Tokens (Cobalt)

## Color Palette

The Cobalt palette is designed for a near-future military interface, with a focus on readability and clear states.

*   **Primary (JSLC / Neutral):**
    *   `Cobalt-500` (Base): `#1A56DB` - Main UI accents, friendly units.
    *   `Cobalt-300` (Highlight): `#7E9CF2` - Hover states, active selections.
    *   `Cobalt-900` (Background): `#111827` - HUD backgrounds, panels.
*   **Secondary (AoI / Hostile):**
    *   `Crimson-500` (Base): `#E02424` - Hostile units, critical damage.
    *   `Crimson-300` (Highlight): `#F98080` - Hover states for hostiles.
*   **Neutral / Protected:**
    *   `UN-Blue-500`: `#418FDE` - UN assets, protected civilians, humanitarian elements.
    *   `UN-Blue-100`: `#D1E4F9` - Background tints for protected zones.
*   **Alerts & Status:**
    *   `Amber-500`: `#FACA15` - Warnings, disputed sites, lawfare alerts.
    *   `Emerald-500`: `#31C48D` - Verified safe, recoveries, positive PR gains.
    *   `Slate-400`: `#9CA3AF` - Disabled, frozen, or unavailable actions.
*   **Special (JCOM Orbital):**
    *   `Neon-Cyan-400`: `#22D3EE` - Orbital jurisdiction, immune elements.

## Typography

*   **Font Family:** `Inter`, `Roboto Mono` (for data/numbers).
*   **Scale:**
    *   `Header 1`: 24px, Bold, Cobalt-500 - Main HUD panel titles.
    *   `Header 2`: 18px, Semi-Bold, White - Secondary panel headers (e.g., Cable feed).
    *   `Body`: 14px, Regular, Slate-300 - General text, descriptions, tooltips.
    *   `Data/Numbers`: 14px, `Roboto Mono`, Regular - PR values, timers, coordinates.
    *   `Micro/Labels`: 10px, Bold, Slate-400, Uppercase - Small tags ("JCOM ORBITAL", "UN ASSET").

## Hierarchy & Layout

*   **Z-Index:**
    *   `10`: Background panels (opacity 85%, `#111827`).
    *   `20`: Standard UI elements, buttons, meters.
    *   `30`: Tooltips, hover assessments (e.g., PR Assessment).
    *   `40`: Critical Alerts (FLOTILLA WIPE, CONDEMNATION), Screen-center tickers.
*   **Spacing:** 4px base grid (4px, 8px, 12px, 16px, 24px, 32px).

## Icon Spec

*   **Size:** 24x24 base, 32x32 for command buttons.
*   **Style:** Minimalist line-art, 2px stroke, flat.
*   **Specifics:**
    *   **Protected:** Shield outline with UN Blue tint.
    *   **Orbital:** Satellite icon with Neon-Cyan glow.
    *   **Freeze:** Snowflake or Lock icon in Amber-500.
    *   **Lawfare:** Gavel or Cable feed icon.
