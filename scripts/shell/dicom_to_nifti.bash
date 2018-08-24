#!/bin/bash

#set -x

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

ZIPFILE="${INPUT_DIR}/dcm.zip"

if [ ! -f "${ZIPFILE}" ]; then
    echo "Error: Input file does not contain dcm.zip : $ZIPFILE"
    usage
    exit 1
fi

# Create tmp directory and unzip dicoms into this directory
TMPDIR=$(mktemp -d)
trap "rm -r $TMPDIR" EXIT

TMPDIR_DCM="${TMPDIR}/dcm"
TMPDIR_OUTPUT="${TMPDIR}/output"

mkdir -p "${TMPDIR_DCM}"
mkdir -p "${TMPDIR_OUTPUT}"

# unzip dcm files to the temporary dcm directory
unzip -q "${ZIPFILE}" -d "${TMPDIR_DCM}"

## Using mrconvert
#/usr/local/bin/mrtrix3/bin/mrconvert \
#    -export_grad_fsl "${TMPDIR_OUTPUT}/nifti.bval" \
#        "${TMPDIR_OUTPUT}/nifti.bvec" \
#        "${TMPDIR_DCM}" "${TMPDIR_OUTPUT}/nifti.nii"
#gzip "${TMPDIR_OUTPUT}/nifti.nii"

# Using new version of dcm2niix
~/software/dcm2niix/dcm2niix -f nifti -z y \
    -o "${TMPDIR_OUTPUT}" \
    "${TMPDIR_DCM}"

# copy dcm files to output
cp "${TMPDIR_OUTPUT}"/* "${OUTPUT_DIR}"

# copy xml over
cp -f "${INPUT_DIR}"/*.xml "$OUTPUT_DIR"

