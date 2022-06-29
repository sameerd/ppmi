#! /usr/local/bin/Rscript
library(dplyr)

# The Purpose of this script is to combine Datadictionary, pagelist, codelist files
files <- c('../../data_docs/Data_Dictionary_-__Annotated_.csv',
           '../../data_docs/FOUND_RFQ_Dictionary.csv',
           '../../data_docs/PPMI_Online_Dictionary.csv')
dd <- data.table::fread(files[1], header=T, sep=',') %>%
  as.data.frame()

rfq <- data.table::fread(files[2], header=T, sep=',') %>%
  as.data.frame()
rfq$MOD_NAME[ rfq$MOD_NAME == 'RFQ_Anti-Inflammatory Medication History' ] <- 
  'RFQ_Anti-Inflammatory_Medication_History'

onl <- data.table::fread(files[3], header=T, sep=',') %>%
  as.data.frame()
onl$MOD_NAME <- paste0(onl$MOD_NAME, '_ONL')


keeps <- c("MOD_NAME", "ITM_NAME", "DSCR", "ITM_TYPE", "FLD_LEN", "DECML")

#fix timestamps:
rfq[grepl('timestamp', rfq$ITM_NAME),]$ITM_TYPE <- 'TIMESTAMP'
dd[dd$ITM_NAME %in% 'LAST_UPDATE',]$ITM_TYPE <- 'TIMESTAMP'

main <- as.data.frame(rbind( dd[,keeps], rfq[,keeps], onl[,keeps] ))

# Add Missing FOUND files
temp <- rbind( 
    c('RFQ_FOUNDSRDX', '', 'Patient Self-reported diagnosis RFQ Found',	'', '', NA),
    c('RFQ_FOUNDSRDX', 'PATNO', 'PPMI Patient Number',	'CHAR', 8, NA),
    c('RFQ_FOUNDSRDX', 'EVENT_NAME', 'Event Name',	'CHAR', 20, NA),
    c('RFQ_FOUNDSRDX', 'SRDXDATE', 'Date self-reported diagnosis reported',	'DATE', '', NA),
    c('RFQ_FOUNDSRDX', 'FOPTRDX', 'Subject reported diagnosis',	'CHAR', 200, NA),
    c('RFQ_FOUNDSRDX', 'FOPTRDXOTHER', 'Subject reported diagnosis - other specify',	'CHAR', 500, NA),
    c('RFQ_FOUNDSRDX', 'update_stamp', 'Time the record was ingested/updated in the data warehouse',	'TIMESTAMP', '', NA), 
    c("RFQ_PARTICIPANTS", '',            "Patient Enrollment Status RFQ Found",  '',      '', NA),
    c("RFQ_PARTICIPANTS", "FOCONSENTDT", "Date signed consent form received",   "DATE",   '', NA),
    c("RFQ_PARTICIPANTS", "FOFOLLOWMO",  "Number of Months followed in FOUND",  "NUMBER", 3, 0),
    c("RFQ_PARTICIPANTS", "FOFOLLOWST",  "FOUND follow-up status",              "NUMBER", 2, 0),
    c("RFQ_PARTICIPANTS", "FOSTATUS",    "FOUND STATUS",                        "NUMBER", 2, 0),
    c("RFQ_PARTICIPANTS", "PATNO",       "PPMI Patient Number",                 "CHAR",   8, NA	),
    c("RFQ_PARTICIPANTS", "LAST_UPDATE", "Time the record was ingested/updated in the data warehouse",	"TIMESTAMP", '', NA)
)
colnames(temp) <- colnames(main)
main <- as.data.frame(rbind( temp,  main))

#Fix page desc names with space in ITM_NAME
main[ main$ITM_NAME == ' ',]$ITM_NAME <- ''

