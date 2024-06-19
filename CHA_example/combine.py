import pandas as pd
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

def combine_count_files(prefix, ratios, num, savefileprefix):
    for ratio in ratios:
        results = defaultdict(lambda: [])
        for i in range(1, num+1):
            filename = prefix.format(ratio, i)
            temp = pickle.load(open(filename, 'rb'))
            for t in temp.keys():
                results[t].extend(temp[t])
        pickle.dump(dict(results),open(savefileprefix.format(ratio),'wb'))
    return results 

num=100
ratios = [15]
prefix = 'jobs/count_result_SiAlratio{}_{}.p'
savefileprefix ='jobs/count_result_summary_{}.p'
results = combine_count_files(prefix, ratios, num, savefileprefix)

