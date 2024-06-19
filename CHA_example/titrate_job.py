py_template = '''import pandas as pd
import numpy as np
import copy
from math import *
import os
import random
from collections import defaultdict
import csv
from functools import reduce
from copy import deepcopy
import pickle
from timeit import default_timer as timer
from matplotlib import pyplot as plt
from ase import Atoms
from ase.io import read
from ase.io import write
from ase.visualize import view
import itertools
import time

from utilities import *
from classes import *

lattice=pickle.load(open('lattice.p','rb'))
structure=pickle.load(open('structure.p','rb'))
penalty=pickle.load(open('penalty.p', 'rb'))

str_vecs = pickle.load(open('str_vecs_no1NN_SiAlratio{0}_{1}.p','rb')) # load the vectors we just generated
titration_groups=[['2-11','2-7'],['2-8','2-9','2-15','2-18','2-19','2-20','2-21']] # pairs you want to tirate
titration_results=structure.titrate_clusters_multi_configs(str_vecs, titration_groups= titration_groups,titrate_num=1,hist=1) # titrate
pickle.dump(titration_results, open('titration_results_{0}_{1}.p','wb')) # save the results

'''
qscript_template = '''#!/bin/bash
#$ -q long
#$ -pe smp 1
#$ -t 1-100
#$ -l h=!q16copt*

python TJ_{0}_$SGE_TASK_ID.py
'''
ratios = [3,5,7,10,15,20,25,30,35,40]
for ratio in ratios:
    for i in range(1,101):
        filename = 'jobs/TJ_{}_{}.py'.format(ratio,i) # generate 100 python files, each file is corresponding to each vector file.
        with open(filename, 'w+') as file:
            file.write(py_template.format(ratio,i))
    filename =  'jobs/TJ_{}.sh'.format(ratio) # generate a job array script to submit the 100 python jobs.
    with open(filename, 'w+') as file:
        file.write(qscript_template.format(ratio,i))    