# Find Pages without INDV descriptions:
adds <- rbind(
  c("AGE_AT_VISIT",              '', "Patient age at visit",  '', '', NA),
  c("AMBULATORY",                '', "Derived ambulatory metrics from digital sensor recordings",  '', '', NA),
  c("Biospecimen_Analysis",      '', "Biospecimin testing results",                                '', '', NA),
  c("BIOSPECIMEN_BRAIN_CATALOG", '', "Catalog of Postmortem Brain Samples",  '', '', NA),
  c("BIOSPECIMEN_CELL_CATALOG",  '', "Metadata of available ISUM Cell lines",  '', '', NA),
  c("BIOSPECIMEN_SLIDE_CATALOG", '', "Catalog of Postmortem Brain pathology slides",  '', '', NA),
  c("COVANCE",                   '', "Blood Chemistry and Hematology Data",  '', '', NA),
  c("FOUND",                     '', "Patient Consent and followup visit data",  '', '', NA),
  c("FOUNDSRDX",                 '', "Patient Self-reported diagnosis",  '', '', NA),
  c("INBEDTIMES",                '', "Derived rest metrics from digital sensor recordings",  '', '', NA),
  c("IUSM_CATALOG",              '', "Metadata of ISUM Biospecimins collected",  '', '', NA),
  c("ONWRIST",                   '', "Derived wearable metrics from digital sensor recordings",  '', '', NA),
  c("SLEEPMETRICS",              '', "Derived sleep metrics from digital sensor recordings",  '', '', NA),
  c("PULSERATE",                 '', "Derived pulse metrics data from digital sensor recordings",  '', '', NA),
  c("PRV",                       '', "Derived pulse variability metrics data from digital sensor recordings",  '', '', NA),
  c("PATH_RESULTS",              '', "Postmortem Brain Pathology Results",  '', '', NA),
  c("SLEEPSTAGE",                '', "Derived sleep stage metrics data from digital sensor recordings",  '', '', NA),
  c("ST_CATALOG",                '', "Symptomatic Therapy replaces Visit",  '', '', NA),
  c("STEPCOUNT",                 '', "Derived step metrics data data from digital sensor recordings",  '', '', NA),
  c("TIMEZONE",                  '', "Derived timezone metricsdata from digital sensor recordings",  '', '', NA)
)
colnames(adds) <- colnames(main)

main <- as.data.frame(rbind(main, adds))
main <- main[order(main$MOD_NAME),]

##############################################################################
# Annotate the CSF/Plasma data
npx <- list(
 "PROJ196CSFCARDIONPX" = "PPMI Project 196 CSF Cardio NPX",
 "PROJ196CSFINFNPX" = "PPMI Project 196 CSF INF NPX",
 "PROJ196CSFONCNPX" = "PPMI Project 196 CSF ONC NPX",
 "PROJ196CSFNEURONPX" = "PPMI Project 196 CSF NEU NPX",
 "PROJ196PLASMACARDIONPX" = "PPMI Project 196 Plasma Cardio NPX",
 "PROJ196PLASMAINFNPX" = "PPMI Project 196 Plasma INF NPX",
 "PROJ196PLASMAONCNPX" = "PPMI Project 196 Plasma ONC NPX",
 "PROJ196PLASMANEURONPX" = "PPMI Project 196 Plasma NEURO NPX"
)

cnts <- list(
  "PROJ196CSFCARDIO"= 'PPMI Project 196 CSF Cardio Counts',
  "PROJ196CSFINFCOUNT" = 'PPMI Project 196 CSF INF_Counts',
  "PROJ196CSFONC" = 'PPMI Project 196 CSF ONC_Counts',
  "PROJ196CSFNEUROCOUNT" = 'PPMI Project 196 CSF NEURO_Counts',
  "PROJ196PLASMACARDIO" = 'PPMI Project 196 Plasma CARDIO_Counts',
  "PROJ196PLASMAINFCOUNT" = 'PPMI Project 196 Plasma INF_Counts',
  "PROJ196PLASMAONCCOUNTS" = 'PPMI Project 196 Plasma ONC_Counts',
  "PROJ196PLASMANEURO" = 'PPMI Project 196 Plasma Neuro_Counts'
)

