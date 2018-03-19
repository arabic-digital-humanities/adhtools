# research-scripts

Scripts for manipulating Arabic texts.

## Usage

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
