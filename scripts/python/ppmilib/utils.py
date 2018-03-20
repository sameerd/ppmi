import pandas

basedir = "../.."

def fetch_ppmi_data_file(filename, directory):
    """Read in the csv files from the data directory"""
    full_path = basedir + "/" + directory + "/" + filename
    return pandas.read_csv(full_path, dtype={'PATNO':str})

