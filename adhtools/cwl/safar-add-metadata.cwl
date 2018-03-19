#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "/home/jvdzwaan/code/research-scripts/python/safar_add_metadata.py"]
requirements:
  InitialWorkDirRequirement:
    listing: $(inputs.in_files)

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
