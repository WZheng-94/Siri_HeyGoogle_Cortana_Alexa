# command: python topic_model.py number_topic number_word input output
# purpose: save topic modeling result with given number of topics and 
#		   number of words

import sys
import pandas as pd 
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def trans_text(df):
	'''
	transform the text to list
	'''

	df = pd.read_csv(df, names = ['text'])
	df = df.drop_duplicates()
	text = df.text.tolist()

	return text

def get_topic(text, number_topic, number_word):
	'''
	text: a list of tweets
	'''

	number_topic = int(number_topic)
	number_word = int(number_word)
	vect = CountVectorizer(min_df = 20, max_df = 0.95, stop_words='english', 
							token_pattern='(?u)\\b\\w\\w\\w+\\b').fit(text)
	x = vect.fit_transform(text) 

	corpus = gensim.matutils.Sparse2Corpus(x, documents_columns=False)   
	id_map = dict((v, k) for k, v in vect.vocabulary_.items()) 
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = number_topic, 
						id2word = id_map, passes = 25, random_state = 34)  

	# ldamodel.print_topics(num_topics = number_topic, num_words = number_word)

	return ldamodel


def main():

	number_topic, number_word, ipfile, opfile = sys.argv[1:]

	text = trans_text(ipfile)

	model = get_topic(text, number_topic, number_word)

	top_words = []
	for t in range(model.num_topics):
		top_words.extend([(t, ) + x for x in model.show_topic(t, topn = int(number_word))])

	pd.DataFrame(top_words, columns=['Topic', 'Word', 'P']).to_csv(opfile) 






if __name__ == '__main__':

	main()


# model.save(opfile)

# model = gensim.models.LdaModel.load('topic.model')
