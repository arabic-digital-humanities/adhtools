#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.openiti2txt"]

inputs:
  in_file:
    type: File
    inputBinding:
      position: 2

outputs:
  out_file:
    type: File
    outputBinding:
      glob: "*"
