#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: |-
  Analyze a directory of text files in OpenITI format using SAFAR.
      
      Calls `safar-split-and-analyze-file.cwl` for each file in the input directory.
      
      Inputs:
          analyzer (enum): The SAFAR analyzer to use. Options are (Alkhalil, BAMA).
          in_dir (Directory): Directory containing files to analyze.
          metadata (File): The name of the csv file containing the corpus metadata.
          cp (string): The class path including where the SAFAR binaries can be found.
          size (int): Maximum file size in bytes. The text is spilt on the first 
              space after the desired file size is reached. So the file size slightly 
              differs between files.
      
      Output:
          A list of files in SAFAR analyzer XML. There is an output file for each file 
              in the input directory.
      
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
  metadata: File
  cp: string
  size: int?
outputs:
  safar_output:
    outputSource: safar-split-and-analyze-file/out_file
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
  safar-split-and-analyze-file:
    run: safar-split-and-analyze-file.cwl
    in:
      cp: cp
      metadata: metadata
      txt_file: ls/out_files
      analyzer: analyzer
      size: size
    out:
    - out_file
    scatter:
    - txt_file
    scatterMethod: dotproduct
