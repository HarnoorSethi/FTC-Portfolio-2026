"""usage: python3 bf_run.py <module> [func ...]   -> builds that module's page functions to /tmp/work/out/bf_<module>_<func>.png
each page function has signature  f(D)  and must call D.page(...) exactly once"""
import sys, importlib
sys.path.insert(0, '/tmp/work/build')
from pf import *
import pf
mod = importlib.import_module(sys.argv[1])
funcs = sys.argv[2:] or [n for n in dir(mod) if n.startswith('page_') and n[5:].isdigit()]
D = Deck()
for fn in funcs:
    getattr(mod, fn)(D)
for i, pg in enumerate(D.pages):
    pg.img.save('/tmp/work/out/bf_%s_%s.png' % (sys.argv[1], funcs[i]))
print('\n'.join(pf.WARN) or 'no overflow warnings')
ov = check_overlaps(D); print('\n'.join(ov) or 'no overlaps')
D.save('/tmp/work/out/bf_%s.pptx' % sys.argv[1])
