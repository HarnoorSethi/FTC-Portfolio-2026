import build2 as build
from pf import WARN, check_overlaps, check_text_on_images
D=build.D
for i,pg in enumerate(D.pages):
    pg.img.save(f'/tmp/work/out/v2_{i:02d}.png')
D.save('/tmp/work/out/portfolio2.pptx')
print(len(D.pages),'pages'); print('\n'.join(WARN) or 'no overflow warnings')
ov=check_overlaps(D); print('\n'.join(ov) or 'no overlaps')
print('\n'.join(check_text_on_images(D)) or 'no text-on-image')
