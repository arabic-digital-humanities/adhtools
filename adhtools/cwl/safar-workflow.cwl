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
    outputSource: safar-add-metadata/out_dir
    type: Directory
steps:
  txt2safar-input:
    run: txt2safar-input.cwl
    in:
      in_file: book
    out:
    - metadata
    - out_dir
  SafarAnalyze:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_dir: txt2safar-input/out_dir
      analyzer: analyzer
    out:
    - out_files
  safar-add-metadata:
    run: safar-add-metadata.cwl
    in:
      in_files: SafarAnalyze/out_files
      meta_in: txt2safar-input/metadata
    out:
    - out_dir
