import ppmilib.utils as utils
import corex.corex as ce

data_dict_pd = utils.fetch_ppmi_data_file("Data_Dictionary.csv", "docs")

data_dict_nupdrs3 = data_dict_pd[data_dict_pd.MOD_NAME == "NUPDRS3"]
data_dict_nupdrs3 = data_dict_nupdrs3[data_dict_nupdrs3.SEQ_NO > 0]
data_dict_nupdrs3 = dict(zip(data_dict_nupdrs3.ITM_NAME, data_dict_nupdrs3.DSCR))

mds_updrs_3 = utils.fetch_ppmi_data_file("MDS_UPDRS_Part_III__Post_Dose_.csv",  \
        "motor")


mask = (mds_updrs_3.EVENT_ID == "BL")
mask = mask & (mds_updrs_3.PAG_NAME == "NUPDRS3")

mds_updrs_3_bl = mds_updrs_3[mask]

part_3_vars = [x for x in mds_updrs_3_bl.columns if (x[:2] == "NP" or x[:2] == "PN")]

len(part_3_vars == 33)


part_3_values = mds_updrs_3_bl[part_3_vars]

# drop missing values
part_3_values = part_3_values.dropna()

part_3_values = part_3_values.as_matrix()
part_3_values = part_3_values.astype(np.int_)


layer1 = ce.Corex(n_hidden=4)

layer1.fit(part_3_values)

variables = [None] * (layer1.clusters.max() + 1)

for i in range(layer1.clusters.size):
    cluster = layer1.clusters[i]
    if variables[cluster] is None:
        variables[cluster] = []
    print (cluster)
    print (part_3_vars[i])
    variables[layer1.clusters[i]].append(part_3_vars[i])
    
for i in range(len(variables)):
    print("Cluster " + str(i+1) +" : tcs %.2f" % layer1.tcs[i])
    for value in variables[i]:
        print(data_dict_nupdrs3[value])
    print("")





