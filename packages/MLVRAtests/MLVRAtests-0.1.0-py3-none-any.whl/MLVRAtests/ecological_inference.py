import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pymc3 as pm
import pandas

# N = Population
# X = Target Pop as Percentage
# T = Vote Share  
# 0.5 chosen as lmbds defualt to match [King, 1999]
# Z = X as covariate to make [King, 1990]

def ei_2_party_cov(Z, X, T, N, lmbda):
    with pm.Model() as covariate_model: 
        p = len(X)
        Tprime_obs = T * N
        
        alp = pm.Flat('alp')
        bet = pm.Flat('bet')
        gam = pm.Flat('gam')
        dlt = pm.Flat('dlt')
        
        d_1 = pm.Exponential('d_1', lmbda)
        d_2 = pm.Exponential('d_2', lmbda)

        c_1 = d_1*pm.math.exp(alp + bet*Z)
        c_2 = d_2*pm.math.exp(gam + dlt*Z)
    
        b_1 = pm.Beta('b_1', alpha = c_1, beta = d_1, shape=p)
        b_2 = pm.Beta('b_2', alpha = c_2, beta = d_2, shape=p)
    
        theta = X * b_1 + (1 - X) * b_2
        Tprime = pm.Binomial('Tprime', n=N , p=theta, observed=Tprime_obs)
    
    return covariate_model

def ecological_inference(Total_Population_Col, Target_Population_Col, 
                        Target_Vote_Share_Percentage, covariate=None, lmbda=0.5):
    if not covariate:
        covariate = Target_Population_Col
    model = ei_2_party_cov(Z=covariate, X=Target_Population_Col,T=Target_Vote_Share_Percentage,N=Total_Population_Col,lmbda=lmbda)
    with model:
        model_trace = pm.sampling.sample(progressbar=False)
    return model_trace