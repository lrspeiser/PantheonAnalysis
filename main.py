import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_data(filepath='all_redshifts_PVs.csv'):
    """Load and perform initial data cleaning."""
    data = pd.read_csv(filepath)

    # Calculate some useful derived quantities
    data['redshift_diff'] = data['zcmb'] - data['zhel']
    data['abs_PV'] = np.abs(data['PV'])

    return data

def create_comprehensive_plots(data):
    """Create a comprehensive set of plots analyzing key aspects of the dataset."""
    fig = plt.figure(figsize=(15, 12))
    gs = plt.GridSpec(3, 2, figure=fig)

    # 1. Redshift distribution
    ax1 = fig.add_subplot(gs[0, 0])
    sns.histplot(data=data, x='zcmb', bins=50, ax=ax1)
    ax1.set_title('CMB Frame Redshift Distribution')
    ax1.set_xlabel('zcmb')

    # 2. Peculiar velocity distribution
    ax2 = fig.add_subplot(gs[0, 1])
    sns.histplot(data=data, x='PV', bins=50, ax=ax2)
    ax2.set_title('Peculiar Velocity Distribution')
    ax2.set_xlabel('PV (km/s)')

    # 3. Sky distribution
    ax3 = fig.add_subplot(gs[1, :])
    scatter = ax3.scatter(data['RA'], data['Dec'], c=data['zcmb'], 
                         cmap='viridis', alpha=0.6, s=5)
    plt.colorbar(scatter, ax=ax3, label='Redshift')
    ax3.set_title('Sky Distribution of SNe')
    ax3.set_xlabel('RA (deg)')
    ax3.set_ylabel('Dec (deg)')

    # 4. Host galaxy statistics
    ax4 = fig.add_subplot(gs[2, 0])
    host_counts = data['has_host'].value_counts()
    ax4.bar(['Without Host', 'With Host'], 
            [host_counts[0], host_counts[1]])
    ax4.set_title('Host Galaxy Statistics')

    # 5. Group membership statistics
    ax5 = fig.add_subplot(gs[2, 1])
    group_counts = data['in_group'].value_counts()
    ax5.bar(['Not in Group', 'In Group'], 
            [group_counts[0], group_counts[1]])
    ax5.set_title('Group Membership Statistics')

    plt.tight_layout()
    return fig

def compute_detailed_statistics(data):
    """Compute detailed statistics about the sample."""
    stats = {
        'Total SNe': len(data),
        'Mean Redshift (CMB)': data['zcmb'].mean(),
        'Median Redshift (CMB)': data['zcmb'].median(),
        'Redshift Range': f"{data['zcmb'].min():.3f} to {data['zcmb'].max():.3f}",
        'Mean PV (km/s)': data['PV'].mean(),
        'Median PV (km/s)': data['PV'].median(),
        'SNe with Hosts (%)': (data['has_host'].mean() * 100),
        'SNe in Groups (%)': (data['in_group'].mean() * 100),
        'Mean zHD Error': data['zHDerr'].mean(),
    }

    # Add redshift statistics for different frames
    for z_type in ['zhel', 'zcmb', 'zHD']:
        subset = data[data[z_type] > 0]  # Only positive redshifts
        stats[f'{z_type} stats'] = {
            'mean': subset[z_type].mean(),
            'std': subset[z_type].std(),
            'median': subset[z_type].median()
        }

    return stats

def main():
    # Load and process data
    data = load_and_clean_data()

    # Compute statistics
    stats = compute_detailed_statistics(data)

    # Print statistics
    print("\nPantheon+ Sample Statistics:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for subkey, subvalue in value.items():
                print(f"  {subkey}: {subvalue:.4f}")
        else:
            print(f"{key}: {value}")

    # Create and show plots
    fig = create_comprehensive_plots(data)
    plt.show()

if __name__ == "__main__":
    main()