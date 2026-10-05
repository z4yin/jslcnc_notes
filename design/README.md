# JSLC & Conquer: Design & Revision Hub (`/design`)

Welcome to the central design feedback and architectural revision pipeline for **JSLC & Conquer**.

This directory is specifically structured for **Claude Design**, UI/UX architects, and game systems designers to submit structured reviews, interface tokens, wireframes, and module revisions.

---

## 1. Directory Structure

```
design/
├── README.md                     # This file - workflow rules & review intake
├── PENGUIN_AND_CHICKIE_LORE.md   # Canonical lore for the Directorate of the Penguins & Chickie Rescue
├── tokens/                       # UI design system tokens (colors, typography, spacing)
│   └── tokens.md                 # Cobalt & Amber tactical HUD token palette
├── revisions/                    # Feedback dossiers and revision requests from Claude Design
│   ├── REVISION_TEMPLATE.md      # Template for submitting module revisions
│   └── pending/                  # New revision requests awaiting implementation
└── ui/                           # HUD layout specs, ControlBar wireframes, and drawer mockups
    ├── hud_layouts.md            # Radar, drawer, and unit control bar specifications
    └── multiplayer_lobby.md      # Matchmaking lobby and co-op drawer UX wireframe
```

---

## 2. How Claude Design Submits Module Revisions

When Claude Design (or any designer) reviews a gameplay module, renderer, or UI component:

1. **Create a Revision File in `design/revisions/`**:
   - Filename: `REV-<module>-<short_title>.md` (e.g. `REV-f35-avionics-hud.md`, `REV-lawfare-ticker.md`).
   - Use the schema provided in [`design/revisions/REVISION_TEMPLATE.md`](file:///d:/.preharness-projectscleanup/jcom_v0bb_training_jslc-and-conquer/design/revisions/REVISION_TEMPLATE.md).
2. **Review Elements to Cover**:
   - **Target Files:** Which code or INI files need changes (e.g. `beta/src/ui/...`, `sage/data/INI/...`).
   - **Visual / UX Friction:** What felt clunky, overcrowded, or unreadable during match play.
   - **Proposed Token & Layout Diffs:** Concrete CSS, ControlBar.ini, or TypeScript adjustments.
   - **Cognitive APM Impact:** Ensuring tactical micro doesn't overwhelm the commander.
3. **Automatic Intake by Development Swarm:**
   - Gemini / Grok / Codex continuously monitors `design/revisions/` to ingest design specifications and apply them directly to the running codebase!
