import numpy as np
import pandas as pd

import ppmilib
import ppmilib.updrs3 as updrs3
import ppmilib.cognitive as cognitive
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


# Create a dictionary that expands the column names into descriptions
data_dict = DataDictionary.create()
column_namesd = data_dict.get_column_dict("NUPDRS3")

# Benton Judgment of Line Orientation Score #
benton_df = cognitive.fetch_benton_judgement_line_orientation(
                 event_id="BL", page_name = "BENTONOD", 
                 keep_important_cols_only=True)
mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, benton_df, on="PATNO")

# Hopkins Verbal Learning Test #
hvlt_df = cognitive.fetch_hopkins_verbal_learning_test(event_id="BL", 
        page_name="HVLT", keep_important_cols_only=True)

mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, hvlt_df, on="PATNO")

# Letter Number Sequencing #
lns_df = cognitive.fetch_letter_number_sequencing(event_id="BL",
        page_name="LNSPD", keep_important_cols_only=True)
mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, lns_df, on="PATNO")

# Semantic Fluency #
sem_df = cognitive.fetch_semantic_fluency(event_id="BL", page_name="SFT", 
        keep_important_cols_only = True)
mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, sem_df, on="PATNO")


# Symbol Digit Modalities #
sdm_df = cognitive.fetch_symbol_digit_modalities(event_id="BL",
        page_name="SDM", keep_important_cols_only=True):
mds_updrs_3_bl = pd.merge(mds_updrs_3_bl, sdm_df, on="PATNO")

# MOCA
moca_df = cognitive.fetch_moca_assesment(event_id="BL|SC", 
        page_name="MOCA", keep_important_cols_only=False)

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
