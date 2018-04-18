#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: SubworkflowFeatureRequirement
- class: ScatterFeatureRequirement
inputs:
  analyzer:
    default:
    - Alkhalil
    - BAMA
    type: string[]
  in_dir: Directory
  cp: string
  index_dir_name:
    default: index
    type: string
  xml_dir_name:
    default: xml
    type: string
outputs:
  indexed:
    outputSource: gather-dirs/out
    type: Directory
  xml:
    outputSource: gather-dirs-1/out
    type: Directory
steps:
  analyze-and-index-dir-1:
    run: analyze-and-index-dir.cwl
    in:
      cp: cp
      in_dir: in_dir
      analyzer: analyzer
      index_name: analyzer
      xml_dir_name: analyzer
    out:
    - indexed
    - merged_dir
    scatter:
    - analyzer
    - index_name
    - xml_dir_name
    scatterMethod: dotproduct
  gather-dirs:
    run: gather-dirs.cwl
    in:
      in_dirs: analyze-and-index-dir-1/indexed
    out:
    - out
  gather-dirs-1:
    run: gather-dirs.cwl
    in:
      in_dirs: analyze-and-index-dir-1/merged_dir
    out:
    - out
