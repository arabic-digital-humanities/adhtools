#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

requirements:
  EnvVarRequirement:
    envDef:
      LANG: en_US.UTF-8    # This value is apparently used by SAFAR for the output file encoding

baseCommand: ["java"]

arguments:
  - valueFrom: SafarAnalyze
    position: 3
  - valueFrom: $(runtime.outdir)
    position: 5

inputs:
  cp:
    type: string
    inputBinding:
      position: 2
      prefix: -cp

  in_dir:
    type: Directory
    inputBinding:
      position: 4
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
