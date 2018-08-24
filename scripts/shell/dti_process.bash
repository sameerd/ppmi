#!/bin/bash

# Pipeline to convert Nifti files to DTI
# Steps
# 1. fslroi
# 2. Brain extraction
# 3. eddy correct
# 4. rotate bvecs

set -x

PROGRAM_NAME=$0

INPUT_DIR=$1
OUTPUT_DIR=$2

function usage {
    echo "usage: $PROGRAM_NAME inputdir outputdir"
    echo "  inputdir  : specify input directory (must contain dcm.zip)"
    echo "  outputdir : specify output directory"
}

if [ ! -d "${INPUT_DIR}" ]; then
   echo "Error: Input Directory : ${INPUT_DIR} does not exist"
   usage
   exit 1
fi

if [ ! -d "${OUTPUT_DIR}" ]; then
   echo "Error: Output Directory : ${OUTPUT_DIR} does not exist"
   usage
   exit 1
fi

echo "Input Dir is : ${INPUT_DIR}"
echo "Output Dir is : ${OUTPUT_DIR}"

# Create tmp directory and unzip dicoms into this directory
TMPDIR=$(mktemp -d)
trap "rm -r $TMPDIR" EXIT
echo $TMPDIR

cp "${INPUT_DIR}"/* "${TMPDIR}"

NIFTI_FILE="${TMPDIR}"/nifti.nii.gz
MERGE_FILE="${TMPDIR}"/nifti_merge.nii.gz
ROI_FILE="${TMPDIR}"/nodif.nii.gz
BET_FILE="${TMPDIR}"/nodif_bet.nii.gz
ECC_FILE="${TMPDIR}"/nifti_ecc.nii.gz
ECC_LOG="${TMPDIR}"/nifti_ecc.ecclog
BVEC_FILE="${TMPDIR}"/nifti.bvec
BVAL_FILE="${TMPDIR}"/nifti.bval
ROT_BVEC_FILE="${TMPDIR}"/nifti_rot.bvec

# NOT sure whether we need to MERGE or not
fslmerge -t "${MERGE_FILE}" "${NIFTI_FILE}"
fslroi "${MERGE_FILE}" "${ROI_FILE}" 0 1
bet2 "${ROI_FILE}" "${BET_FILE}" -m -f 0.2
#bet2 "${MERGE_FILE}" "${BET_FILE}" -m -f 0.2
# Eddy correct requires python 2 so change the path
# FIXME: a better solution would be to install python-virtualenv
PATH=/usr/bin:$PATH eddy_correct "${NIFTI_FILE}" "${ECC_FILE}"  0
fdt_rotate_bvecs "${BVEC_FILE}" "${ROT_BVEC_FILE}" "${ECC_LOG}"

## copy eddy corrected files to output
cp "${ECC_FILE}" "${OUTPUT_DIR}"/dti.nii.gz
cp "${ROT_BVEC_FILE}" "${OUTPUT_DIR}"/bvecs
cp "${BVAL_FILE}" "${OUTPUT_DIR}"/bvals
cp "${BET_FILE}" "${OUTPUT_DIR}"/nodif_brain.nii.gz

# copy xml over
cp -f "${INPUT_DIR}"/*.xml "$OUTPUT_DIR"
cp -f "${INPUT_DIR}"/*.json "$OUTPUT_DIR"

