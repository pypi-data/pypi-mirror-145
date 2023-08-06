import logging
import json
import pickle
import os
import pandas as pd
import datetime
logger = logging.getLogger(__name__)

"""

Old functions that should not be again used are saved here and excluded from the init file. They remain only for logging
purposes

"""

def correct_C90_dates(df):
    # C90 changed it's configuration in may 2021, so we need to eliminate records before
    C90_start_date = datetime.datetime.strptime('2021-05-01', '%Y-%m-%d').date()
    logger.info(f'shape before C90 date correction: {df.shape}')
    df = df.loc[~ ((df['idCampaign'] == '90') & (df['campaign_bulk_date'] < C90_start_date))]
    logger.info(f'shape after C90 date correction: {df.shape}')
    return df

def create_month_status(df):
    logger.info("Creating Month of the date column")
    if 'campaign_bulk_date' in df.columns:
        df['MonthStatus'] = pd.DatetimeIndex(
            df['campaign_bulk_date']).month.astype('int16')
        df['MonthStatus'] = df['MonthStatus'].astype("category")
    return df