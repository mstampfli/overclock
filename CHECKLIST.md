# OVERCLOCK — work checklist

Cadence: compile + commit + push after each item.

## Shipped (awaiting your test)
- [x] In-game lobby: bots / round length / kills-to-win + PRACTICE / HOST / JOIN(by IP)  ← **test MP**

## Open
### Quick
- [x] Reset ammo / shield / health (everything) between rounds
- [x] Reduce katana range a bit
- [x] Velocity bar grey (so it's not confused with the blue shield bar)
- [x] Explosive: smaller range damage-falloff (more damage in the vicinity)
- [x] Overclock: faster reload + unlimited reserve mags
- [x] Hit-location damage: headshot 2x > torso 1x > legs 0.65x

### Medium
- [ ] Center text EVERYWHERE
- [x] Allow binds on the MOUSE buttons (LMB/RMB/MMB/M4/M5)
- [x] Shield = blue, Overclocked = orange (real model tint); enemies pop while I am overclocked
- [ ] Put the weapon actually IN the hands (bone attach — engine joint API)

### Big
- [x] Fullscreen + windowed-fullscreen (Settings -> Display cycle, persisted)
- [ ] Customizable crosshair + a crosshair editor (Valorant-like)
- [x] Real scoreboard (per-actor kills on TAB) + editable, persisted username

> If multiplayer is broken after the join system, that jumps to the top.

## Round 2 (feedback)
- [x] Shielded actors are solid BLUE; overclocked enemies bright RED (stronger glow) — real tint
- [x] Scoreboard panel is transparent (checkerboard dim)
- [x] Lobby title no longer overlaps the Name field
- [x] Kill feed (top-right, "KILLER > VICTIM")
- [x] Confirmed: rollback + server authority already in the netcode
- [ ] Sync names + shield/OC state to remote players (no metadata channel yet)
- [ ] Menu reorg + submenus (settings is cramped)
- [ ] Center text everywhere (proper pass)
- [ ] Crosshair editor · weapon bone-attach · portable build (font)
