"""figures.py -> runs figures.js, then writes a WebP beside every PNG and shrinks the PNG (used as the share image)."""
import os, subprocess, glob
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); subprocess.run(['node', os.path.join(D, 'figures.js')], check=True)
tot = 0
for f in sorted(glob.glob(os.path.join(D, '..', 'rsm-theme', 'assets', 'fig', '*.png'))):
    im = Image.open(f).convert('RGB'); im.save(f[:-4] + '.webp', 'WEBP', quality=82, method=6)
    im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(f, optimize=True); tot += os.path.getsize(f[:-4] + '.webp')
print('webp total %d KB' % (tot // 1024))
