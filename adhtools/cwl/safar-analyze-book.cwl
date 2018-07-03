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
outputs:
  safar_output_dir:
    type: Directory
    outputSource: safar-add-metadata-3/out_dir
steps:
  txt2safar-input-3:
    run: txt2safar-input.cwl
    in:
      in_file: book
    out:
    - out_dir
    - out_dir_meta
    - out_file_meta
  SafarAnalyze:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_dir: txt2safar-input-3/out_dir
      analyzer: analyzer
    out:
    - out_files
  safar-add-metadata-3:
    run: safar-add-metadata.cwl
    in:
      in_dir_meta: txt2safar-input-3/out_dir_meta
      in_files: SafarAnalyze/out_files
      in_file_meta: txt2safar-input-3/out_file_meta
    out:
    - out_dir
