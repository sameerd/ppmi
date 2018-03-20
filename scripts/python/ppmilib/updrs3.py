from . import utils

def fetch_updrs_3_file(event_id="BL", page_name="NUPDRS3"):
    """Get the UPDRS Part 3 data. The default arguments will return baseline
    UPDRS3 data pre-dose data. Pass in nones to get the raw file"""

    mds_updrs_3 = utils.fetch_ppmi_data_file(
            "MDS_UPDRS_Part_III__Post_Dose_.csv", "motor")

    # Create a mask of the baseline
    event_id_mask = None
    if event_id is not None:
        event_id_mask = (mds_updrs_3.EVENT_ID == event_id)

    # Create a mask of the NUPDRS3 page (this is pre-dose)
    page_name_mask = None
    if page_name is not None:
        page_name_mask = (mds_updrs_3.PAG_NAME == page_name)

    combined_mask = None
    if event_id_mask is None:
        combined_mask = page_name_mask
    else: # event_id_mask is not None
        combined_mask = event_id_mask
        if page_name_mask is not None:
            combined_mask = combined_mask & page_name_mask

    ret = mds_updrs_3
    if combined_mask is not None:
        ret = mds_updrs_3[combined_mask]

    return ret


def extract_subscore_column_names(df):
    """Extract the column names for the subscores of UPDRS3"""
    return [x for x in df.columns if (x[:2] == "NP" or x[:2] == "PN")]

def get_non_tremor_columns(side = None):
    """ This gets the columns associated with Bradykinesia or rigidity. 
        side : can be None, 'right' or 'left' """

    # NP3RIGRU 3.3b Rigidity - RUE
    # PN3RIGRL 3.3d Rigidity - RLE
    # NP3FTAPR 3.4a Finger Tapping Right Hand
    # NP3HMOVR 3.5a Hand movements - Right Hand
    # NP3PRSPR 3.6a Pronation-Supination - Right Hand
    # NP3TTAPR 3.7a Toe tapping - Right foot
    # NP3LGAGR 3.8a Leg agility - Right leg

    right_side_columns = ["NP3RIGRU", "PN3RIGRL", "NP3FTAPR", "NP3HMOVR",
            "NP3PRSPR", "NP3TTAPR", "NP3LGAGR"]

    # NP3RIGLU 3.3c Rigidity - LUE
    # NP3RIGLL 3.3e Rigidity - LLE
    # NP3FTAPL 3.4b Finger Tapping Left Hand
    # NP3HMOVL 3.5b Hand movements - Left Hand
    # NP3PRSPL 3.6b Pronation-Supination - Left Hand
    # NP3TTAPL 3.7b Toe tapping - Left foot
    # NP3LGAGL 3.8b Leg agility - Left leg

    left_side_columns = ["NP3RIGLU", "NP3RIGLL", "NP3FTAPL", "NP3HMOVL",
            "NP3PRSPL", "NP3TTAPL", "NP3LGAGL"]

    ret = None
    if side is None:
        ret = right_side_columns + left_side_columns
    elif side == 'right':
        ret = right_side_columns
    elif side == 'left':
        ret = left_side_columns
    else:
        raise ValueError("side must be None or 'left' or 'right'")

    return ret


def get_tremor_columns(side=None):
    """ This gets the columns associated with tremor. 
        side : can be None, 'right' or 'left' """
    
    # NP3PTRMR 3.15a Postural tremor - Right Hand
    # NP3KTRMR 3.16a Kinetic tremor - Right hand
    # NP3RTARU 3.17a Rest tremor amplitude - RUE
    # NP3RTARL 3.17c Rest tremor amplitude - RLE

    right_side_columns = ["NP3PTRMR", "NP3KTRMR", "NP3RTARU", "NP3RTARL"]


    # NP3PTRML 3.15b Postural tremor - Left hand
    # NP3KTRML 3.16b Kinetic tremor - Left hand
    # NP3RTALU 3.17b Rest tremor amplitude - LUE
    # NP3RTALL 3.17d Rest tremor amplitude - LLE

    left_side_columns = ["NP3PTRML", "NP3KTRML", "NP3RTALU", "NP3RTALL"]

    ret = None
    if side is None:
        ret = right_side_columns + left_side_columns
    elif side == 'right':
        ret = right_side_columns
    elif side == 'left':
        ret = left_side_columns
    else:
        raise ValueError("side must be None or 'left' or 'right'")

    return ret

def get_right_columns(include_tremor=True):
    ret = get_non_tremor_columns(side='right')
    if include_tremor is True:
        ret += get_tremor_columns(side='right')
    return ret

def get_left_columns(include_tremor=True):
    ret = get_non_tremor_columns(side='left')
    if include_tremor is True:
        ret += get_tremor_columns(side='left')
    return ret

def compute_lateralization_index(df, include_tremor=True):
    """ Compute the lateralization index for side dominant classification"""
    right_index = sum([df[col] for col in get_right_columns(include_tremor)])
    left_index = sum([df[col] for col in get_left_columns(include_tremor)])

    lat_index = (right_index - left_index) / (right_index + left_index)
    return lat_index


