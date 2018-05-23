#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
inputs:
  stemmer:
    default: LIGHT10
    type: string
  book: File
  cp: string
outputs:
  safar_output_dir:
    outputSource: safar-add-metadata/out_dir
    type: Directory
steps:
  txt2safar-input:
    run: txt2safar-input.cwl
    in:
      in_file: book
    out:
    - out_dir
    - out_dir_meta
    - out_file_meta
  SafarStem:
    run: SafarStem.cwl
    in:
      cp: cp
      in_dir: txt2safar-input/out_dir
      stemmer: stemmer
    out:
    - out_files
  safar-add-metadata:
    run: safar-add-metadata.cwl
    in:
      in_dir_meta: txt2safar-input/out_dir_meta
      in_file_meta: txt2safar-input/out_file_meta
      in_files: SafarStem/out_files
    out:
    - out_dir
