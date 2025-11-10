import matplotlib.pyplot as plt
import numpy as np

def plot_er_decomposition_ff5(data_rolling_ff5, data_ff5, trading_days=252):
    """breakdown chart of the ER FF5"""
    factors = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
    
    factor_returns = {}
    for factor in factors + ['RF']:
        gross = (data_ff5[factor].astype(float) / 100 + 1).cumprod().iloc[-1]
        annualized = gross ** (trading_days / len(data_ff5)) - 1
        factor_returns[factor] = annualized
    
    # last observations
    alpha = data_rolling_ff5['Alpha_FF5'].iloc[-1]
    alpha_annual = ((1 + alpha / 100) ** trading_days - 1)
    
    # Contributions
    contributions = {
        'Alpha': alpha_annual,
        'Risk-Free Rate': factor_returns['RF'],
        'Mkt-RF': data_rolling_ff5['Beta_Mkt-RF'].iloc[-1] * factor_returns['Mkt-RF'],
        'SMB': data_rolling_ff5['Beta_SMB'].iloc[-1] * factor_returns['SMB'],
        'HML': data_rolling_ff5['Beta_HML'].iloc[-1] * factor_returns['HML'],
        'RMW': data_rolling_ff5['Beta_RMW'].iloc[-1] * factor_returns['RMW'],
        'CMA': data_rolling_ff5['Beta_CMA'].iloc[-1] * factor_returns['CMA']
    }
    

    labels = list(contributions.keys())
    values = [v * 100 for v in contributions.values()] 
    
  
    colors = {
        'Alpha': '#8B008B',           # Purple
        'Risk-Free Rate': '#696969',  # Gray
        'Mkt-RF': "#2b74a9",          # Blue
        'SMB': '#ff7f0e',             # Orange
        'HML': '#2ca02c',             # Green
        'RMW': '#d62728',             # Red
        'CMA': "#8837d4"              # Light Purple
    }
    bar_colors = [colors[label] for label in labels]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars = ax.bar(labels, values, color=bar_colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.2f}%',
                ha='center', va='bottom' if height > 0 else 'top',
                fontsize=11, fontweight='bold')
    
    # Total ER
    total_er = sum(values)
    
    ax.set_ylabel('Contribution to Expected Return (%)', fontsize=13, fontweight='bold')
    ax.set_title(f'FF5 Expected Return Decomposition (Current)\nTotal ER = {total_er:.2f}%', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)
    
    plt.xticks(rotation=45, ha='right', fontsize=11)
    
    legend_text = f"Current Date: {data_rolling_ff5.index[-1].strftime('%Y-%m-%d')}\n"
    legend_text += f"R² (FF5): {data_rolling_ff5['R2_FF5'].iloc[-1]:.4f}"
    
    ax.text(0.75, 0.95, legend_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    return fig

