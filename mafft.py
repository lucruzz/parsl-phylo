#!/usr/bin/env python
import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from pathlib import Path

parsl.config.retries = 2
parsl.load(config)

p = Path('.')
fastanumbered = list(p.glob('./intermediate_files/*.fastaNumbered'))

@bash_app
def MAFFT(infile, stdout, stderr = parsl.AUTO_LOGNAME):
    return 'mafft {} > {}'.format(infile, stdout)

for i in fastanumbered:
    outfile = './intermediate_files/{}.mafft'.format(i.stem)
    mafft_future =  MAFFT(i, stdout = outfile)
mafft_future.result()
