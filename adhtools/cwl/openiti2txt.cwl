#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "nlppln.commands.openiti2txt"]

inputs:
  in_file:
    type: File
    inputBinding:
      position: 2

outputs:
  out_files:
    type: File
    outputBinding:
      glob: "*"
