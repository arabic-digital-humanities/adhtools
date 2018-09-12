#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
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
    outputSource: safar-add-metadata-file-1/out_file
    type: File
steps:
  openiti2txt-4:
    run: openiti2txt.cwl
    in:
      in_file: txt_file
    out:
    - out_file
  split-text-size:
    run: split-text-size.cwl
    in:
      in_file: openiti2txt-4/out_file
      size: size
    out:
    - out_files
  SafarAnalyze-5:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_files: split-text-size/out_files
      analyzer: analyzer
    out:
    - out_files
  merge-safar-xml-3:
    run: merge-safar-xml.cwl
    in:
      in_files: SafarAnalyze-5/out_files
    out:
    - out_file
  safar-filter-analyses-1:
    run: safar-filter-analyses.cwl
    in:
      in_file: merge-safar-xml-3/out_file
    out:
    - out_file
  safar-add-metadata-file-1:
    run: safar-add-metadata-file.cwl
    in:
      in_file: safar-filter-analyses-1/out_file
      in_file_meta: metadata
    out:
    - out_file
