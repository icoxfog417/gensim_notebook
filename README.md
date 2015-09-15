# gensim_notebook

This document will show you how to use topic model by [gensim](https://radimrehurek.com/gensim/index.html).


# Installation

You have to install below libraries.

* Numpy
* Scipy
* gensim
* iPython notebook

(Please see the `conda_requirements.txt`).

# Preparation

The data for this tutorial is from [Recruit HotPepper Beauty API](http://webservice.recruit.co.jp/beauty/reference.html). So you need api key of it.

If you get api key, then execute below scripts.

* scripts/download_data.py
* scripts/make_corpus.py


```
python download_data.py your_api_key
```
It is for downloading the json data from api (extract hair salons data near the Tokyo).


```
python make_corpus path_to_downloaded_json_file
```

It is for making the corpus from json data. You can set some options to restrict the words in corpus. Please see the help of this script.

After executing above scripts, you will have corpus and dictionary in your `data` folder. 

Then, execute [notebook](https://github.com/icoxfog417/gensim_notebook/blob/master/topic_model_evaluation.ipynb).
