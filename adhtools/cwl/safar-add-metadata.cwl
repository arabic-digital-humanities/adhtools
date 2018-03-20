#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.safar_add_metadata"]
requirements:
  InitialWorkDirRequirement:
    listing: $(inputs.in_files)
  EnvVarRequirement:
    envDef:
      LC_ALL: C.UTF-8
      LANG: C.UTF-8

arguments:
  - valueFrom: $(runtime.outdir)
    position: 1

inputs:
  meta_in:
    type: File
    inputBinding:
      position: 1
  in_files:
    type: File[]

outputs:
  out_files:
    type: File[]
    outputBinding:
      glob: "*.xml"
