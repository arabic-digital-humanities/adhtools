#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
inputs:
  analyzer:
    default: Alkhalil
    type: string
  book: File
  cp: string
outputs:
  safar_output_dir:
    outputSource: safar-add-metadata-2/out_dir
    type: Directory
steps:
  txt2safar-input-2:
    run: txt2safar-input.cwl
    in:
      in_file: book
    out:
    - out_dir
    - out_dir_meta
    - out_file_meta
  SafarAnalyze-2:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_dir: txt2safar-input-2/out_dir
      analyzer: analyzer
    out:
    - out_files
  safar-add-metadata-2:
    run: safar-add-metadata.cwl
    in:
      in_dir_meta: txt2safar-input-2/out_dir_meta
      in_file_meta: txt2safar-input-2/out_file_meta
      in_files: SafarAnalyze-2/out_files
    out:
    - out_dir
