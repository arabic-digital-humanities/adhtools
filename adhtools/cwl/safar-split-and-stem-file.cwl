#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: |-
  Stem a text file in OpenITI format using SAFAR.
      
      To be able to retain information about headers and quotes, the text is first 
      split into files for text, headers and quotes. Next, the resulting files are
      split based on file size, because SAFAR crashes if the output XML files become
      too large. Next, the small files are stemmed using SAFAR and the resulting XML
      files are merged into one big file, containing metadata and information about 
      which words are part of headers and quotes.
      
      Inputs:
          stemmer (enum): The SAFAR stemmer to use. Options are (KHOJA, LIGHT10, 
              ISRI, MOTAZ, TASHAPHYNE).
          txt_file (File): The name of the file to stem, should be in a text in 
              OpenITI format.
          metadata (File): The name of the csv file containing the corpus metadata.
          cp (string): The class path including where the SAFAR binaries can be found.
      
      Output:
          File in SAFAR stemmer output, containing metadata and information about headers
              and quotes.
      
requirements:
- class: SubworkflowFeatureRequirement
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
  txt_file: File
  metadata: File
  cp: string
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
  SafarStem:
    run: SafarStem.cwl
    in:
      cp: cp
      in_files: split-file-chapters/out_files
      stemmer: stemmer
    out:
    - out_files
  merge-safar-xml:
    run: merge-safar-xml.cwl
    in:
      in_files: SafarStem/out_files
    out:
    - out_file
  safar-add-metadata-file:
    run: safar-add-metadata-file.cwl
    in:
      in_file: merge-safar-xml/out_file
      in_file_meta: metadata
    out:
    - out_file
