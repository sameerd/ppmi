import numpy as np
import pandas as pd

import ppmilib
import ppmilib.updrs3 as updrs3
from ppmilib.patient import Patient, PatientDict
from ppmilib.datadictionary import DataDictionary

import corex.corex as ce
from corex.utils import PrepareForCorex

from ete3 import Tree, ClusterTree, TreeStyle

# Get the UPDRS Part 3 
# dataframe of baseline UPDRS3 data of the NUPDRS3 page (this is pre-dose)
mds_updrs_3_bl = updrs3.fetch_updrs_3_file(event_id="BL", page_name="NUPDRS3")
updrs3_column_names = updrs3.extract_subscore_column_names(mds_updrs_3_bl)

patientsd = PatientDict.create()


# get the Benton Line Orientation Test data
# Create a dictionary that expands the column names into descriptions
data_dict = DataDictionary.create()
column_namesd = data_dict.get_column_dict("NUPDRS3")

# Benton Judgment of Line Orientation Score #
benton_df = ppmilib.utils.fetch_ppmi_data_file(
            "Benton_Judgment_of_Line_Orientation.csv", "non_motor")
benton_df = benton_df[(benton_df.EVENT_ID == "BL") & (benton_df.PAG_NAME == "BENTONOD")]

benton_cols_to_sum = [x for x in benton_df.columns.values.tolist() if x.startswith("BJLOT")]
#len(benton_cols_to_sum) == 30
benton_df["BJLOT"] = benton_df[benton_cols_to_sum].sum(axis=1)

mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, benton_df[["PATNO", "BJLOT"]] , on="PATNO")


# Hopkins Verbal Learning Test #
hvlt_df = ppmilib.utils.fetch_ppmi_data_file(
            "Hopkins_Verbal_Learning_Test.csv", "non_motor")
# It looks like all the data here is baseline so the next line is not strictly necessary
hvlt_df = hvlt_df[(hvlt_df.EVENT_ID == "BL") & (hvlt_df.PAG_NAME == "HVLT")]

# HVLT Immediate Recall
hvlt_df["HVLT_IR"] = hvlt_df[["HVLTRT%d"%i for i in range(1,4)]].sum(axis=1)

# HVLT Discrimination Recognition 
hvlt_df["HVLT_DR"] = hvlt_df["HVLTREC"] - (hvlt_df["HVLTFPRL"] + hvlt_df["HVLTFPUN"])

mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, 
        hvlt_df[["PATNO", "HVLTRDLY", "HVLTREC", "HVLT_IR", "HVLT_DR"]] , on="PATNO")



# Letter Number Sequencing #
lns_df = ppmilib.utils.fetch_ppmi_data_file(
            "Letter_-_Number_Sequencing__PD_.csv", "non_motor")
# Restrict to baseline
lns_df = lns_df[(lns_df.EVENT_ID == "BL") & (lns_df.PAG_NAME == "LNSPD")]

lns_cols = [x for x in lns_df.columns.values.tolist() if 
                    x.startswith("LNS") and len(x) == 5]
# len(lns_cols) == 21
lns_df["LNS_SUM"] = lns_df[lns_cols].sum(axis=1)
mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, 
        lns_df[["PATNO", "LNS_SUM"]] , on="PATNO")


# Semantic Fluency #
sem_df = ppmilib.utils.fetch_ppmi_data_file(
            "Semantic_Fluency.csv", "non_motor")
# Restrict to baseline
sem_df = sem_df[(sem_df.EVENT_ID == "BL") & (sem_df.PAG_NAME == "SFT")]
sem_df["SFT_SUM"] = sem_df[["VLTANIM", "VLTVEG", "VLTFRUIT"]].sum(axis=1)
mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, 
        sem_df[["PATNO", "SFT_SUM"]] , on="PATNO")


# Symbol Digit Modalities #
sdm_df = ppmilib.utils.fetch_ppmi_data_file(
            "Symbol_Digit_Modalities.csv", "non_motor")
# Restrict to baseline
sdm_df = sdm_df[(sdm_df.EVENT_ID == "BL") & (sdm_df.PAG_NAME == "SDM")]
mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, 
    sdm_df[["PATNO", "SDMTOTAL"]] , on="PATNO")

# MOCA
moca_df = ppmilib.utils.fetch_ppmi_data_file(
            "Montreal_Cognitive_Assessment__MoCA_.csv", "non_motor")
# Restrict to baseline

