"""assemble the 16 ByteForce-replica pages -> pptx + preview pdf"""
import sys, importlib
sys.path.insert(0, '/tmp/work/build')
from pf import *
import pf
D = Deck()
mods = {1: 'bfp_A', 2: 'bfp_A', 3: 'bfp_A', 4: 'bfp_B', 5: 'bfp_B', 6: 'bfp_B', 7: 'bfp_C', 8: 'bfp_C', 9: 'bfp_C',
        10: 'bfp_D', 11: 'bfp_D', 12: 'bfp_D', 13: 'bfp_E', 14: 'bfp_E', 15: 'bfp_F', 16: 'bfp_F'}
for n in range(1, 17):
    m = importlib.import_module(mods[n])
    getattr(m, 'page_%02d' % n)(D)
OUT = '/tmp/work/out/'
for i, pg in enumerate(D.pages):
    pg.img.save(OUT + 'v3_%02d.png' % (i + 1))
for _sl in D.prs.slides:
    for _sh in _sl.shapes:
        if _sh.left is not None and _sh.left + _sh.width > D.prs.slide_width:
            _sh.width = D.prs.slide_width - _sh.left
D.save(OUT + 'portfolio3.pptx')
print(len(D.pages), 'pages')
print('\n'.join(pf.WARN) or 'no overflow warnings')
print('\n'.join(check_overlaps(D)) or 'no overlaps')
from PIL import Image
ims = [Image.open(OUT + 'v3_%02d.png' % i).convert('RGB') for i in range(1, 17)]
ims[0].save(OUT + 'preview3.pdf', save_all=True, append_images=ims[1:], resolution=144)
