import requests
from pathlib import Path
import time 

HHS_REGION_MAP = {
    1: {"CT", "ME", "MA", "NH", "RI", "VT"},
    2: {"NJ", "NY"},
    3: {"DE", "DC", "MD", "PA", "VA", "WV"},
    4: {"AL", "FL", "GA", "KY", "MS", "NC", "SC", "TN"},
    5: {"IL", "IN", "MI", "MN", "OH", "WI"},
    6: {"AR", "LA", "NM", "OK", "TX"},
    7: {"IA", "KS", "MO", "NE"},
    8: {"CO", "MT", "ND", "SD", "UT", "WY"},
    9: {"AZ", "CA", "HI", "NV"},
    10: {"AK", "ID", "OR", "WA"},
}

STATE_ABBREVS = {
    "ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR",
    "CALIFORNIA": "CA", "COLORADO": "CO", "CONNECTICUT": "CT", "DELAWARE": "DE",
    "FLORIDA": "FL", "GEORGIA": "GA", "HAWAII": "HI", "IDAHO": "ID",
    "ILLINOIS": "IL", "INDIANA": "IN", "IOWA": "IA", "KANSAS": "KS",
    "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
    "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS",
    "MISSOURI": "MO", "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH", "NEW JERSEY": "NJ", "NEW MEXICO": "NM", "NEW YORK": "NY",
    "NORTH CAROLINA": "NC", "NORTH DAKOTA": "ND", "OHIO": "OH", "OKLAHOMA": "OK",
    "OREGON": "OR", "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC", "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX",
    "UTAH": "UT", "VERMONT": "VT", "VIRGINIA": "VA", "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV", "WISCONSIN": "WI", "WYOMING": "WY",
    "DISTRICT OF COLUMBIA": "DC",
}

def state_to_hhs_region(state):
    """Map US state (name or 2-letter code) to HHS Region (1-10)."""
    state = state.strip().upper()

    if len(state) > 2:
        state = STATE_ABBREVS.get(state, state)

    for region, states in HHS_REGION_MAP.items():
        if state in states:
            return f"Region {region}"

    return None



def add_week_column(flu_df):
    """
    Given a df with YEAR and WEEK columns, 
    makes a datetime col with the start of the week
    """
    flu_df['week_start'] = pd.to_datetime(
        (flu_df['YEAR'] * 100 + flu_df['WEEK']).astype(str) + '0', 
        format='%Y%W%w'
    )
    return flu_df


def fetch_and_cache(data_url, file, data_dir="data", force=False):
    """
    Download and cache a url and return the file object.
    
    data_url: the web address to download
    file: the file in which to save the results.
    data_dir: (default="data") the location to save the data
    force: if true the file is always re-downloaded 
    
    return: The pathlib.Path object representing the file.
    """
    
    ### BEGIN SOLUTION
    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok = True)
    file_path = data_dir / Path(file)
    # If the file already exists and we want to force a download then
    # delete the file first so that the creation date is correct.
    if force and file_path.exists():
        file_path.unlink()
    if force or not file_path.exists():
        print('Downloading...', end=' ')
        resp = requests.get(data_url)
        with file_path.open('wb') as f:
            f.write(resp.content)
        print('Done!')
        last_modified_time = time.ctime(file_path.stat().st_mtime)
    else:
        last_modified_time = time.ctime(file_path.stat().st_mtime)
        print("Using cached version that was downloaded (UTC):", last_modified_time)
    return file_path
    ### END SOLUTION
    

def head(filename, lines=5):
    """
    Returns the first few lines of a file.
    
    filename: the name of the file to open
    lines: the number of lines to include
    
    return: A list of the first few lines from the file.
    """
    from itertools import islice
    with open(filename, "r") as f:
        return list(islice(f, lines))
    
