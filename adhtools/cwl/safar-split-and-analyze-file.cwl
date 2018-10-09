#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
inputs:
  analyzer:
    default: Alkhalil
    type:
      type: enum
      symbols:
      - Alkhalil
      - BAMA
  txt_file: File
  metadata: File
  cp: string
  size: int?
outputs:
  out_file:
    outputSource: safar-add-metadata-file-2/out_file
    type: File
steps:
  split-file-chapters-2:
    run: split-file-chapters.cwl
    in:
      txt_file: txt_file
    out:
    - out_files
  SafarAnalyze-7:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_files: split-file-chapters-2/out_files
      analyzer: analyzer
    out:
    - out_files
  merge-safar-xml:
    run: merge-safar-xml.cwl
    in:
      in_files: SafarAnalyze-7/out_files
    out:
    - out_file
  safar-filter-analyses:
    run: safar-filter-analyses.cwl
    in:
      in_file: merge-safar-xml/out_file
    out:
    - out_file
  safar-add-metadata-file-2:
    run: safar-add-metadata-file.cwl
    in:
      in_file: safar-filter-analyses/out_file
      in_file_meta: metadata
    out:
    - out_file
