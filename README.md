# UC MIQP

IBM CPLEX optimization tools implementation on electrical power system

## Installation

### Install EPSLab

1. Using command prompt:

    ```bash
    python setup.py install # python3 in some cases
    ```

### Install Python and necessary library

1. Install python from [Python Website](https://www.python.org/downloads/)
2. Install library using Command Prompt by typing:

    ```bash
    pip install numpy pandas
    ```

3. If you only going to test with restricted number of constraints and variable, install:

    ```bash
    pip install cplex
    ```

### Install ILOG

1. Uninstall cplex community version:

    ```bash
    pip uninstall cplex
    ```

2. Download ILOG at [IBM](https://www.ibm.com/academic/technology/data-science)
3. Install ILOG
4. Find the location of `setup.py` and install it.

    ```bash
    python setup.py install
    ```

Note: If you use ubuntu, the location of ILOG `setup.py` is likely to be `cd /opt/ibm/ILOG/CPLEX_Studio1210/python`

## Usage

### Run EPSLab

EPSLab require all file and only those file in a single folder as an input. See `data/` for example

```python
# import
from epslab import UC

# parameters
input_folder_name='inputFolderCSVSingleState'
constraints = ['consUC', 'consMUTMDT']

# initiate
theCase=UC()

# enter constraints list
theCase.inputCons(constraints)

# enter folder data path
CURRENTPATH=os.getcwd() #alternatively: os.path.dirname(__file__)
PATH=os.path.join(CURRENTPATH,'data',input_folder_name)
theCase.inputDataPath(PATH) # folder path, not file path

# Problem Formulation
theCase.makeProblem()

# Print Problem Parameters
theCase.printIndex()
theCase.printNumberOfData()

# Run
theCase.run_UC()

# Print Output
theCase.printOutput()
theCase.partialCost(decimal_place=4)
theCase.getSummaryDic(print_summary_dic=True)
theCase.exportToCSV(name_mark=False)
```

### Chosing constraints

All available constraints can be seen in `example/example.py`, in `constraints`.

### Chosing Data File

1. Prepare your data file (chose between xlsx or csv)
2. Data must follow one of the template available in `data`
3. Copy your data file to a folder
4. Enter the `PATH_TO_DATA_FOLDER` in `.inputDataPath(PATH_TO_DATA_FOLDER)`

### Save Result

1. Your result will be automatically saved with folder naming based on input_folder_name
2. To avoid replacing previous result, make sure to change the name of your input folder

### Data Manual

1. Number of state must be consistent in everything (busData, REData, loadData)
2. The number of state is refer to the number oh row in loadData
3. In busLoad, busSun, and busWind the columns are in (s,t): s1t1,s1t2,...,s2t1,s2t2,...

### Editing Data in Code

You can replace data from `.inputDataPath(PATH_TO_DATA_FOLDER)` using `.inputData(data_name,data_value)` and vice versa.

```python
theCase=UC() # inherit the class
data_name='loadData' # the name of the data, must follow template
data_value=[150,150,150] # data type can be list, numpy, and pd.DataFrame
theCase.inputData(data_name,data_value)
```

## Contributing

Just give pull request

## Authors

* **Muhammad Yasirroni** - [yasirroni](https://github.com/yasirroni)

See also the list of [contributors](https://github.com/yasirroni/bin-dec-converter/graphs/contributors) who participated in this project.

## Acknowledgement

1. [Universitas Gadjah Mada](https://www.ugm.ac.id/)
2. [IBM](https://www.ibm.com/)
3. [Ir. Sarjiya, S.T., M.Eng., Ph.D., IPU](https://www.researchgate.net/profile/Sarjiya_Sarjiya)