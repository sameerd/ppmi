import numpy as np

def PrepareForCorex(df, updrs3_column_names):
    """Prepare the dataframe for input into Corex"""
    # reduce to part 3 variables only
    x = df[updrs3_column_names]
    # drop NA's for now. FIXME: replace by -1's later
    x = x.dropna()
    # cast to integer matrix
    x = x.as_matrix().astype(np.int_)
    return x


