# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 10:46:39 2018

@author: Pedro
"""

import random
import math

def generate_individual(act, pred):
    individual = {}
    for i in act:
        individual[i] = 0
    individual[1] = 1
    for j in individual.keys()[1:]:
        l = []
        for k in xrange(2, act[-1] + 1):
            if all(i in individual.values() for i in pred[k]):
                if k not in individual.values():
                    l.append(k)
        individual[j] = random.choice(l)
    return individual.values()

def initial_population(act, pred, size):
    initial_population = []
    for i in xrange(1, size+1):
        initial_population.append(generate_individual(act, pred))
    return initial_population

def fitnessFourResources(ind, D, suc, r1u, r2u, r3u, r4u, r1a, r2a, r3a, r4a, maxD):
    
    pred = {}

    for i in ind:
        pred[i] = []
    
    for idx, value in enumerate(suc.values()):
        for n in value:
            pred[n].append(idx + 1)
    
    start_time_pred = {}
    for i in ind:
        start_time_pred[i] = []
    
    start_time = {}
    start_time[1] = 0
    finish_time = {}
    finish_time[1] = 0
    start_time_pred[1] = 0
    
    for i in ind[1:]:
        if len(pred[i]) == 1:
            start_time_pred[i].append(start_time[pred[i][0]])
            start_time[i] = start_time_pred[i][0] + D[pred[i][0]-1]
            finish_time[i] = start_time[i] + D[i-1]
        else:
            for p in pred[i]:
                start_time_pred[i].append(start_time[p])
                start_time[i] = max(start_time_pred[i]) + \
                D[pred[i][start_time_pred[i].index(max(start_time_pred[i]))]-1]
                finish_time[i] = start_time[i] + D[i-1]
    start_time[start_time.keys()[-1]] = max(start_time.values()[0:-1])
    finish_time[finish_time.keys()[-1]] = max(finish_time.values()[0:-1])
    
    schedule = {}
    schedule[1] = 0
    
    r1_time = {}
    r2_time = {}
    r3_time = {}
    r4_time = {}
    for i in xrange(0, maxD + 1):
        r1_time[i] = 0
        r2_time[i] = 0
        r3_time[i] = 0
        r4_time[i] = 0
    
    fitness = {}
    
    for j in ind:
        K = []
        for k in xrange(start_time[j], maxD + 1):
            r1_time[k] += r1u[j-1]
            r2_time[k] += r2u[j-1]
            r3_time[k] += r3u[j-1]
            r4_time[k] += r4u[j-1]
            if all(i <= r1a for i in r1_time.values()[start_time[j]:finish_time[j] + 1]) and \
             all(i <= r2a for i in r2_time.values()[start_time[j]:finish_time[j] + 1]) and \
             all(i <= r3a for i in r3_time.values()[start_time[j]:finish_time[j] + 1]) and \
             all(i <= r4a for i in r4_time.values()[start_time[j]:finish_time[j] + 1]):
                schedule[j] = start_time[j]
                fitness[j] = finish_time[j]
            else:
                if r1_time[k] > r1a:
                    K.append(k)
                if r2_time[k] > r2a and k not in K:
                    K.append(k)
                if r3_time[k] > r3a and k not in K:
                    K.append(k)
                if r4_time[k] > r4a and k not in K:
                    K.append(k)
                if len(K) == 1:
                    schedule[j] = max(K)
                    fitness[j] = schedule[j] + D[j-1]
                else:
                    for m in K[0:-1]:
                        if K[K.index(m) + 1] - m == 1:
                            schedule[j] = max(K)
                            fitness[j] = schedule[j] + D[j-1]
                        elif 1 < K[K.index(m) + 1] - m < D[j-1]:
                            schedule[j] = max(K)
                            fitness[j] = schedule[j] + D[j-1]
                        elif K[K.index(m) + 1] - m > D[j-1]:
                            schedule[j] = m
                            fitness[j] = schedule[j] + D[j-1]
                            break
        for p in xrange(start_time[j], maxD + 1):
            r1_time[p] -= r1u[j-1]
            r2_time[p] -= r2u[j-1]
            r3_time[p] -= r3u[j-1]
            r4_time[p] -= r4u[j-1]
        for n in xrange(schedule[j], fitness[j] + 1):
            r1_time[n] += r1u[j-1]
            r2_time[n] += r2u[j-1]
            r3_time[n] += r3u[j-1]
            r4_time[n] += r4u[j-1]
        for s in suc[j]:
            if start_time[s] < fitness[j]:
                start_time[s] = fitness[j]
                finish_time[s] = start_time[s] + D[s-1]
    return [schedule, fitness, r1_time, r2_time, r3_time, r4_time, ind]
              
def crossover(ind1, ind2, act, pred):
    
    activities = range(1, act[-1] + 1)

    c1 = {}

    for i in activities:
        c1[i] = 0

    for i in ind1[0:(act[-1]/2)]:
        c1[ind1.index(i) + 1] = i
        if i in activities:
            activities.remove(i)

    for i in ind2[(act[-1]/2):]:
        if i not in c1.values():
            if all(j in c1.values() for j in pred[i]):
                c1[ind2.index(i) + 1] = i
                activities.remove(i)

    for i in c1.keys():
        p = []
        if c1[i] == 0:
            for k in activities:
                if all(j in c1.values()[0:i] for j in pred[k]):
                    if k not in c1.values()[0:i]:
                        p.append(k)
            c1[i] = random.choice(p)
    
    activities2 = range(1, act[-1] + 1)
    
    c2 = {}
    
    for i in activities2:
        c2[i] = 0
    
    for i in ind2[0:(act[-1]/2)]:
        c2[ind2.index(i) + 1] = i
        if i in activities:
            activities2.remove(i)
    
    for i in ind1[(act[-1]/2):]:
        if i not in c2.values():
            if all(j in c2.values() for j in pred[i]):
                c2[ind1.index(i) + 1] = i
                activities2.remove(i)
    
    for i in c2.keys():
        p = []
        if c2[i] == 0:
            for k in activities2:
                if all(j in c2.values()[0:i] for j in pred[k]):
                    if k not in c2.values()[0:i]:
                        p.append(k)
            c2[i] = random.choice(p)
    
    return [c1.values(), c2.values()]

def mutation(ind, pred, act):
    
    m = []
    for i in ind[1:len(act)-1]:
        if i not in pred[ind[ind.index(i) + 1]]:
            m.append(i)
    mposition = ind.index(random.choice(m))
    
    a, b = mposition, mposition + 1
    ind[a], ind[b] = ind[b], ind[a]
    
    return ind

def fitnessLineOfBalance(act, ind, duration, pred, suc, r_availability, Dt, Tm, n):
    
    start_time_pred = {}
    for i in ind:
        start_time_pred[i] = []
        
    start_time = {}
    start_time[1] = 0
    finish_time = {}
    finish_time[1] = 0
    start_time_pred[1] = 0
        
    for i in ind[1:]:
        if len(pred[i]) == 1:
            start_time_pred[i].append(start_time[pred[i][0]])
            start_time[i] = start_time_pred[i][0] + duration[pred[i][0]-1]
            finish_time[i] = start_time[i] + duration[i-1]
        else:
            for p in pred[i]:
                start_time_pred[i].append(start_time[p])
                start_time[i] = max(start_time_pred[i]) + \
                duration[pred[i][start_time_pred[i].index(max(start_time_pred[i]))]-1]
                finish_time[i] = start_time[i] + duration[i-1]
    start_time[start_time.keys()[-1]] = max(start_time.values()[0:-1])
    finish_time[finish_time.keys()[-1]] = max(finish_time.values()[0:-1])
    
    Tb = finish_time[ind[-1]]
    
    Tr = Dt - (Tb + Tm)
    
    R = (n-1)/Tr
    
    r_usage = [0]
    
    for i in duration[1:11]:
        r_usage.append(math.ceil(R*i))
    
    r_usage.append(0)
    
    real_R = {}
    
    real_R[1] = 0
    
    for j in act[1:11]:
        real_R[j] = r_usage[j-1]/duration[j-1]
    
    real_R[act[-1]] = 0
    
    durationLob = {}
    
    durationLob[1] = 0
    
    for k in act[1:11]:
        durationLob[k] = (n-1)/real_R[k]
    
    durationLob[act[-1]] = 0
    
    start_time = {}
    start_time[1] = 0
    finish_time = {}
    finish_time[1] = 0
    start_time_pred = {}
    for i in act:
        start_time_pred[i] = []
    start_time_pred[1] = [0]
    
    for i in ind[1:]:
        if i == ind[1]:
            start_time_pred[i].append(finish_time[pred[i][0]])
            start_time[i] = start_time_pred[i][0]
            finish_time[i] = start_time[i] + durationLob[i] + duration[i-1]
        else:
            if len(pred[i]) == 1:
                start_time_pred[i].append(finish_time[pred[i][0]])
                if real_R[i] >= real_R[pred[i][0]]:
                    start_time[i] = start_time_pred[i][0] - durationLob[i]
                    finish_time[i] = start_time[i] + durationLob[i] + duration[i-1]
                if real_R[i] < real_R[pred[i][0]]:
                    start_time[i] = start_time_pred[i][0] - durationLob[pred[i][0]]
                    finish_time[i] = start_time[i] + durationLob[i] + duration[i-1]
            else:
                for p in pred[i]:
                    start_time_pred[i].append(finish_time[p])
                m = max(start_time_pred[i])
                if real_R[i] >= real_R[pred[i][start_time_pred[i].index(m)]]:
                    start_time[i] = m - durationLob[i]
                    finish_time[i] = start_time[i] + durationLob[i] + duration[i-1]
                if real_R[i] < real_R[pred[i][start_time_pred[i].index(m)]]:
                    start_time[i] = m - durationLob[pred[i][start_time_pred[i].index(m)]]
                    finish_time[i] = start_time[i] + durationLob[i] + duration[-1]
    start_time[start_time.keys()[-1]] = max(start_time.values()[0:-1])
    finish_time[finish_time.keys()[-1]] = max(finish_time.values()[0:-1])                
    
    schedule = {}
    schedule[1] = 0
        
    r_time = {}
    
    for i in xrange(0, Dt + 1):
        r_time[i] = 0
        
    fitness = {}
       
    for j in ind:
        K = []
        for k in xrange(int(start_time[j]), Dt + 1):
            r_time[k] += r_usage[j-1]
            if all(i <= r_availability for i in r_time.values()[int(start_time[j]):int(finish_time[j]) + 1]):
                schedule[j] = start_time[j]
                fitness[j] = finish_time[j]
            else:
                if r_time[k] > r_availability:
                    K.append(k)
                if len(K) == 1:
                    schedule[j] = max(K) + 1
                    fitness[j] = schedule[j] + durationLob[j] + duration[j-1]
                else:
                    for m in K[0:-1]:
                        if K[K.index(m) + 1] - m == 1:
                            schedule[j] = max(K) + 1
                            fitness[j] = schedule[j] + durationLob[j] + duration[j-1]
                        elif 1 < K[K.index(m) + 1] - m < durationLob[j]:
                            schedule[j] = max(K) + 1
                            fitness[j] = schedule[j] + durationLob[j] + duration[j-1]
                        elif K[K.index(m) + 1] - m > durationLob[j]:
                            schedule[j] = m + 1
                            fitness[j] = schedule[j] + durationLob[j] + duration[j-1]
                            break
        for p in xrange(int(start_time[j]), Dt + 1):
            r_time[p] -= r_usage[j-1]
        for n in xrange(int(schedule[j]), int(fitness[j]) + 1):
            r_time[n] += r_usage[j-1]
        for s in suc[j]:
            if start_time[s] < fitness[j]:
                if real_R[s] >= real_R[j]:
                    start_time[s] = fitness[j] - durationLob[s]
                    finish_time[s] = start_time[s] + durationLob[s] + duration[s-1]
                elif real_R[s] < real_R[j]:
                    start_time[s] = fitness[j] - durationLob[j]
                    finish_time[s] = start_time[s] + durationLob[s] + duration[s-1]
    schedule[schedule.keys()[-1]] = max(schedule.values()[0:-1])
    fitness[fitness.keys()[-1]] = max(fitness.values()[0:-1])
    
    return [schedule, fitness, r_time, real_R, durationLob, ind]

def fitnessOneResource(ind, D, suc, r1u, r1a, maxD):
    
    pred = {}

    for i in ind:
        pred[i] = []
    
    for idx, value in enumerate(suc.values()):
        for n in value:
            pred[n].append(idx + 1)
    
    start_time_pred = {}
    for i in ind:
        start_time_pred[i] = []
    
    start_time = {}
    start_time[1] = 0
    finish_time = {}
    finish_time[1] = 0
    start_time_pred[1] = 0
    
    for i in ind[1:]:
        if len(pred[i]) == 1:
            start_time_pred[i].append(start_time[pred[i][0]])
            start_time[i] = start_time_pred[i][0] + D[pred[i][0]-1]
            finish_time[i] = start_time[i] + D[i-1]
        else:
            for p in pred[i]:
                start_time_pred[i].append(start_time[p])
                start_time[i] = max(start_time_pred[i]) + \
                D[pred[i][start_time_pred[i].index(max(start_time_pred[i]))]-1]
                finish_time[i] = start_time[i] + D[i-1]
    start_time[start_time.keys()[-1]] = max(start_time.values()[0:-1])
    finish_time[finish_time.keys()[-1]] = max(finish_time.values()[0:-1])
    
    schedule = {}
    schedule[1] = 0
    
    r1_time = {}
    for i in xrange(0, maxD + 1):
        r1_time[i] = 0
    
    fitness = {}
    
    for j in ind:
        K = []
        for k in xrange(start_time[j], maxD + 1):
            r1_time[k] += r1u[j-1]
            if all(i <= r1a for i in r1_time.values()[start_time[j]:finish_time[j] + 1]):
                schedule[j] = start_time[j]
                fitness[j] = finish_time[j]
            else:
                if r1_time[k] > r1a:
                    K.append(k)
                if len(K) == 1:
                    schedule[j] = max(K)
                    fitness[j] = schedule[j] + D[j-1]
                else:
                    for m in K[0:-1]:
                        if K[K.index(m) + 1] - m == 1:
                            schedule[j] = max(K)
                            fitness[j] = schedule[j] + D[j-1]
                        elif 1 < K[K.index(m) + 1] - m < D[j-1]:
                            schedule[j] = max(K)
                            fitness[j] = schedule[j] + D[j-1]
                        elif K[K.index(m) + 1] - m > D[j-1]:
                            schedule[j] = m
                            fitness[j] = schedule[j] + D[j-1]
                            break
        for p in xrange(start_time[j], maxD + 1):
            r1_time[p] -= r1u[j-1]
        for n in xrange(schedule[j], fitness[j] + 1):
            r1_time[n] += r1u[j-1]
        for s in suc[j]:
            if start_time[s] < fitness[j]:
                start_time[s] = fitness[j]
                finish_time[s] = start_time[s] + D[s-1]
    return [schedule, fitness, r1_time,  ind]   