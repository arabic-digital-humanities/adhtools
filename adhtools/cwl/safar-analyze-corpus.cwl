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
    type: Directory
    outputSource: gather-dirs-2/out
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
  gather-dirs-2:
    run: gather-dirs.cwl
    in:
      dir_name: index_name
      in_dirs: safar-analyze-book/safar_output_dir
    out:
    - out
