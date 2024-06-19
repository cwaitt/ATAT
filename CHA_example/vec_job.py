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

Al_num = int(round(1/(1+{0})*972)) # 972-T CHA supercell. eg: Si/Al=15, Al_num = int(round(1/(1+15)*972)) = 60.
num_vecs = 100 # 100 vectors in this jobs
num_steps = 5000 # swap 5000 times for each vector

str_vecs = structure.random_config_swap(atom_num=Al_num, penalty=penalty, num_vecs=num_vecs, num_step=num_steps) # do the swapping
    
pickle.dump(str_vecs, open('str_vecs_no1NN_SiAlratio{0}_{1}.p','wb')) # save the results

'''
qscript_template = '''#!/bin/bash
#$ -q long
#$ -pe smp 1
#$ -t 1-100
#$ -l h=!q16copt*

python J_{0}_$SGE_TASK_ID.py
'''

ratios = [3,5,7,10,15,20,25,30,35,40] # Si/Al ratio

for ratio in ratios:
    for i in range(0,101):
        filename = 'jobs/J_{}_{}.py'.format(ratio,i) # generate 100 python files, each file has 100 vectors in it, that's how we generate 10,000 vectors parallelly.
        with open(filename, 'w+') as file:
            file.write(py_template.format(ratio,i))
    filename =  'jobs/J_{}.sh'.format(ratio) # generate a job array script to submit the 100 python jobs.
    with open(filename, 'w+') as file:
        file.write(qscript_template.format(ratio,i))    
