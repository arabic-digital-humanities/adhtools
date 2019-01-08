#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

requirements:
  InitialWorkDirRequirement:
    listing: $(inputs.in_files)
  EnvVarRequirement:
    envDef:
      LANG: en_US.UTF-8    # This value is apparently used by SAFAR for the output file encoding
      LC_ALL: C.UTF-8


baseCommand: ["java"]

arguments:
  - valueFrom: SafarStem
    position: 2
  - valueFrom: $(runtime.outdir)
    position: 4
  - valueFrom: $(runtime.outdir)
    position: 3

inputs:
  cp:
    type: string
    inputBinding:
      position: 1
      prefix: -cp

  in_files:
    type: File[]
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
