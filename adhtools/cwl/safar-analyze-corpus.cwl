#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
- class: ScatterFeatureRequirement
inputs:
  analyzer:
    default: Alkhalil
    type: string
  in_dir: Directory
  cp: string
  index_name:
    default: corpus
    type: string
outputs:
  safar_output:
    outputSource: gather-dirs-2/out
    type: Directory
steps:
  ls-3:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-analyze-book-2:
    run: safar-analyze-book.cwl
    in:
      book: ls-3/out_files
      cp: cp
      analyzer: analyzer
    out:
    - safar_output_dir
    scatter:
    - book
    scatterMethod: dotproduct
  gather-dirs-2:
    run: gather-dirs.cwl
    in:
      in_dirs: safar-analyze-book-2/safar_output_dir
      dir_name: index_name
    out:
    - out
