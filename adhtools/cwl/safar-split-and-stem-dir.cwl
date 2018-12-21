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
  metadata: File
  regex:
    default:
    - '### |'
    - '### ||'
    type: string[]
  cp: string
outputs:
  out_files:
    outputSource: safar-split-and-stem-file/out_file
    type:
      type: array
      items: File
steps:
  ls-5:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-split-and-stem-file:
    run: safar-split-and-stem-file.cwl
    in:
      cp: cp
      txt_file: ls-5/out_files
      metadata: metadata
      stemmer: stemmer
    out:
    - out_file
    scatter:
    - txt_file
    scatterMethod: dotproduct
