from transformers import pipeline
from bs4 import BeautifulSoup
import requests

#Uses a summarizer already built into pipelines and makes it into a variable to easily call whenever
#You can choose to do different models, but some can take up a lot of storage which is not needed for a small project
summarizer = pipeline("summarization")
 
#Gives the AI a code to scrape and we will call this the URL in this code
URL = "https://medium.com/@nityasav/from-pixels-to-perfection-how-ray-tracing-and-ai-are-redefining-realism-in-gaming-film-and-a406c40516f2"
#requests is 'getting' all the data from the URL and all the files relevant to it which we will later break down
r = requests.get(URL)

#This uses beautiful soup to go through all the html files and only look for text from our previous 'r' 
soup = BeautifulSoup(r.text, 'html.parser')
#Assigns a new variable called results to all h1 tags and p tags which are titles and paragraphs on the article itself
#Also uses a method called 'find_all' to do this
results = soup.find_all(['h1', 'p'])
 
#Goes through each result in results and removes each h1 tag in front of the text and also p tags
text = [result.text for result in results]
ARTICLE = ' '.join(text)

#Replacing all punctuation which ends a sentence with the same thing, but also ending it with <eos>
ARTICLE = ARTICLE.replace('.', '.<eos>')
ARTICLE = ARTICLE.replace('!', '!<eos>')
ARTICLE = ARTICLE.replace('?', '?<eos>')
#With that eos tag, you can split each sentence into distinct sentences which we can iterate through individually
sentences = ARTICLE.split('<eos>')

max_chunk = 500
current_chunk = 0
chunks = []
#Goes through each sentence in the whole list of sentences
#Will give us individual words in each sentence
for sentence in sentences:
    #Checking if length of chunks is equal to the current chunk as it is current chunk is going to increment
    if len(chunks) == current_chunk +1:
        #Within the previous if, we again check if the legnth of chunks added to the length of the word is less than max chunk which is 500
        if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
            #extends chunk with the word if it is less
            chunks[current_chunk].extend(sentence.split(' '))
        else:
            #else we just increment chunk
            current_chunk += 1
            #We also append the word into chunks again
            chunks.append(sentence.split(' '))
    else:
        #We would then print the current chunk which would basically be the words and appending each word into the loop to keep printing
        print(current_chunk)
        chunks.append(sentence.split(' '))
    
#We will then take the previous code to make our chunks be less than 500 words each so we can start summarizing
for chunk_id in range(len(chunks)):
    chunks[chunk_id] = ' '.join(chunks[chunk_id])

#You can check length of each chunk by len(chunks[anynumber].split(' '))
 
#We will pass through all the chunks, and give it a maximum keyword parameter and minimum keyword using pipelines
#res will be the summary itself and we can then summarize each chunk on it's own but we have to combine it into one big result
res = summarizer(chunks, max_length = 30, min_length = 10, do_sample = False)

#Dictionaries have keys and values and the key in this case is just the summary text string
#We go through each value and join it through a for loop where we can make one summary and not multiple
text = ' '.join([summ['summary_text'] for summ in res]) 
 
with open('blogsummry.txt', 'w') as f:
    f.write(text)
