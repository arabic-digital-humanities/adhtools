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
  index_name:
    default: corpus
    type: string
outputs:
  safar_output:
    type:
      items: Directory
      type: array
    outputSource: safar-analyze-book/safar_output_dir
steps:
  ls:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-analyze-book:
    run: safar-analyze-book.cwl
    in:
      cp: cp
      book: ls/out_files
      analyzer: analyzer
    out:
    - safar_output_dir
    scatter:
    - book
    scatterMethod: dotproduct
