import pandas as pd
import numpy as np
import statsmodels.api as sm

def cal_rolling_beta(df, model, window=252, min_periods=126, trading_days=252):
    """Calculate Rolling Betas for FF3 & FF5 model"""
    model_factors = {
        'FF3': ['Mkt-RF', 'SMB', 'HML'],
        'FF5': ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
    }
    if model not in model_factors:
        raise ValueError(f"Invalid model: '{model}'")
    
    required = model_factors[model]
    all_required = required + ['orcl_excess_returns']
    missing = [c for c in all_required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns: '{missing}'")
    
    rolling_results = []

    for i in range(len(df)):
        start = max(0, i - window + 1)
        end = i + 1
        window_df = df.iloc[start:end]

        if len(window_df) < min_periods:
            result = {f'Beta_{factor}': np.nan for factor in required}
            result['Alpha'] = np.nan
            result['R2'] = np.nan
            rolling_results.append(result)
            continue

        y = window_df['orcl_excess_returns']
        X = sm.add_constant(window_df[required])

        try:

            reg_model = sm.OLS(y, X).fit()
            result = {}
            for factor in required:
                result[f'Beta_{factor}'] = reg_model.params[factor]
            result['Alpha'] = reg_model.params['const']
            result['R2'] = reg_model.rsquared
            
            rolling_results.append(result)

        except Exception as e :
            result = {f'Beta_{factor}': np.nan for factor in required}
            result['Alpha'] = np.nan
            result['R2'] = np.nan
            rolling_results.append(result)

    df_rolling = pd.DataFrame(rolling_results, index=df.index)
    df_rolling = df_rolling.rename(columns={
        'Alpha': f'Alpha_{model}',
        'R2': f'R2_{model}'
    })

    factor_returns = {}
    for factor in required + ['RF']:  
        gross = (df[factor].astype(float) / 100 + 1).cumprod().iloc[-1]
        annualized = gross ** (trading_days / len(df)) - 1
        factor_returns[factor] = annualized

    alpha_annual = ((1 + df_rolling[f'Alpha_{model}'] / 100) ** trading_days - 1)
    rolling_er = alpha_annual + factor_returns['RF']
    
    for factor in required:
        beta_col = f'Beta_{factor}'
        rolling_er += df_rolling[beta_col] * factor_returns[factor]

    df_rolling[f'Rolling_ER_{model}'] = rolling_er
    final_data = pd.concat([df, df_rolling], axis=1)

    return final_data
            