base_cnts <- rbind( 
  c('', '', '',	'', '', NA),
  c('', 'PATNO', 'PPMI Patient Number',	'CHAR', 9, NA),
  c('', 'EVENT_ID', 'Visit ID',	'CHAR', 3, NA),
  c('', 'PLATEID', 'ID of the plate the assay was preformed on',	'CHAR', '', NA),
  c('', 'PANEL', 'Target Array Panel type',	'CHAR', 6, NA),
  c('', 'ASSAY', 'Gene name of the assay target',	'CHAR', '', NA),
  c('', 'OLINKID', 'OLink ID',	'CHAR', 8, NA),
  c('', 'UNIPROT', 'UNIPROT ID of the assay target',	'CHAR', 6, NA),
  c('', 'COUNT', 'Raw value used to determine NPX values',	'NUMBER', '', NA),
  c('', 'INCUBATIONCONTROLCOUNT', 'Internal control: Olink internal assay control used in QC',	'NUMBER', '', NA),
  c('', 'AMPLIFICATIONCONTROLCOUNT', 'Internal control: Olink internal assay control used in QC',	'NUMBER', '', NA),
  c('', 'EXTENSIONCONTROLCOUNT', 'Internal and Normalization control: Olink internal assay control used in QC and normalization of counts for NPX values',	'NUMBER', '', NA),
  c('', 'update_stamp', 'Time the record was ingested/updated in the data warehouse',	'TIMESTAMP', '', NA) 
)
colnames(base_cnts) <- colnames(main)

base_npx <- rbind( 
  c('', '', '',	'', '', NA),
  c('', 'PATNO', 'PPMI Patient Number',	'CHAR', 9, NA),
  c('', 'EVENT_ID', 'Visit ID',	'CHAR', 3, NA),
  c('', 'INDEX', '',	'NUMBER', '', NA),
  c('', 'OLINKID', 'OLink ID',	'CHAR', 8, NA),
  c('', 'UNIPROT', 'UNIPROT ID of the assay target',	'CHAR', 6, NA),
  c('', 'ASSAY', 'Gene name of the assay target',	'CHAR', '', NA),
  c('', 'MISSINGFREQ', '',	'NUMBER', 6, 4),
  c('', 'PANEL', 'Target Array Panel type',	'CHAR', '', NA),
  c('', 'PANEL_LOT_NR', 'Assay Pannel Lot ID',	'CHAR', '6', NA),
  c('', 'PLATEID', 'ID of the plate the assay was preformed on',	'CHAR', '', NA),
  c('', 'QC_WARNING', 'Quality Control Value',	'CHAR', '', NA),
  c('', 'LOD', 'Limit of detection ( 3 sds below NPX mean for the assay)',	'NUMBER', '', 4),
  c('', 'NPX', 'Normalized protein expression (Log 2 scale)', 	'NUMBER', '', 4),
  c('', 'update_stamp', 'Time the record was ingested/updated in the data warehouse',	'TIMESTAMP', '', NA) 
)
colnames(base_npx) <- colnames(main)

#### loop through and build the data dictionary matrix for every plate

for( entry in names(npx)){
  temp <- base_npx
  temp[,1] <- entry
  temp[1,3] <- npx[[entry]]
  main <- as.data.frame(rbind(main, temp))
}

for( entry in names(cnts)){
  temp <- base_cnts
  temp[,1] <- entry
  temp[1,3] <- cnts[[entry]]
  main <- as.data.frame(rbind(main, temp))
}

# Add the proteomics translate id from the annotations file and move annotations file to deprecated folder
pqtl <-data.table::fread('../../data_docs/Project_151_pQTL_in_CSF.csv', header = T, sep = ',') %>%
  as.data.frame()
pqtl_batch <-data.table::fread('../../data_docs/Project_151_pQTL_in_CSF_Batch_Corrected.csv', header = T, sep = ',') %>%
  as.data.frame()
annot <-data.table::fread('../../data_docs/PPMI_Project_151_pqtl_Analysis_Annotations_20210210.csv', header = T, sep = ',') %>%
  as.data.frame()

# Clean weird extract columns
annot <- annot[ ,c('CHIP_PROBE_ID', 'SOMA_SEQ_ID', 'TARGET_GENE_ID', 'TARGET_GENE_SYMBOL', 'ORGANISM','DESCRIPTION_HH') ]

#Pull Multi IDs
multi <- annot[ annot$SOMA_SEQ_ID %in% names(table(annot$SOMA_SEQ_ID)[ table(annot$SOMA_SEQ_ID) > 1]), ] 
multi_ids <- multi$SOMA_SEQ_ID[!duplicated(multi$SOMA_SEQ_ID)]

# Filter out multi mapped SOMA_SEQ_ID's
annot <- annot[ !(annot$SOMA_SEQ_ID %in% names(table(annot$SOMA_SEQ_ID)[ table(annot$SOMA_SEQ_ID) > 1])), ] 

mulit_mat <- matrix(NA, length(multi_ids), dim(annot)[2]) %>%
  as.data.frame()
