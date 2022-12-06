# FAIRxCheck

This small python3 tool automates the FAIR analysis by cross (x) checking them in 3 different online tools ([FAIRChecker](https://fair-checker.france-bioinformatique.fr/), [F-UJI](https://www.f-uji.net/index.php), [FAIR Enough](https://fair-enough.semanticscience.org/)). Once the analysis is done, the tool outputs an individual report and and aggregated one containing the average FAIR score of the analysed resource. Examples of the reports can be found in the reports folder. 

### Installation

Install the required packages defined in the requirements file.
```bash
pip3 install -r requirements.txt
```

### Usage

Pass a list of URLs inside a csv file, like so:
```bash
python3 fairxcheck.py resources_list.csv 
```

The tool uses selenium with the Gecko driver (Firefox) by default, it can be changed to Chrome using the `-drv Chrome` argument. 
```bash
python3 fairxcheck.py --driver Firefox resources_list.csv
```