import utils

class DataDictionary(object):
    """ Wrapper for the data dictionary to explain all the variable names """

    def __init__(self, datadict_df):
        self.datadict_df = datadict_df

    def get_column_dict(self, modname):
        """ Get a dictionary of all the variable names in a module """
        ret = self.datadict_df[self.datadict_df.MOD_NAME == modname]
        ret = ret[ret.SEQ_NO > 0]
        return dict(zip(ret.ITM_NAME, ret.DSCR))

    @staticmethod
    def create():
        datadict_df = utils.fetch_ppmi_data_file("Data_Dictionary.csv", "docs")
        return DataDictionary(datadict_df)



