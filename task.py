import pandas as pd
from sqlalchemy import create_engine

# Connecting to my database using SQLAlchemy
engine = create_engine('postgresql+psycopg2://postgres:Super1@localhost:5432/experiment')

# Read data from my PostgreSQL Database as pandas DataFrames
experiments_df = pd.read_sql('SELECT * FROM experiments', engine)
plates_df = pd.read_sql('SELECT * FROM plates', engine)
wells_df = pd.read_sql('SELECT * FROM wells', engine)

# Include well_row and well_column in the wells DataFrame before pivoting
wells_df_prep = wells_df[['well_id', 'well_row', 'well_column', 'plate_id', 'property_name', 'property_value']]

# Pivot the data in order to convert rows of property_name and property_value into columns
experiments_pivot = experiments_df.pivot(index='experiment_id', columns='property_name',
                                         values='property_value').reset_index()
plates_pivot = plates_df.pivot(index=['plate_id', 'experiment_id'], columns='property_name',
                               values='property_value').reset_index()
wells_pivot = wells_df_prep.pivot(index=['well_id', 'plate_id', 'well_row', 'well_column'], columns='property_name',
                                  values='property_value').reset_index()

# Merge well level data with plate level data
merged_df = pd.merge(wells_pivot, plates_pivot, on='plate_id', suffixes=('_well', '_plate'), how='left')

# To merge result with experiment-level data
final_df = pd.merge(merged_df, experiments_pivot, on='experiment_id', suffixes=('', '_experiment'), how='left')

# Reorder the final columns and to ensure 'well_id', 'well_row', 'well_column' come first
final_columns = ['well_id', 'well_row', 'well_column'] + [col for col in final_df.columns if
                                                          col not in ['well_id', 'well_row', 'well_column']]
final_df = final_df[final_columns]
final_df.fillna('none', inplace=True)

# Save the result to an .xlsx file
final_df.to_excel('combined_results.xlsx', index=False)

