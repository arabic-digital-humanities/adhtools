#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
- class: ScatterFeatureRequirement
inputs:
  analyzer:
    default: Alkhalil
    type:
      type: enum
      symbols:
      - Alkhalil
      - BAMA
  in_dir: Directory
  cp: string
  index_name:
    default: corpus
    type: string
  action:
    default: create
    type: string
  index_format:
    default: safar-analyzer
    type: string
  text_direction:
    default: rtl
    type: string
  content_viewable:
    default: true
    type: boolean
  xml_dir_name:
    default: xml
    type: string
outputs:
  indexed:
    type: Directory
    outputSource: blacklabindexer/out_dir
  merged_dir:
    type: Directory
    outputSource: gather-dirs-2/out
steps:
  ls:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-analyze-book:
    run: safar-analyze-book.cwl
    in:
      cp: cp
      book: ls/out_files
      analyzer: analyzer
    out:
    - safar_output_dir
    scatter:
    - book
    scatterMethod: dotproduct
  gather-dirs-2:
    run: gather-dirs.cwl
    in:
      dir_name: xml_dir_name
      in_dirs: safar-analyze-book/safar_output_dir
    out:
    - out
  blacklabindexer:
    run: https://raw.githubusercontent.com/arabic-digital-humanities/BlackLabIndexer-docker/master/blacklabindexer.cwl
    in:
      content_viewable: content_viewable
      index_name: index_name
      action: action
      in_dir: gather-dirs-2/out
      text_direction: text_direction
      index_format: index_format
    out:
    - out_dir
