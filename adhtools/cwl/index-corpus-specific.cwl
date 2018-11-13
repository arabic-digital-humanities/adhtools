#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
- class: MultipleInputFeatureRequirement
inputs:
  generic_yaml: File
  specific_yaml: File
  yaml_name: string
  in_dir: Directory
  index_name:
    default: corpus
    type: string
  action:
    default: create
    type: string
  index_format:
    default: safar-stemmer
    type: string
  xmx:
    default: 2G
    type: string
outputs:
  indexed:
    outputSource: blacklabindexer/out_dir
    type: Directory
steps:
  merge-yaml:
    run: merge-yaml.cwl
    in:
      in_files:
      - generic_yaml
      - specific_yaml
      out_name: yaml_name
    out:
    - out_file
  blacklabindexer:
    run: https://raw.githubusercontent.com/arabic-digital-humanities/BlackLabIndexer-docker/master/blacklabindexer.cwl
    in:
      action: action
      config: merge-yaml/out_file
      in_dir: in_dir
      index_format: index_format
      index_name: index_name
      xmx: xmx
    out:
    - out_dir
