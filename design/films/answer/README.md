# Be the answer (58 seconds, narrated)

- `film.html`: the film, one SVG stage driven by `renderAt(t)`. Scene timings come from `timeline.json`.
- `gen-narration.py <voice spec> <out> [speed]`: synthesises the ten narration lines with Kokoro
  (kokoro-onnx, model v1.0, Apache 2.0) and writes the wav and the timeline. The film uses a blend,
  `am_michael:0.55+am_onyx:0.45` at speed 0.93: a measured narrator with a deeper register.
- `render.js`: steps the film at 30 frames a second with Playwright into `frames/`.

    node render.js
    ffmpeg -framerate 30 -i frames/f%05d.jpg -i narr.wav -af loudnorm -c:v libx264 -pix_fmt yuv420p -crf 23 -c:a aac -movflags +faststart ../../../site/assets/film-answer.mp4

Sam is a drawing, not a client. The narrator is a synthetic voice and is not Thomas. Captions: `site/assets/film-answer.vtt`.
Voice: Kokoro-82M (Apache 2.0).
