import pandas as pd
import openpyxl

experiments_df = pd.read_csv('experiments.csv')
plates_df = pd.read_csv('plates.csv')
wells_df = pd.read_csv('wells.csv')

wells_df_prep = wells_df[['well_id', 'well_row', 'well_column', 'plate_id', 'property_name', 'property_value']]

experiments_pivot = experiments_df.pivot(index='experiment_id', columns='property_name',
                                         values='property_value').reset_index()
plates_pivot = plates_df.pivot(index=['plate_id', 'experiment_id'], columns='property_name',
                               values='property_value').reset_index()
wells_pivot = wells_df_prep.pivot(index=['well_id', 'plate_id', 'well_row', 'well_column'], columns='property_name',
                                  values='property_value').reset_index()

merged_df = pd.merge(wells_pivot, plates_pivot, on='plate_id', suffixes=('_well', '_plate'), how='left')

final_df = pd.merge(merged_df, experiments_pivot, on='experiment_id', suffixes=('', '_experiment'), how='left')

# Reorder the final columns and ensure 'well_id', 'well_row', 'well_column' come first
final_columns = ['well_id', 'well_row', 'well_column'] + [col for col in final_df.columns if
                                                          col not in ['well_id', 'well_row', 'well_column']]
final_df = final_df[final_columns]

# Save the result to the combined_results.xlsx file
final_df.to_excel('combined_results.xlsx', index=False)
