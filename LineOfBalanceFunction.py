# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 09:33:20 2019

@author: Pedro
"""

import generate_individual
from time import time
import random
import datetime
import pandas as pd


act = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

duration = [0, 2, 1, 4, 1, 1, 1, 1, 2, 2, 1, 0]

pred = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}

suc = {1: [2], 2: [3], 3: [4], 4: [5, 7, 8, 9], 5: [6], 6: [10], 7: [10], 8: [10], 9: [10], 10: [11], 11: [12], 12: []}

for idx, value in enumerate(suc.values()):
    for n in value:
        pred[n].append(idx + 1)

ind = generate_individual.generate_individual(act, pred)

Dt = 4*22

Tm = 10

n = 9.

r_availability = 5

############### GA PARAMETERS ###############

population_size = 10
mating_pool = 10
mutation_rate = 0.1
crossover_rate = 0.5
elite_size = 2
generations = 20

############### GENETIC ALGORITHM ###############

        
initial_population = generate_individual.initial_population(act, pred, population_size)
        
counter = 0
start_time = time()
timeout = time() + 500
        
while counter != generations:
    counter += 1
        
    best = []
    convergence = []
        
    for i in initial_population:
        best.append([generate_individual.fitnessLineOfBalance(act, i, duration,pred, suc, r_availability, Dt, Tm, n)[1][12], i])
    best = sorted(best)
            
    for i in best:
        convergence.append(i[0])
            
    if convergence.count(convergence[0]) >= 15:
        end_time = time()
        break
    
    end_time = time()
    if end_time > timeout:
        break      
    
    next_generation = []
        
    for i in best[0:elite_size]:
        next_generation.append(i[1])
        
    while len(next_generation) != mating_pool:
        tournament1 = random.choice(best)
        tournament2 = random.choice(best)
        parent1 = min(tournament1, tournament2)
        tournament3 = random.choice(best)
        tournament4 = random.choice(best)
        parent2 = min(tournament3, tournament4)
        if random.random() > crossover_rate:
            crossover = generate_individual.crossover(parent1[1], parent2[1], act, pred)
        else:
            crossover = [parent1[1], parent2[1]]
        if random.random() > mutation_rate:
            child1 = generate_individual.mutation(crossover[0], pred, act)
            child2 = generate_individual.mutation(crossover[1], pred, act)
        else:
            child1 = crossover[0]
            child2 = crossover[1]
        next_generation.append(child1)
        next_generation.append(child2)
            
        initial_population = next_generation

print counter, end_time - start_time, best

lineOfBalance = generate_individual.fitnessLineOfBalance(act, best[0][1], duration, pred, suc, r_availability, Dt, Tm, n)
start = lineOfBalance[0]
finish = lineOfBalance[1]
real_R = lineOfBalance[3]
durationLob = lineOfBalance[4]

usage = lineOfBalance[2]

startLob = {}
finishLob = {}

RLob = real_R.values()

DLob = duration[1:11]

for i in start.keys()[0:len(act)-1]:
    startLob[i] = float(start[i+1])

for i in xrange(2, int(n)+1):
    for j in xrange(1, len(act)-1):
        startLob[j + (len(act)-2)*(i-1)] = startLob[j] + (i-1)/RLob[j]

for i in start.keys()[0:len(act)-1]:
    finishLob[i] = startLob[i] + duration[i]

for i in xrange(2, int(n)+1):
    for j in xrange(1, len(act)-1):
        finishLob[j + (len(act)-2)*(i-1)] = int(finishLob[j] + (i-1)/RLob[j])

sucLob = {}

for i in startLob.keys():
    startLob[i] = int(startLob[i])
    finishLob[i] = int(finishLob[i])

for i in xrange(len(startLob.keys())+1, len(startLob.keys())+len(act)-1):
    startLob[i] = finishLob[i - len(act) + 2]
    finishLob[i] = startLob[i]
now = datetime.datetime.today()

dic0 = startLob
dic1 = finishLob
dic2 = {}
for i in dic0.keys():
    d = []
    start_date = now + datetime.timedelta(days=dic0[i])
    finish_date = now + datetime.timedelta(days=dic1[i])
    dic2[i] = [start_date.strftime("%d/%m/%Y"), finish_date.strftime("%d/%m/%Y")]

d = pd.DataFrame(dic2, index=['START TIME', 'FINISH TIME']).T
d.to_csv('output.csv')
