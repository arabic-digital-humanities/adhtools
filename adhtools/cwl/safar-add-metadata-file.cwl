#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.safar_add_metadata_file"]

doc: |
  Add metadata from a csv file to a SAFAR XML file.

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
  in_file_meta:
    type: File
    inputBinding:
      position: 2

outputs:
  out_file:
    type: File
    outputBinding:
      glob: "*.xml"
