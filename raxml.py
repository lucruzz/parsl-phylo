#!/usr/bin/env python
import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from pathlib import Path

parsl.config.retries = 2
parsl.load(config)

p = Path('.')
phylip = list(p.glob('./results/*.phylip'))
mfMG = sorted(list(p.glob('./results/*.mg.modelFromMG.txt')))

@bash_app
def raxml(phylipfile, mfMGfile, stderr = parsl.AUTO_LOGNAME):
    return 'python $SWIFT_PHYLO/execute_raxml.py ./results {} {} 2 4'.format(phylipfile, mfMGfile)

for i, j in zip(phylip, mfMG):
    print(i, j)
    raxml_future = raxml(i, j)
    raxml_future.result()
