#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: ScatterFeatureRequirement
inputs:
  in_dir: Directory
outputs:
  out_files:
    outputSource: split-xml-chapters/out_files
    type:
      type: array
      items:
        type: array
        items: File
steps:
  ls:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  split-xml-chapters:
    run: split-xml-chapters.cwl
    in:
      in_file: ls/out_files
    out:
    - out_files
    scatter:
    - in_file
