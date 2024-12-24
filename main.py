import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_data(filepath='all_redshifts_PVs.csv'):
    """Load and perform initial data cleaning."""
    print("Loading data from CSV...")
    data = pd.read_csv(filepath)
    print(f"Loaded {len(data)} rows")

    print("Calculating derived quantities...")
    # Calculate derived quantities
    data['redshift_diff'] = data['zcmb'] - data['zhel']
    data['abs_PV'] = np.abs(data['PV'])

    # Verify columns
    expected_columns = {
        'SNID': 'SNID',
        'zhel': 'zhel',
        'zcmb': 'zcmb',
        'zHD': 'zHD',
        'PV': 'PV',
        'zhelerr': 'zhelerr',
        'zHDerr': 'zHDerr',
        'has_host': 'has_host',
        'in_group': 'in_group'
    }

    print("Verifying columns in dataset...")
    for col in expected_columns.values():
        if col not in data.columns:
            print(f"Missing column: {col}")
            raise ValueError(f"Column {col} is missing from the dataset")
        print(f"Verified column: {col}")

    print("Adding derived columns...")

    return data

def process_data(data):
    """Process the data and create additional columns for analysis."""
    print("Processing data...")

    # Create processed dataframe with selected and computed columns
    processed_data = pd.DataFrame()

    # Copy over original columns
    original_columns = ['SNID', 'zhel', 'zcmb', 'zHD', 'PV', 'has_host', 'in_group']
    for col in original_columns:
        processed_data[col] = data[col]

    # Add computed columns
    print("Computing derived quantities...")
    processed_data['redshift_diff'] = data['zcmb'] - data['zhel']
    processed_data['abs_PV'] = np.abs(data['PV'])
    processed_data['z_relative_error'] = data['zhelerr'] / data['zhel']
    processed_data['host_status'] = data['has_host'].map({1: 'With Host', 0: 'No Host'})
    processed_data['group_status'] = data['in_group'].map({1: 'In Group', 0: 'Not in Group'})

    return processed_data

def compute_statistics(data):
    """Compute statistics for the sample."""
    print("Computing statistics...")
    stats = {
        'total_SNe': len(data),
        'mean_zcmb': data['zcmb'].mean(),
        'median_zcmb': data['zcmb'].median(),
        'min_zcmb': data['zcmb'].min(),
        'max_zcmb': data['zcmb'].max(),
        'mean_PV': data['PV'].mean(),
        'median_PV': data['PV'].median(),
        'host_fraction': data['has_host'].mean(),
        'group_fraction': data['in_group'].mean(),
        'mean_zHD_error': data['zHDerr'].mean()
    }

    # Create a DataFrame with the statistics
    stats_df = pd.DataFrame([stats])
    return stats_df

def save_results(processed_data, stats_df):
    """Save processed data and statistics to CSV files."""
    print("Saving results to CSV files...")

    # Save processed data
    processed_data.to_csv('pantheon_plus_processed.csv', index=False)
    print("Saved processed data to pantheon_plus_processed.csv")

    # Save statistics
    stats_df.to_csv('pantheon_plus_statistics.csv', index=False)
    print("Saved statistics to pantheon_plus_statistics.csv")

def analyze_redshift_frames(data):
    """Analyze differences between redshift frames."""
    print("\nAnalyzing redshift frames...")

    differences = {
        'zhel_vs_zcmb': data['zhel'] - data['zcmb'],
        'zhel_vs_zHD': data['zhel'] - data['zHD'],
        'zcmb_vs_zHD': data['zcmb'] - data['zHD']
    }

    # Save redshift differences analysis
    redshift_diff_df = pd.DataFrame(differences)
    redshift_diff_df.to_csv('redshift_differences.csv', index=False)
    print("Saved redshift differences to redshift_differences.csv")

    return differences

