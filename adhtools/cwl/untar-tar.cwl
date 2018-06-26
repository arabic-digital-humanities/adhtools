#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
inputs:
  tarfile: File
  out_name: string
outputs:
  tar_out:
    outputSource: tar-compress/tar_out
    type: File
steps:
  untar:
    run: untar.cwl
    in:
      tarfile: tarfile
    out:
    - out_files
  tar-compress:
    run: tar-compress.cwl
    in:
      tarfile: out_name
      in_dir: untar/out_files
    out:
    - tar_out
