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
			hashtags = [x.lower() for x in hashtags]
			for hashtag in hashtags:
				if hashtag in targets:
					rv.append(row)
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

	rv = pd.DataFrame(rv)

	rv.to_csv(opfile, index=False)

	# with open(opfile, 'w') as f:
	# 	writer = csv.writer(f, lineterminator='\n')
	# 	for val in rv:
	# 		writer.writerow([val])

if __name__ == '__main__':
	main()

   
