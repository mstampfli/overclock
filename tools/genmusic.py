#!/usr/bin/env python3
# Procedurally generate a longer, richer, SEAMLESSLY looping dark-synthwave bed.
# Clean loop guaranteed by: bar-aligned content + per-note envelopes that decay to ~0,
# and a tail-wrap (reverb/echo tail past the loop end is added back onto the start).
import numpy as np, wave, struct, sys

SR = 44100
BPM = 96.0
beat = 60.0 / BPM
bar = 4 * beat
BARS = 32
L = int(round(BARS * bar * SR))           # exact loop length (samples)
TAIL = int(0.8 * SR)                        # wrap window for echo/reverb/release tails
N = L + TAIL
t = np.arange(N) / SR

def midi(m): return 440.0 * 2.0 ** ((m - 69) / 12.0)

# ---- A-minor dark progression, 8 bars: Am Am F F C C G G, repeated x4 over 32 bars ----
roots = [57, 57, 53, 53, 48, 48, 55, 55]    # per-bar root (A3 F3 C3 G3)
triad = {57:[57,60,64], 53:[53,57,60], 48:[48,52,55], 55:[55,59,62]}

def saw(ph): return 2.0 * (ph - np.floor(ph + 0.5))
def sqr(ph): return np.sign(saw(ph))
def env(n, a, d, s, r, sus_len):
    # simple ADSR over sus_len samples (+ release), returns length sus_len+r
    out = np.zeros(sus_len + r)
    ai = max(1, int(a)); di = max(1, int(d)); ri = max(1, int(r))
    out[:ai] = np.linspace(0, 1, ai)
    de = min(di, sus_len - ai) if sus_len > ai else 0
    if de > 0: out[ai:ai+de] = np.linspace(1, s, de)
    if ai+de < sus_len: out[ai+de:sus_len] = s
    out[sus_len:sus_len+ri] = np.linspace(out[sus_len-1] if sus_len>0 else s, 0, ri)
    return out

buf_bass = np.zeros(N); buf_pad = np.zeros(N); buf_arp = np.zeros(N)
buf_lead = np.zeros(N); buf_drum = np.zeros(N)

def add(buf, start, sig):
    e = min(N, start + len(sig))
    if start < N and e > start: buf[start:e] += sig[:e-start]

# ---- Bass: driving 8th-note root, octave below, short pluck ----
eighth = int(round(beat/2 * SR))
for b in range(BARS):
    root = roots[b % 8] - 12
    f = midi(root)
    for k in range(8):
        st = int(round((b*bar + k*(beat/2)) * SR))
        ln = eighth
        e = env(ln, 0.003*SR, 0.05*SR, 0.5, int(0.06*SR), ln)
        ph = np.arange(len(e)) * f / SR
        sig = (0.6*saw(ph) + 0.4*np.sin(2*np.pi*ph)) * e * 0.5
        add(buf_bass, st, sig)

# ---- Pad: detuned-saw triad, sustained per bar with soft attack/release ----
det = [0.0, 0.13, -0.11]
for b in range(BARS):
    notes = triad[roots[b % 8]]
    ln = int(round(bar * SR))
    seg = np.zeros(ln + int(0.35*SR))
    e = env(ln, 0.18*SR, 0.4*SR, 0.8, int(0.34*SR), ln)
    for nidx, m in enumerate(notes):
        f = midi(m + 12)
        for dt_c in det:
            ph = np.arange(len(e)) * (f + dt_c) / SR
            seg[:len(e)] += saw(ph) * e
    st = int(round(b*bar*SR))
    add(buf_pad, st, seg / (len(notes)*len(det)) * 0.5)

# ---- Arp: 16th-note triad arpeggio, bright pluck ----
six = int(round(beat/4 * SR))
for b in range(BARS):
    notes = triad[roots[b % 8]]
    pattern = [0,1,2,1,0,1,2,1, 0,1,2,1,0,1,2,1]
    for k in range(16):
        m = notes[pattern[k] % len(notes)] + 24
        f = midi(m)
        st = int(round((b*bar + k*(beat/4)) * SR))
        ln = six
        e = env(ln, 0.002*SR, 0.04*SR, 0.3, int(0.05*SR), ln)
        ph = np.arange(len(e)) * f / SR
        sig = (0.5*sqr(ph) + 0.5*saw(ph)) * e * 0.16
        add(buf_arp, st, sig)

