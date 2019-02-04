#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.split_text_size"]

doc: |
  Split a text in separate files of a certain size.

requirements:
  EnvVarRequirement:
    envDef:
      LC_ALL: C.UTF-8
      LANG: C.UTF-8

inputs:
  in_file:
    type: File
    inputBinding:
      position: 1
  size:
    type: int?
    inputBinding:
      prefix: --size

outputs:
  out_files:
    type: File[]
    outputBinding:
      glob: "*.txt"
