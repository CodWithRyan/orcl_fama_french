# Oracle Stock Analysis: Fama-French Factor Models

## 🎯 Project Overview

This project applies **Fama-French multi-factor models** (FF3, FF5) to analyze Oracle Corporation's stock returns and estimate expected returns using both static and rolling window approaches.

### 👀 Key Features
- ✅ Static analysis with FF3 and FF5 models
- ✅ Rolling beta estimation (252-day window)
- ✅ Rolling Expected Return calculation
- ✅ Comprehensive visualizations and comparisons
- ✅ Modular, reusable code architecture

## 📌 Main Findings

| Model | Static ER | Rolling ER (Mean) | R² Mean |
|-------|-----------|-------------------|---------|
| FF3   | 20.6%     | 20.6%            | 38.3%   |
| FF5   | 18.9%     | 18.9%            | 39.5%   |

**Key Insight:** FF5 explains ~40% of Oracle's return variance. The remaining 60% is idiosyncratic risk related to Oracle-specific factors (cloud transition, AI investments, acquisitions, etc.).

## 🚀 Quick Start

### ⚙️ Installation
```bash
# Clone the repository
git clone https://github.com/codwithryan/orcl_fama_french.git
cd orcl_fama_french

# Install dependencies
pip install -r requirements.txt
```

### Usage
```python
# Run the complete analysis
jupyter notebook notebooks/03_final_report.ipynb
```

## 📁 Project Structure
```
oracle-fama-french-analysis/
├── src/                    # Source code modules
|   ├── __init__.py                     
│   ├── data_loader.py     # Data loading and cleaning
│   ├── factor_models.py   # FF3/FF5 models
│   ├── rolling_analysis.py # Rolling beta/ER calculations
│   └── visualization.py    # Plotting functions
├── notebooks/              # Jupyter notebooks
│   └── 03_final_report.ipynb
├── results/                # Output files
│   ├── figures/           # PNG charts
│   └── tables/            # CSV results
└── README.md
```

## 📈 Methodology

### Data Sources
- **Oracle prices:** Yahoo Finance (2016-2025)
- **Fama-French factors:** Kenneth French Data Library

### Models Implemented
1. **FF3:** Market, SMB (Size), HML (Value)
2. **FF5:** FF3 + RMW (Profitability) + CMA (Investment)

### Rolling Window
- Window: 252 trading days (~1 year)
- Minimum periods: 126 days
- Updated daily

## 📊 Key Visualizations

### Rolling Expected Return
![Rolling ER](results/figures/rolling_er_comparison.png)

### Rolling Betas (FF5)
![Rolling Betas](results/figures/rolling_betas_ff5.png)

## 🔬 Technical Details

### Dependencies
- Python 3.8+
- pandas, numpy
- statsmodels
- matplotlib, seaborn

See `requirements.txt` for complete list.

### Running Tests
```bash
pytest tests/
```

## 📝 References

- Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*.

## 👤 Author

**🧑🏽‍💻 Bonny Ryan F.N.**


## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Kenneth French Data Library for factor data