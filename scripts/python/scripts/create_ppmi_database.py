import sys
import os
import os.path
import subprocess

import sqlite3

import pandas as pd

# Merge the files split into many files
path="Rscript ../R/Merge_Partials.r"
subprocess.call(path, shell=True)

# Create the updated data dictionary and shuffle deprecated files out
path="Rscript ../R/Create_data_dictionary.r"
subprocess.call(path, shell=True)

# Fix for not being able to import ppmilib when running from the command line
# See https://stackoverflow.com/questions/29548587/import-fails-when-running-python-as-script-but-not-in-ipython
sys.path = [''] + sys.path # Add current directory to the path
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
        # Real in annotated codelist N = 44
        "Participation_in_Other_Studies_Log.csv":"OTHCTRL",
        "AV-133_PET_Analysis.csv":"PET_AV133_SBR",
        "Modified_Semantic_Fluency.csv":"SFT",
        "Other_Clinical_Features.csv":"OTHFEATPD",
        "Clinical_Labs.csv":"CLINLAB",
        "Primary_Clinical_Diagnosis.csv":"PRIMDXPD",
        "Adverse_Event_Telephone_Assessment.csv":"TEL",
        "PD_Diagnosis_History.csv":"PDDXHIST",
        "Documentation_of_Informed_Consent.csv":"CONSENT",
        "Concomitant_Medication_Log.csv":"CONMED",
        "Inclusion_Exclusion.csv":"INCEXC",
        "Early_Imaging_Pregnancy_Test.csv":"AVPREGNANC",
        "LEDD_Concomitant_Medication_Log.csv":"LEDDLOG",
        "Benton_Judgement_of_Line_Orientation.csv":"LINEORNT",
        "University_of_Pennsylvania_Smell_Identification_Test__UPSIT_.csv":"UPSIT",
        "Screen_Fail.csv":"SCRNFAIL",
        "MDS-UPDRS_Part_I_Patient_Questionnaire.csv":"NUPDRS1P",
        "Features_of_Parkinsonism.csv":"FEATPD",
        "MDS_UPDRS_Part_III.csv":"NUPDRS3",
        "Early_Imaging_Eligibility.csv":"AVELIG",
        "MDS_UPDRS_Part_II__Patient_Questionnaire.csv":"NUPDRS2P",
        "MDS-UPDRS_Part_III_ON_OFF_Determination___Dosing.csv":"NUPDRDOSE",
        "Vital_Signs.csv":"VITAL",
        "MRI_Metadata.csv":"MRI_ACQUISITION",
        "Early_Imaging_Screen_Fail.csv":"AVSCRNFAIL",
        "Grey_Matter_Volume.csv":"GMVOLUME",
        "Early_Imaging_Conclusion_of_Study_Participation.csv":"AVCONCL",
        "_Tau_Substudy__MK-6240_PET_Imaging.csv":"TAUIMAG",
        "Prodromal_Cohort_Eligibility.csv":"PROELIG",
        "DaTScan_Analysis.csv":"DATSCAN_SBR",
        "Current_Biospecimen_Analysis_Results.csv":"Biospecimen_Analysis",
        "AV-133_PET_Metadata.csv":"PET_AV133_ACQUISITION",
        "_Tau_Substudy__Report_of_Pregnancy.csv":"TAUREPPREG",
        "Report_of_Pregnancy.csv":"REPPREG",
        "TAU_PET_Analysis.csv":"PET_TAU_SUVR",
        "DaTScan_Visual_Interpretation_Results.csv":"DATSCAN_VI_RESULTS",
        "Early_Imaging_Report_of_Pregnancy.csv":"AVREPPREG",
        "_Tau_Substudy__Pregnancy_Test.csv":"TAUPREGNANC",
        "Gait_Data___Arm_swing.csv":"GAIT",
        "iu_genetic_consensus_20220310.csv":"iu_genetic_consensus",
        "Age_at_visit.csv":"AGE_AT_VISIT",
        "TAU_PET_Metadata.csv":"PET_TAU_ACQUISITION",
        "Participant_Status.csv":"PATIENT_STATUS",
        "DaTScan_Metadata.csv":"DATSCAN_ACQUISITION",
        #Online questionares: N = 33 ##__## Need to ammend with _ONLINE
        "Parkinson_s_Disease_Sleep_Scale_PDSS-2__Online_.csv":"PDSS_ONL",
        "Health_History_Annually__Online_.csv":"HEALTHHXANNUAL_ONL",
        "Family_History_of_PD_1st_Degree_Relatives__Online_.csv":"FAMILYHXPD_ONL",
        "Assessment_of_Constipation__Online_.csv":"CONSTIPATION_ONL",
        "Race_and_Ethnicity__Online_.csv":"ETHNICITY_ONL",
        "History_of_Falls_Baseline__Online_.csv":"FALLSBL_ONL",
        "PD_History_Return_Study_Visit_for_PD_Cohort__Online_.csv":"RETURNPD_ONL",
        "Participant_Enrollment_Status__Online_.csv":"PARTICIPANTS_ONL",
        "Hyposmia_1Qx_from_Remote__Online_.csv":"HYPOSMIA1Q_ONL",
        "RBD1Q_Postuma_Acting_out_Dreams__Online_.csv":"RBD1Q_ONL",
        "Age_of_Parkinson_s_Disease_Diagnosis__Online_.csv":"PDAGE_ONL",
        "Health_History_Quarterly__Online_.csv":"HEALTHHXQUART_ONL",
        "Caffeine_Consumption__Online_.csv":"CAFFEINE_ONL",
        "Cognitive_Change__Online_.csv":"COGCHNG_ONL", 
        "Participant-Visit_Information__Online_.csv":"VISITS_ONL",
        "Smoking_History__Online_.csv":"SMOKINGHX_ONL",
        "Parkinson_Anxiety_Scale__Online_.csv":"PAS_ONL",
        "MDS-UPDRS_Part_I_Non-Motor_Aspects__Online_.csv":"NUPDRS1P_ONL",
        "Penn_Parkinson_s_Daily_Activities_Questionnaire-15__Online_.csv":"PDAQ15_ONL",
        "Geriatric_Depression_Scale__Online_.csv":"GDSSHORT_ONL",
        "COVID-19_History__Online_.csv":"COVIDHX_ONL",
        "High_Interest_Questions_for_PD_Cohort__Online_.csv":"HIGHINTQXPD_ONL",
        "Participant_Motor_Function_Questionnaire__Online_.csv":"PQUEST_ONL",
        "High_Interest_Questions_for_Non-PD_Cohort__Online_.csv":"HIGHINTQXNONPD_ONL",
        "Socioeconomic_Status__Online_.csv":"SES_ONL",
        "MDS-UPDRS_Part_II_Motor_Aspects__Online_.csv":"NUPDRS2P_ONL",
        "Epworth_Sleepiness_Scale__Online_.csv":"EPWORTH_ONL",
        "Head_Injuries__Online_.csv":"HEAD_ONL",
        "PPMI_RBD_Sleep_Questionnaire__Online_.csv":"RBD2_ONL",
        "History_of_Falls_Surveillance__Online_.csv":"FALLSSV_ONL",
        "Registration_Information__Online_.csv":"SCREENER_ONL",
        "Medication_History__Online_.csv":"MEDICATIONHX_ONL",
        "PD_History_Return_Study_Visit_for_NonPD_Cohort__Online_.csv":"RETURNNONPD_ONL",
        #Peripheral Biospecimins (CSF/Plasma) N = 18
        "Project_151_pQTL_in_CSF.csv":"PROJ151CSFPQTL",
        "Project_151_pQTL_in_CSF_Batch_Corrected.csv":"PROJ151CSFPQTLBATCHCOR",
        "PPMI_Project_196_CSF_Cardio_Counts.csv":"PROJ196CSFCARDIO",
        "PPMI_Project_196_CSF_Cardio_NPX.csv":"PROJ196CSFCARDIONPX",
        "PPMI_Project_196_CSF_INF_Counts.csv":"PROJ196CSFINFCOUNT",
        "PPMI_Project_196_CSF_INF_NPX.csv":"PROJ196CSFINFNPX",
        "PPMI_Project_196_CSF_ONC_Counts.csv":"PROJ196CSFONC",
        "PPMI_Project_196_CSF_ONC_NPX.csv":"PROJ196CSFONCNPX",
        "PPMI_Project_196_CSF_NEURO_Counts.csv":"PROJ196CSFNEUROCOUNT",
        "PPMI_Project_196_CSF_NEU_NPX.csv":"PROJ196CSFNEURONPX",
        "PPMI_Project_196_Plasma_CARDIO_Counts.csv":"PROJ196PLASMACARDIO",
        "PPMI_Project_196_Plasma_Cardio_NPX.csv":"PROJ196PLASMACARDIONPX",
        "PPMI_Project_196_Plasma_INF_Counts.csv":"PROJ196PLASMAINFCOUNT",
        "PPMI_Project_196_Plasma_INF_NPX.csv":"PROJ196PLASMAINFNPX",
        "PPMI_Project_196_Plasma_ONC_Counts.csv":"PROJ196PLASMAONCCOUNTS",
        "PPMI_Project_196_Plasma_ONC_NPX.csv":"PROJ196PLASMAONCNPX",
        "PPMI_Project_196_Plasma_Neuro_Counts.csv":"PROJ196PLASMANEURO",
        "PPMI_Project_196_Plasma_NEURO_NPX.csv":"PROJ196PLASMANEURONPX",
        # FOUND FILES N = 16
        "FOUND_Self-Reported_Dx.csv":"RFQ_FOUNDSRDX",
        "FOUND_Enrollment_Status.csv":"RFQ_PARTICIPANTS",
        "FOUND_RFQ_Anti-Inflammatory_Meds.csv":"RFQ_Anti-Inflammatory_Medication_History", 
        "FOUND_RFQ_Residential_History.csv":"RFQ_residential",
        "FOUND_RFQ_Physical_Activity.csv":"RFQ_physical_activity",
        "FOUND_RFQ_Pesticides_Non-Work.csv":"RFQ_pesticides_in_nonwork_setting",
        "FOUND_RFQ_Toxicant_History.csv":"RFQ_toxicant",
        "FOUND_RFQ_Alcohol.csv":"RFQ_alcohol",
        "FOUND_RFQ_Female_Reproductive_Health.csv":"RFQ_female_reproductive_health",
        "FOUND_RFQ_Smoking_History.csv":"RFQ_smoking",
        "FOUND_RFQ_Occupation.csv":"RFQ_occupation",
        "FOUND_RFQ_Head_Injury.csv":"RFQ_head_injury",
        "FOUND_RFQ_Calcium_Channel_Blockers.csv":"RFQ_calcium_channel_blocker_medication_history",
        "FOUND_RFQ_Height___Weight.csv":"RFQ_height_and_weight",
        "FOUND_RFQ_Pesticides_at_Work.csv":"RFQ_pesticides_at_work",
        "FOUND_RFQ_Caffeine.csv":"RFQ_caffeine",
        # Custom/Unkown N = 9 
        "PPMI_Original_Cohort_BL_to_Year_5_Dataset_Apr2020.csv":"OGCOHORTBLYR5",
        "PPMI_Prodromal_Cohort_BL_to_Year_1_Dataset_Apr2020.csv":"PRODROMALCOHORTBLYR5",
        "Targeted___untargeted_MS-based_proteomics_of_urine_in_PD.csv":"MSPROTEOMICSURINE",
        "iPSC_Catalog_Metadata.csv":"BIOSPECIMEN_CELL_META",
        "Subject_Cohort_History.csv":"SUBCOHORTHIST",
        "Pilot_Biospecimen_Analysis_Results.csv":"Biospecimen_Analysis_PILOT",
        "Metabolomic_Analysis_of_LRRK2_PD.csv":"LRRK2PD",
        "Deprecated_Biospecimen_Analysis_Results.csv":"Biospecimen_Analysis_Dep",
        "PPMI_PD_Variants_Genetic_Status_WGS_20180921.csv":"PD_WGSVARS",
        "Laboratory_Procedures_with_Elapsed_Times.csv":"LAB_ELAPSED",
        # Wearble Files
        "sleepmetrics2.csv":"SLEEPMETRICS",
        "stepcount.csv":"STEPCOUNT",
        "onwrist.csv":"ONWRIST",
        "timezone.csv":"TIMEZONE",
        "sleepstage.csv":"SLEEPSTAGE",
        "inbedtimes.csv":"INBEDTIMES",
        "prv.csv":"PRV",
        "pulserate.csv":"PULSERATE",
        "ambulatory.csv":"AMBULATORY",
        "IUSM_BIOSPECIMEN_CELL_CATALOG.csv":"BIOSPECIMEN_CELL_CATALOG",
        "IUSM_ASSAY_DEV_CATALOG.csv":"ASSAY_DEV_CATALOG",
        "IUSM_CATALOG.csv":"IUSM_CATALOG",
        #Codelist and Data Dictionaries N = 14
        "Code_List.csv":"CODELISTDEP",
        "Code_List_-_Harmonized.csv":"CODELIST_HARM",
        "Code_List_-__Annotated_.csv":"CODELIST",
        "Data_Dictionary.csv":"DICT",
        "Data_Dictionary_-_Harmonized.csv":"DATADICT_HARM",
        "Data_Dictionary_-__Annotated_.csv":"DATADICT_HARM_ANN",
        "FOUND_RFQ_Dictionary.csv":"DATADICT_FOUND",
        "Page_Descriptions.csv":"PAGEDESC",
        "PPMI_Online_Dictionary.csv":"DICT_ONL",
        "PPMI_Online_Codebook.csv":"CODELIST_ONL",
        "PPMI_Project_151_pqtl_Analysis_Annotations_20210210.csv":"p151_Anno",
        "Derived_Variable_Definitions_and_Score_Calculations.csv":"Derive",
        "Deprecated_Variables.csv":"DEP_VAR",
        "Deprecated_Biospecimen_Analysis_Results.csv":"DEPBIO",
        }
    def __init__(self, filename):
        self.filename = filename
        self.base_filename = os.path.basename(filename)
        self.pd_file = ppmilib.utils.fetch_raw_ppmi_data_file(filename)
        #self.pd_file = alt_fetch_raw_ppmi_data_file(filename)
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
            ("patno" in self.pd_headers) or \
            ("ALIAS_ID" in self.pd_headers) or \
            ("subject" in self.pd_headers) or \
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
    #tmax = pd_results.table_name.map(lambda x: 0 if x is None else len(x)).max()
    #if (tmax > 8):
        #print ("Maximum Table name is larger than 8")
        #print (pd_results[tmax > 8])

