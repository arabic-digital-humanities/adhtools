#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: |-
  Add metadata to all xml files in a directory
      
      Calls `safar-split-and-stem-file.cwl` for each file in the input directory.
         
      Inputs:
          in_dir (Directory): The directory containing the input files.
          metadata (File): The name of the csv file containing the corpus metadata.
      
      Output:
          A list of xml files with metadata. There is an output file for each file 
              in the input directory.
      
requirements:
- class: ScatterFeatureRequirement
inputs:
  in_dir: Directory
  metadata: File
outputs:
  out_files:
    outputSource: safar-add-metadata-file/out_file
    type:
      type: array
      items: File
steps:
  ls:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-add-metadata-file:
    run: safar-add-metadata-file.cwl
    in:
      in_file: ls/out_files
      in_file_meta: metadata
    out:
    - out_file
    scatter:
    - in_file
    scatterMethod: dotproduct
