#!/usr/bin/env python
import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from pathlib import Path

parsl.config.retries = 2
parsl.load(config)

p = Path('.')
mafft = list(p.glob('./intermediate_files/*.mafft'))

@bash_app
def readseq(infile, stdout, stderr = parsl.AUTO_LOGNAME):
    return 'java -jar $SWIFT_PHYLO/readseq.jar -all -f=12 {0} -o {1}'.format(infile, stdout)

for i in mafft:
    outfile = './results/{}.phylip'.format(i.stem)
    readseq_future =  readseq(i, stdout = outfile)
readseq_future.result()
