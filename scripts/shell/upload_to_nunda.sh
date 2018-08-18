#!/bin/bash

set -x

# Set XNAT_USER, XNAT_PASS, XNAT_HOST, XNAT_ROOT
. ~/bin/set_nunda_vars.sh


# Look at Project XML
#curl -u ${XNAT_USER}:${XNAT_PASS} -X GET "${XNAT_ROOT}/data/projects/PPMI_DTI?format=xml"

# Create Subject
# FIXME: Add year of birth
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105?gender=male&handedness=right&education=18&race=RAWHITE" 

# CREATE SUBJECT WITH XML
# FIXME: Test if this works with post instead of put
#curl -u ${XNAT_USER}:${XNAT_PASS} -X POST "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105" -F "file=@3105.xml"

# Add Baseline Experiment
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL?xnat:mrSessionData/date=03/24/2011" 

SUBJECT_DATA_DIR="/home/sld0465/projects/ppmi/data_collection/output/3105"

# FIXME: Add original PPMI xml to some resources directory

## Add DTI_1 scan
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_DTI_1?xsiType=xnat:mrScanData&mrScanData/type=DTI"
## Add DTI_1 scan resources directory
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_DTI_1/resources/DICOM?format=DICOM&content=DTI_RAW"
## Add DTI_1 scan resources files
#curl -u ${XNAT_USER}:${XNAT_PASS} -X POST "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_DTI_1/resources/DICOM/files?extract=true" -F "file=@${SUBJECT_DATA_DIR}/Baseline/DTI_1/dcm.zip"

## Add DTI_2 scan
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_DTI_2?xsiType=xnat:mrScanData&mrScanData/type=DTI"
## Add DTI_2 scan resources directory
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_DTI_2/resources/DICOM?format=DICOM&content=DTI_RAW"
## Add DTI_2 scan resources files
#curl -u ${XNAT_USER}:${XNAT_PASS} -X POST "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_DTI_2/resources/DICOM/files?extract=true" -F "file=@${SUBJECT_DATA_DIR}/Baseline/DTI_2/dcm.zip"

## Add T1_1 scan
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_T1_1?xsiType=xnat:mrScanData&mrScanData/type=MPRAGE"
## Add T1_1 scan resources directory
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_T1_1/resources/DICOM?format=DICOM&content=MPRAGE_RAW"
## Add T1_1 scan resources files
#curl -u ${XNAT_USER}:${XNAT_PASS} -X POST "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_T1_1/resources/DICOM/files?extract=true" -F "file=@${SUBJECT_DATA_DIR}/Baseline/T1_1/dcm.zip"

## Add T2_1 scan
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_T2_1?xsiType=xnat:mrScanData&mrScanData/type=T2"
## Add T2_1 scan resources directory
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_T2_1/resources/DICOM?format=DICOM&content=T2_RAW"
## Add T2_1 scan resources files
#curl -u ${XNAT_USER}:${XNAT_PASS} -X POST "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_T2_1/resources/DICOM/files?extract=true" -F "file=@${SUBJECT_DATA_DIR}/Baseline/T2_1/dcm.zip"

## Add PD_1 scan
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_PD_1?xsiType=xnat:mrScanData&mrScanData/type=T2_PD"
## Add T2_1 scan resources directory
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_PD_1/resources/DICOM?format=DICOM&content=T2_PD_RAW"
## Add T2_1 scan resources files
#curl -u ${XNAT_USER}:${XNAT_PASS} -X POST "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL/scans/BL_PD_1/resources/DICOM/files?extract=true" -F "file=@${SUBJECT_DATA_DIR}/Baseline/PD_1/dcm.zip"


# Trigger pipelines
# FIXME: Use import service
# curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/BL?triggerPipelines=true&pullDataFromHeaders=true&fixScanTypes=true"


# Delete subject
# curl -u ${XNAT_USER}:${XNAT_PASS} -X DELETE "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105"


# curl  -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/Baseline/scans/DTI_1/resources/DICOM?format=DICOM&content=DTI_RAW"
#  426  curl  -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/Baseline/scans/DTI_1/resources/DICOM/files?extract=true" -F "file.zip=@clean.zip"
#
