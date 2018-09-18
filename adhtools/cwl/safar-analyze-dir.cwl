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
  in_dir: Directory
  recursive:
    default: false
    type: boolean?
  cp: string
outputs:
  out_files:
    outputSource: SafarAnalyze-4/out_files
    type:
      type: array
      items: File
steps:
  ls-8:
    run: ls.cwl
    in:
      in_dir: in_dir
      recursive: recursive
    out:
    - out_files
  SafarAnalyze-4:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_files: ls-8/out_files
      analyzer: analyzer
    out:
    - out_files
