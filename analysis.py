"""Reproducible vehicle-listing analysis. Associations do not establish causality."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_URL = 'https://practicum-content.s3.us-west-1.amazonaws.com/datasets/vehicles_us.csv'


def prepare_data(raw):
    df = raw.copy()
    df['date_posted'] = pd.to_datetime(df['date_posted'], errors='raise')
    for col in ['price', 'model_year', 'odometer', 'cylinders', 'days_listed']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Preserve the fact that a value was missing, rather than silently hiding it.
    for col in ['model_year', 'odometer', 'cylinders', 'paint_color', 'is_4wd']:
        df[col + '_missing'] = df[col].isna()
    for col in ['model_year', 'odometer']:
        by_model = df.groupby('model')[col].transform('median')
        df[col] = df[col].fillna(by_model).fillna(df[col].median())
    modes = df.groupby('model')['cylinders'].agg(
        lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan)
    fallback = df['cylinders'].mode()
    if fallback.empty:
        raise ValueError('No observed cylinder values; cannot infer a fallback.')
    df['cylinders'] = df['cylinders'].fillna(df['model'].map(modes)).fillna(fallback.iloc[0]).astype('int64')
    df['paint_color'] = df['paint_color'].fillna('unknown')
    # The source dataset encodes absence of four-wheel drive with missing values.
    df['is_4wd'] = df['is_4wd'].fillna(0).astype('int64')
    df['vehicle_age'] = df['date_posted'].dt.year - df['model_year']
    # Age zero has no defined annual mileage. Future model years remain invalid.
    df.loc[df['vehicle_age'] < 0, 'vehicle_age'] = np.nan
    df['annual_mileage'] = df['odometer'].div(df['vehicle_age'].where(df['vehicle_age'] > 0))
    return df


def without_outliers(df, column):
    """IQR filter for ONE variable; never reuse the bounds of another variable."""
    q1, q3 = df[column].quantile([0.25, 0.75])
    if pd.isna(q1) or pd.isna(q3):
        return df.iloc[0:0].copy()
    iqr = q3 - q1
    return df.loc[df[column].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)].copy()


def summarize_types(df, minimum=50):
    summary = df.groupby('type').agg(ad_count=('type', 'size'), mean_price=('price', 'mean'))
    return summary.loc[summary.ad_count >= minimum].sort_values(
        ['ad_count', 'mean_price'], ascending=[False, False])


def run_analysis(source=DATA_URL, output_dir='results'):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(source)
    df = prepare_data(raw)
    summary = summarize_types(df)
    summary.to_csv(output / 'vehicle_types.csv')
    for col in ['price', 'vehicle_age', 'odometer', 'cylinders']:
        filtered = without_outliers(df, col)
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        for ax, data, title in zip(axes, [df, filtered], ['Original', 'IQR filtered']):
            data[col].dropna().hist(bins=40, ax=ax)
            ax.set(title=f'{title}: {col}', xlabel=col, ylabel='Listings')
        fig.tight_layout()
        fig.savefig(output / f'{col}_iqr.png', dpi=140)
        plt.close(fig)
    selected_types = summary.head(2).index.tolist()
    fig, ax = plt.subplots(figsize=(8, 5))
    for kind in selected_types:
        subset = df.loc[df.type.eq(kind)]
        ax.scatter(subset.vehicle_age, subset.price, alpha=0.15, s=8, label=kind)
    ax.set(xlabel='Vehicle age', ylabel='Listed price', title='Most frequent eligible vehicle types')
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / 'popular_types_price.png', dpi=140)
    plt.close(fig)
    # Sensitivity: compare observed values with the completed dataset.
    sensitivity = []
    for col in ['model_year', 'odometer', 'cylinders']:
        sensitivity.append({'column':col,
                            'missing_count':int(df[col + '_missing'].sum()),
                            'observed_median':float(raw[col].median()),
                            'completed_median':float(df[col].median())})
    pd.DataFrame(sensitivity).to_csv(output / 'imputation_sensitivity.csv', index=False)
    metrics = {'rows':len(df), 'selected_types':selected_types,
               'selection_rule':'At least 50 listings, sorted by listing count',
               'caution':'Listings are not completed sales. Associations are not causal effects.'}
    (output / 'summary.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    print(json.dumps(metrics, indent=2))
    return df, summary


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default=DATA_URL)
    parser.add_argument('--output', default='results')
    args = parser.parse_args()
    run_analysis(args.data, args.output)
