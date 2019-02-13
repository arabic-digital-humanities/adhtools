#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.openiti2txt"]

doc: |
  Remove metadata from a text in OpenITI format.

requirements:
  EnvVarRequirement:
    envDef:
      LC_ALL: C.UTF-8
      LANG: C.UTF-8

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
