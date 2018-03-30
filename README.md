# Big data text similarity UTN FRRO

## Requirements

In order to run the scripts you will need:

 - Python 3.X
 - Numpy
 - SciPy
 - Gensim

Besides, the following tools will be needed if you want to run the scripts with some of the specific techniques:
- [nltk](http://www.nltk.org/) (BOW, Semantic*)
- [scikit](http://scikit-learn.org/) (TF-IDF, low performance)
- [fasttext](https://github.com/salestock/fastText.py) (FastText)
- [gensim] (https://radimrehurek.com/gensim/) (TF-IDF, high performance)

**You will need `wordnet`, `wordnet_ic`, `brown` and `punkt` packages*

## Examples
The `data` folder contains some files in order to run the scripts. You will find an example command for each script in this documentation file.


## Scripts
This project has 4 main scripts:


#### preProcessQuestions.py

This script pre-process the questions by removing some special characters and spelling out numbers.

You can run it with the following command:

```
python3 preProcessQuestions.py -quora data/quora_duplicate_questions.tsv -results data/question_pairs.csv
```


#### computeDistance.py

Given a file with pairs of questions, it computes the distance between the sentences of each pair.

**List of parameters:**
```
-technique  Technique {bow, tfidf, gtfidf, w2v, ft, sem} (required)
-questions  Questions file path (required)
-workers    Number of parallel processes [5]
-previous   Previous results file path (useful when you need to resume an unfinished experiment)
```

You can run an example with the following command:
```
python3 computeDistance.py -t bow -q data/question_pairs.csv
```


#### computeError.py

This experiment takes several samples of the questions pairs and computes the average threshold* and the error of each sample.

**The threshold is used to determine whether or not two sentences are related (they are related when their distance is less or equal than the threshold)*

**List of parameters**
```
-technique  Technique {bow, tfidf, gtfidf w2v, ft, sem} (required)
-training   Training file path (required)
-questions  Questions file path (required)
-np         Number of pairs for training (the rest are for validation purposes) (required)
-workers    Number of parallel processes [5]
-previous   Previous results file path (useful when you need to resume an unfinished experiment)
```
The `training` file is a `.csv ` containing a group of pairs ids. Each column of the file represents a sample.

You can run an example with the following command:
```
python3 computeError.py -technique bow -training data/train_valid_400k.csv -questions data/question_pairs.csv -np 242574
```


#### confusionMatrix.py

This experiment computes the confusion matrix of a specific technique.

**List of parameters**
```
-technique  Technique {bow, tfidf, gtfidf, w2v, ft, sem} (required)
-training   Training file path (required)
-questions  Questions file path (required)
-threshold  Threshold value (required)
-np         Number of pairs for training (the rest are for validation purposes) (required)
-workers    Number of parallel processes [5]
-previous   Previous results file path (useful when you need to resume an unfinished experiment)
```
The `threshold` parameter could be taken from the result file of `computeError.py` calculating the average threshold.

You can run an example with the following command:
```
python3 confusionMatrix.py -technique bow -training data/confusion_matrix_ids.csv -questions data/question_pairs.csv -threshold 0.05 -np 242574
```

Note:
- TF-IDF was done in this project with two different approaches. One (tfidf technique in the list of parameters) with scikit-learn library which is low performance but easily understood. The other one (gtfidf technique) with gensim library which is much higher in terms of performance but a little bit more difficult to understand 