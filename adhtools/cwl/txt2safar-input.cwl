#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.txt2safar_input"]

inputs:
  in_file:
    type: File
    inputBinding:
      position: 1

outputs:
  out_dir:
    type: Directory
    outputBinding:
      glob: "$(inputs.in_file.nameroot)"
  metadata:
    type: File
    outputBinding:
      glob: "*.xml"
