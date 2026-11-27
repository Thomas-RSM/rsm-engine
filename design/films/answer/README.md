# Be the answer (30 seconds)

`film.html` is the film: one SVG stage driven by `renderAt(t)`. `render.js` steps it at 30 frames a second
with Playwright and writes `frames/`; ffmpeg turns the frames into `site/assets/film-answer.mp4` and `.webm`.

    node render.js
    ffmpeg -framerate 30 -i frames/f%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 22 -movflags +faststart -an ../../../site/assets/film-answer.mp4

Sam is a drawing, not a client. No voice, no stock footage; captions are in `site/assets/film-answer.vtt`.
