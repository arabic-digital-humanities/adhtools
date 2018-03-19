# research-scripts

Scripts for manipulating Arabic texts.

## Installation

```
git clone git@github.com:arabic-digital-humanities/research-scripts.git
cd research-scripts
python setup.py develop
```

## Usage

### Preprocess input text files

* `adhtools/txt2safar_input.py`: Given a text file (in OpenITI format), create a text file for each page and an xml file containing the metadata.
* `adhtools/safar_add_metadata.py`: Add metadata from the txt files to the xml file with SAFAR analyzer results.

### Analyze a text using SAFAR

To analyze a text using SAFAR, you need to [download the SAFAR binaries from the website](http://arabic.emi.ac.ma/safar/?q=download), and extract the zip file.
Add to your class path:
* the `SAFAR` directory
* the `SAFAR/lib` directory
* the directory containing the compiled `SafarAnalyze` (from this repository (`java/SafarAnalyze.java`))

Then run the analyzer:
```
java -cp ".:/path/to/SAFAR/*:/path/to/SAFAR/lib/*:/path/to/research-scripts/bin/ SafarAnalyze </path/to/input/directory> </path/to/output/directory> <SAFAR analyzer (Alkhalil|BAMA|MADAMIRA)>
```

Or use the CWL specification:
```
cwltool /path/to/research-scripts/java/cwl/SafarAnalyze.cwl --cp <what to add to the class path> --in_dir </path/to/input/directory> --analyzer <SAFAR analyzer (Alkhalil|BAMA|MADAMIRA)>
```
