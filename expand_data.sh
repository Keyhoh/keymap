wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
wget https://github.com/attardi/wikiextractor/raw/master/WikiExtractor.py
python ./WikiExtractor.py -o extracted -b 1M enwiki-latest-pages-articles.xml.bz2