# What is it?

Python script for generating word cloud from chat history in [VK](https://vk.com).

# Installation

```bash
virtualenv venv -p python3
cd venv/bin
source ./activate
pip install -r <path_to_project>/requirements.txt
```

# Usage

* Save chat history to html:

![vk](resources/vk.png)

* Choose png-mask needed for word cloud
* Create instance of `WordCloudMaker` with at least a path to the message history and mask, then process it:

```python
from word_cloud import WordCloudMaker

obj = WordCloudMaker(path_to_html=...,
                     path_to_mask=...)

obj.process()
```

# Additional parameters

* **custom_stopwords** (*default = ()*) - set of specific stopwords
* **min_word_len** (*default = 3*) - minimum length of word 
* **max_words** (*default = 2000*) - maximum number of words
* **max_font_size** (*default = 20*) - maxium font_size of each word
* **enlargement_factor** (*default = 4*) - words cloud image enlargement ratio compared with mask shape

# Examples
