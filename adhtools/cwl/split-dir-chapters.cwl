#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: |-
  Call split-file-chapters.cwl for a Directory of files.
      
      Scattered version of split-file-chapters.cwl.
      
      Input:
          in_dir (Directory): The directory containing texts to be processed.
          
      Output:
          A list (of lists) of text files, that can be analyzed or stemmed using SAFAR.
      
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
  ls:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  split-file-chapters:
    run: split-file-chapters.cwl
    in:
      txt_file: ls/out_files
    out:
    - out_files
    scatter:
    - txt_file
    scatterMethod: dotproduct
