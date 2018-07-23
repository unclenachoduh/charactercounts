import sys, os, operator, re

# take a string, and two dictionaries with K=char, V=count for this doc and all docs
# Return both dictionaries, updated for input string
def countChars(text, characters, all_characters):
	for char in text:
		# current doc
		if char not in characters:
			characters[char] = 1
		else:
			characters[char] += 1

		# all docs
		if char not in all_characters:
			all_characters[char] = 1
		else:
			all_characters[char] += 1

	return [characters, all_characters]

# take a file location and name
# return pertinent strings with non-translateable content removed
# write readable edited strings and pure string for character counts to file
def unJunk(location, filename):
	plaintext = [] # text portion of a line with id and outer quotations removed

	text = open(location).read().split("\n")

	grab = False # for multi-line strings. If True, grab string even if not marked with correct id type
	grabpos = 0 # index marker to concatenate all grab strings

	for line in text:
		if re.search("^msgid", line) or (re.search("^\"", line) and grab == True): # look for id type marker or grab string
			
			if line == "msgid \"\"" or line == "msgid_plural \"\"": # mark future strings as grab
				grab = True
			else:
				onlytext = re.sub("(^msgid \"|^msgid_plural \"|^\"|\"$)", "", line) # remove id marker and quotes

				if re.search("^\"", line): # If its a grab string
					if grabpos == 0:	# If its the first grab string, dont concatenate to last
						plaintext.append(onlytext)
						grabpos += 1
					else:	# If its not the first grab string, concatenate to last
						plaintext[len(plaintext) - 1] += onlytext
				else:	# If it's not a grab string, append
					plaintext.append(onlytext)
		else:
			grab = False # close grab

	cleantext = "" # Just a character string
	wout = open("search_text/" + file, "w+") # file for character string
	wout_readable = open("readable_text/" + file, "w+") # human-readable version of character string

	for line in plaintext:
		cleanline = re.sub("(\%\d\$s|\%s|\%d|\{\{[^\}\}]*\}\}|\{[^\}]*\}|<[^>]*>|\%\([^\)]*\)s)", "", line) # remove markup and vars
		
		# Because characer coun matters, convert HTML symbols to unicode literals
		cleanline = re.sub("&ndash;", "–", cleanline)
		cleanline = re.sub("&hellip;", "...", cleanline)
		cleanline = re.sub("&middot;", "·", cleanline)
		cleanline = re.sub("&bull;", "•", cleanline)
		cleanline = re.sub("&rsquo;", "’", cleanline)
		cleanline = re.sub("&amp;", "&", cleanline)
		cleanline = re.sub("&times;", "×", cleanline)
		cleanline = re.sub("&#9658;", "►", cleanline)
		cleanline = re.sub("&raquo;", "»", cleanline)
		cleanline = re.sub("\t", "	", cleanline)

		# This only removes strings that are not translateable
		if re.search("[a-zA-Z]", cleanline):
			wout.write(cleanline)
			wout_readable.write(cleanline + "\n")
			cleantext += cleanline

	return cleantext

if __name__ == "__main__":
	foldername = sys.argv[1]

	output = "results/"

	all_chars = {} # Dictionary for all docs

	for file in os.listdir(foldername):
		filepath = os.path.join(foldername, file)

		charCounts = {} # dictionary for this doc

		# get translateable text
		text = unJunk(filepath, file)

		# count chars
		results = countChars(text, charCounts, all_chars)
		charCounts = results[0]
		all_chars = results[1]

		# Sort and write for this doc
		data = sorted(charCounts.items(), key=operator.itemgetter(1), reverse=True)
		
		wout = open(output + file, "w+")
		stringblock = ""
		total = 0
		for line in data:
			stringblock += line[0] + "\t" + str(line[1]) + "\n"
			total += line[1]

		stringblock = "Total\t" + str(total) + "\n" + stringblock
		wout.write(stringblock)

	# sort and write for all docs
	data = sorted(all_chars.items(), key=operator.itemgetter(1), reverse=True)

	wout = open(output + "all", "w+")
	stringblock = ""
	total = 0
	for line in data:
		stringblock += line[0] + "\t" + str(line[1]) + "\n"
		total += line[1]

	stringblock = "Total\t" + str(total) + "\n" + stringblock
	wout.write(stringblock)
		