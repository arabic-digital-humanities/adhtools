#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
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
  size: int?
outputs:
  out_file:
    outputSource: safar-add-metadata-file/out_file
    type: File
steps:
  split-file-chapters-2:
    run: split-file-chapters.cwl
    in:
      txt_file: txt_file
    out:
    - out_files
  SafarStem-1:
    run: SafarStem.cwl
    in:
      cp: cp
      in_files: split-file-chapters-2/out_files
      stemmer: stemmer
    out:
    - out_files
  merge-safar-xml:
    run: merge-safar-xml.cwl
    in:
      in_files: SafarStem-1/out_files
    out:
    - out_file
  safar-add-metadata-file:
    run: safar-add-metadata-file.cwl
    in:
      in_file: merge-safar-xml/out_file
      in_file_meta: metadata
    out:
    - out_file
