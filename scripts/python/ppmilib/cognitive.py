import utils

# All the routines for cognitive data go in here

def fetch_benton_judgement_line_orientation(event_id="BL", 
        page_name="BENTONOD", keep_important_cols_only=True): 
    """ returns dataframe with Benton Judgment of Line Orientation Score """
    benton_df = utils.fetch_ppmi_data_file(
            "Benton_Judgment_of_Line_Orientation.csv", "non_motor")
    benton_df = benton_df[(benton_df.EVENT_ID == event_id) & 
                          (benton_df.PAG_NAME == page_name)]

    benton_cols_to_sum = [x for x in benton_df.columns.values.tolist() if 
                          x.startswith("BJLOT")]
    #len(benton_cols_to_sum) == 30
    benton_df["BJLOT"] = benton_df[benton_cols_to_sum].sum(axis=1)

    if (keep_important_cols_only): # only want the total score
        benton_df = benton_df[["PATNO", "BJLOT"]]

    return(benton_df)


def fetch_hopkins_verbal_learning_test(event_id="BL",
        page_name="HVLT", keep_important_cols_only=True):
    """ Hopkins Verbal Learning Test """
    hvlt_df = utils.fetch_ppmi_data_file("Hopkins_Verbal_Learning_Test.csv", 
            "non_motor")
    # It looks like all the data here is baseline so the next line is not
    # strictly necessary
    hvlt_df = hvlt_df[(hvlt_df.EVENT_ID == event_id) & 
                      (hvlt_df.PAG_NAME == page_name)]

    # HVLT Immediate Recall
    hvlt_df["HVLT_IR"] = hvlt_df[["HVLTRT%d"%i for i in range(1,4)]].sum(axis=1)

    # HVLT Discrimination Recognition 
    hvlt_df["HVLT_DR"] = hvlt_df["HVLTREC"] - \
        (hvlt_df["HVLTFPRL"] + hvlt_df["HVLTFPUN"])

    if (keep_important_cols_only): # only want a few columns
        hvlt_df = hvlt_df[["PATNO", "HVLTRDLY", "HVLTREC", 
                                    "HVLT_IR", "HVLT_DR"]]

    return(hvlt)


def fetch_letter_number_sequencing(event_id="BL", page_name="LNSPD", 
        keep_important_cols_only=True):
    """ Letter Number Sequencing """
    lns_df = utils.fetch_ppmi_data_file("Letter_-_Number_Sequencing__PD_.csv", 
                "non_motor")
    # Restrict to baseline
    lns_df = lns_df[(lns_df.EVENT_ID == event_id) & 
                    (lns_df.PAG_NAME == page_name)]

    lns_cols = [x for x in lns_df.columns.values.tolist() if 
                        x.startswith("LNS") and len(x) == 5]
    # len(lns_cols) == 21
    
    lns_df["LNS_SUM"] = lns_df[lns_cols].sum(axis=1)

    if (keep_important_cols_only):
        lns_df = lns_df[["PATNO", "LNS_SUM"]]

    return(lns_df)

def fetch_semantic_fluency(event_id="BL", page_name="SFT", 
        keep_important_cols_only=True):
    """ Semantic Fluency"""

    sem_df = utils.fetch_ppmi_data_file("Semantic_Fluency.csv", "non_motor")
    
    # Restrict to baseline
    sem_df = sem_df[(sem_df.EVENT_ID == event_id) & 
                    (sem_df.PAG_NAME == page_name)]
    sem_df["SFT_SUM"] = sem_df[["VLTANIM", "VLTVEG", "VLTFRUIT"]].sum(axis=1)

    if (keep_important_cols_only):
        sem_df = sem_df[["PATNO", "SFT_SUM"]]

    return(sem_df)


def fetch_symbol_digit_modalities(event_id="BL", page_name="SDM",
        keep_important_cols_only=True):
    """ Symbol Digit Modalities"""
    sdm_df = utils.fetch_ppmi_data_file("Symbol_Digit_Modalities.csv", 
            "non_motor")
    # Restrict to baseline
    sdm_df = sdm_df[(sdm_df.EVENT_ID == event_id) & 
                    (sdm_df.PAG_NAME == page_name)]
    
    if (keep_important_cols_only):
        sdm_df = sdm_df[["PATNO", "SDMTOTAL"]]

    return(sdm_df)


def fetch_moca_assesment(event_id="BL|SC", page_name="MOCA",
        keep_important_cols_only=True):
    """ Fetch the MOCA assesment. 
        This doesn't work right now for event ID's other than than BL|SC. 
    """

    moca_df = utils.fetch_ppmi_data_file(
            "Montreal_Cognitive_Assessment__MoCA_.csv", "non_motor")

    # Restrict to baseline as well as screening because the test was
    # administered at both places
    event_mask = None
    if event_id.contains("|"):
        event_id_sp = event_id.split("|")
        event_mask = (moca_df.EVENT_ID == event_id_sp[0]) | \
                     (moca_df.EVENT_ID == event_id_sp[1])
    else:
        event_mask = (moca_df.EVENT_ID == event_id)

    moca_df = moca_df[(event_mask) & (moca_df.PAG_NAME == page_name)]

    # now look for places where we have both BL and SC and remove SC
    # Looks like only one patient is scored at both BL and SC
    # Lets replace them with the baseline version
    mask = moca_df.PATNO.duplicated(keep=False) & (moca_df.EVENT_ID == "SC")
    moca_df = moca_df[~mask]

    # Check to see that we only have unique patients in our dataframe
    #len(moca_df.PATNO.unique()) == moca_df.shape[0]

    if(keep_important_cols_only):
        moca_df = moca_df["PATNO", "MCATOT"]

    return(moca_df)


