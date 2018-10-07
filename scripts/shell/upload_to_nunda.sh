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


SUBJECT_DATA_DIR="/home/sld0465/projects/ppmi/data_collection/working/raw_zip/3105"
XNAT_EXPT="${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/Baseline"

TMPDIR=/home/sld0465/tmp/one_subject
mkdir -p TMPDIR
cd $TMPDIR

cp -r ~/projects/ppmi/data_collection/working/raw_zip/3105/Baseline BL
cp -r ~/projects/ppmi/data_collection/working/raw_zip/3105/Month\ 12 V04
cp -r ~/projects/ppmi/data_collection/working/raw_zip/3105/Month\ 24 V06
cp -r ~/projects/ppmi/data_collection/working/raw_zip/3105/Month\ 36 V08

zip -r 3105_BL.zip BL
zip -r 3105_V04.zip V04
zip -r 3105_V06.zip V06
zip -r 3105_V08.zip V08

# Add Baseline Experiment
#curl -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_EXPT}?xnat:mrSessionData/date=03/24/2011" 

curl -u ${XNAT_USER}:${XNAT_PASS} -X POST --form project=PPMI_DTI \
	--form subject=3105 \
	--form session=3105_BL \
	--form image_archive=@/home/sld0465/tmp/one_subject/3105_BL.zip \
	"${XNAT_ROOT}/data/services/import"

curl -u ${XNAT_USER}:${XNAT_PASS} -X POST --form project=PPMI_DTI \
	--form subject=3105 \
	--form session=3105_V04 \
	--form image_archive=@/home/sld0465/tmp/one_subject/3105_V04.zip \
	"${XNAT_ROOT}/data/services/import"

curl -u ${XNAT_USER}:${XNAT_PASS} -X POST --form project=PPMI_DTI \
	--form subject=3105 \
	--form session=3105_V06 \
	--form image_archive=@/home/sld0465/tmp/one_subject/3105_V06.zip \
	"${XNAT_ROOT}/data/services/import"

curl -u ${XNAT_USER}:${XNAT_PASS} -X POST --form project=PPMI_DTI \
	--form subject=3105 \
	--form session=3105_V08 \
	--form image_archive=@/home/sld0465/tmp/one_subject/3105_V08.zip \
	"${XNAT_ROOT}/data/services/import"

# Delete subject
# curl -u ${XNAT_USER}:${XNAT_PASS} -X DELETE "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105"


# curl  -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/Baseline/scans/DTI_1/resources/DICOM?format=DICOM&content=DTI_RAW"
#  426  curl  -u ${XNAT_USER}:${XNAT_PASS} -X PUT "${XNAT_ROOT}/data/projects/PPMI_DTI/subjects/3105/experiments/Baseline/scans/DTI_1/resources/DICOM/files?extract=true" -F "file.zip=@clean.zip"
#
