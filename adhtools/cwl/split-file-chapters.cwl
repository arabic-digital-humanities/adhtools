#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: ScatterFeatureRequirement
inputs:
  txt_file: File
outputs:
  out_files:
    outputSource: flatten-list/out_files
    type:
      type: array
      items: File
steps:
  openiti2txt-1:
    run: openiti2txt.cwl
    in:
      in_file: txt_file
    out:
    - out_file
  split-text-openiti-markers:
    run: split-text-openiti-markers.cwl
    in:
      in_file: openiti2txt-1/out_file
    out:
    - out_files
  split-text-size-1:
    run: split-text-size.cwl
    in:
      in_file: split-text-openiti-markers/out_files
    out:
    - out_files
    scatter:
    - in_file
    scatterMethod: dotproduct
  flatten-list:
    run: flatten-list.cwl
    in:
      list: split-text-size-1/out_files
    out:
    - out_files
