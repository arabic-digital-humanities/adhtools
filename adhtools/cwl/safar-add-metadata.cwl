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
  in_dir_meta:
    type: Directory
    inputBinding:
      position: 2
  in_files:
    type: File[]
  in_file_meta:
    type: File
    inputBinding:
      position: 3

outputs:
  out_dir:
    type: Directory
    outputBinding:
      glob: "$(inputs.in_file_meta.nameroot)"
