#!/opt/local/bin/python
# module power iteration clustering

import numpy as NP
from scipy.cluster.vq import kmeans2

def calcNorm1(v):
    return NP.sum(NP.fabs(v))

def calcDelta(v,v2):
    return NP.sum(NP.fabs(v2-v))

def normalize(v):
    max=v.max()
    min=v.min()
    return (v-min)/(max-min)

def initVector(m):
    n=m.shape[0]
    ovec=NP.matrix(NP.ones(n)).T
    v=m*ovec
    sinv=1.0/NP.sum(v)
    return v*sinv

def pic(a, maxiter, eps):
    m = NP.matrix(a)
    d1 = NP.matrix(NP.diag(a.sum(0))).I
    w = d1*m
    n=w.shape[0]
    v=initVector(m)
    for i in range(maxiter):
        v2=w*v
        ninv=1.0/calcNorm1(v2)
        v2*=ninv
        delta=calcDelta(v,v2)
        v=v2
        if (delta*n)<eps:
            break
    return normalize(v)