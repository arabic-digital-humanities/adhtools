#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: |
  Index a corpus with corpus specific metadata.

      Inputs:
          generic_yaml (File): yaml file containing the generic indexer configuration, 
              i.e., one of the blacklab indexer formats from 
              https://github.com/arabic-digital-humanities/index-safar.
              Specifies how to index SAFAR analyzer/stemmer output.
          specific_yaml (File): yaml file containing the corpus specific indexer 
              configuration, i.e., one of the files from 
              https://github.com/arabic-digital-humanities/corpus-blacklab-metadata-config.
              Determines what metadata and how the metadata is displayed in the corpus frontend.
          yaml_name (str): name for the file in which the generic_yaml and specific_yaml are 
              combined. In practice this should be either ``safar-analyzer.blf.yaml`` or 
              ``safar-stemmer.blf.yaml``.
          in_dir (Directory): Directory containing SAFAR XML files.
          index_name (str): The name of the index (default: corpus).
          action (str): The action that should be performed on the index, e.g., creation 
              (default: create). Other options are explained on 
              http://inl.github.io/BlackLab/indexing-with-blacklab.html#index-supported-format.
          index_format (str): The index format to be used, i.e., either ``safar-stemmer`` or 
              ``safar-analyzer`` (see https://github.com/arabic-digital-humanities/index-safar).
          xmx (str): Optional parameter to set the Java heap space (default: 2G).

      Outputs:
          Directory containing a BlackLab index.
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
