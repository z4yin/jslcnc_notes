# SAGE C++ Engine Architecture

The JSLC and Conquer project has fully migrated to a C++ SAGE (Strategy Action Game Engine) architecture. This document explains the core paradigms of the new engine.

## 1. Module System (Object + Body + Update)
Every entity in the game is built via composition using the SAGE module model:
- **Object:** The root entity container.
- **Body:** Handles health, armor, and physical state.
- **Update:** Defines behavior per tick (e.g., \JslcLogisticsUpdate\, \UnConvoySubsystem\).

## 2. Lockstep Determinism
To support authoritative networking and replays, the engine operates on strict lockstep determinism:
- Fixed logic step of **1/30s** (30 logic frames per second).
- Floating point conversions use deterministic epsilon rounding bounds.
- Randomness is strictly controlled via a seeded **Mulberry32** PRNG and **FNV-1a** string hashing for named streams (e.g., \weather\, \capture\, \logistics\).

## 3. Data-Driven INI Configurations
Hardcoded values have been stripped out. All units, weapons, and rules are now driven by INI templates loaded at runtime from \sage/data/INI/\:
- \WeaponTemplate\: Defines lethality and jurisdiction (e.g., \TERRESTRIAL\ vs \ORBITAL\).
- \ObjectTemplate\: Defines KindOf tags (e.g., \PROTECTED_CIVILIAN\).

## 4. The Event Contract
The simulation logic is decoupled from the UI. The engine pushes state changes to the Presentation layer strictly through a unidirectional event queue (e.g., \PR_DELTA\, \LAWFARE_WARNING\). The UI reads these events and never mutates the simulation directly.
