#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "/home/jvdzwaan/code/research-scripts/python/txt2safar_input.py"]

inputs:
  in_file:
    type: File
    inputBinding:
      position: 1

outputs:
  out_dir:
    type: Directory
    outputBinding:
      glob: "$(inputs.in_file.basename)"
  metadata:
    type: File
    outputBinding:
      glob: "*.xml"
