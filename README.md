# Pantheon+ Supernova Analysis

This analysis is based on the Pantheon+ dataset of Type Ia supernovae, primarily drawing from the following papers:

## Key Reference Papers

1. **The Pantheon+ Analysis: The Full Dataset and Light-Curve Release**
   - Authors: Scolnic, D., Brout, D., et al. (2022)
   - Contains 1701 light curves of 1550 unique, spectroscopically confirmed Type Ia supernovae

2. **Draft version February 9, 2022**
   - Contains detailed analysis methodology and improvements over previous Pantheon dataset
   - Significantly increased sample size, particularly at low redshift

## Dataset Overview

The dataset includes:
- **Total SNe**: 2,287 entries
- **Redshift range**: 0.001 to 2.261
- **Host galaxy fraction**: ~59.5%
- **Group membership**: ~5.8%

## Analysis Components

Our analysis processes the following key measurements:
1. Different redshift frames (heliocentric, CMB, Hubble diagram)
2. Peculiar velocities
3. Host galaxy associations
4. Group membership

### Comparisons to the Reference Papers

This implementation builds upon the methodologies described in the papers but includes additional enhancements:
- **Column verification**: Automated validation of input dataset columns to prevent missing or misaligned data.
- **Distance discrepancies**: Incorporates the analysis of measured vs. expected distances using both peculiar velocities and redshift corrections.
- **Derived quantities**: Automated calculation of derived metrics such as `redshift_diff`, `abs_PV`, and `z_relative_error` to enhance dataset insights.

Key results align closely with the methodologies described in Scolnic et al. (2022) but are verified using modern Python-based data processing techniques.

## Output Files

The analysis produces several files:
1. `pantheon_plus_processed.csv`: Processed supernova data with computed quantities
2. `pantheon_plus_statistics.csv`: Summary statistics of the sample
3. `redshift_differences.csv`: Analysis of different redshift frames
4. `pantheon_analysis_plots.png`: Visualization of key relationships
5. `distance_analysis.csv`: Distance discrepancy analysis
6. `distance_comparison.png`: Plot of expected vs. measured distances

## Visualizations

### Main Analysis Plot
![Pantheon Analysis](pantheon_analysis_plots.png)

This plot includes:
1. **Heliocentric vs CMB Frame Redshift comparison**
2. **Peculiar Velocities distribution by group membership**
3. **Distribution of Redshift Differences**
4. **Peculiar Velocity vs Redshift relationship**

### Distance Comparison Plot
![Distance Comparison](distance_comparison.png)

This plot compares the expected vs. measured distances of supernovae, highlighting deviations potentially due to peculiar velocities.

## Code Structure

The analysis code performs the following steps:
1. **Data loading and cleaning**: Reads and validates the dataset, ensuring all required columns are present.
2. **Processing and computation**: Derives new quantities such as `redshift_diff` and categorizes host/group statuses.
3. **Statistical analysis**: Computes summary statistics, such as mean and median values of key parameters.
4. **Visualizations**: Generates detailed plots to analyze relationships in the data.
5. **Saving results**: Outputs processed data and analysis results into structured CSV files.

## Dependencies

- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`

## Usage

Run the main analysis script:
```bash
python main.py
```

## References

1. Scolnic, D., et al. (2022), "The Pantheon+ Analysis: The Full Dataset and Light-Curve Release"
2. Brout, D., et al. (2022b), "The Pantheon+ Analysis: Cosmological Constraints"
3. Riess, A. G., et al. (2022), "A Comprehensive Measurement of the Local Value of the Hubble Constant with 1 km/s/Mpc Uncertainty from the Hubble Space Telescope and the SH0ES Team"

