#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
- class: ScatterFeatureRequirement
inputs:
  in_dir: Directory
outputs:
  texts:
    outputSource: split-file-chapters/out_files
    type:
      type: array
      items:
        type: array
        items: File
steps:
  ls-2:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  split-file-chapters:
    run: split-file-chapters.cwl
    in:
      txt_file: ls-2/out_files
    out:
    - out_files
    scatter:
    - txt_file
    scatterMethod: dotproduct
