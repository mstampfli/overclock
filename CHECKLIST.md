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
- [x] Crosshair presets (6 slots saved to disk) + portable font (bundled OFL Saira Condensed Black fallback)
- [x] Death drops a reserve shield only if you had >=1; un-popped reserves lost on death (player + bots)
- [x] HUD: fatter/wider bars; kill feed top-left + player name highlighted + clears on fresh game
- [x] Dash: 0 cooldown, top speed DERIVED from the slide max (auto-synced)
- [x] Unified bullet tracers (player drawn once from the eye, no double-draw)
- [x] Crate <-> actor knockback (local movers only; flying crates only knock if moving toward you)

## MP / netcode - FINDINGS from the autonomous loop (needs a separate channel + live test)
- The replicated state is f32 slots 0..20 (STATE_MAX 32). Movement fills 0..20. Slots 21..29 are
  used by sim_step as LOCAL-ONLY working state (21 = physics body handle read as net_local_state(21),
  22 = windup, 23 = wallrun flag, 24/25 wall normals, 26..29 slide/knock). They are NOT replicated on
  purpose: replicating slot 21 would reconcile a client's local handle to the host's -> broken physics.
- So combat state (hp/shield/cells/oc/names) CANNOT ride free state slots. It needs a SEPARATE metadata
  channel in aurora-net (alongside the input/state replication). net_is_server() already exists for the
  host-authority branch; net_player_state(id, slot) now exists to read replicated slots (building block).
- PLAN (do with a live 2-client test): add a per-player metadata blob channel in aurora-net (snapshot.rs/
  channel.rs); host owns hp/shield/cells/oc/name, replicates it; clients display remote hp/shield/oc tint
  + names; host-authoritative damage (apply on host, lag-comp via lagcomp.rs, replicate); bot + crate run
  on host only. Tried free-slot replication in the loop -> reverted (would clobber the handle).

## MP / netcode (the big remaining block - needs live 2-client testing)
- [ ] Host-authoritative combat branch: on the host, apply damage to ALL players + bots and replicate;
      clients only predict feedback (hitmarker/tracer) and reconcile. Uses existing predict.rs + lagcomp.rs.
- [ ] Replicated combat state channel: per-player hp/shield/cells/OC + names (the missing metadata channel).
      Once this exists, melee/explosive/hitscan can include remotes (host-authoritatively) and crates can be
      host-owned so remotes interact with them properly.
- [ ] Bot/entity authority: bots run on the HOST only and replicate to clients as remotes (today they may
      run locally on every client = desync). Part of the same host-authority pass.
- [ ] Crate (physics) authority: crates simulated on the HOST and replicated; today they're local per
      client (cosmetic), so remote crate interaction was reverted until this lands.

## Visual / polish (do LAST, per request)
- [ ] Electric/Fresnel rim shield shader (LAST)
- [ ] Mantle mechanic (LAST-LAST)
- [ ] weapon bone-attach (needs an engine joint-transform builtin)
- [ ] Menu reorg + submenus (user said menu is fine for now - deprioritised)

## Refactor
- [x] Death-centralization: one last_hit + per-frame death sweep replacing the 3 duplicated death sites.
      ALSO fixed explosive kills not scoring (scoreboard + kill feed). Verified by sim_death.aur.
- [x] Katana: 2.8m range, 75 dmg straight to HP (BYPASSES shield); box push way down (still felt too strong)

## AUTONOMOUS LOOP ORDER (user asleep - implement EVERYTHING, compile+commit+push each step)
1. [x] Weapon bone-attach: engine r3d_draw_on_joint + joint names/dump; weapons ride hand bone (joint 29).
       Local h_* offsets are a best guess - TUNE BY EYE to seat in the grip.
2. MP / host-authority: replicated combat state (hp/shield/cells/names) + host-authoritative damage + bot/crate
   authority, on aurora-net predict.rs/lagcomp.rs. Keep PRACTICE working; verify with sims; do not break the game.
3. [x] Fresnel / electric rim shield shader: r3d_draw_shield + ObjU params2; cyan animated rim on
       shielded actors (bots + remotes) instead of the flat blue tint. Shader validated by pipeline tests.
4. [x] Mantle mechanic: airborne chest-height ledge-grab -> pull up+over onto the ledge (~0.32s),
       slot 31, snappy. Verified by sim_mantle.aur (triggers, clears the top, lands on the platform).

## LOOP COMPLETE - all backlog items done. Remaining items need the USER:
- MP host-authority (replicated combat state + host damage + bot/crate authority): needs a new aurora-net
  metadata channel + a LIVE 2-client test. Plan documented above.
- Weapon bone-attach: engine + wiring done; the hand_o* local offsets need EYE-TUNING to seat the weapon.
- Fresnel shield + mantle: implemented + sim/pipeline-verified; want a visual/feel review when you play.
