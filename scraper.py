# Copyright Anshuman73.
# Visit anshuman73.github.io for more info.
# Released under MIT License.
# Works with Python 2.7

import urllib
import os
try:
	from bs4 import BeautifulSoup
except:
	import pip
	print 'Downloading dependency BeautifulSoup...'
	pip.main(['install', 'beautifulsoup4'])
	from bs4 import BeautifulSoup

def main():
	cwd = os.getcwd()
	print '\nChecking if /images directory exists..'
	if not os.path.exists(cwd + '/images'):
		print 'Making directory /images\n'
		os.makedirs(cwd + '/images')
	else:
		print '\ndirectory "/images" exists, moving on...\n'

	base_url = 'http://www.commitstrip.com/en/page/'

	print 'Querying number of pages of comic strips'
	initial = urllib.urlopen(base_url + '1').read()
	pages = int(initial[initial.find('Page 1 of') + 9:initial.find('<', initial.find('Page 1 of'))].strip())
	print 'Found ' + str(pages) + ' pages of Comic ...oops, Commit Strips'

	for page in xrange(1, pages + 1):
		print '\n###Downloading all comics listed on page ' + str(page) + '\n'
		url = base_url + str(page)
		soup = BeautifulSoup(urllib.urlopen(url).read())
		excerpts = soup.select('.excerpt')
		
		for excerpt in excerpts:
			strip_link = excerpt.a['href']
			strip_soup = BeautifulSoup(urllib.urlopen(strip_link).read())
			name = strip_soup.select('.entry-title')[0].string
			name = name.replace(':', '-')
			if name.endswith('.'): #Some names have '.' in the end and this messes with path names
				name = name[:-1]
			name = ''.join(letter for letter in name if letter in '-_. abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')  #Because some names contain characters not acceptable in path names
			img_url = strip_soup.select('.entry-content')[0].img['src']
			if not os.path.exists(cwd + '/images/' + name):
				print 'Downloading image - ' + name
				try:
					urllib.urlretrieve(img_url.encode('utf8'), cwd + '/images/' + name)
				except:
					print '\nERROR: The Image "' + name + '" could not be downloaded.\nPlease Visit ' + img_url + ' to download the image manually.\n'
			else:
				print 'The Image "' + name + '" already exists. Skipping...'

if raw_input('\nPress Enter to start:') == '':
	main()