colnames(mulit_mat) <- colnames(annot)
mulit_mat$SOMA_SEQ_ID <- multi_ids

for( id in mulit_mat$SOMA_SEQ_ID ){
  mulit_mat[ mulit_mat$SOMA_SEQ_ID == id,]$CHIP_PROBE_ID <- 
    paste0( multi[ multi$SOMA_SEQ_ID %in% id,]$CHIP_PROBE_ID, collapse = ':')
  
  mulit_mat[ mulit_mat$SOMA_SEQ_ID == id,]$TARGET_GENE_ID<- 
    paste0( multi[ multi$SOMA_SEQ_ID %in% id,]$TARGET_GENE_ID, collapse = ':')
  
  mulit_mat[ mulit_mat$SOMA_SEQ_ID == id,]$TARGET_GENE_SYMBOL<- 
    paste0( multi[ multi$SOMA_SEQ_ID %in% id,]$TARGET_GENE_SYMBOL, collapse = ':')
  
  mulit_mat[ mulit_mat$SOMA_SEQ_ID == id,]$ORGANISM<- 
    paste0( multi[ multi$SOMA_SEQ_ID %in% id,]$ORGANISM, collapse = ':')
  
  mulit_mat[ mulit_mat$SOMA_SEQ_ID == id,]$DESCRIPTION_HH<- 
    paste0( multi[ multi$SOMA_SEQ_ID %in% id,]$DESCRIPTION_HH, collapse = ':')
}

annot <- rbind(annot, mulit_mat) %>%
  as.data.frame()
row.names(annot) <- annot$SOMA_SEQ_ID

# Annotate the pQTL Columns
pqtl$CHIP_PROBE_ID <- annot[ pqtl$TESTNAME,]$CHIP_PROBE_ID
pqtl$TARGET_GENE_ID <- annot[ pqtl$TESTNAME,]$TARGET_GENE_ID
pqtl$TARGET_GENE_SYMBOL <- annot[ pqtl$TESTNAME,]$TARGET_GENE_SYMBOL
pqtl$ORGANISM <- annot[ pqtl$TESTNAME,]$ORGANISM
pqtl$DESCRIPTION_HH <- annot[ pqtl$TESTNAME,]$DESCRIPTION_HH

pqtl_batch$CHIP_PROBE_ID <- annot[ pqtl_batch$TESTNAME,]$CHIP_PROBE_ID
pqtl_batch$TARGET_GENE_ID <- annot[ pqtl_batch$TESTNAME,]$TARGET_GENE_ID
pqtl_batch$TARGET_GENE_SYMBOL <- annot[ pqtl_batch$TESTNAME,]$TARGET_GENE_SYMBOL
pqtl_batch$ORGANISM <- annot[ pqtl_batch$TESTNAME,]$ORGANISM
pqtl_batch$DESCRIPTION_HH <- annot[ pqtl_batch$TESTNAME,]$DESCRIPTION_HH

pqtl$DESCRIPTION_HH <- gsub( ',',' /',pqtl$DESCRIPTION_HH )
pqtl_batch$DESCRIPTION_HH <- gsub( ',',' /',pqtl_batch$DESCRIPTION_HH )


pqtl <- pqtl[ , colnames(pqtl)[ !(colnames(pqtl) %in% 'column_label')] ]
pqtl_batch <- pqtl_batch[ , colnames(pqtl_batch)[ !(colnames(pqtl_batch) %in% 'column_label')] ]

