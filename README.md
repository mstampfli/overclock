# OVERCLOCK

A first-person, stylized low-poly, momentum movement arena shooter, written
entirely in [Aurora](https://github.com/mstampfli/aurora). Chain wallruns,
slide-hops, and air-dashes to carry speed, then convert that movement into kills.
Build the **Overclock** meter through kills and stylish movement, trigger it, and
become a glowing, snowballing threat for a few seconds.

The game is pure Aurora gameplay on top of the engine's general primitives: the
GPU renderer, physics, audio, the rebindable input layer, and a generic netcode
framework. The movement model is registered with that framework via `net_sim`,
so client prediction, rollback replay, and the authoritative server all run the
exact same step and cannot drift.

See [DESIGN.md](DESIGN.md) for the full design doc.

## Build and run

Requires the `aurorac` toolchain from the Aurora repo on your `PATH`.

```
aurorac run playground.aur      # play the movement feel playground (Esc quits)
aurorac build playground.aur -o overclock   # compile a standalone native binary
```

## Status

Playable greybox. In so far:

- **Movement.** Ground and air acceleration, air-strafe, momentum-preserving
  friction, slide and slide-hop (the main ground speed tool), double-jump, and
  air-dash. Wallrun with a 45-degree climb cap, wall-jump, and a wall-exit fling
  that reads the wall geometry: a small pop off the top edge, a momentum-keeping
  launch off the side edge.
- **Grappling hook** (E). A strong, axis-locked pull toward the anchor that you
  swing on but cannot fight directly.
- **Combat.** Hitscan weapon with magazine, ammo, and reload; paper-thwack
  hitmarkers and a crosshair; directional damage indicator, low-health red
  vignette, light screen shake, and a death/respawn cycle.
- **Overclock** (F when the meter is full). Built from kills and stylish
  movement; while active it buffs fire rate and reload, dims the world, and lights
  up enemies so they read through the haze.
- **FFA loop.** Kill-target win condition, round timer, and a HUD (crosshair,
  speed bar, timer, score, Overclock meter). Bots collide with the world and the
  player.
- **Multiplayer.** Two players on loopback via the shared `net_sim` step.

Next: a real arena map, more weapons, smarter bots, and team modes.

## Controls (default, rebindable)

- Move: WASD
- Jump / double-jump: Space
- Slide: Left Ctrl
- Air-dash: Left Shift
- Grapple: E
- Fire: Left mouse
- Reload: R
- Overclock (meter full): F
- Look: mouse
