#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
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
  archive: File
  cp: string
  index_name:
    default: corpus
    type: string
outputs:
  result:
    type: File
    outputSource: zip-dir-flat/zip_file
steps:
  archive2dir:
    run: archive2dir.cwl
    in:
      archive: archive
    out:
    - out_dir
  safar-analyze-corpus:
    run: safar-analyze-corpus.cwl
    in:
      index_name: index_name
      cp: cp
      in_dir: archive2dir/out_dir
      analyzer: analyzer
    out:
    - safar_output
  zip-dir-flat:
    run: zip-dir-flat.cwl
    in:
      in_dir: safar-analyze-corpus/safar_output
    out:
    - zip_file
