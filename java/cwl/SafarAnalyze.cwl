#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

requirements:
  EnvVarRequirement:
    envDef:
      LANG: en_US.UTF-8    # This value is apparently used by SAFAR for the output file encoding

baseCommand: ["java"]

arguments:
  - "SafarAnalyze"
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
  analyzer:
    type: string
    default: Alkhalil
    inputBinding:
      position: 5

outputs:
  out_files:
    type: File[]
    outputBinding:
      glob: "*.xml"
