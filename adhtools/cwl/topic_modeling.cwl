#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "adhtools.topic_modeling"]
doc: |
  Perform topic modeling with LDA on SAFAR stemmed XML files
  
  The result is three files: a model.pkl file, a csv file with most important words per topic and a csv file with the topic distribution per document.
  The model.pkl can be loaded and applied on unseen documents.
  
requirements:
  EnvVarRequirement:
    envDef:
      LC_ALL: C.UTF-8
      LANG: C.UTF-8

inputs:
  in_dir:
    type: Directory
    inputBinding:
      position: 0
  stop_words:
    type: File?
    inputBinding:
      prefix: --stop_words=
      separate: false
  n_iter:
    type: int?
    inputBinding:
      prefix: --n_iter=
      separate: false
  nr_topics:
    type: int?
    inputBinding:
      prefix: --nr_topics=
      separate: false
  input_type:
    default: stemmer
    type:
      type: enum
      symbols:
      - stemmer
      - analyzer

outputs:
  out_files:
    type: File[]
    outputBinding:
      glob: "*"