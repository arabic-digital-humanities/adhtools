#!/usr/bin/env cwl-runner
cwlVersion: cwl:v1.0
class: CommandLineTool
baseCommand: [tar, zcf]
arguments:
inputs:
  - id: tarfile
    type: string
    inputBinding:
      position: 1
  - id: in_dir
    type: Directory
    inputBinding:
      position: 3

outputs:
  - id: tar_out
    type: File
    outputBinding:
      glob: $(inputs.tarfile)