def create_analysis_plots(data):
    """Create detailed analysis plots."""
    print("\nCreating analysis plots...")

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # Plot 1: Redshift correlations
    ax = axes[0, 0]
    ax.scatter(data['zhel'], data['zcmb'], alpha=0.5, s=5)
    ax.set_xlabel('Heliocentric Redshift')
    ax.set_ylabel('CMB Frame Redshift')
    ax.set_title('Heliocentric vs CMB Frame Redshift')

    # Plot 2: PV distribution by group status
    ax = axes[0, 1]
    sns.boxplot(data=data, x='group_status', y='PV', ax=ax)
    ax.set_title('Peculiar Velocities by Group Membership')

    # Plot 3: Redshift differences
    ax = axes[1, 0]
    ax.hist(data['redshift_diff'], bins=50)
    ax.set_xlabel('Redshift Difference (zcmb - zhel)')
    ax.set_title('Distribution of Redshift Differences')

    # Plot 4: PV vs Redshift
    ax = axes[1, 1]
    ax.scatter(data['zcmb'], data['PV'], alpha=0.5, s=5)
    ax.set_xlabel('CMB Frame Redshift')
    ax.set_ylabel('Peculiar Velocity')
    ax.set_title('PV vs Redshift')

    plt.tight_layout()
    plt.savefig('pantheon_analysis_plots.png')
    print("Saved plots to pantheon_analysis_plots.png")

    return fig

def analyze_distance_discrepancy(data):
    """Analyze the difference between expected and measured distances."""
    print("\nAnalyzing distance discrepancies...")

    # Constants
    H0 = 70  # Hubble constant in km/s/Mpc
    c = 299792.458  # Speed of light in km/s

    # Calculate distances in Mpc
    # Expected distance from Hubble flow
    data['expected_distance'] = data['zhel'] * (c/H0)  # Simple Hubble law

    # Measured distance including peculiar velocity corrections
    data['measured_distance'] = (data['zHD'] * c/H0)

    # Calculate discrepancy
    data['distance_discrepancy'] = data['measured_distance'] - data['expected_distance']

    # Save distance analysis
    distance_df = pd.DataFrame({
        'SNID': data['SNID'],
        'redshift_hel': data['zhel'],
        'redshift_HD': data['zHD'],
        'expected_distance': data['expected_distance'],
        'measured_distance': data['measured_distance'],
        'discrepancy': data['distance_discrepancy'],
        'PV': data['PV']
    })

    distance_df.to_csv('distance_analysis.csv', index=False)
    print("Saved distance analysis to distance_analysis.csv")

    # Create distance comparison plot
    plt.figure(figsize=(12, 8))
    plt.scatter(data['expected_distance'], data['measured_distance'], 
                alpha=0.5, s=5, c=data['PV'], cmap='coolwarm')
    plt.colorbar(label='Peculiar Velocity (km/s)')

    # Add diagonal line for reference
    max_dist = max(data['expected_distance'].max(), data['measured_distance'].max())
    min_dist = min(data['expected_distance'].min(), data['measured_distance'].min())
    plt.plot([min_dist, max_dist], [min_dist, max_dist], 'r--', alpha=0.5, 
             label='Expected=Measured')

    plt.xlabel('Expected Distance (Mpc)')
    plt.ylabel('Measured Distance (Mpc)')
    plt.title('Expected vs Measured Distances for Type Ia Supernovae')

    # Add text box with statistics
    stats_text = f"Mean discrepancy: {data['distance_discrepancy'].mean():.1f} Mpc\n"
    stats_text += f"Median discrepancy: {data['distance_discrepancy'].median():.1f} Mpc\n"
    stats_text += f"Std discrepancy: {data['distance_discrepancy'].std():.1f} Mpc"
    plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes, 
             bbox=dict(facecolor='white', alpha=0.8), verticalalignment='top')

    plt.legend()
    plt.tight_layout()
    plt.savefig('distance_comparison.png')
    print("Saved distance comparison plot to distance_comparison.png")

    return distance_df

def main():
    print("Starting Pantheon+ analysis...")

    # Original analysis
    data = load_and_clean_data()
    processed_data = process_data(data)
    stats_df = compute_statistics(data)
    save_results(processed_data, stats_df)

    # New additional analysis
    redshift_differences = analyze_redshift_frames(processed_data)
    fig = create_analysis_plots(processed_data)

    # Distance analysis that compares supernova vs. redshift
    distance_df = analyze_distance_discrepancy(processed_data)

    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total SNe: {len(data)}")
    print(f"Redshift Range: {data['zcmb'].min():.3f} to {data['zcmb'].max():.3f}")
    print(f"SNe with Hosts: {(data['has_host'].mean() * 100):.1f}%")
    print(f"SNe in Groups: {(data['in_group'].mean() * 100):.1f}%")

    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
