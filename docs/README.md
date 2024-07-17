# HunCor2Vec

This lightweight Python app provides automation tools to easily
retrieve material form the [Hungarian Webcorpus 2.0](https://hlt.bme.hu/en/resources/webcorpus2), train a Word2Vec
model with the said texts, and evaluate the results.

The app features an easy-to-use command line menu structure,
implemented with the [pick](https://github.com/aisk/pick) package.

Training and querying tasks utilize the [gensim](https://github.com/piskvorky/gensim) library's Word2Vec module.

Available tools:

- <u>Webcorpus 2.0 Scraper</u> and <u>Webcorpus 2.0 Downloader</u>: retrieve all file links and automate the entire corpus file download process.
- <u>Word2Vec Trainer</u>: easily train a Word2Vec model with any plain-text or CoNLL-U formatted, multi-file corpus. Saving and resuming is supported.
- <u>Word2Vec Query</u>: evaluate the trained model with the most common methods.

Tested on: Windows 11 and Lubuntu 22.04 LTS with Python version 3.10.11.

---

**[Contact](mailto:lcs_it@proton.me)**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
