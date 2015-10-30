#Script Name 	:search_dictionary_for_certain_keys.py
#Author 		: Jon Kolman

#Created 		:October 23th, 2015


#description recursively searches the keys of a supplied dictionary for a specific key and returns the first value where the keys match


def search_dictionary_for_certain_keys(key, dictionary):
	for k, value in dictionary.iteritems():
		if k == key or k.__contains__(key) or key.__contains__(k):
			return value
			
		else:
			if isinstance(value, dict):
				item = search_dictionary_for_certain_keys(key, value)
				if item is not None:
					return item




