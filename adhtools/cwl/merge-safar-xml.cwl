#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.merge_safar_xml"]

doc: |
  Merge separate SAFAR output files into a single output file.

  Before stemming or analyzing, the text files are split into multiple small
  files. This is done to prevent SAFAR from running out of memory when it has
  to write a very large XML file to disk. After stemming or analyzing, the
  xml output files for the split text have to be combined into a single output
  xml file. This file contains the command line tool to do this.

requirements:
  InlineJavascriptRequirement: {}
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
  in_files:
    type: File[]

outputs:
  out_file:
    type: File
    outputBinding:
      glob: ${return inputs.in_files[0].nameroot.split('-')[0]+'.xml';}
