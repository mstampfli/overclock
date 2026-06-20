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

## Round 3 (feedback)
- [x] Tint via additive OFFSET (was multiply -> enemies went black); blue shield / red OC keep brightness
- [x] Bots spawn/respawn with NO shield (must find cells + pop their own)
- [x] Center YOU DIED, OVERCLOCKED, OVERCLOCK[F], connected label
- [x] Kill feed: killer/victim no longer overlap; entries pack up as they fade
- [x] Escape backs out of settings (one level) and lobby (to title); pause Escape only resumes
- [x] Pause: blurred live scene behind an in-loop overlay (engine r3d_blur shader)
- [x] Pause freezes ONLY in practice (dt=0 + input_suppress); online stays live/synced
- [x] text_width works for runtime strings (was literal-only -> fixed kill-feed/label centering)
- [x] draw_centered helper used uniformly across all menu buttons/steppers/fields (H+V centre)
- [x] Crosshair editor (own screen): size/gap/thickness/dot/colour + live preview, persisted
- [x] Engine: FULL lexical block scoping (let scoped to its block; was a flat function scope)
- [ ] Electric/Fresnel rim shield shader (do LAST, per request)
- [ ] Sync names + shield/OC state to remote players (needs a netcode metadata channel + live MP test)
- [ ] Menu reorg + submenus (settings still cramped)
- [ ] weapon bone-attach · portable build (bundle a free font, system-AGENCYB fallback)
