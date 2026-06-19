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

Playable. In so far:

- **Movement.** Ground and air acceleration, air-strafe, momentum-preserving
  friction, slide and slide-hop (the main ground speed tool), double-jump, and
  air-dash. Wallrun with a 45-degree climb cap, wall-jump, and a wall-exit fling
  that reads the wall geometry: a small pop off the top edge, a momentum-keeping
  launch off the side edge.
- **Tacticals.** A grappling hook (E) - a strong, axis-locked pull you swing on -
  and a frag grenade (G): an arcing, bouncing charge that detonates on a fuse with
  radial damage and physics knockback (it shoves crates, bots, and you - frag-jump
  for movement tech). Explosions self-damage at close range.
- **Weapons.** A hitscan rifle (1) and a single-shot, travel-time rocket launcher
  (2) that explodes on impact - lead your target. Magazines, ammo, and reload.
- **Combat feel.** Crosshair and hitmarkers, directional damage indicator,
  low-health vignette, screen shake, and a death/respawn cycle.
- **Survivability.** No passive regen. Health from heal pads + enemy drops
  (instant). Shields are Apex-style: pick up cells, then hold to apply one (you
  slow down and can't slide/dash/fire). You drop unused cells on death; shields
  are scarce.
- **Overclock** (F when the meter is full). Built from kills and stylish movement;
  while active it buffs fire rate and reload, resets tactical cooldowns, grants a
  small overshield, dims the world, and lights up enemies. Resets on death.
- **Arena + FFA loop.** A walled arena with a central high-ground block, buildings
  with rooftops, freestanding wallrun walls, cover, and loose crates. Kill-target
  win, round timer, and a HUD. Bots collide with the world and the player.
- **Multiplayer.** Two players on loopback via the shared `net_sim` step.

Next: smarter bots, more weapons, and team modes.

## Controls (default, rebindable)

- Move: WASD
- Jump / double-jump: Space
- Slide: Left Ctrl
- Air-dash: Left Shift
- Fire: Left mouse
- Weapons: 1 (rifle), 2 (rocket launcher)
- Reload: R
- Grapple: E
- Frag grenade: G
- Apply shield cell (hold): Q
- Overclock (meter full): F
- Look: mouse
