#!/usr/bin/env python
import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from pathlib import Path

parsl.config.retries = 2
parsl.load(config)

p = Path('.')
fasta = list(p.glob('./input/ORTHO*'))   
fastaNumbered, ma, phylip, mg, mfMG = [], [], [], [], []
k = 0

@bash_app
def fastanumbered(in_file, stderr = parsl.AUTO_LOGNAME, stdout = './intermediate_files/{}.fastaNumbered'.format(parsl.AUTO_LOGNAME)):
    return 'fastaNumbered {} {}'.format(in_file, stdout)

@bash_app
def mafft(in_file, stderr = parsl.AUTO_LOGNAME, stdout = './intermediate_files/{}.mafft'.format(parsl.AUTO_LOGNAME)):
    return 'mafft {} > {}'.format(in_file, stdout)

@bash_app
def readseq(in_file, stderr = parsl.AUTO_LOGNAME, stdout = './results/{}.phylip'.format(parsl.AUTO_LOGNAME)):
    return 'readseq {} {}'.format(in_file, stdout)

@bash_app
def modelgenerator(in_file, stderr = parsl.AUTO_LOGNAME, stdout = './results/{}.mg'.format(parsl.AUTO_LOGNAME)):
    return 'modelgenerator {} {}'.format(in_file, stdout)

@bash_app
def cleanModelgenerator(in_file, stderr = parsl.AUTO_LOGNAME):
    return 'cleanModelgenerator {}'.format(in_file)

@bash_app
def raxml(phylip_file, mfMG_file, stderr = parsl.AUTO_LOGNAME):
    return 'raxml {} {} 2 4'.format(phylip_file, mfMG_file)

for i in fasta:
    fastaNumbered_future =  fastanumbered(i)
    fastaNumbered_future.result()
    src = Path('./intermediate_files/-1.fastaNumbered')
    dst = Path('./intermediate_files/{:0>4}.fastaNumbered'.format(k))
    os.rename(src, dst)
    fastaNumbered.append(dst)

    mafft_future = mafft(fastaNumbered[k])
    mafft_future.result()
    src = Path('./intermediate_files/-1.mafft')
    dst = Path('./intermediate_files/{:0>4}.mafft'.format(k))
    os.rename(src, dst)
    ma.append(dst)

    phylip_future = readseq(ma[k])
    phylip_future.result()
    src = Path('./results/-1.phylip')
    dst = Path('./results/{:0>4}.phylip'.format(k))
    os.rename(src, dst)
    phylip.append(dst)

    mg_future = modelgenerator(phylip[k])
    mg_future.result()
    src = Path('./results/-1.mg')
    dst = Path('./results/{:0>4}.mg'.format(k))
    os.rename(src, dst)
    mg.append(dst)

    mfMG_future = cleanModelgenerator(mg[k])
    mfMG_future.result()
    dst = Path('./results/{:0>4}.mg.modelFromMG.txt'.format(k))
    mfMG.append(dst)
    
    r_future = raxml(phylip[k], mfMG[k])
    r_future.result()
    k = k + 1
