#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

requirements:
  EnvVarRequirement:
    envDef:
      LANG: en_US.UTF-8    # This value is apparently used by SAFAR for the output file encoding

baseCommand: ["java"]

arguments:
  - valueFrom: SafarStem
    position: 2
  - valueFrom: $(runtime.outdir)
    position: 4

inputs:
  cp:
    type: string
    inputBinding:
      position: 1
      prefix: -cp

  in_dir:
    type: Directory
    inputBinding:
      position: 3
  stemmer:
    type:
      type: enum
      symbols:
      - KHOJA
      - LIGHT10
      - ISRI
      - MOTAZ
      - TASHAPHYNE
    default: LIGHT10
    inputBinding:
      position: 5

outputs:
  out_files:
    type: File[]
    outputBinding:
      glob: "*.xml"
