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
  metadata: File
  cp: string
  size: int?
outputs:
  safar_output:
    outputSource: safar-split-and-analyze-file/out_file
    type:
      type: array
      items: File
steps:
  ls-3:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-split-and-analyze-file:
    run: safar-split-and-analyze-file.cwl
    in:
      cp: cp
      metadata: metadata
      txt_file: ls-3/out_files
      analyzer: analyzer
      size: size
    out:
    - out_file
    scatter:
    - txt_file
    scatterMethod: dotproduct
