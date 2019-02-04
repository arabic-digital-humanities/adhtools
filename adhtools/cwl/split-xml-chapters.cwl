#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.split_xml_chapters"]

doc: |
  Split SAFAR analyzer XML with header information into chapters.

  The result is a SAFAR XML file for each chapter. If the input XML file does not
  contain header information, the input file is copied.

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
  levels:
    type: int?
    inputBinding:
      prefix: --levels

outputs:
  out_files:
    type: File[]
    outputBinding:
      glob: "$(inputs.in_file.nameroot)*"
