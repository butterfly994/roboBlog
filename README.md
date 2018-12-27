# RoboBlog

This project consists of two parts: extracting blog posts from Medium and then using them as data for a random text generator based on Markov Chains. I used the web scraping library Scrapy to collect articles on Medium by parsing the different Medium topics, then the 10 latest articles in each Medium topic, then using Beautiful Soup to extract the text of those 10 articles and write it to a file. The web scraper currently has a download delay of one second.

Some post-processing is done on the collected text, not limited to but including removing Further Reading and citation sections, removing numbered list features, removing illustration credits (as illustrations do not show up in the generated text), and removing double quotes for longer quotations.

The collected blog posts are then used as data for the random text generator, which generates three words at a time. The random text generator has a few additional optomizations, such as keeping track of current sentence length to avoid overly long sentences, and keeping track of words that start and end sentences to create a coherent sample.

## To Collect Articles

Run the following command: `scrapy runspider article_spider.py` from within the RoboBlog directory. This will append the text of the 10 latest articles from each Medium topic to the `sampleText.txt` file. With the current `download_delay` setting, this will take around 40 minutes to run to completion.

## To Generate Random Text

After running the web scraping routine, run the following command: `python markov.py` from within the RobBlog directory. This will generate a random text sample of random length (between roughly 1000 to 2000 words) and write it to the file `output.txt`.

## Works Cited

The following two Medium articles were key in my initial research for this project: 
- [How I built a leaderboard with the top Medium stories of all time. And how it almost died.](https://medium.freecodecamp.org/how-i-built-top-medium-stories-e07a32cf5255)
- [Automated Text Generator using Markov Chain](https://hackernoon.com/automated-text-generator-using-markov-chain-de999a41e047)