#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.extract_metadata"]
requirements:
  EnvVarRequirement:
    envDef:
      LC_ALL: C.UTF-8
      LANG: C.UTF-8

inputs:
  in_file:
    type: File
    inputBinding:
      position: 0

outputs:
  out_txt:
    type: File
    outputBinding:
      glob: "*.txt"
  out_meta:
    type: File
    outputBinding:
      glob: "*.xml"