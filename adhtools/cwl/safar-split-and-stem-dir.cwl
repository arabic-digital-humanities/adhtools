#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: |-
  Analyze a directory of text files in OpenITI format using SAFAR.
      
      Calls `safar-split-and-stem-file.cwl` for each file in the input directory.
         
      Inputs:
          stemmer (enum): The SAFAR stemmer to use. Options are (KHOJA, LIGHT10, 
              ISRI, MOTAZ, TASHAPHYNE).
          in_dir (Directory): Directory containing files to analyze.
          metadata (File): The name of the csv file containing the corpus metadata.
          cp (string): The class path including where the SAFAR binaries can be found.
      
      Output:
          A list of files in SAFAR stemmer XML. There is an output file for each file 
              in the input directory.
      
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
  metadata: File
  cp: string
outputs:
  out_files:
    outputSource: safar-split-and-stem-file/out_file
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
  safar-split-and-stem-file:
    run: safar-split-and-stem-file.cwl
    in:
      cp: cp
      metadata: metadata
      txt_file: ls/out_files
      stemmer: stemmer
    out:
    - out_file
    scatter:
    - txt_file
    scatterMethod: dotproduct
