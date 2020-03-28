import pandas as pd
import sys
import logging
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-geoId", help="Country or region id", default ="ZA", type=str)
parser.add_argument("-filename", help="Raw Data File", \
default ="data/COVID-19-geographic-disbtribution-worldwide-2020-03-27.xlsx", type=str)
parser.add_argument("-save", help="Save Image as output.png", default =False, type=bool)


LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def import_data(filename = None):
    df = pd.read_excel (filename)
    return df

def filter_by_country(df, geoId):
    df_filter = df.loc[df['geoId'] == geoId]
    return df_filter

def sort_by_date(df):
    df_sorted = df.sort_values(by = "dateRep", ascending=True)
    return df_sorted

def get_country(df):
    return df["countriesAndTerritories"].unique()[0]


def run(geoId , filename, save_image):
    # geoId = "DZ"
    df_raw =  import_data(filename)

    df = filter_by_country(df_raw, geoId =geoId)
    df = sort_by_date(df)
    df['total_cases'] = df["cases"].cumsum()
    country_name = get_country(df)


    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,6))


    #Figure 1
    df.plot.bar(x="dateRep", y=["cases"], color='b',  ax=axes[0], title =f"New Cases in {country_name}", legend=False)
    df.plot(x="dateRep", y=["cases"], color='b',  style='.', ax=axes[0], title =f"New Cases in {country_name}", legend=False)


    # date_form = DateFormatter("%m-%d")
    # axes[0].xaxis.set_major_formatter(date_form)


    #Figure 2
    df.plot(x="dateRep", y=["total_cases"], style='.', ax=axes[1], title =f"Total_Cases in {country_name}", legend=False)
    df.plot(x="dateRep", y=["total_cases"], ax=axes[1], legend=False)

    if save_image is True:
        fig.savefig('images/number_of_cases.png')

    plt.show()



if __name__ == "__main__":
    try:
        args = parser.parse_args()
        LOGGER.info(f"Corona Plotting with geoId = {args.geoId}: Starting...")
        run(geoId = args.geoId, filename = args.filename, save_image = args.save)
        LOGGER.info("Corona Plotting: Finished")
    except Exception as exc:
        LOGGER.exception(f"Corona Plotting failed, {exc}")
        raise exc
