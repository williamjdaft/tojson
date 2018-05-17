#!/usr/bin/python
import urllib
import re
###gdhjahbjdfktttttttt
table = 0
decod = ''
assignee = ''
details = ''
contentUpdated = ''
created = ''
itemId = 0
kind = ''
priority = 0
reporter = ''
status = 0
title = ''
updated = ''

def priorityWord(num): # convert priority number to required string
	d = {'1': 'trivial', '2': 'minor', '3': 'major', '4': 'critical', '5': 'blocker'}
	return d[num]

def statusWord(num): # convert status id to required string (only open/resolved)
	d = {'0': 'resolved', '1': 'open'}
	return d[num]

def decodeUrl(url):
	url = urllib.unquote_plus(url).decode('utf8', 'ignore')
	url = re.sub('<[^<]+?>', '', url)
	return url

testFile = open("test.txt","w")

with open("tracker.xml","r") as tracker: # open and read xml file line by line
	data = tracker.readlines()

for line in data:
	split = line.split(']')
	decodedLine = decodeUrl(split[0])
	if "<table name=\"tracker_item\">" in line: # starts at relevant table
		table = 1
		testFile.write('{\n    \"issues\": [\n')
	if "<table name=\"tracker_item_message\">" in line: # starts at relevant table
		table = 3
		testFile.write('    \"comments\": [\n')
	if (table == 1):
		if "/table" in line:
			testFile.write('\n    ],\n')
			table = 0
		elif "<row id=\"0\"" in line:
			testFile.write('        {\n')
		elif "<row" in line:
			testFile.write(',\n        {\n')
		elif "\"submitted_by\"" in line:
			split = decodedLine.split("]")
			use = split[0]
			uuse = use[15:]
			if uuse[15:] =='':
				assignee = ('\"assignee\": null,')
				reporter = ('\"reporter\": null,')
			else: 
				assignee = ('\"assignee\": \"{0}\",'.format(uuse.encode('utf-8')))
				reporter = ('\"reporter\": \"{0}\",'.format(uuse.encode('utf-8')))
		elif "\"details\"" in line:
			split = decodedLine.split("]")
			use = split[0]
			uuse = use[15:]			
			if uuse == '':
				details = ('\"content\": null,')
			else:
				details = ('\"content\": \"{0}\",'.format(uuse.encode('utf-8')))
			# attempt at distinguishing 'kind'
			if "bug" in line:
				kind = ('\"kind\": \"bug\"')
			elif "propos" in line:
				kind = ('\"kind\": \"proposal\"')
			elif "task" in line:
				kind = ('\"kind\": \"task\"')
			else: # not ideal, but generally any left will be enhancements
				kind = ('\"kind\": \"enhancement\"')
		elif "\"last_modified_date\"" in line:
			split = decodedLine.split("]")
			use = split[0]
			uuse = use[15:]
			contentUpdated = ('\"content_updated_on\": \"{0}\",'.format(uuse.encode('utf-8')))
			updated = ('\"updated_on\": \"{0}\"'.format(uuse.encode('utf-8'))) #same date
		elif "\"open_date\"" in line:
			split = decodedLine.split("]")
			use = split[0]
			uuse = use[15:]
			created = ('\"created_on\": \"{0}\",'.format(uuse.encode('utf-8')))
		elif "\"tracker_item_id\"" in line:
			split = decodedLine.split("]")
			use = split[0]
			uuse = use[15:]
			itemId = ('\"id\": {0},'.format(uuse.encode('utf-8')))
		elif "\"priority\"" in line:
			pNum = decodedLine[15:]
			pWord = priorityWord(pNum)
			priority = ('\"priority\": \"{0}\",'.format(pWord))
		elif "\"status_id\"" in line:
			sNum = decodedLine[15:]
			sWord = statusWord(sNum)
			status = ('\"status\": \"{0}\",'.format(sWord))
		elif "\"summary\"" in line:
			split = decodedLine.split("]")
			use = split[0]
			uuse = use[15:]
			title = ('\"title\": \"{0}\",'.format(uuse.encode('utf-8')))
		elif "/row" in line: # prints whole row in correct order when complete - messy but it works - could use textwrapping to improve visuals and fix content lines wrapping right to the start of the next line
			testFile.write('            {0}\n            {1}\n            {2}\n            {3}\n            {4}\n            {5}\n            {6}\n            {7}\n            {8}\n            {9}\n            {10}\n        }}'.format(assignee, details, contentUpdated, created, itemId, kind, priority, reporter, status, title, updated))
	if (table == 3):
		if "/table" in line:
			testFile.write('\n    ],\n')
			table = 0
		elif "<row id=\"0\"" in line:
			testFile.write('        {\n')
		elif "<row" in line:
			testFile.write(',\n        {\n')
		elif "\"body\"" in line:
			split = line.split("<")
			use = split[2]
			ssplit = use.split("]")
			uuse = ssplit[0]
			if uuse[8:] == '':
				content = ('\"content\": null,')
			else:
				content = ('\"content\": \"{0}\",'.format(uuse[8:]))
		elif "\"adddate\"" in line:
			split = line.split("<")
			use = split[2]
			ssplit = use.split("]")
			uuse = ssplit[0]
			created_on = ('\"created_on\": \"{0}\",'.format(uuse[8:]))
		elif "\"tracker_item_message_id\"" in line:
			split = line.split("<")
			use = split[2]
			ssplit = use.split("]")
			uuse = ssplit[0]
			tracker_id = ('\"id\": \"{0}\",'.format(uuse[8:]))
		elif "\"tracker_item_id\"" in line:
			split = line.split("<")
			use = split[2]
			ssplit = use.split("]")
			uuse = ssplit[0]
			issue = ('\"issue\": \"{0}\",'.format(uuse[8:]))
		elif "\"submitted_by\"" in line:
			split = line.split("<")
			use = split[2]
			ssplit = use.split("]")
			uuse = ssplit[0]
			if uuse[8:] =='':
				user = ('\"user\": null')
			else:
				user = ('\"user\": \"{0}\"'.format(uuse[8:]))
		elif "/row" in line: # prints whole row in correct order when complete - messy but it works - could use textwrapping to improve visuals and fix content lines wrapping right to the start of the next line
			testFile.write('            {0}\n            {1}\n            {2}\n            {3}\n            {4}\n        }}'.format(content, created_on, tracker_id, issue, user)) # W change words to ones you've made

