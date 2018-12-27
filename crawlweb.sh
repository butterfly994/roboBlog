#!/usr/bin/env bash

truncate -s 0 ./sampleText.txt 
scrapy runspider ./article_spider.py