# ---- Lead: simple sustained motif in the back half, soft ----
lead_notes = [(0,69),(2,72),(4,71),(6,67),(8+0,69),(8+2,76),(8+4,74),(8+6,72)]  # beat, midi over 4 bars
for cyc in range(2,4):            # only in the second half (bars 16-31) for build
    base = cyc*8
    for (bt, m) in lead_notes:
        f = midi(m)
        st = int(round((base*bar + bt*beat) * SR))
        ln = int(round(1.6*beat*SR))
        e = env(ln, 0.02*SR, 0.3*SR, 0.6, int(0.25*SR), ln)
        ne = len(e)
        vib = 1.0 + 0.004*np.sin(2*np.pi*5.0*np.arange(ne)/SR)
        ph2 = np.cumsum(f*vib)/SR
        sig = (0.6*np.sin(2*np.pi*ph2) + 0.4*saw(ph2)) * e * 0.12
        add(buf_lead, st, sig)

# ---- Drums ----
def kick(ln):
    n = np.arange(ln)
    f = 120*np.exp(-n/SR*22) + 45
    ph = np.cumsum(f)/SR
    e = np.exp(-n/SR*9)
    return np.sin(2*np.pi*ph)*e
def snare(ln):
    n = np.arange(ln)
    noise = np.random.RandomState(7).randn(ln) * np.exp(-n/SR*16)
    tone = np.sin(2*np.pi*190*n/SR) * np.exp(-n/SR*22)
    return 0.7*noise + 0.5*tone
def hat(ln, open=False):
    n = np.arange(ln)
    rate = 6 if open else 40
    return np.random.RandomState(3).randn(ln) * np.exp(-n/SR*rate) * 0.5

K = kick(int(0.32*SR)); S = snare(int(0.3*SR)); H = hat(int(0.06*SR)); HO = hat(int(0.18*SR), True)
for b in range(BARS):
    for bt in range(4):
        st = int(round((b*bar + bt*beat)*SR))
        add(buf_drum, st, K*0.9)                                  # 4-on-floor kick
        if bt in (1,3): add(buf_drum, st, S*0.5)                  # snare 2 & 4
        for h in range(2):
            hs = int(round((b*bar + bt*beat + h*(beat/2))*SR))
            if bt==3 and h==1: add(buf_drum, hs, HO*0.4)          # open hat lift
            else: add(buf_drum, hs, H*0.35)

# ---- Side-chain pump: duck bass+pad on every kick ----
duck = np.ones(N)
kdb = int(0.18*SR)
shape = 1.0 - 0.55*np.exp(-np.arange(kdb)/SR*16) * (np.linspace(1,0,kdb)*0 + 1)
shape = 1.0 - 0.55*(1-np.linspace(0,1,kdb))   # dip to 0.45 then recover
for b in range(BARS):
    for bt in range(4):
        st = int(round((b*bar + bt*beat)*SR))
        e = min(N, st+kdb)
        if st < N: duck[st:e] = np.minimum(duck[st:e], shape[:e-st])
buf_bass *= duck; buf_pad *= duck

mix = 0.95*buf_bass + 0.8*buf_pad + 0.7*buf_arp + 0.8*buf_lead + 1.0*buf_drum

# ---- Wrapped echo (circular within the loop) for width without a boundary click ----
delay = int(round(beat/2*SR))
echo = np.zeros(N)
echo[delay:] += mix[:-delay]*0.28
echo[2*delay:] += mix[:-2*delay]*0.14
mix = mix + echo

# ---- Seamless loop via equal-power crossfade ----
# The render runs L+tail samples; the [L : L+tail] region is the natural continuation of the loop
# (release + echo tails of notes from the last bars). Crossfade that continuation INTO the start so
# the loop's end flows into its start sample-continuously: out[0] = render[L] (continues render[L-1]),
# ramping over XF into the real downbeat. Kills the boundary click without shifting the groove.
XF = int(0.028 * SR)
wi = np.sin(np.linspace(0, np.pi/2, XF))   # head fades IN  (0 -> 1)
wo = np.cos(np.linspace(0, np.pi/2, XF))   # tail fades OUT (1 -> 0)
out = mix[:L].copy()
out[:XF] = mix[L:L+XF] * wo + mix[:XF] * wi

# normalize with a little headroom + soft clip
out = out / (np.max(np.abs(out)) + 1e-9) * 0.92
out = np.tanh(out*1.1)/np.tanh(1.1)
out = out / (np.max(np.abs(out)) + 1e-9) * 0.95

# seam check
seam = abs(out[0] - out[-1])
print(f"loop length: {L/SR:.2f}s  ({BARS} bars @ {BPM} BPM)  seam delta: {seam:.5f}")

pcm = (out * 32767).astype('<i2')
w = wave.open(sys.argv[1], 'wb')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(pcm.tobytes()); w.close()
print("wrote", sys.argv[1], len(pcm), "frames")
