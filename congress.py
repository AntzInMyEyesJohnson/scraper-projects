import json


def addcongress():
	with open('congress.json', 'r') as jin:
		jdata = json.load(jin)
		mfullnames = []
		i = 0
		while i < len(jdata):
			mfullnames.append(jdata[i]['name']['official_full'].replace(".", "").strip())
			i += 1
		with open('hunters.txt', 'r') as huntin:
			linels = huntin.readline().strip().replace(', ', ',').replace(', Jr,', ' Jr,').split(',')
			hunters = set(mfullnames + linels)
			# print(hunters)
			with open('hunters.txt', 'w') as huntout:
				huntout.write(', '.join(hunters).strip().lstrip(', '))

addcongress()
