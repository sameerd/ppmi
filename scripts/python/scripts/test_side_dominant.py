import numpy as np
import pandas as pd

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

# Create a dictionary that expands the column names into descriptions
data_dict = DataDictionary.create()
column_namesd = data_dict.get_column_dict("NUPDRS3")


lat_index = updrs3.compute_lateralization_index(mds_updrs_3_bl)

side_dominance = pd.cut(lat_index, [-1000,-0.1, 0.1, 1000], 
        labels=["left", "assym", "right"] )
mds_updrs_3_bl["side_dominance"] = side_dominance

# lets only get the patients where side dominance is not Null
# this usually happens when most subscores are zero
updrs3_lateral_bl  = mds_updrs_3_bl[~side_dominance.isnull()]
#updrs3_lateral_bl.shape
#updrs3_lateral_bl.side_dominance.unique()

right_columns = updrs3.get_right_columns()
left_columns = updrs3.get_left_columns()

def rename_side_dominant_column(colr, coll):
    """ Give names to dominant/nondominant columns
        We iterate through the strings and assume that they are mostly equal
        When they are not equal we look for R and L and replace that with D
        (Dominant) and N (Non-Dominant)
    """ 
    def replace_letters(r,l):
        """ Replace letters with D and N only if r=R and l=L""" 
        ret = (r,l)
        if r == "R" and l == "L":
            ret = ("D", "N") 
        return ret 
    return map(lambda x: "".join(x), # join individual chars into strings
            zip(*[replace_letters(r,l) for r,l in zip(colr, coll)]))
            

dominant_columns, non_dominant_columns =  zip(*
    [rename_side_dominant_column(x,y) for x,y in 
    zip(right_columns, left_columns)])


for i in range(len(right_columns)):
    # if the side dominance is 'right' then assign the right column to the
    # dominant column else assign the left column
    updrs3_lateral_bl.loc[:, dominant_columns[i]] = \
        updrs3_lateral_bl[right_columns[i]].where(
                updrs3_lateral_bl['side_dominance'] == 'right', 
                updrs3_lateral_bl[left_columns[i]])
    # if the side dominance is not 'right' then assign the right column to the
    # non-dominant column else assign the left column
    updrs3_lateral_bl.loc[:, non_dominant_columns[i]] = \
        updrs3_lateral_bl[right_columns[i]].where(
                updrs3_lateral_bl['side_dominance'] != 'right', 
                updrs3_lateral_bl[left_columns[i]])

# this assignment screws up the assym category so lets drop those

updrs3_side_bl = updrs3_lateral_bl[
        updrs3_lateral_bl['side_dominance'] != 'assym']
#updrs3_lateral_bl.shape
#updrs3_side_bl.shape

# Create a Patients Dictionary
patient_dict = PatientDict.create()
# Create masks of enrolled patients and PD patients
enrolled_mask = patient_dict.get_enrolled_mask(updrs3_side_bl.PATNO)
pd_mask = patient_dict.get_pd_mask(updrs3_side_bl.PATNO)

# Reduce to only enrolled PD patients
updrs3_side_bl_enrolled_pd = updrs3_side_bl[enrolled_mask & pd_mask]
updrs3_side_bl_enrolled_pd.shape

updrs3_side_names = list(updrs3_column_names) # make a copy()
for i, name in enumerate(updrs3_column_names):
    for j, rname in enumerate(right_columns):
        if name == rname:
            updrs3_side_names[i] = dominant_columns[j]
            column_namesd[dominant_columns[j]] = \
                column_namesd[rname] + " - Dominant"
    for j, lname in enumerate(left_columns):
        if name == lname:
            updrs3_side_names[i] = non_dominant_columns[j]
            column_namesd[non_dominant_columns[j]] = \
                column_namesd[lname] + " - NonDominant"

updrs3_side_expanded_column_names = [column_namesd[x] for 
        x in updrs3_side_names]
updrs3_side_expanded_column_names

updrs3_side_values = PrepareForCorex(updrs3_side_bl, updrs3_side_names)
print(updrs3_side_values.shape)

updrs3_side_enrolled_pd_values = PrepareForCorex(
        updrs3_side_bl_enrolled_pd, updrs3_side_names)
print(updrs3_side_enrolled_pd_values.shape)


from test_corex_updrs3 import ConvertListofClustersToTree, CreateListOfClusters

#X = updrs3_side_values
X = updrs3_side_enrolled_pd_values

layer1 = ce.Corex(n_hidden=12, dim_hidden=5)
Y1 = layer1.fit_transform(X)
layer1.clusters
C1 = np.unique(layer1.clusters).size
layer1.tc # 5.09
layer1.tcs
Y1.shape
layer1.labels[0]
retl = CreateListOfClusters(layer1, updrs3_side_expanded_column_names)
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
