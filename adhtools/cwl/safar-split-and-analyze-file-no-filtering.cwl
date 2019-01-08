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
  split_regex_small:
    default:
    - Milestone300
    - '### |'
    - '### ||'
    type: string[]
outputs:
  out_file:
    outputSource: safar-add-metadata-file-1/out_file
    type: File
steps:
  openiti2txt-3:
    run: openiti2txt.cwl
    in:
      in_file: txt_file
    out:
    - out_file
  split-text-1:
    run: split-text.cwl
    in:
      in_file: openiti2txt-3/out_file
      regex: split_regex_small
    out:
    - out_files
  SafarAnalyze-3:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_files: split-text-1/out_files
      analyzer: analyzer
    out:
    - out_files
  merge-safar-xml-1:
    run: merge-safar-xml.cwl
    in:
      in_files: SafarAnalyze-3/out_files
    out:
    - out_file
  safar-add-metadata-file-1:
    run: safar-add-metadata-file.cwl
    in:
      in_file: merge-safar-xml-1/out_file
      in_file_meta: metadata
    out:
    - out_file
