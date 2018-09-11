#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
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
  in_file: File
  metadata: File
  regex:
    default:
    - '### |'
    - '### ||'
    type: string[]
  cp: string
outputs:
  out_file:
    outputSource: safar-add-metadata-file-3/out_file
    type: File
steps:
  openiti2txt-2:
    run: openiti2txt.cwl
    in:
      in_file: in_file
    out:
    - out_file
  split-text:
    run: split-text.cwl
    in:
      in_file: openiti2txt-2/out_file
      regex: regex
    out:
    - out_files
  SafarStem-3:
    run: SafarStem.cwl
    in:
      cp: cp
      in_files: split-text/out_files
      stemmer: stemmer
    out:
    - out_files
  merge-safar-xml-2:
    run: merge-safar-xml.cwl
    in:
      in_files: SafarStem-3/out_files
    out:
    - out_file
  safar-add-metadata-file-3:
    run: safar-add-metadata-file.cwl
    in:
      in_file: merge-safar-xml-2/out_file
      in_file_meta: metadata
    out:
    - out_file
