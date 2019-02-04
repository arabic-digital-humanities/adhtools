#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.safar_filter_analyses"]

doc: |
  Reduce file size of SAFAR output files by removing unnecessary analyses.

  For every word in a text, SAFAR can return many analyses. Often these analyses
  differ on other aspects than the ones we are interested in (i.e., root and
  stem). Because large files are more difficult to handle, we remove everything
  we don't need.

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

outputs:
  out_file:
    type: File
    outputBinding:
      glob: $(inputs.in_file.basename)
