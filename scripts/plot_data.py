import pandas as pd
import sys
import logging
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-GeoId", help="Country or region id", default ="ZA", type=str)
parser.add_argument("-filename", help="Raw Data File", \
default ="data/COVID-19-geographic-disbtribution-worldwide-2020-03-21.xlsx", type=str)


LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def import_data(filename = None):
    df = pd.read_excel (filename)
    return df

def filter_by_country(df, GeoId):
    df_filter = df.loc[df['GeoId'] == GeoId]
    return df_filter

def sort_by_date(df):
    df_sorted = df.sort_values(by = "DateRep", ascending=True)
    return df_sorted

def get_country(df):
    return df["Countries and territories"].unique()[0]


def run(GeoId , filename):
    # GeoId = "DZ"
    df_raw =  import_data(filename)

    df = filter_by_country(df_raw, GeoId =GeoId)
    df = sort_by_date(df)
    df['Total_Cases'] = df["Cases"].cumsum()
    country_name = get_country(df)


    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,6))


    #Figure 1
    df.plot.bar(x="DateRep", y=["Cases"], color='b',  ax=axes[0], title =f"New Cases in {country_name}", legend=False)
    df.plot(x="DateRep", y=["Cases"], color='b',  style='.', ax=axes[0], title =f"New Cases in {country_name}", legend=False)


    # date_form = DateFormatter("%m-%d")
    # axes[0].xaxis.set_major_formatter(date_form)


    #Figure 2
    df.plot(x="DateRep", y=["Total_Cases"], style='.', ax=axes[1], title =f"Total_Cases in {country_name}", legend=False)
    df.plot(x="DateRep", y=["Total_Cases"], ax=axes[1], legend=False)

    plt.show()



if __name__ == "__main__":
    try:
        args = parser.parse_args()
        LOGGER.info(f"Corona Plotting with GeoId = {args.GeoId}: Starting...")
        run(GeoId = args.GeoId, filename = args.filename)
        LOGGER.info("Corona Plotting: Finished")
    except Exception as exc:
        LOGGER.exception(f"Corona Plotting failed, {exc}")
        raise exc
