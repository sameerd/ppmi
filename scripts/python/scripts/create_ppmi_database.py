import os
import os.path

import sqlite3

import pandas as pd

import ppmilib
import ppmilib.utils

class PPMIFile:
    """ 
        Read in a csv ppmi file and extract/set information about it. 
          * We figure out what table name to put the csv file in. 
            - First check and see if we have assigned a table name
            - If there is a single page name in the csv file use that
            - If we cannot figure out a table name then don't put it in the db
    
    """

    file_tabled = {
        "FOUND_Status.csv":"FOUND",
        "IUSM_CATALOG.csv":"IUSM",
        "TAP-PD_OPDM_Assessment.csv":"OPDM",
        "TAP-PD_Kinetics_Device_Testing.csv":"KINETICS",
        "Center-Subject_List.csv":"CENTER",
        "Data_Dictionary.csv":"DATADICT",
        "Benton_Judgment_of_Line_Orientation.csv":"BENTON",
        "DaTSCAN_SPECT_Visual_Interpretation_Assessment.csv":"SPECTASS",
        "MRI_Imaging_Data_Transfer_Information_Source_Document.csv":"MRITRANS",
        "FBB_Metadata.csv":"FBBMETA",
        "FBB_Analysis_Data.csv":"FBBANAL",
        "Pilot_Biospecimen_Analysis_Results_Projects_101_and_103.csv":"BIOANAL",
        "DaTscan_Striatal_Binding_Ratio_Results.csv":"DATSBR",
        "AV-133_Image_Metadata.csv":"IMGMETA",
        "2011_Pilot__Projects_101,_102,_and_103.csv":"PILOT11",
        "Clinical_Labs.csv":"CLINLABS",
        "Page_Descriptions.csv":"PAGEDESC",
        "ST_CATALOG.csv":"STCAT",
        "RBD_PSG_Eligibility.csv":"RBDPSG",
        "SPECT_Scan_Information_Source_Document.csv":"SPECTSCN",
        "Olfactory_UPSIT.csv":"OLFUPSIT",
        "DATScan_Analysis.csv":"DATANAL",
        "ind_dat_source_data.csv":"INDDAT",
        "Inclusion_Exclusion.csv":"INCEXC",
        "ind_mri_source_data.csv":"INDMRI",
        "Patient_Status.csv":"PATSTAT",
        "MDS_UPDRS_Part_III__Post_Dose_.csv":"NUPDRS3",
        "Initiation_of_PD_Medication-_incidents.csv":"INITMEDS",
        "Cognitive_Categorization.csv":"COGCAT",
        "AV-133_SBR_Results.csv":"AV133SBR",
        "IUSM_BIOSPECIMEN_CELL_CATALOG.csv":"IUSMCAT",
        "Biospecimen_Analysis_Results.csv":"BIORES",
        "Code_List.csv":"CODELIST",

        # resolve conflicts
        "Laboratory_Procedures_with_Elapsed_Times.csv":"LABTIMES",
        "Laboratory_Procedures.csv":"LABPROC",
        "Neurological_Exam_-_Cranial_Nerves.csv":"NEURCRAN",
        "PASE_-_Household_Activity.csv":"PASEHSE",
        "PASE_-_Leisure_Time_Activity.csv":"PASETIME",
        "Lower_Extremity_Function__Mobility_.csv":"NQOLEEFS",
        "Upper_Extremity_Function-_Short_Form.csv":"NQOUEEFS"
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
        """ 
        pat_id is mostly PATNO but sometimes is study_subject_id (in some MRI
        files)
        """
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
        resultsd["pag_cnt"] = self.pag_names_cnt
        resultsd["table_name"] = self.table_name
        return(resultsd)

    def to_sql(self, con, index=False, *args, **kwargs):
        """
            FIXME: Use SQLAlchemy and keys if queries becomes slow
        """
        ret = None
        if self.table_name is not None:
            ret = self.pd_file.to_sql(self.table_name, con, index=index,
                    *args, **kwargs)
        return(ret)


if __name__ == "__main__":
    ppmi_curs = ppmilib.utils.SqliteCursor.ppmi()

    filenames = ppmilib.utils.fetch_ppmi_csv_filenames()
    results = []

    # process the csv files one by one
    for filename in filenames:
        ppmi_file = PPMIFile(filename)
        print("Processing %s" % ppmi_file.base_filename)
        results.append(ppmi_file.fetch_summary_dict())
        ppmi_file.to_sql(ppmi_curs.connection(), index=False, 
                ##Warning## if_exists="replace") # use carefully
                if_exists="fail")

    pd_results = pd.DataFrame.from_dict(results)
    pd_results.to_csv("output/ppmi_files_results.csv", index=False)

    # Check table_names for collisions
    collisions = pd_results[pd_results.table_name.duplicated(keep=False)]
    if len(collisions):
        print(collisions)

    # Check for the maximum length of the table name
    tmax = pd_results.table_name.map(lambda x: 0 if x is None else len(x)).max()
    if (tmax > 8):
        print ("Maximum Table name is larger than 8")
        print (pd_results[tmax > 8])

