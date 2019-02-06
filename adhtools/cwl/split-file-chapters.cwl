#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: |-
  Split a text in OpenITI format in smaller pieces.
      
      First, the OpenITI metadata is removed. Next, the file is split on
      OpenITI markers, to be able to retain information about headers and
      quotes. Finally, the files are split based on file size, to make
      sure SAFAR does not crash on big input files.
      
      Input:
          txt_file (File): The name of the input file, a text in OpenITI format.
          
      Output:
          A list of text files, that can be analyzed or stemmed using SAFAR.
      
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
  openiti2txt:
    run: openiti2txt.cwl
    in:
      in_file: txt_file
    out:
    - out_file
  split-text-openiti-markers:
    run: split-text-openiti-markers.cwl
    in:
      in_file: openiti2txt/out_file
    out:
    - out_files
  split-text-size:
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
      list: split-text-size/out_files
    out:
    - out_files