with open("filesystem.xml","r") as filesystem: # open and read xml file line by line
	data2 = filesystem.readlines()

for line in data2:
		if "<table name=\"filesystem\">" in line: # starts at relevant table
			table = 4
			testFile.write('    \"attachments\": [\n')
		if "/table" in line:
			testFile.write('\n    ]')
			table = 0
		elif "<row id=\"0\"" in line:
			testFile.write('        {\n')
		elif "<row" in line:
			testFile.write(',\n        {\n')
		elif "\"file_name\"" in line:
			split = line.split("<")
			use = split[2]
			ssplit = use.split("]")
			uuse = ssplit[0]
			filename = ('\"file_name\": \"{0}\",'.format(uuse[8:]))
			path = ('\"path\": \"attachments/{0}\",'.format(uuse[8:]))
		elif "\"ref_id\"" in line:
			split = line.split("<")
			use = split[2]
			ssplit = use.split("]")
			uuse = ssplit[0]
			ref_id = ('\"ref_id\": \"{0}\",'.format(uuse[8:]))
		elif "posted_by" in line:
			split = line.split("<")
			use = split[2]
			ssplit = use.split("]")
			uuse = ssplit[0]
			if uuse[8:] =='':
				user = ('\"user\": null')
			else:
				user = ('\"user\": \"{0}\"'.format(uuse[8:]))
		elif "/row" in line:
			testFile.write('            {0}\n            {1}\n            {2}\n            {3}\n        }}'.format(filename, ref_id, path, user))
testFile.write('\n}')
