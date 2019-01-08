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
  - valueFrom: SafarAnalyze
    position: 3
  - valueFrom: $(runtime.outdir)
    position: 5
  - valueFrom: $(runtime.outdir)
    position: 4


inputs:
  cp:
    type: string
    inputBinding:
      position: 2
      prefix: -cp

  in_files:
    type: File[]
  analyzer:
    type:
      type: enum
      symbols:
      - Alkhalil
      - BAMA
      - MADAMIRA
    default: Alkhalil
    inputBinding:
      position: 6
  xmx:
    type: string
    default: -Xmx4096m
    inputBinding:
      position: 1

outputs:
  out_files:
    type: File[]
    outputBinding:
      glob: "*.xml"
