#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
- class: ScatterFeatureRequirement
inputs:
  analyzer:
    default: Alkhalil
    type: string
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
    outputSource: blacklabindexer-2/out_dir
    type: Directory
  merged_dir:
    outputSource: gather-dirs/out
    type: Directory
steps:
  ls-1:
    run: ls.cwl
    in:
      in_dir: in_dir
    out:
    - out_files
  safar-analyze-book-1:
    run: safar-analyze-book.cwl
    in:
      book: ls-1/out_files
      cp: cp
      analyzer: analyzer
    out:
    - safar_output_dir
    scatter:
    - book
    scatterMethod: dotproduct
  gather-dirs:
    run: gather-dirs.cwl
    in:
      in_dirs: safar-analyze-book-1/safar_output_dir
    out:
    - out
  blacklabindexer-2:
    run: https://raw.githubusercontent.com/arabic-digital-humanities/BlackLabIndexer-docker/master/blacklabindexer.cwl
    in:
      action: action
      in_dir: gather-dirs/out
      index_format: index_format
      index_name: index_name
      content_viewable: content_viewable
      text_direction: text_direction
    out:
    - out_dir
