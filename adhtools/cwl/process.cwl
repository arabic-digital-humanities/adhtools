#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
inputs:
  analyzer:
    default: Alkhalil
    type: string
  book: File
outputs:
  analyzed:
    type:
      type: array
      items: File
    outputSource: SafarAnalyze/out_files
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
      in_dir: txt2safar-input/out_dir
      analyzer: analyzer
    out:
    - out_files
