# Be the answer (57 seconds, narrated)

- `film.html`: the film, one SVG stage driven by `renderAt(t)`. Scene timings come from `timeline.json`.
- `gen-narration.py <speaker> <out>`: synthesises the ten narration lines with Piper and writes the
  wav and the timeline. Voice: Piper `en-us-libritts-high`, speaker 198 (LibriTTS, CC BY 4.0, so
  commercial use is allowed with attribution; the non-commercial Ryan voice was rejected for that reason).
- `render.js`: steps the film at 30 frames a second with Playwright into `frames/`.

    node render.js
    ffmpeg -framerate 30 -i frames/f%05d.jpg -i narr.wav -af loudnorm -c:v libx264 -pix_fmt yuv420p -crf 23 -c:a aac -movflags +faststart ../../../site/assets/film-answer.mp4

Sam is a drawing, not a client. The narrator is a synthetic voice and is not Thomas. Captions: `site/assets/film-answer.vtt`.
Voice attribution: LibriTTS corpus (Zen et al., 2019), CC BY 4.0, via the Piper project.
