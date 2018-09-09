# purpose: extract English entries with specific hashtag
# command: python extract_hashtag.py input output hashtag1 hashtag2 ...

import pandas as pd 
import sys
import csv

def extract_tweet(df, targets):

	rv = []
	for ind, row in df.iterrows():
		try:
			hashtags = row['hashtags'].split('; ')
			for hashtag in targets:
				if hashtag in targets:
					rv.append(row['text'])
					break
		except:
			continue

	return rv

def main():

	ipfile, opfile = sys.argv[1:3]
	targets = sys.argv[3:]

	df = pd.read_csv(ipfile)
	df = df[df['lang'] == 'en']

	rv = extract_tweet(df, targets)

	with open(opfile, 'w') as f:
		writer = csv.writer(f, lineterminator='\n')
		for val in rv:
			writer.writerow([val])

if __name__ == '__main__':
	main()

   
