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
  recursive:
    default: false
    type: boolean
  cp: string
outputs:
  safar_output:
    outputSource: safar-analyze-book-1/safar_output_dir
    type:
      type: array
      items: Directory
steps:
  ls-6:
    run: ls.cwl
    in:
      in_dir: in_dir
      recursive: recursive
    out:
    - out_files
  safar-analyze-book-1:
    run: safar-analyze-book.cwl
    in:
      book: ls-6/out_files
      cp: cp
      analyzer: analyzer
    out:
    - safar_output_dir
    scatter:
    - book
    scatterMethod: dotproduct
