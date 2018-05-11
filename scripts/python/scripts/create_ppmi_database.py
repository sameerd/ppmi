import os
import os.path

import sqlite3

import pandas as pd

import ppmilib
import ppmilib.utils

class PPMIFile:

    file_tabled = {
        "TAP-PD_OPDM_Assessment.csv":"OPDM",
        "TAP-PD_Kinetics_Device_Testing.csv":"KINETICS",
        "Center-Subject_List.csv":"CENTER",
        "Data_Dictionary.csv":"DATADICT",
        "Benton_Judgment_of_Line_Orientation.csv":"BENTON",
        "DaTSCAN_SPECT_Visual_Interpretation_Assessment.csv":"DATSCAN",
        "FBB_Metadata.csv":"FBB"
        }

    def __init__(self, filename):
        self.filename = filename
        self.base_filename = os.path.basename(filename)
        self.pd_file = ppmilib.utils.fetch_raw_ppmi_data_file(filename)
        self.pd_headers = self.pd_file.columns.values.tolist()
        self.has_pat_id = self.check_for_pat_id()
        self.pag_names = self.extract_pag_names()
        self.pag_names_cnt = len(self.pag_names)
        self.table_name = self.make_table_name()

    def check_for_pat_id(self):
        return ("PATNO" in self.pd_headers) or \
               ("study_subject_id" in self.pd_headers)

    def extract_pag_names(self):
        pag_names = []
        if "PAG_NAME" in self.pd_headers:
            pag_name_counts = self.pd_file.PAG_NAME.value_counts() 
            pag_names = pag_name_counts.index.tolist()
        return(pag_names)

    def make_table_name(self):
        ret = None
        # first check to see if we have a name preset
        if self.base_filename in PPMIFile.file_tabled:
            ret = PPMIFile.file_tabled[self.base_filename]
        # now look and see if there is a unique page_name
        elif len(self.pag_names) == 1:
            ret = self.pag_names[0]
        return(ret)

    def fetch_summary_dict(self):
        resultsd = {}
        resultsd["basename"] = self.base_filename
        resultsd["pat_id"] = self.has_pat_id
        resultsd["pag_names"] = self.pag_names_cnt
        resultsd["table_name"] = self.table_name
        return(resultsd)



if __name__ == "__main__":
    ppmi_curs = ppmilib.utils.SqliteCursor.ppmi()

    filenames = ppmilib.utils.fetch_ppmi_csv_filenames()
    results = []

    # process the csv files one by one
    for filename in filenames:
        ppmi_file = PPMIFile(filename)
        results.append(ppmi_file.fetch_summary_dict())

    pd_results = pd.DataFrame.from_dict(results)
    pd_results.to_csv("output/ppmi_files_results.csv", index=False)