# restrict to baseline as well as screening because the test was 
# administered at both places
moca_df = moca_df[((moca_df.EVENT_ID == "BL") | (moca_df.EVENT_ID == "SC")
    ) & (moca_df.PAG_NAME == "MOCA")]
# now look for places where we have both BL and SC and remove SC
# Looks like only one patient is scored at both BL and SC
# Lets replace them with the baseline version
mask = moca_df.PATNO.duplicated(keep=False) & (moca_df.EVENT_ID == "SC")
moca_df = moca_df[~mask]

# Check to see that we only have unique patients in our dataframe
#len(moca_df.PATNO.unique()) == moca_df.shape[0]

mca_cols = [x for x in moca_df.columns.values if x.startswith("MCA")]
len(mca_cols)
mca_subscore_cols = [x for x in mca_cols if x not in 
                        ("MCATOT", "MCAVFNUM")]

# * Checking if raw calculations match up with MCATOT * #
#moca_df["MCA_TOT"] = moca_df[mca_subscore_cols].sum(axis=1)
#
#patientsd.add_socio_economics()
#
## drop all the patients that have moca but do not have status
#mask = np.array([False if x not in patientsd.patientsd.keys() else 
#            True for x in moca_df.PATNO])
#moca_df = moca_df[mask]
#
#moca_df["EDUCYRS"] = patientsd.get_education_years(moca_df.PATNO)
#
#mask = (moca_df["MCA_TOT"] < 30) & (moca_df["EDUCYRS"] <= 12)
#moca_df.MCA_TOT[mask] += 1
#
#import matplotlib.pyplot as plt
#plt.plot(moca_df.MCATOT - moca_df.MCA_TOT)
#plt.show() 

# MCATOT and MCA_TOT look fairly similar to each other except for a few outliers
# FIXME: The outliers need to be checked and understood



mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, 
    moca_df[["PATNO", "MCATOT"] + mca_subscore_cols] , on="PATNO")

enrolled_mask = patientsd.get_enrolled_mask(mds_updrs_3_bl.PATNO)
pd_mask = patientsd.get_pd_mask(mds_updrs_3_bl.PATNO)
# Reduce to only enrolled PD patients
mds_updrs_3_bl_enrolled_pd = mds_updrs_3_bl[enrolled_mask & pd_mask]
mds_updrs_3_bl_enrolled_pd.shape

# now analyze the data
from test_corex_updrs3 import ConvertListofClustersToTree, CreateListOfClusters

updrs3_expanded_column_names = [column_namesd[x] for 
        x in updrs3_column_names]
updrs3_expanded_column_names

moca_dict = data_dict.get_column_dict("MOCA")
moca_expanded_column_names = ["MOCA - " + moca_dict[x] for x in mca_subscore_cols]


mca_tot_min = np.nanmin(mds_updrs_3_bl_enrolled_pd["MCATOT"])
mca_tot_max = np.nanmax(mds_updrs_3_bl_enrolled_pd["MCATOT"])
mds_updrs_3_bl_enrolled_pd["MCATOT_ADJ"] = (mds_updrs_3_bl_enrolled_pd["MCATOT"] - mca_tot_min - 0.1) * 5 / (mca_tot_max - mca_tot_min)

#moca_updrs3 = PrepareForCorex(mds_updrs_3_bl_enrolled_pd, updrs3_column_names + ["MCATOT_ADJ"])
moca_updrs3 = PrepareForCorex(mds_updrs_3_bl_enrolled_pd, updrs3_column_names + mca_subscore_cols)
print(moca_updrs3.shape)
moca_updrs3


X = moca_updrs3

layer1 = ce.Corex(n_hidden=12, dim_hidden=5)
Y1 = layer1.fit_transform(X)
layer1.clusters
C1 = np.unique(layer1.clusters).size
layer1.tc # 5.09
layer1.tcs
Y1.shape
layer1.labels[0]
#retl = CreateListOfClusters(layer1, updrs3_expanded_column_names + ["MCA Scaled Total"])
retl = CreateListOfClusters(layer1, updrs3_expanded_column_names + moca_expanded_column_names)
retl



#layer2 = ce.Corex(n_hidden=C1-1)
layer2 = ce.Corex(n_hidden=5, dim_hidden=5)
Y2 = layer2.fit_transform(Y1)
layer2.clusters
C2 = np.unique(layer1.clusters).size
layer2.tc
layer2.tcs

retl2 = CreateListOfClusters(layer2, retl)
retl2

t = ConvertListofClustersToTree(retl2)
t.show()
#
