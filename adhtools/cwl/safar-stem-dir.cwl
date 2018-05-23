#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
- class: ScatterFeatureRequirement
inputs:
  stemmer:
    default: LIGHT10
    type: string
  in_dir: Directory
  cp: string
  index_name:
    default: corpus
    type: string
outputs:
  safar_output:
    outputSource: safar-stem-book/safar_output_dir
    type:
      type: array
      items: Directory
steps:
  ls-2:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-stem-book:
    run: safar-stem-book.cwl
    in:
      book: ls-2/out_files
      cp: cp
      stemmer: stemmer
    out:
    - safar_output_dir
    scatter:
    - book
    scatterMethod: dotproduct
