import os
import json

base_dir = r"d:\.preharness-projectscleanup\jcom_v0bb_training_jslc-and-conquer\docs\sage\golden\new"

vectors = {
    "convoy/spawn_schedule.jsonl": [
        { "v": 1, "kind": "init", "module": "convoy", "seed": 1337, "tunables": {}, "state": {} },
        { "v": 1, "kind": "step", "frame": 0, "frames": 5000 },
        { "v": 1, "kind": "expect", "frame": 5000, "state": {}, "events": [], "note": "Placeholder for exact spawn schedule dependent on Mulberry32." }
    ],
    "convoy/hijack_channel.jsonl": [
        { "v": 1, "kind": "init", "module": "convoy", "seed": 1337, "tunables": {}, "state": { "trucks": { "t1": { "team": "Neutral_UN", "hp": 400 } } } },
        { "v": 1, "kind": "input", "frame": 10, "op": "startHijack", "args": { "truckId": "t1", "hijackerId": "h1" } },
        { "v": 1, "kind": "step", "frame": 10, "frames": 45 },
        { "v": 1, "kind": "input", "frame": 55, "op": "damage", "args": { "targetId": "h1", "amount": 10 } },
        { "v": 1, "kind": "step", "frame": 55, "frames": 45 },
        { "v": 1, "kind": "expect", "frame": 100, "state": { "trucks": { "t1": { "team": "Neutral_UN" } } }, "events": [], "note": "Damage interrupts 3-second (90 frame) hijack channel." }
    ],
    "convoy/siphon_totals.jsonl": [
        { "v": 1, "kind": "init", "module": "convoy", "seed": 1337, "tunables": {}, "state": { "trucks": { "t1": { "arms": 120, "supplies": 300 } }, "aoiSupplies": 0, "aoiArms": 0 } },
        { "v": 1, "kind": "input", "frame": 0, "op": "startSiphon", "args": { "truckId": "t1", "siphonerId": "s1" } },
        { "v": 1, "kind": "step", "frame": 0, "frames": 300 },
        { "v": 1, "kind": "expect", "frame": 300, "state": { "aoiSupplies": 100, "aoiArms": 40 }, "events": [], "note": "10s of siphon: 10 supplies/s = 100, 4 arms/s = 40." }
    ],
    "convoy/recovery.jsonl": [
        { "v": 1, "kind": "init", "module": "convoy", "seed": 1337, "tunables": {}, "state": { "jslcLegitimacy": 50, "trucks": { "t1": { "team": "AoI", "immobilized": True } } } },
        { "v": 1, "kind": "input", "frame": 0, "op": "startRecovery", "args": { "truckId": "t1", "boarderId": "b1" } },
        { "v": 1, "kind": "step", "frame": 0, "frames": 90 },
        { "v": 1, "kind": "expect", "frame": 90, "state": { "jslcLegitimacy": 58, "trucks": { "t1": { "team": "Neutral_UN" } } }, "events": [ { "type": "PR_DELTA", "who": "JSLC", "delta": 8, "reason": "UN_CONVOY_RECOVERED" } ], "note": "3s recovery channel restores team to Neutral_UN and grants +8 PR." }
    ],
    "shield/dig_timing.jsonl": [
        { "v": 1, "kind": "init", "module": "shield", "seed": 1337, "tunables": {}, "state": { "structures": { "s1": { "cache": None } }, "aoiFunds": 1000 } },
        { "v": 1, "kind": "input", "frame": 0, "op": "digBeneath", "args": { "structureId": "s1", "workerId": "w1" } },
        { "v": 1, "kind": "step", "frame": 0, "frames": 1200 },
        { "v": 1, "kind": "expect", "frame": 1200, "state": { "structures": { "s1": { "cache": "c1" } }, "aoiFunds": 600 }, "events": [ { "type": "SHIELD_CACHE_BUILT", "structureId": "s1", "cacheId": "c1" } ], "note": "40s (1200 frames) dig time, costs 400 funds." }
    ],
    "shield/strikes.jsonl": [
        { "v": 1, "kind": "init", "module": "shield", "seed": 1337, "tunables": {}, "state": { "jslcLegitimacy": 100, "structures": { "s1": { "state": "unverified", "conf": 0.30 }, "s2": { "state": "confirmed", "conf": 0.95 } } } },
        { "v": 1, "kind": "input", "frame": 10, "op": "damage", "args": { "targetId": "s1", "weaponLethality": "LETHAL", "amount": 1000 } },
        { "v": 1, "kind": "step", "frame": 10, "frames": 1 },
        { "v": 1, "kind": "expect", "frame": 11, "state": { "jslcLegitimacy": 0 }, "events": [ { "type": "PR_DELTA", "who": "JSLC", "delta": -119, "reason": "UN_SITE_STRIKE_UNVERIFIED", "note": "round(28 * (2.0 - 0.30) * 2.5) = 119, legitimacy clamped to 0." } ] },
        { "v": 1, "kind": "input", "frame": 20, "op": "damage", "args": { "targetId": "s2", "weaponLethality": "LETHAL", "amount": 1000 } },
        { "v": 1, "kind": "step", "frame": 20, "frames": 1 },
        { "v": 1, "kind": "expect", "frame": 21, "state": { "jslcLegitimacy": 0 }, "events": [ { "type": "PR_DELTA", "who": "JSLC", "delta": -10, "reason": "UN_SITE_STRIKE_VERIFIED", "note": "round(28 * (2.0 - 0.95) * 0.35) = 10" } ] }
    ],
    "flotilla/lethal_wipeout.jsonl": [
        { "v": 1, "kind": "init", "module": "flotilla", "seed": 1337, "tunables": {}, "state": { "jslcLegitimacy": 80, "aoiPopularSupport": 20, "flotillas": { "f1": { "vessels": ["v1", "v2"] } } } },
        { "v": 1, "kind": "input", "frame": 10, "op": "damage", "args": { "targetId": "v1", "weaponLethality": "LETHAL", "amount": 10 } },
        { "v": 1, "kind": "step", "frame": 10, "frames": 1 },
        { "v": 1, "kind": "expect", "frame": 11, "state": { "jslcLegitimacy": 0, "aoiPopularSupport": 45 }, "events": [ { "type": "PR_DELTA", "who": "JSLC", "delta": -80, "reason": "FLOTILLA_LETHAL_WIPEOUT" }, { "type": "FLOTILLA_LETHAL_INCIDENT", "vesselId": "v1" } ], "note": "First lethal hit wipes out PR." },
        { "v": 1, "kind": "input", "frame": 20, "op": "damage", "args": { "targetId": "v2", "weaponLethality": "LETHAL", "amount": 10 } },
        { "v": 1, "kind": "step", "frame": 20, "frames": 1 },
        { "v": 1, "kind": "expect", "frame": 21, "state": { "jslcLegitimacy": 0, "aoiPopularSupport": 45 }, "events": [], "note": "Second hit does not trigger wipeout." }
    ],
    "orbital/immunity.jsonl": [
        { "v": 1, "kind": "init", "module": "orbital", "seed": 1337, "tunables": {}, "state": { "freezeActive": True, "powers": { "p_terr": { "jurisdiction": "TERRESTRIAL" }, "p_orb": { "jurisdiction": "ORBITAL" } } } },
        { "v": 1, "kind": "input", "frame": 10, "op": "activatePower", "args": { "powerId": "p_terr" } },
        { "v": 1, "kind": "step", "frame": 10, "frames": 1 },
        { "v": 1, "kind": "expect", "frame": 11, "state": {}, "events": [ { "type": "STRATEGIC_POWER_BLOCKED", "powerId": "p_terr", "reason": "ROE_FREEZE" } ], "note": "Terrestrial power blocked by ROE freeze." },
        { "v": 1, "kind": "input", "frame": 20, "op": "activatePower", "args": { "powerId": "p_orb" } },
        { "v": 1, "kind": "step", "frame": 20, "frames": 1 },
        { "v": 1, "kind": "expect", "frame": 21, "state": { "powers": { "p_orb": { "state": "active" } } }, "events": [], "note": "Orbital power ignores ROE freeze." }
    ],
    "lawfare/condemnation_rebuttal.jsonl": [
        { "v": 1, "kind": "init", "module": "lawfare", "seed": 1337, "tunables": {}, "state": { "jslcLegitimacy": 50, "aoiPopularSupport": 50, "activeCondemnation": { "id": "c1", "jslcDelta": -6, "staged": True } } },
        { "v": 1, "kind": "input", "frame": 10, "op": "rebutCondemnation", "args": { "condemnationId": "c1" } },
        { "v": 1, "kind": "step", "frame": 10, "frames": 1 },
        { "v": 1, "kind": "expect", "frame": 11, "state": { "jslcLegitimacy": 56 }, "events": [ { "type": "PR_DELTA", "who": "JSLC", "delta": 6, "reason": "LAWFARE_CONDEMNATION_REBUTTED" } ], "note": "Rebuttal of staged incident refunds 100% of -6 penalty." }
    ]
}

for path, data in vectors.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        for line in data:
            f.write(json.dumps(line) + "\n")
    print(f"Created {full_path}")
