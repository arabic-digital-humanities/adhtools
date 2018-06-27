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
  index_name:
    default: corpus
    type: string
outputs:
  safar_output:
    type:
      items: Directory
      type: array
    outputSource: safar-stem-book-1/safar_output_dir
steps:
  ls:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-stem-book-1:
    run: safar-stem-book.cwl
    in:
      cp: cp
      book: ls/out_files
      stemmer: stemmer
    out:
    - safar_output_dir
    scatter:
    - book
    scatterMethod: dotproduct
