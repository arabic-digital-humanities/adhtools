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
  book: File
  cp: string
  split_regex_small:
    default: Milestone300
    type: string
  dir_name:
    default: subbooks
    type: string
outputs:
  out_file:
    outputSource: safar-add-metadata-file-1/out_file
    type: File
steps:
  extract_metadata-1:
    run: extract_metadata.cwl
    in:
      in_file: book
    out:
    - out_meta
    - out_txt
  split-text-1:
    run: split-text.cwl
    in:
      in_file: extract_metadata-1/out_txt
      regex: split_regex_small
    out:
    - out_files
  save-files-to-dir-2:
    run: save-files-to-dir.cwl
    in:
      dir_name: dir_name
      in_files: split-text-1/out_files
    out:
    - out
  SafarAnalyze-3:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_dir: save-files-to-dir-2/out
      analyzer: analyzer
    out:
    - out_files
  save-files-to-dir-3:
    run: save-files-to-dir.cwl
    in:
      dir_name: dir_name
      in_files: SafarAnalyze-3/out_files
    out:
    - out
  merge-safar-xml-1:
    run: merge-safar-xml.cwl
    in:
      in_dir: save-files-to-dir-3/out
    out:
    - out_file
  safar-add-metadata-file-1:
    run: safar-add-metadata-file.cwl
    in:
      in_file: merge-safar-xml-1/out_file
      in_file_meta: extract_metadata-1/out_meta
    out:
    - out_file
