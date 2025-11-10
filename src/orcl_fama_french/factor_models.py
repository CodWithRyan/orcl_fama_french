import pandas as pd
import numpy as np 
import statsmodels.api as sm


def create_regression_model(data, model):
    """Create FF3 or FF5 regression model"""
    import statsmodels.api as sm
    
    model_factors = {
        'FF3': ['Mkt-RF', 'SMB', 'HML'],
        'FF5': ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
    }
    
    if model not in model_factors:
        raise ValueError(f"Invalid model: '{model}'")
    
    factors = model_factors[model]
    y = data['orcl_excess_returns']
    X = sm.add_constant(data[factors])
    
    return sm.OLS(y, X).fit()

def cal_exp_ret(reg, data, model, trading_days=252):
    """Calculate expected return for FF3 or FF5"""
    model_factors = {
        'FF3': ['Mkt-RF', 'SMB', 'HML', 'RF'],
        'FF5': ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']
    }
    
    if model not in model_factors:
        raise ValueError(f"Invalid model: {model}")
    
    required = model_factors[model]
    
    # Validation
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise KeyError(f"Missing columns: {missing}")
    if len(data) == 0:
        raise ValueError("DataFrame is empty")
    
    # Annualised alpha
    alpha_daily = reg.params['const']
    alpha_annualised = ((alpha_daily / 100 + 1) ** trading_days - 1)
    
    # annualised returns
    gross = (data[required].astype(float) / 100 + 1).cumprod().iloc[-1]
    annualised_ret = gross ** (trading_days / len(data)) - 1
    
    # Expected Return
    er = alpha_annualised + float(annualised_ret['RF'])
    
    # Add factors
    factors = [f for f in required if f != 'RF']
    for factor in factors:
        er += reg.params[factor] * float(annualised_ret[factor])
    
    return er








