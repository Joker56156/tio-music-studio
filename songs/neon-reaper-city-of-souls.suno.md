# NEON REAPER (City Of Souls) — TIO Suno V5.5 Package

House-spec rebuild for **Suno V5.5, Custom Mode, cloned Default voice**. Follows
the TIO Expanded Structure, 808 front-loaded, anchor repeat before negatives,
cadence variance per verse, whispered/`[echoing]` breakdown with a thesis anchor,
and a final-hook word-flip.

Lane: horrorcore-tinged dark trap / dark cyber-phonk. Concept POV flips from
*the reaper harvests the city* → *the city wakes up and unplugs the reaper*.

---

## STYLE PROMPT  (Suno "Style of Music" box)

```
Dark cyber-phonk, horrorcore-tinged dark trap, distorted 808 sub-bass, 66 BPM half-time, menacing nocturnal glitch-dread, RGB-split glitch hi-hats, eerie detuned synth bells, chopped pitched-down vocal samples, neon-city sirens, gradual downward pitch drift, dubby cathedral reverb, rap-to-sing switching, cinematic cyber-horror phonk, no autotune, no falsetto, no clean vocals
```

*Anchor: "Dark cyber-phonk" (start) → "cinematic cyber-horror phonk" (end), before negatives. 808 named right after the genre pair.*

---

## LYRICS  (Suno "Lyrics" box, Custom Mode)

```
[Instrumental Intro]
[Deep sub-bass rumble, distant sirens, rain on neon, RGB-split hats fading in]

[Hook]
[Distorted 808 drop, pitched-down chopped vocal chant]
[Half-time, heavy reverb on vocal tail]
Neon reaper (reaper), glitchin' through your dreams
Nothin' in this city's ever what it seems
Souls in every window but they never hear the screams
Neon reaper (reaper) — paint it, tear the seams

[Verse 1]
[Rapped, slow menacing flow]
[half-time]
Pink phantom on the skyline, low glow
Antenna horns pick the signal from your soul
Death don't dress in black no more
It's bathed in neon, knockin' door to door
[double-time]
Towers start to tremble when I manifest
RGB corruption bleedin' through the mess
Magenta on the reaper, chromatic and possessed
They wanted somethin' brighter — here's the blight, I guess
[half-time]
Every heartbeat's a download in the red
Every soul a file I already read
Meter tickin' backwards in your chest
Sleep is just the buffer 'fore the rest

[Hook]
[Distorted 808 drop, pitched-down chopped vocal chant]
Neon reaper (reaper), glitchin' through your dreams
Nothin' in this city's ever what it seems
Souls in every window but they never hear the screams
Neon reaper (reaper) — paint it, tear the seams

[Verse 2]
[Rapped, deeper pitched-down delivery]
[double-time]
Corruption in the concrete, digital decay
Pixel bones and fractal horns lightin' up the prey
404 on your future, I'm the error in the way
Reaper-dot-exe when the streetlights fray
[half-time]
Death became a filter, death became a trend
Upload your confession, hit the void, ascend
[double-time]
Press start to keep breathin', but the continue's dead
Static for a halo, neon 'round my head
Screens keep glowin' while the real ones fade
Everybody's ghostin', that's the life they made
[half-time]
I don't make the hunger, I'm just what it fed
The city built the reaper, now it sleeps in dread

[Breakdown]
[whispered]
[echoing]
We built the glow that eats us

Coded our own reaper

Prayed to the screen that reaps us

[Build]
[Rising sub-bass, filtered snare roll, hats accelerating, pitch climbing]
[chant, layered]
Louder... louder... the signal's breakin' through
Louder... louder... the city's comin' to

[Drop]
[Massive distorted 808 slide, beat drops, glitch stutter]
[shouted, tight]
Reaper in RGB — I paint the whole block red
Reaper in RGB — livin' rent-free in your head

[Verse 3]
[Rapped, aggressive]
[half-time]
But somethin' in the wires start to fight
A pulse that don't flatline under the light
[double-time]
Kids of the static learnin' how to see
Unplug the halo, break the frequency
[half-time]
Reaper on the run now, the mask start to crack
The souls that I collected all be linkin' back
They found the source code, found the human thread
Turns out the reaper's just a fear they fed

[Verse 4]
[Rap-to-sing switching, building]
[half-time]
So look up from the glow, feel your own heartbeat
Realer than a reaper, realer than the feed
[double-time]
Every borrowed hour that they tried to reap
Belongs to the livin', and the livin' don't sleep
[half-time]
Magenta start to fade to the mornin' blue
Turns out the city's soul was always you
Neon on the reaper flickerin' out
This is what the light was really about

[Final Hook]
[Distorted 808, layered chant, cathartic]
Neon reaper (reaper), glitchin' outta my dreams
Everything's exactly what it seems
City full of souls and now they hear the screams
Neon reaper (reaper) — we sew it, mend the seams

[Outro]
[whispered, distant]
The city never sleeps...
[echoing] but neither do the ones who woke up
[Fade Out]
```

*Final-hook word-flip: "through your dreams" → "outta my dreams"; "nothin' is what it seems" → "everything's exactly what it seems"; "never hear the screams" → "now they hear"; "tear the seams" → "mend the seams."*

---

## SUNO SETTINGS

- **Mode:** Custom · **Model:** V5.5
- **Instrumental:** OFF (vocal track)
- **Voice:** Default (cloned TIO voice) · **Custom Model:** None
- **Explicit:** clean — no explicit tag needed
- **Strategy:** generate 4–5 versions, pick best. If words crowd at 66 BPM,
  bump to **84–88 BPM half-time** — keeps the same slow, heavy felt tempo but
  gives the dense verses room (house rule for dense-lyric tracks).
- **If short of 3:30:** Extend from `[Outro]` with
  `[Callback: continue same dark cyber-phonk groove and pitched-down vocal character]`.
- Watch the `[Drop]` beat-switch and the Verse-3 mask-crack turn; reinforce with
  `[Vocal Style: Aggressive Rapped]` if the shift flattens.

---

### What changed vs. the earlier ACE-Step preset
- Rebuilt to the **TIO Expanded Structure** with full verse minimums (V1/V2 = 12,
  V3/V4 = 8) instead of the short 2-verse cut.
- Added **cadence variance** (`[double-time]`/`[half-time]`) inside every verse.
- Added a **thesis-anchored breakdown** ("We built the glow that eats us") in
  `[whispered]`+`[echoing]` brackets, max 3 lines, max spacing.
- Gave it the missing **narrative + word-flip**: the reaper is revealed as the
  city's own fear, and the final hook flips every hook line into resolution.
- Re-ordered the style box to house spec: **808 immediately after the genre
  pair, anchor repeat, negatives last**, cloned-voice lane exclusions.
