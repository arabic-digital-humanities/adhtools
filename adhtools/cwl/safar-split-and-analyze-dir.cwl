#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
- class: ScatterFeatureRequirement
inputs:
  analyzer:
    default: Alkhalil
    type:
      type: enum
      symbols:
      - Alkhalil
      - BAMA
  in_dir: Directory
  cp: string
  split_regex_small:
    default: Milestone300
    type: string
outputs:
  safar_output:
    outputSource: safar-split-and-analyze-file-1/out_file
    type:
      type: array
      items: File
steps:
  ls-2:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-split-and-analyze-file-1:
    run: safar-split-and-analyze-file.cwl
    in:
      book: ls-2/out_files
      cp: cp
      analyzer: analyzer
      split_regex_small: split_regex_small
    out:
    - out_file
    scatter:
    - book
    scatterMethod: dotproduct
