#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
label: Analyze Arabic texts using SAFAR.
requirements:
- class: SubworkflowFeatureRequirement
inputs:
  analyzer:
    default: Alkhalil
    label: Analyzer
    type:
      type: enum
      symbols:
      - Alkhalil
      - BAMA
  archive:
    label: Zip file containing texts in OpenITI format
    type: File
  cp:
    default: .:/home/jvdzwaan/data/tmp/adh/jars/*:/home/jvdzwaan/code/research-scripts/bin/
    type: string
  index_name:
    default: corpus
    type: string
outputs:
  result:
    type: File
    outputSource: zip-dir-flat-1/zip_file
steps:
  archive2dir-1:
    run: archive2dir.cwl
    in:
      archive: archive
    out:
    - out_dir
  safar-analyze-corpus-1:
    run: safar-analyze-corpus.cwl
    in:
      index_name: index_name
      cp: cp
      in_dir: archive2dir-1/out_dir
      analyzer: analyzer
    out:
    - safar_output
  zip-dir-flat-1:
    run: zip-dir-flat.cwl
    in:
      in_dir: safar-analyze-corpus-1/safar_output
    out:
    - zip_file
