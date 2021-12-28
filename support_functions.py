import os
import urllib.request
import shutil
import zipfile
import datetime

deacot_file = "/tmp/deacot2021.txt"
da_file = "/tmp/deacot_DA_2021.txt"

# Data Retrieval and Handling

# Function to retrieve reports
def get_COT(url, file_name):
    with urllib.request.urlopen(url) as response, open(file_name, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
        with zipfile.ZipFile(file_name) as zf:
            zf.extractall()


# Function to ensure data freshness
def get_reports():
    freshness_date = datetime.datetime.now() - datetime.timedelta(days=7)
    if os.path.exists(deacot_file):
        filetime = datetime.datetime.fromtimestamp(os.path.getmtime(deacot_file))
        if (filetime - datetime.timedelta(days=7)) <= freshness_date:
            print("Deacot file is available and Data is fresh -- Using cached data")
        else:
            get_COT(
                "https://www.cftc.gov/files/dea/history/deacot2021.zip",
                "deacot2021.zip",
            )
            os.rename(r"annual.txt", deacot_file)
            print("Deacot file is available and Data is stale -- Updating data")
    else:
        print("Deacot file is not available -- Downloading data")
        get_COT(
            "https://www.cftc.gov/files/dea/history/deacot2021.zip", "deacot2021.zip"
        )
        os.rename(r"annual.txt", deacot_file)

if __name__ == "__main__":
    get_reports()