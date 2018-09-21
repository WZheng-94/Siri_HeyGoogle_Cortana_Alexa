# commdand: python extract_text.py input outpout
# purpose: exract clean text from the whole dataset for text analysis

import pandas as pd
import sys
import re


def clean_text(df):

	regex_1 = re.compile(r'((RT )?@\w+: )', re.IGNORECASE)
	regex_2 = re.compile(r'(https?[://\w\.\-\/]+)', re.IGNORECASE)
	# regex_3 = re.compile(r'(@\w+ )', re.IGNORECASE)
	rv = df.apply(lambda x:regex_1.sub('',x))
	rv = rv.apply(lambda x:regex_2.sub('',x))

	return rv

def main():

	ipfile, opfile = sys.argv[1:]

	df_raw = pd.read_csv(ipfile)
	if df_raw.text.isnull().sum() > 0:
		print('missing value')
	#no missing value in text col, in total 412373

	text = df_raw[df_raw['lang'] == 'en']['text']
	# in total 283723

	text_clean = clean_text(text)

	text_clean.to_csv(opfile, index=False)


if __name__ == '__main__':

	main()
