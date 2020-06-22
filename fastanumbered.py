#!/usr/bin/env python
import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from pathlib import Path

parsl.config.retries = 2
parsl.load(config)

p = Path('.')
fasta = list(p.glob('./ORTHOMCL*'))

@bash_app
def fastanumbered(infile, stdout, stderr = parsl.AUTO_LOGNAME):
    return 'perl $SWIFT_PHYLO/numberFasta.pl {} > {}'.format(infile, stdout)

for i in fasta:
    outfile = './intermediate_files/{}.fastaNumbered'.format(i.stem[8:])
    fastaNumbered_future =  fastanumbered(i, stdout = outfile)
fastaNumbered_future.result()
