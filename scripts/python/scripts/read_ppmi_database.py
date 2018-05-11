
import pandas as pd

import ppmilib
import ppmilib.utils

if __name__ == "__main__":
    ppmi_curs = ppmilib.utils.SqliteCursor.ppmi()

    results = pd.read_sql("""
        SELECT PATSTAT.PATNO, NUPDRS3.EVENT_ID, NUPDRS3.NP3FACXP 
        FROM PATSTAT
        INNER JOIN NUPDRS3 ON
            PATSTAT.PATNO = NUPDRS3.PATNO
        WHERE
            PATSTAT.RECRUITMENT_CAT = 'PD' AND
            PATSTAT.ENROLL_STATUS = 'Enrolled' AND
            NUPDRS3.EVENT_ID = 'BL';
        """, ppmi_curs.connection())
