import os
import sys
import numpy as np
import cPickle as pickle
import math
from natsort import natsorted
from PIL import Image
from PIL import ImageOps
from array import *
import random
import fnmatch
import shutil

def recursive_glob(rootdir='.', str1='', str2=''):
	print " searching for '{}' and '{}' in {} ...".format( str1, str2, rootdir )
	return [os.path.join(rootdir, filename)
		for rootdir, dirnames, filenames in os.walk(rootdir)
		for filename in filenames if (str1 in filename and str2 in filename)]
	
def main():	
	print "[WARNING] This code assumes less! POSITIVES than NEGATIVE examples..."

	## PARAMS ##
	pos_str = 'pos'
	neg_str = 'neg'
	roi_unique_str = '_t00000_r00000'
	
	## RUN ##
	input_dir1 = sys.argv[1]
	input_dir2 = sys.argv[2]
	input_dir3 = sys.argv[3]
	input_dir4 = sys.argv[4]
	output_dir = sys.argv[5]
	search_ending = sys.argv[6]
	
	pos_names1 = recursive_glob(input_dir1, pos_str, search_ending)
	pos_names2 = recursive_glob(input_dir2, pos_str, search_ending)
	pos_names3 = recursive_glob(input_dir3, pos_str, search_ending)
	pos_names4 = recursive_glob(input_dir4, pos_str, search_ending)
	pos_names = pos_names1 + pos_names2 + pos_names3 + pos_names4
	nr_pos_names = pos_names.__len__()
	print " Found {} files with search pattern '{}*{}'.".format( nr_pos_names, pos_str, search_ending )
	
	neg_names1 = recursive_glob(input_dir1, neg_str, search_ending)
	neg_names2 = recursive_glob(input_dir2, neg_str, search_ending)
	neg_names3 = recursive_glob(input_dir3, neg_str, search_ending)
	neg_names4 = recursive_glob(input_dir4, neg_str, search_ending)
	neg_names = neg_names1 + neg_names2 + neg_names3 + neg_names4
	nr_neg_names = neg_names.__len__()
	print " Found {} files with search pattern '{}*{}'.".format( nr_neg_names, neg_str, search_ending )
	
	if nr_pos_names > nr_neg_names:
		raise NameError(' This code assumes less! POSITIVES than NEGATIVE examples.')	
	
	# POSITIVE FILES
	print " ... copying files with '{}' to '{}' ...".format( pos_str, output_dir )
	counter = 0
	for n in pos_names:
		counter += 1
		# copy file n to output_dir
		shutil.copy(n, output_dir)
		
		if counter % 2000 == 0:
			print " copy image {} of {}:".format( counter, nr_pos_names )
			print n
			
	# NEGATIVE FILES (just unique ROIs)
	print " ... randomly shuffel NEGATIVE names..."
	random.shuffle(neg_names)	
	
	print " ... copying files with '{}' AND '{}' to '{}' ...".format( neg_str, roi_unique_str, output_dir )
	roi_unique_counter = 0
	for n in neg_names:
		if roi_unique_counter == nr_pos_names:
			print " breaking 1st NEGATIVE loop."
			break					
			
		if roi_unique_str in n:
			roi_unique_counter += 1
			# copy file n to output_dir
			shutil.copy(n, output_dir)
			
			if roi_unique_counter % 100 == 0:
				print " copy image {} of {} (total = {}):".format( roi_unique_counter, nr_pos_names, nr_neg_names )
				print n		
				

	print " Found a total of {} unique NEGATIVE ROIs.".format( roi_unique_counter )				

	# NEGATIVE FILES (remaining randomly sampled ROIs)
	print " ... copying files with '{}' BUT NOT '{}' to '{}' ...".format( neg_str, roi_unique_str, output_dir )
	counter = roi_unique_counter
	for n in neg_names:
		if counter == nr_pos_names:
			print " breaking 2nd NEGATIVE loop."
			break		
			
		if roi_unique_str not in n:
			counter += 1
			# copy file n to output_dir
			shutil.copy(n, output_dir)
			
			if counter % 2000 == 0:
				print " copy image {} of {} (total = {}):".format( counter, nr_pos_names, nr_neg_names )
				print n			

	print " Found a total of {} extra sampled NEGATIVE ROIs.".format( counter - roi_unique_counter )				
	print " and copied them to: {}".format( output_dir )

if __name__ == '__main__':
	main()
