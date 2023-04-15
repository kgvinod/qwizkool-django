# qwizkool-nlp
NLP based implementation of QwizKool

## Installation instructions

##### Clone the repository
```git clone git@github.com:kgvinod/qwizkool-nlp.git```

##### Go into the project directory
```cd qwizkool-nlp```

##### Create a virtual environment to avoid messing with your system wide packages
```
python3 -m venv .venv
source .venv/bin/activate
```
##### Install dependencies
```pip install -r requirements.txt ```

##### Build and locally install the qwizkoolnlp package
```pip install .```

##### Run the unit tests
```
python setup.py test
or
pytest -s -v
```
##### Test drive using the console application
```python app/main.py ```

## Code layout / guideines
##### Package folder
The qwizkoolnlp package folder is located in ```./qwizkoolnlp```. Everything under this folder will be packaged into qwizkoolnlp
package when '```pip install .```' is run. All client code imports (such as in apps, tests) are structured assuming that the qwizkoolnlp library is installed.

##### ./tests folder
All automated unit tests should be added here. Refer existing ones in this folder to see how to write one. These tests will be run by the CI system. It can also be run manually by using '```python setup.py test```' or '```pytest -s -v```'.

##### ./app folder
Applications that use the qwizkoolnlp library are hosted here. These are typically test applications with console interface or a GUI used for test driving the library and for demonstration. These apps ARE NOT run by the CI system automatically.

##### Adding/modifying code
The meat of the project is under ```./qwizkoolnlp/*```. If you are modifying/adding to existing functionality, try to sub-class the existing class and add/override existing implementation. Then, write testers in ./tests and demo/usage applications in ./app. Once everything is verified, modify the client to use the sub-class, overridden methods etc.

##### NLP library
[Spacy NLP](https://spacy.io/) is used by the current implementation. Although it is preferred that we stick with one NLP library, using other NLP libraries such as NLTK is not precluded. The default model used is the "small web" model. You can install other models, such as the large web model using ```python -m spacy download en_core_web_lg```. More information is available [here](https://spacy.io/usage/models). Please keep the default to use small models, since the GitHub CI sometimes times out and fails with large package downloads.




