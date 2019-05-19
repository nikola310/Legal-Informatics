# Requirements:

```
Python >= 3.0
pip for installing dependencies
```

# HowToGuide:

## External dependencies:
 - numpy
 - matplotlib
 - scipy
 - selenium  
 - html2text  
 - beautifulsoup4  
 - Markdown
 - nltk
 - gensim
 - pandas
 - scikit-learn
 - Owlready2
 - rdflib
 
All of which can be installed through pip:

```
pip install dependency
```

## Data sets:

Full data set containing text, html and metadata files can be downloaded [here.](https://drive.google.com/file/d/1MZNLFx2YXmkP3lr0of24kulJDfjB_g4l/view?fbclid=IwAR0Nu-ARTJTNaydArcyROy7gAMgItqvTZ3NUOtKc7KeI1AsK4sb9EZijCT0)

Training data set used for NER and that can be used as the corpus for calculating judgements similarity using TF-IDF vectors and test data set used for NER, classification and whose judgement texts could be used as individual query judgements for calculating judgements similarity using TF-IDF vectors can be found [here.](https://drive.google.com/file/d/11wLWHle4ZOE3vxiHFlE_Bcx9yuSufSU7/view?fbclid=IwAR3AKcjDreLg3kkT-_i9a5UqUGxov10j7dbC4BBOUEED1FGLhPFZv0Xeaqw)

XML files of training and test data set containing annotations can be found [here.](https://drive.google.com/file/d/1-9h8qXFpcpUmSZL_ER9pyPZ1wjsOVHde/view?fbclid=IwAR0Z6Navat4pmyyfQwr6VZEGXio1fvTW59Iepz8aUkskxJZbewaorTPFWJ4)

Training set for classification can be found here [here.](https://drive.google.com/file/d/1eGADulolDFxV5GPxyV_iiZepTCnbH2gS/view?fbclid=IwAR3ZRs1Vc8rptsFWG08isANkiqK8vIWxWAbM4BFU20AvEpLZwjWQziJ7_jg)

## Scraping:

To get identification numbers to individual judgements run the script scraper.py. When you run it a window will appear, 
asking you to select the directory in which the identification numbers will be saved. Identification numbers are stored in 
files, each named after a specific judgement type.

To get html and metadata for all individual judgements run the script names_processing.py. When you run it a window will 
appear, asking you to select the directory where files containing identification numbers are stored. This script will use
those identification numbers to create links to individual judgements and then get the necessary data (html and metadata). Data will be stored in directories, each named after a specific judgement type.

To get plain text contained inside the html format of judgements run the script htmlTotxt.py. When you run it a window will 
appear, asking you to select the directory in which all html judgement files are stored. The script will recursively search 
for all files containing judgements in html format, and for each of those files it will create a file containing its plain 
text.

## Judgement similarity using TF-IDF:

To find top 10 most similar judgements to a specified one by comparing TF-IDF vectors with cosine measure run the script 
judgementSimilarity.py. When you run it a window will appear asking you to select the directory which contains your corpus 
of judegments from which 10 most similar judgement to a specified one will be returned. After selecting the directory, an 
index file will be created in the directory "judgementSimilarityOutput". It may take a couple of minutes, depending on the 
amount of judgements in the corpus. After the index file is created, a new window will appear asking you to select a 
judgement file for which 10 most similar judgements from the indexed corpus will be found and their names, paths and similarity
measures will be printed out in the console.

## Named Entity Recognition (NER)

The MAE annotation tool used in this project can be found [here](https://keighrim.github.io/mae-annotation/), as well as the link to its How to Use Guide and all the other relevant information surrounding it. The annotation task file required by MAE that contains all annotation classes used for annotating judgement named entities, is named dtdLegalInformatics.dtd and can be found in the directory 'annotation'.

To create files in the XML format that the MAE anotation tool can open run the script judgementToXml.py. When you run int a 
window will appear asking you to select the directory which containts the judgement files you wish to convert to that format.
Inside that directory a new one will be created with the name "out", in which the newly created files will be stored.

The CRF++ software used for performing NER in this project can be found [here](https://taku910.github.io/crfpp/), as well as all the other relevant information surrounding it.

To create training/test file required for CRF++ from XML files that contain annotations run the script tokenizeJudgements.py.
When you run it you will first be asked to give the name to the file that will be created. After that a window will appear
asking you to select the directory which contains the XML files with annotations. Also that is the directory in which the 
newly created file will be stored.

Files used for training/testing CRF++ in this project are located in the directory 'crf_files'. To train CRF++ run the command 'crf_learn template train model' where template refers to the template file required by CRF++, train refers to the file containing named entities used for training and model refers to the name of the file which represents the trained model. For example in this project the command looked like: 'crf_learn template judgementsTrain model_v1'. To test CRF++ run the command 'crf_test -m model test (> output)' where model refers to the file representing the trained model, test refers to the file used for testing and output refers to the file where named entities that CRF++ predicts for each token will be written. If output is not specified test file will be used instead of it. For example in this project the command looked like: 'crf_test -m model_v1 judgementsTest > output'. In should be noted that if the folder containing CRF++ installation is not added as a Path variable these commands need to be written inside the directory the specified files are located. To output the accuracy of the trained CRF++ model when predicting named entities for a specified test file run the Python script conlleval.py inside the folder in which the file containing expected and predicted named entity values for each token is located. For example in this project running this script looked like: 'python conlleval.py < output'. After running this command the accuracy scores will be printed in the console.

To create a file containing entities that CRF++ found for each judgement run the script parseJudgementEntities.py.
When you run in you will first be asked to give the name to the file that will be created. After that a window will appear 
asking you to select the file containing entities in the format required by CRF++. Finally a window will appear asking you
to select the directory which contains plain text files for judgements, so that entities can be found and parsed from the original text.

## Classification:

In order to generate csv output judgements need to be sorted into following folders:
- acquittal
- conditional
- rejected
- verdict

After running generate_csv.py file chooser will be opened to choose directory containing judgement categories.
CSV file will be generated as out.csv in selected directory.

In order to classify judgements there needs to be two csv files in directory:
- out_training.csv
- out_test.csv

After running classification.py results for both Naive Bayes and SVM will be generated into json files.

## Ontology:

To instantiate the ontology cbr_judgements run the script instantiate_ontology.py. First you need to set the path to the
HermiT Reasoner in your local file system by changing the value to the variable owlready2.JAVA_EXE. Files containing
entities and classification results for judgements that are to be used for instantiation need to be placed in the directory
"data" located in the same directory as the script (Files used in the script by default are instantiateJudgements and 
predictions_svm_instantiate.json). After running the script a window will appear asking you to select the directory which
contains data (text and metadata) for all judgements that need to be instantiated. 


To run queries to the ontology cbr_judgements run the script sparql_queries.py. Files containing entities and classification 
results for judgements that are to be used for creating queries need to be placed in the directory "data" located in the same 
directory as the script (Files used in the script by default are queryJudgements and predictions_svm_query.json). Results for
each individual judgements will be written to a file. All those files will be saved in the directory queryResults located in the same 
directory as the script.
