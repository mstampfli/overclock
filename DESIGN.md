# OVERCLOCK - Game Design Doc

A first-person, stylized low-poly, momentum movement arena shooter built in Aurora.
Working title: **OVERCLOCK**. This is the living spec; everything below is a
decision unless marked "open".

## Pitch

Grounded-fast first-person arena combat where mastery is flow: chain wallruns,
slide-hops, and air-dashes to carry speed, then convert that movement into kills.
Build the **Overclock** meter through kills and stylish movement, trigger it, and
become a glowing, snowballing threat for a few seconds.

## Pillars

1. **Movement is the skill.** Speed is earned and preserved; the map is a
   playground. Titanfall 2 / Apex feel: weighty-but-fast, momentum-preserving.
2. **Aggression and flow are rewarded.** The Overclock mechanic pays you for
   chaining movement and kills, not for camping.
3. **Readable and stylized.** Clean low-poly shapes, bold color, high readability.

## Core decisions

| Area | Decision |
|---|---|
| Feel reference | Titanfall 2 / Apex (momentum-preserving, grounded-fast) |
| Perspective | First-person |
| Pace | Grounded-fast: slide-hops/wallruns BUILD speed; mastery = flow |
| Movement (v1) | Wallrun + wall-jump, slide + slide-hop, double-jump + air-dash |
| Tacticals (cooldown) | Grappling hook + frag grenade (universal, 1-2 gadgets) |
| Gunplay | Mix: some hitscan, some projectile/travel-time (Titanfall-style) |
| Health model | Apex-style: shields + regenerating/healing health |
| Mode (v1) | Arena FFA, ~6-8 players, then team objective, then maybe PvE |
| Win condition | Kill limit OR timer (whichever first) |
| Art | Stylized low-poly; greybox now, art pass later |

## The Overclock mechanic (signature)

A meter (0-100) that fills from:
- Kills (large), assists (small).
- **Style**: chaining wallruns / slide-hops, airborne kills, no-touch-the-ground
  streaks, fast multi-kills.
- Decays slowly out of combat so it must be earned and spent.

At full, the player triggers **OVERCLOCKED** for ~10s:
- Increased move speed, faster fire / instant reloads, tactical cooldowns reset,
  a small overshield.
- Loud visual: emissive body glow (uses the renderer's emissive + IBL), screen
  edge tint, audio sting.
- Kills during Overclock extend it slightly (snowball, but capped).

Ties name -> mechanic -> the exact fantasy: reward flow + aggression. Built after
movement + shooting land. (Open: exact fill weights, duration, overshield amount.)

## Movement controller (feel targets)

Grounded-fast tuning (starting point, all tunable, all data-driven):
- Ground: high accel + friction, capped run speed; crisp stops.
- Air: Quake-style air-strafe acceleration (small cap, projected) so turning while
  strafing in the air builds speed.
- Slide: crouch while grounded + moving boosts speed, very low friction; slide-hop
  (jump out of a slide) preserves horizontal speed so chains accelerate.
- Wallrun: run along a wall while airborne and moving along it; reduced gravity,
  along-wall acceleration, time-limited; wall-jump pushes off the normal + up,
  keeping momentum.
- Double-jump: one air jump, refreshed on ground/wall.
- Air-dash: short cooldown burst in the look/move direction.

The controller is the single shared simulation step run by client prediction and
the authoritative server, so they cannot drift.

## Combat

- Weapons: a mix of hitscan (snappy) and projectile/travel-time (rewards leading
  fast movers). Start with 2-3 archetypes.
- TTK: moderate, so movement matters mid-fight (reposition, re-peek, escape).
- Health: shields (topped via pickups) layered over regenerating/healing health.
- Hit validation: server-authoritative, lag-compensated (engine rewinds targets
  to the shooter's view tick).

## Modes (roadmap)

1. **Arena FFA** (v1): ~6-8 players, kill-limit-or-timer, fast respawns. Fill with
   bots while building; fun solo or online.
2. **Team objective** (next): CTF / domination / hardpoint.
3. **PvE / co-op** (maybe): horde or movement challenges.

## Maps

Mixed combat arenas: some verticality (walls to run, ledges, rooftops), some
lanes, some open cover. The geometry should reward and enable movement without
being only a parkour course.

## Architecture (modular, ground-up)

**Game fully in Aurora.** The Rust engine provides only general, reusable
primitives; all gameplay is written in `.aur`.

- **Engine (Rust), general:** GPU renderer (PBR, CSM, SSAO, IBL, point shadows,
  instancing), physics (rapier3d) + queries, audio (incl. 3D), the **rebindable
  input-action layer**, and a **generic netcode framework** (transport,
  prediction, reconciliation, interpolation, lag-comp, interest, delta).
- **The netcode runs the game's Aurora sim function** (`net_sim`) over an opaque
  per-player state blob each tick (prediction, replay, and server authority all
  call it), so the movement and game rules live in Aurora, not the engine. The
  engine reads only `state[0..3]` = x,y,z and `state[3]` = yaw for transform /
  interpolation / lag-comp; the rest of the blob is game-defined.
- **Game (Aurora):** the movement controller, weapons, Overclock, HUD, spawns,
  scoring, modes, map definition. Rewritable without touching Rust.

Modularity rules:
- **No hardcoded inputs.** The game binds abstract actions (MoveForward, Jump,
  Slide, Dash, Fire, Tactical1/2, Overclock, ...) to input codes via the
  input-action layer; everything is rebindable at runtime (settings menu).
- **Data-driven settings.** Movement tuning, sensitivity, FOV, gameplay constants
  live in one config place and are settable at runtime; nothing inline-hardcoded.

## Build order

1. **Movement feel** (current): greybox FP playground, the Aurora movement
   controller on the net-shared sim, mouse-look, speed/state HUD, camera FX. Tune
   until it feels great, solo as host.
2. Guns + shields/health + a target dummy / bots.
3. The FFA loop: spawns, scoring, kill-limit/timer, respawns.
4. The Overclock meter + state.
5. Tacticals (grapple, frag). Polish, then team modes.

## Open questions

- Overclock exact fill weights / duration / overshield.
- Weapon roster + per-weapon feel.
- Bot AI depth for solo play.
- Real-network hardening + matchmaking/servers (later).
