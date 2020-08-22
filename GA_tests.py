# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 10:24:32 2018

@author: Pedro
"""
import generate_individual
import random
from time import time

############### READ DOCUMENT ###############

instances_30 = ['j3029_7.sm', 'j3030_3.sm', 'j3047_4.sm']

instances_60 = ['j606_3.sm', 'j6026_10.sm', 'j6010_5.sm']

instances_90 = ['j9011_4.sm', 'j906_4.sm', 'j9011_10.sm']

instances_301 = ['j3010_10.sm', 'j3029_7.sm', 'j3038_10.sm', 'j3030_3.sm', 'j305_1.sm', 'j3044_7.sm',\
               'j3033_2.sm', 'j304_2.sm', 'j3047_4.sm', 'j3035_10.sm', 'j3043_6.sm', 'j3016_4.sm',\
               'j3022_6.sm', 'j3018_4.sm', 'j3034_5.sm']

instances_601 = ['j606_3.sm', 'j6015_4.sm', 'j6034_2.sm', 'j607_7.sm', 'j6026_10.sm', 'j6019_10.sm',\
             'j6012_7.sm', 'j608_2.sm', 'j6010_5.sm', 'j602_3.sm', 'j6042_10.sm', 'j608_3.sm',\
             'j6014_7.sm', 'j603_4.sm', 'j6024_8.sm']

instances_901 = ['j9017_7.sm', 'j9011_4.sm', 'j9012_6.sm', 'j906_4.sm', 'j901_4.sm', 'j903_9.sm',\
                 'j9011_10.sm', 'j9013_1.sm', 'j902_6.sm', 'j904_4.sm', 'j9010_7.sm', 'j9015_7.sm',\
                 'j9010_10.sm', 'j9017_3.sm', 'j906_6.sm']

iterations = 0
while iterations != 1:
    iterations += 1
    for i in instances_90:
        projeto = open(i, 'r').readlines()
        p = {}
        for i in xrange(1, 93):
            p[i] = []
        for linha in projeto[18:110]:
            p[projeto.index(linha) - 17] = linha.split()
        for j in p.keys():
            p[j] = list(map(int, p[j]))
        activities = p.keys()
        suc = {}
        for i in activities:
            suc[i] = p[i][3:]
        d = {}
        for linha in projeto[114:206]:
            d[projeto.index(linha) - 83] = linha.split()
        for j in d.keys():
            d[j] = list(map(int, d[j]))
        duration = []
        r1_usage = []
        r2_usage = []
        r3_usage = []
        r4_usage = []
        for k in d.keys():
            duration.append(d[k][2])
            r1_usage.append(d[k][3])
            r2_usage.append(d[k][4])
            r3_usage.append(d[k][5])
            r4_usage.append(d[k][6])
        r1_availability = list(map(int, projeto[209].split()))[0]
        r2_availability = list(map(int, projeto[209].split()))[1]
        r3_availability = list(map(int, projeto[209].split()))[2]
        r4_availability = list(map(int, projeto[209].split()))[3]
        horizon = int(projeto[6].split()[-1])
        pred = {}
            
        for i in activities:
            pred[i] = []
            
        for idx, value in enumerate(suc.values()):
            for n in value:
                pred[n].append(idx + 1)

############### GA PARAMETERS ###############

        population_size = 50
        mating_pool = 50
        mutation_rate = 0.1
        crossover_rate = 0.5
        elite_size = 2
        generations = 100

############### GENETIC ALGORITHM ###############

        
        initial_population = generate_individual.initial_population(activities, pred, population_size)
        
        counter = 0
        start_time = time()
        #timeout = time() + 1500
        g_best = []
        
        while counter != generations:
            counter += 1
        
            best = []
            convergence = []
        
            for i in initial_population:
                best.append([generate_individual.fitnessFourResources(i, duration, suc, r1_usage, r2_usage, r3_usage, r4_usage, \
                                                                 r1_availability, r2_availability, r3_availability, r4_availability, horizon)[0][92], i])
            best = sorted(best)
            
            g_best.append(best[0][0])
            
            #for i in best:
                #convergence.append(i[0])
            
            #if convergence.count(convergence[0]) >= 25:
                #end_time = time()
                #break
    
            #end_time = time()
            #if end_time > timeout:
                #break      
    
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
                    crossover = generate_individual.crossover(parent1[1], parent2[1], activities, pred)
                else:
                    crossover = [parent1[1], parent2[1]]
                if random.random() > mutation_rate:
                    child1 = generate_individual.mutation(crossover[0], pred, activities)
                    child2 = generate_individual.mutation(crossover[1], pred, activities)
                else:
                    child1 = crossover[0]
                    child2 = crossover[1]
                next_generation.append(child1)
                next_generation.append(child2)
            
            initial_population = next_generation

        print g_best 





