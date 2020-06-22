#!/usr/bin/env python
import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from pathlib import Path

parsl.config.retries = 2
parsl.load(config)

p = Path('.')
modelgenerator = list(p.glob('./results/*.mg'))

@bash_app
def cleanModelgenerator(infile, stderr = parsl.AUTO_LOGNAME):
    return 'python $SWIFT_PHYLO/clean_modelgenerator.py {}'.format(infile)

for i in modelgenerator:
    mfMG_future =  cleanModelgenerator(i)
mfMG_future.result()
