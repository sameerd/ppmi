import os
import os.path

import sqlite3

import pandas as pd

import ppmilib
import ppmilib.utils



if __name__ == "__main__":
    ppmi_curs = ppmilib.utils.SqliteCursor.ppmi()

    filenames = ppmilib.utils.fetch_ppmi_csv_filenames()

    results = []

    # process the csv files one by one
    for filename in filenames:
        resultsd = {}

        pd_file = ppmilib.utils.fetch_raw_ppmi_data_file(filename)
        pd_headers = pd_file.columns.values.tolist()

        base_filename = os.path.basename(filename)
        resultsd["base_filename"] = base_filename
        has_pat_id = ("PATNO" in pd_headers) or \
                ("study_subject_id" in pd_headers)
        resultsd["has_pat_id"] = has_pat_id

        pg_str = None # List of Page Names in the csv file
        pg_values = None
        if "PAG_NAME" in pd_headers:
            pg_name_counts = pd_file.PAG_NAME.value_counts() 
            pg_values = pg_name_counts.index.tolist()
            pg_str = len(pg_values)
            if len(pg_values) == 1:
                pg_str = pg_values[0]
            elif len(pg_values) < 5:
                pg_str = "%s" % pg_values

        table_name = None
        if pg_str is not None and len(pg_values) == 1: 
            # If we have one page_name then create a table with that name
            table_name = pg_values[0]

        file_tabled = {
                "TAP-PD_OPDM_Assessment.csv":"OPDM",
                "TAP-PD_Kinetics_Device_Testing.csv":"KINETICS",
                "Center-Subject_List.csv":"CENTER",
                "Data_Dictionary.csv":"DATADICT",
                "Benton_Judgment_of_Line_Orientation.csv":"BENTON",
                "DaTSCAN_SPECT_Visual_Interpretation_Assessment.csv":"DATSCAN",
                "FBB_Metadata.csv":"FBB"
            }
        if base_filename in file_tabled:
            table_name = file_tabled[base_filename]
        resultsd["table_name"] = table_name

        # if the file has a PATNO then lets put it into the database
        if has_pat_id is True:
            pass #pd_file.to_sql(name=

        results.append(resultsd)

    pd_results = pd.DataFrame.from_dict(results)
