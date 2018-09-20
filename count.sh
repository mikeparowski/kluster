#!/bin/sh
find ./data/articles/foxnews -empty -type f -delete
find ./data/articles/breitbart -empty -type f -delete
find ./data/articles/thinkprogress -empty -type f -delete
find ./data/articles/theatlantic -empty -type f -delete
find ./data/articles/cnn -empty -type f -delete
find ./data/articles/vice -empty -type f -delete
find ./data/articles/theblaze -empty -type f -delete
find ./data/articles/thefederalist -empty -type f -delete
find ./data/articles/wsj -empty -type f -delete
find ./data/articles/nytimes -empty -type f -delete

fox=$(ls ./data/articles/foxnews | wc -l)
breitbart=$(ls ./data/articles/breitbart | wc -l)
thinkprogress=$(ls ./data/articles/thinkprogress | wc -l)
atlantic=$(ls ./data/articles/theatlantic | wc -l)
cnn=$(ls ./data/articles/cnn | wc -l)
vice=$(ls ./data/articles/vice | wc -l)
blaze=$(ls ./data/articles/theblaze | wc -l)
federalist=$(ls ./data/articles/thefederalist | wc -l)
wsj=$(ls ./data/articles/wsj | wc -l)
nyt=$(ls ./data/articles/nytimes | wc -l)
echo "Fox: ${fox}"
echo "Breitbart: ${breitbart}"
echo "ThinkProgress: ${thinkprogress}"
echo "CNN: ${cnn}"
echo "TheAtlantic: ${atlantic}"
echo "Vice: ${vice}"
echo "TheBlaze: ${blaze}"
echo "TheFederalist: ${federalist}"
echo "WSJ: ${wsj}"
echo "NYTimes: ${nyt}"
