#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.split_text_openiti_markers"]

doc: |
  Split a text in OpenITI format based on the markers that are present.

  To be able to keep track of information on headers, Quran and hadith quotes,
  header and quote text is stored in separate files. These are later merged using
  the merge_safar_xml tool.

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
  out_files:
    type: File[]
    outputBinding:
      glob: "*.txt"
