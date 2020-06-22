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

@bash_app
def modelgenerator(infile, stdout, stderr = parsl.AUTO_LOGNAME):
    return 'java -jar $SWIFT_PHYLO/modelgenerator.jar {} 6'.format(infile, stdout)

for i in phylip:
    outfile = './results/{}.mg'.format(i.stem)
    modelgenerator_future =  modelgenerator(i, stdout = outfile)
modelgenerator_future.result()
