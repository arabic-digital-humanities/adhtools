#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: ScatterFeatureRequirement
inputs:
  in_dir: Directory
  metadata: File
outputs:
  out_files:
    outputSource: safar-add-metadata-file-4/out_file
    type:
      type: array
      items: File
steps:
  ls-7:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-add-metadata-file-4:
    run: safar-add-metadata-file.cwl
    in:
      in_file: ls-7/out_files
      in_file_meta: metadata
    out:
    - out_file
    scatter:
    - in_file
    scatterMethod: dotproduct
