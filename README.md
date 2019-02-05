# research-scripts

Scripts for manipulating Arabic texts.

## Installation

This software requires Python 3.

```
git clone git@github.com:arabic-digital-humanities/research-scripts.git
cd research-scripts
python setup.py develop
```

### Installing SAFAR for morphological analysis

To analyze a text using SAFAR, you need to [download the SAFAR binaries from the website](http://arabic.emi.ac.ma/safar/?q=download), and extract the zip file.
Add to your class path:

* the `SAFAR` directory
* the `SAFAR/lib` directory
* the directory containing the compiled `SafarAnalyze` (from this repository (`java/SafarAnalyze.java`))

Then run the analyzer:
```
java -cp ".:/path/to/SAFAR/*:/path/to/SAFAR/lib/*:/path/to/research-scripts/bin/ SafarAnalyze </path/to/input/directory> </path/to/output/directory> <SAFAR analyzer (Alkhalil|BAMA)>
```

Or use the CWL specification:
```
cwltool /path/to/research-scripts/java/cwl/SafarAnalyze.cwl --cp <what to add to the class path> --in_dir </path/to/input/directory> --analyzer <SAFAR analyzer (Alkhalil|BAMA)>
```

## Workflows

Expected input for the complete workflows are texts in [openITI format](https://alraqmiyyat.github.io/2015/11-08.html). We assume that:
- There is one file per book in the corpus
- There can be 'METADATA' headers at the top of the file which will be omitted/ignored
- There are markers for chapters, that can be used to split the files and add to the metadata (by default we split on (`### |` (books) and `### ||` (chapters)))
- The filename corresponds to the BookURI (the filename is `<BookURI>.txt`)
- There is a separate .csv file with metadata, each row corresponding to one book. The column 'BookURI' can be used to couple with the OpenITI files.
* (NB do we assume any other meta data fields?)

The output of the workflows (list them here) are xml files that can be used for analysis, or indexed in Blacklab.

## Running workflows

The workflows can be run with cwltool. This is a requirement of the research
scripts and therefore installed when research-scripts is installed. The
[nlppln documentation](https://nlppln.readthedocs.io/en/latest/running_workflows.html)
contains  more information about running cwl workflows.

## Top level workflows

* `safar-split-and-analyze-file.cwl`
	- Analyzes txt file, by first splitting in smaller pieces and chapters, and filtering obsolete fields in the resulting xml (reduces file size considerably!)
	- Notebook: `new-analysis-workflows.ipynb`
* `safar-split-and-analyze-dir.cwl`
	- Analyzes directory of txt files, by first splitting in smaller pieces and chapters, and filtering obsolete fields in the resulting xml
	- Notebook: `new-analysis-workflows.ipynb`
* `safar-split-and-stem-file.cwl`
	- Stems txt file, by first splitting in smaller pieces and chapters
	- Notebook: `new-analysis-workflows.ipynb`
* `safar-split-and-stem-dir.cwl`
	- Stems directory of txt files, by first splitting in smaller pieces and chapters
	- Notebook: `new-analysis-workflows.ipynb`
* `split-xml-chapters-dir.cwl`
	- To split the outcome of the analyze or stem workflow in chapters
	- Notebook: `split-xml-chapters-dir-workflow.ipynb`
* `index-corpus-specific.cwl`
	- Workflow to index an analyzed or stemmed corpus for Blacklab. Does not use any substeps from adhtools.
	- Notebook: `index-corpus-specific-formats.ipynb`

## Subworkflows

* `split-file-chapters.cwl`
  - Split a text in OpenITI format in smaller pieces
	- Used by safar-split-and-analyze-file.cwl and safar-split-and-stem-file.cwl
	- Notebook: `new-analysis-workflows.ipynb`

## Steps

* `openiti2txt.cwl`
	- Used by `split-file-chapters.cwl`
* `safar-add-metadata.cwl`
	- Existing python step that adds the metadata for dir instead of directory. Why not using scatter?
* `safar-add-metadata-file.cwl`
	- Used by `safar-split-and-analyze-file.cwl` and `safar-split-and-stem-file.cwl`
* `safar-filter-analyses.cwl`
	- Used by `safar-split-and-analyze-file.cwl`
* `split-text-openiti-markers.cwl`
	- Used by `split-file-chapters.cwl`
* `split-text-size.cwl`
	- Used by `split-file-chapters.cwl`
* `split-xml-chapters.cwl`
	- Python step split-xml-chapters.  Used by `split-xml-chapters-dir.cwl`
* `merge-safar-xml.cwl`
  - Used by `safar-split-and-analyze-file.cwl` and `safar-split-and-stem-file.cwl`

## Other workflows / steps
* `add-metadata-dir.cwl`
	- Scatter of safar-add-metadata-file.cwl
* `extract_metadata-xml.cwl`
	- Existing python step that extracts metdata from directory with xml and puts it into a csv file. Useful??
* `safar-add-metadata.cwl`
	- Existing python step that adds the metadata for dir instead of directory. Why not using scatter?
* `split-dir-chapters.cwl`
	- Scatter of split-file-chapters.cwl. Not used, but maybe useful?
* `split-text.cwl`
	- Python step `split-text.cwl` that splits on regex. Potentially useful for different corpora. Maybe make more generic and part of nlppln?
* `safar-split-and-analyze-file-no-filtering.cwl`
	- Old version of `safar-split-and-analyze-file.cwl`, but retains all fields (remove?)