# Now build data directory entry for each file:
base <- rbind( 
  c('PROJ151CSFPQTL', '', 'PPMI proteomics assessment in CSF',	'', '', NA),
  c('PROJ151CSFPQTL', 'PATNO', 'PPMI Patient Number',	'CHAR', 9, NA),
  c('PROJ151CSFPQTL', 'SEX', 'Patient Sex',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'COHORT', 'Cohort at Participant Creation',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'CLINICAL_EVENT', 'Clinical Event',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'TYPE', 'Sample Type',	'CHAR', 6, NA),
  c('PROJ151CSFPQTL', 'TESTNAME', 'SOMAscan platform Sequence ID',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'TESTVALUE', 'Test Value',	'NUMBER', '', 6),
  c('PROJ151CSFPQTL', 'UNITS', 'Test Unit of Measurement',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'PLATEID', 'Testplate ID',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'RUNDATE', 'Test Date',	'DATE', '', NA),
  c('PROJ151CSFPQTL', 'PROJECTID', 'PPMI Project ID',	'NUMBER', '', NA),
  c('PROJ151CSFPQTL', 'PI_NAME', 'Name of Project PI',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'PI_INSTITUTION', 'Institution of Project PI', 	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'update_stamp', 'Time the record was ingested/updated in the data warehouse',	'TIMESTAMP', '', NA),
  c('PROJ151CSFPQTL', 'CHIP_PROBE_ID', 'SOMAscan Platform Probe ID ',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'TARGET_GENE_ID', 'Target Gene(s) NCBI ID',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'TARGET_GENE_SYMBOL', 'Target Gene(s) Symbol',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'ORGANISM', 'Target Gene(s) Organism of origin',	'CHAR', '', NA),
  c('PROJ151CSFPQTL', 'DESCRIPTION_HH', 'Target Gene(s) Description',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', '', 'PPMI proteomics assessment in CSF batch corrected',	'', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'PATNO', 'PPMI Patient Number',	'CHAR', 9, NA),
  c('PROJ151CSFPQTLBATCHCOR', 'SEX', 'Patient Sex',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'COHORT', 'Cohort at Participant Creation',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'CLINICAL_EVENT', 'Clinical Event',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'TYPE', 'Sample Type',	'CHAR', 6, NA),
  c('PROJ151CSFPQTLBATCHCOR', 'TESTNAME', 'SOMAscan platform Sequence ID',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'TESTVALUE', 'Test Value',	'NUMBER', '', 6),
  c('PROJ151CSFPQTLBATCHCOR', 'UNITS', 'Test Unit of Measurement',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'PLATEID', 'Testplate ID',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'RUNDATE', 'Test Date',	'DATE', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'PROJECTID', 'PPMI Project ID',	'NUMBER', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'PI_NAME', 'Name of Project PI',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'PI_INSTITUTION', 'Institution of Project PI', 	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'update_stamp', 'Time the record was ingested/updated in the data warehouse',	'TIMESTAMP', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'CHIP_PROBE_ID', 'SOMAscan Platform Probe ID ',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'TARGET_GENE_ID', 'Target Gene(s) NCBI ID',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'TARGET_GENE_SYMBOL', 'Target Gene(s) Symbol',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'ORGANISM', 'Target Gene(s) Organism of origin',	'CHAR', '', NA),
  c('PROJ151CSFPQTLBATCHCOR', 'DESCRIPTION_HH', 'Target Gene(s) Description',	'CHAR', '', NA)
)
colnames(base) <- colnames(main)
main <- as.data.frame(rbind(main, base))

# Fix the Lab Elapsed Redundant MOD Name:
items <- c( 
  'REC_ID', 'QUERY', 'CNO', 'PATNO', 'EVENT_ID', 'PAG_NAME', 'INFODT', 'LMDT', 
  'LMTM', 'FASTSTAT', 'PDMEDYN', 'PDMEDDT', 'PDMEDTM', 'UASPEC', 'UASPECDT',
  'UT1TM', 'UT1SPNTM', 'UT1SPNRT', 'UT1SPNDR', 'UT1CFRG', 'UT1FTM', 'BLDWHL',
  'BLDWHLTM', 'BLDWHLVL', 'BLDWHLTMP', 'BLDDRDT', 'BLDRNA', 'BLDRNATM',  'RNAFDT',
  'RNAFTM', 'RNASTTMP', 'BLDPLAS', 'PLASTM', 'PLASPNTM', 'PLASPNRT', 'PLASPNDR', 
  'PLASCFRG', 'PLASVAFT', 'PLAALQN', 'PLASFTM', 'PLASTTMP', 'BLDSER', 'BLDSERTM',
  'BSSPNTM', 'BSSPNRT', 'BSSPNDR', 'BSCFRG', 'BSVAFT', 'BSALQN', 'BSFTM', 'BSSTTMP', 
  'PLASBFCT', 'DurUT1TM', 'DurUT1SPNTM', 'DurUT1FFTM', 'DurPLASTM', 'DurPLASSPNTM',
  'DurPLASFFTM', 'DurBLDSERTM', 'DurSERSPNTM', 'DurSERFFTM')

main[main$MOD_NAME == 'LAB' & main$ITM_NAME %in% items ,]$MOD_NAME <- 'LAB_ELAPSED'

main <- as.data.frame(rbind(
  main, 
  setNames(c('LAB_ELAPSED', '', 'Laboratory Procedures with Elapsed Times',	'', '', NA), colnames(main))
))

#Wearable Data time_zone is mis-annotated:
main[main$MOD_NAME == 'TIMEZONE' & main$ITM_NAME == 'timezone' ,]$ITM_NAME <- 'time_zone'

# WGS Data:
foo <- data.table::fread( '../../data_docs/PPMI_PD_Variants_Genetic_Status_WGS_20180921.csv', header = T, sep = ',' ) %>%
  as.data.frame()

temp_names <- setNames(
  paste0( 'rs', do.call(rbind, strsplit( colnames(foo)[ !(colnames(foo) %in% 'PATNO') ], '_rs' ))[,2] ),
  colnames(foo)[ !(colnames(foo) %in% 'PATNO') ]
)

base <- matrix('',length(temp_names),6)
colnames(base) <- colnames(main)
base[,1] <- 'PD_WGSVARS'
base[,2] <- names(temp_names)
base[,3] <- paste0('Alternate Allele dosage of ', as.character(temp_names), ' (hg19)')
base[,4] <- 'NUMBER'
base[,5] <- 1
base[,6] <- 0

rbind(
  setNames(c('PD_WGSVARS', '', 'Allele Dosage of PD relevant SNPs derived from WGS',	'', '', NA), colnames(main)),
  setNames(c('PD_WGSVARS', 'PATNO', 'Participant ID',	'NUMBER', '18', 0), colnames(main)),
  base
)
main <- as.data.frame(rbind(main, base))

### ISUM 
foo <- data.table::fread( '../../data_docs/IUSM_ASSAY_DEV_CATALOG.csv', header = T, sep = ',' ) %>%
  as.data.frame()

base <- as.data.frame( rbind( 
  main[ main$MOD_NAME %in% c('TRANSITION_STATUS', 'IUSM_CATALOG') & 
    main$ITM_NAME %in% colnames(foo), ],
  main[ main$MOD_NAME %in% c('BIOSPECIMEN_CELL_CATALOG') & 
          main$ITM_NAME %in% c('ADDTL_STOCK_AVAIL_ON_REQ'), ]
))

base$MOD_NAME <- 'ASSAY_DEV_CATALOG'
base2 <- rbind( 
  c('ASSAY_DEV_CATALOG', "" , 'IUSM Assay Catalog (In Development)',        '','', NA),
  c('ASSAY_DEV_CATALOG', "RIN_ROBOT"          , 'RIN machine used',         'CHAR','', NA),
  c('ASSAY_DEV_CATALOG', "QC_CLASS_RNA"       , 'Class of RNA',             'CHAR','', NA),
  c('ASSAY_DEV_CATALOG', "QC_STATUS_DNA_RNA"  , 'Status of RNA/DNA QC',     'CHAR','', NA),
  c('ASSAY_DEV_CATALOG', "CLOTTING"           , 'Is there clotting',        'CHAR','', NA),
  c('ASSAY_DEV_CATALOG', "TURBIDITY"          , 'How cloudy is the sample', 'CHAR','', NA),
  c('ASSAY_DEV_CATALOG', "AVERAGE_HEMOGLOBIN" , 'Hemoglobin levels',        'CHAR','', NA)
  
)
colnames(base2) <- colnames(base)

main <- as.data.frame(rbind(main, base2, base)) 

# IUSM Catalog:
foo <- data.table::fread( '../../data_docs/IUSM_CATALOG.csv', header = T, sep = ',' ) %>%
  as.data.frame()

base <- as.data.frame( rbind( 
  main[ main$MOD_NAME %in% c('IUSM_CATALOG') & 
          main$ITM_NAME %in% colnames(foo), ]
))

base$MOD_NAME <- 'IUSM_CATALOG'
base2 <- rbind( 
  c('IUSM_CATALOG', "" , 'IUSM Assay Catalog',        '','', NA)
)

colnames(base2) <- colnames(base)
main <- as.data.frame(rbind(main, base2, base))

###
foo <- data.table::fread( '../../data_docs/iPSC_Catalog_Metadata.csv', header = T, sep = ',' ) %>%
  as.data.frame()

base <- as.data.frame( rbind( 
  main[ main$ITM_NAME %in% colnames(foo), ]
))
base2<- base[ base$MOD_NAME %in% c('BIOSPECIMEN_CELL_CATALOG', 'TRANSITION_STATUS'), ]
base <- base[ !(base$ITM_NAME %in% base2$ITM_NAME), ]
base <- rbind( base2, base[ !(base$MOD_NAME  %in% 'COVANCE'), ])

base$MOD_NAME <- 'IPSC_Catalog_Metadata'
base2 <- rbind( 
  c( 'IPSC_Catalog_Metadata', ''                          , 'Metadata of Patient Derived iPSC Cell Lines', '', '', NA),
  c( 'IPSC_Catalog_Metadata', 'LINE_USEDBY_FOUNDINPD'     , 'Is this cell line used in FOUND PD', 'CHAR', '3', NA),
  c( 'IPSC_Catalog_Metadata', 'AGE_AT_DIAGNOSIS'          , 'Patient Age at PD Diagnosis', "NUMBER", 4, 1),
  c( 'IPSC_Catalog_Metadata', 'AGE_AT_SAMPLE_COLLECTION'  , 'Patient Age at Sample Collection', "NUMBER", 4, 1)
)
colnames(base2) <- colnames(base)

main <- as.data.frame(rbind(main, base2[1,], base, base2[2:4,]))

### Create Page List:
page <- main[ main$ITM_NAME %in% '', c('MOD_NAME','DSCR')]
colnames(page) <- c('PAG_NAME', 'DSCR')
main <- main[order(main$MOD_NAME),]

### Write and move files
# Move deprecated files to the deprecated folder
file.copy(from = "../../data_docs/Project_151_pQTL_in_CSF.csv",
          to   = "../../data_docs/deprecated/Project_151_pQTL_in_CSF.csv")
file.copy(from = "../../data_docs/Project_151_pQTL_in_CSF_Batch_Corrected.csv",
          to   = "../../data_docs/deprecated/Project_151_pQTL_in_CSF_Batch_Corrected.csv")
file.copy(from = "../../data_docs/PPMI_Project_151_pqtl_Analysis_Annotations_20210210.csv",
          to   = "../../data_docs/deprecated/PPMI_Project_151_pqtl_Analysis_Annotations_20210210.csv")

file.remove('../../data_docs/Project_151_pQTL_in_CSF.csv')
file.remove('../../data_docs/Project_151_pQTL_in_CSF_Batch_Corrected.csv')
file.remove('../../data_docs/PPMI_Project_151_pqtl_Analysis_Annotations_20210210.csv')

# Write New files
write.csv(pqtl, file = "../../data_docs/Project_151_pQTL_in_CSF.csv", row.names = F, quote = F)
write.csv(pqtl_batch, file = "../../data_docs/Project_151_pQTL_in_CSF_Batch_Corrected.csv", row.names = F, quote = F)

# Move basic old files:
movers <- c( 
  "Code_List.csv", "Code_List_-_Harmonized.csv",
  "Data_Dictionary.csv", "Data_Dictionary_-_Harmonized.csv",  'Metabolomic_Analysis_of_LRRK2_PD.csv',
  "Data_Dictionary_-__Annotated_.csv", "FOUND_RFQ_Dictionary.csv", 
  "Page_Descriptions.csv", "PPMI_Online_Dictionary.csv", "PPMI_Online_Codebook.csv",
  "Derived_Variable_Definitions_and_Score_Calculations.csv", "Deprecated_Variables.csv",
  'Deprecated_Biospecimen_Analysis_Results.csv', 'PPMI_Original_Cohort_BL_to_Year_5_Dataset_Apr2020.csv',
  'PPMI_Prodromal_Cohort_BL_to_Year_1_Dataset_Apr2020.csv', 'Subject_Cohort_History.csv',
  'Targeted___untargeted_MS-based_proteomics_of_urine_in_PD.csv', 'Pilot_Biospecimen_Analysis_Results.csv'
)

for( fil in movers ){
  file.copy(from = paste0("../../data_docs/", fil) ,
            to   = paste0("../../data_docs/deprecated/", fil)
          )
  file.remove(paste0("../../data_docs/", fil))

}

# Write Final Page Descriptions and Data Dictionary:
write.csv(main, '../../data_docs/Data_Dictionary.csv', row.names = F, quote = T)
write.csv(page, '../../data_docs/Page_Descriptions.csv', row.names = F, quote = T)
