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

Early. The movement-feel playground is in: ground and air acceleration,
air-strafe, friction, slide and slide-hop, double-jump, and air-dash on a greybox
arena, with rebindable inputs and data-driven tuning. Next: wallrun and
wall-jump, then guns, shields, and the FFA loop.

## Controls (default, rebindable)

- Move: WASD
- Jump / double-jump: Space
- Slide: Left Shift
- Dash: Left Ctrl
- Look: mouse
