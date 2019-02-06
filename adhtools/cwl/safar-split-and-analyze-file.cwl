#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: |-
  Analyze a text file in OpenITI format using SAFAR.
      
      To be able to retain information about headers and quotes, the text is first 
      split into files for text, headers and quotes. Next, the resulting files are
      split based on file size, because SAFAR crashes if the output XML files become
      too large. Next, the small files are analyzed using SAFAR and the resulting XML
      files are merged into one big file, containing metadata and information about 
      which words are part of headers and quotes. Finally, to reduce the size of the 
      output XML, redundant information is filtered out.
      
      Inputs:
          analyzer (enum): The SAFAR analyzer to use. Options are (Alkhalil, BAMA).
          txt_file (File): The name of the file to analyze, should be in a text in 
              OpenITI format.
          metadata (File): The name of the csv file containing the corpus metadata.
          cp (string): The class path including where the SAFAR binaries can be found.
          size (int): Maximum file size in bytes. The text is spilt on the first 
              space after the desired file size is reached. So the file size slightly 
              differs between files.
      
      Output:
          File in SAFAR analyzer output, containing metadata and information about headers
              and quotes.
      
requirements:
- class: SubworkflowFeatureRequirement
inputs:
  analyzer:
    default: Alkhalil
    type:
      type: enum
      symbols:
      - Alkhalil
      - BAMA
  txt_file: File
  metadata: File
  cp: string
  size: int?
outputs:
  out_file:
    outputSource: safar-add-metadata-file/out_file
    type: File
steps:
  split-file-chapters:
    run: split-file-chapters.cwl
    in:
      txt_file: txt_file
    out:
    - out_files
  SafarAnalyze:
    run: SafarAnalyze.cwl
    in:
      cp: cp
      in_files: split-file-chapters/out_files
      analyzer: analyzer
    out:
    - out_files
  merge-safar-xml:
    run: merge-safar-xml.cwl
    in:
      in_files: SafarAnalyze/out_files
    out:
    - out_file
  safar-filter-analyses:
    run: safar-filter-analyses.cwl
    in:
      in_file: merge-safar-xml/out_file
    out:
    - out_file
  safar-add-metadata-file:
    run: safar-add-metadata-file.cwl
    in:
      in_file: safar-filter-analyses/out_file
      in_file_meta: metadata
    out:
    - out_file
