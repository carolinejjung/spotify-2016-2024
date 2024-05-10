
from glob import glob
import json
import pandas as pd

files = glob("*.json") # note: cd into "1-raw-data" folder before running

def json_to_df(file):
    """Given a json, create a dataframe for each file."""
    with open(file, "r") as f:
        list_of_tracks = json.load(f)
    return pd.DataFrame(list_of_tracks)

all_dfs = [json_to_df(file) for file in files]
merged_df = pd.concat(all_dfs).reset_index()

def clean_platform():
    """Reassign platform values to only phone, web, or desktop."""
    unique_values = list(set(merged_df["platform"]))
    phone, web, desktop = [], [], []
    for value in unique_values:
        if "iPhone" in value or "Android" in value or "ios" in value:
            phone.append(value)
        elif "web_player" in value:
            web.append(value)
        else:
            desktop.append(value)
    return phone, web, desktop

# overwrite sensitive data
merged_df["ip_addr_decrypted"] = "hidden"
merged_df["username"] = "bbb"
merged_df["conn_country"] = "hidden"
phone, web, desktop = clean_platform()
merged_df["platform"] = merged_df["platform"].apply(lambda x: "phone" if x in phone else "web" if x in web else "desktop")

# write to csv
merged_df.to_csv("cleaned_data.csv", index=False)
