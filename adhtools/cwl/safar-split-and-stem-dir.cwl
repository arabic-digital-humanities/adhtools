#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
- class: ScatterFeatureRequirement
inputs:
  stemmer:
    default: LIGHT10
    type:
      type: enum
      symbols:
      - KHOJA
      - LIGHT10
      - ISRI
      - MOTAZ
      - TASHAPHYNE
  in_dir: Directory
  cp: string
  split_regex_small:
    default: Milestone300
    type: string
outputs:
  safar_output:
    outputSource: safar-split-and-stem-file/xml_file
    type:
      type: array
      items: File
steps:
  ls-1:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-split-and-stem-file:
    run: safar-split-and-stem-file.cwl
    in:
      cp: cp
      txt_file: ls-1/out_files
      split_regex_small: split_regex_small
      stemmer: stemmer
    out:
    - xml_file
    scatter:
    - txt_file
    scatterMethod: dotproduct
