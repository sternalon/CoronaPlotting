import pandas as pd
import sys
import logging
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-geoId", help="Country or region id", default ="ZA", type=str)
parser.add_argument("-filename", help="Raw Data File", default ="data/latest.xlsx", type=str)
parser.add_argument("-save", help="Save Image as output.png", default =False, type=bool)


LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def import_data(filename = None):
    df = pd.read_excel (filename)
    return df

def filter_by_countries(df, geoId_list):
    df_filter = df.loc[df['geoId'].isin(geoId_list)]
    return df_filter

def sort_by_date(df):
    df_sorted = df.sort_values(by = "dateRep", ascending=True)
    return df_sorted

def get_country(df):
    return df["countriesAndTerritories"].unique()[0]

def filter_by_min_total_cases(df, number):
    df_filter = df.loc[df['total_cases']>number]
    return df_filter


def run(geoId , filename, save_image):
    # Import Data
    df_raw =  import_data(filename)

    #Select Countries to Plot
    geoId_list = ["US", "IT", "CN", "ES", "DE", "BR", "RU", "UK", "KR", "ZA"]

    df = filter_by_countries(df_raw, geoId_list =geoId_list)

    df = sort_by_date(df)

    # Calcualting Cumulative Sum of cases
    df['total_cases'] = df.groupby(['geoId'])['cases'].cumsum()
    df = filter_by_min_total_cases(df, 100)

    # Calcualting Rollowing average for new cases
    window_size = 7
    df['av_cases'] = df.groupby('geoId')['cases'].transform(lambda x: x.rolling(window_size, 1).mean())

    df['growth'] = df['cases']/df['total_cases']
    df['av_growth'] = df.groupby('geoId')['growth'].transform(lambda x: x.rolling(window_size, 1).mean())


    #Plotting Data
    fig, ax = plt.subplots(figsize=(15,6))
    for key, grp in df.groupby(['geoId']):
        ax = grp.plot(ax=ax, kind='line', x='dateRep', y='av_growth', label=get_country(grp))
    plt.legend(loc='best')
    # plt.xscale('log')
    #plt.yscale('log')
    plt.title("Daily Growth Rate (New Cases / Total Cases)")
    plt.ylim((0, 0.4))
    # plt.xlim((80, 10**6))
    plt.xlabel("Date")
    plt.ylabel("Daily Growth")

    if save_image is True:
        fig.savefig('images/growth_plot.png')

    plt.show()


if __name__ == "__main__":
    try:
        args = parser.parse_args()
        LOGGER.info(f"Growth Plotting: Starting...")
        run(geoId = args.geoId, filename = args.filename, save_image = args.save)
        LOGGER.info("Growth Plotting: Finished")
    except Exception as exc:
        LOGGER.exception(f"Flatten Curve Plotting failed, {exc}")
        raise exc
