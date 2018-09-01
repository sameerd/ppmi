# Parkinson's Progressive Markers Initiative [PPMI](https://www.ppmi-info.org/)

## About
This repository has code that is used to process data from the PPMI dataset.
There are **no data files** stored in this repository. 

## Setup the database

1. Apply for data access at [PPMI- Download
   Data](https://www.ppmi-info.org/access-data-specimens/download-data/)

1. After your application is approved and you can log in 
    1. click on `Download` -> `Study-Data`. 
    1. Click the link on the left hand side (bottom) where it says `ALL` 
    1. Download `ALL tabular data` (csv format) and `ALL documents and zip files` [48.0 MB]

1. Clone this github repository

1. Save the downloaded files in the [data_docs directory](./data_docs/) of this cloned repository.
   Extract any zip files if necessary.

1. Run the [create_ppmi_database.py](./python/scripts/create_ppmi_database.py)
   script which will create the ppmi database in the [database directory](./database)

## Using the database

1. Install [DB Browser for SQLite](https://sqlitebrowser.org/) and use it
   to open the database that was created for you in the [database directory](./database). 

1. `DB Browser` will will give you information on all the tables in the
database. You can browser the data by table. After you have extracted information into the 
[data_docs directory](./data_docs/) (see *Setup the database*), you will get
further information on what the columns represent by looking at the files in the [docs
directory](./data_docs/).
   * [Page_Descriptions.csv](./data_docs/Page_Descriptions.csv) A general idea of what the tables are named
   * [Data_Dictionary.csv](./data_docs/Data_Dictionary.csv) A general idea of what the columns in the table are named
   * [Code_List.csv](./data_docs/Code_List.csv) A code book that tells us how certain variables are coded
   * [Derived Variables
     Definition](./data_docs/Derived_Variable_Definitions_and_Score_Calculations.csv)
A document that tells us how to create derived variables like UPDRS scores etc. 

1. Use SQL scripts to extract information from the database.

```sql
WITH A AS ( /* Calculated Part III UPDRS Score for everyone */
  SELECT PATNO, EVENT_ID , 
    NP3SPCH +  NP3FACXP +  NP3RIGN + NP3RIGRU + NP3RIGLU + PN3RIGRL + 
    NP3RIGLL + NP3FTAPR + NP3FTAPL + NP3HMOVR + NP3HMOVL + NP3PRSPR + 
    NP3PRSPL + NP3TTAPR + NP3TTAPL + NP3LGAGR + NP3LGAGL + NP3RISNG + 
    NP3GAIT + NP3FRZGT + NP3PSTBL + NP3POSTR + NP3BRADY + NP3PTRMR +
    NP3PTRML + NP3KTRMR + NP3KTRML + NP3RTARU + NP3RTALU + NP3RTARL + 
    NP3RTALL + NP3RTALJ + NP3RTCON  as UPDRS_SCORE
  FROM NUPDRS3 WHERE 
   PAG_NAME = "NUPDRS3" 
  ORDER BY PATNO)
/* Extract UPDRS scores at Baseline and sort in descending order */
SELECT * from A WHERE EVENT_ID="BL" ORDER BY UPDRS_SCORE DESC
```

You can find more complex sql scripts in the [scripts directory](./scripts/sql/)
