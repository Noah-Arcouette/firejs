#!/bin/python3
from os      import walk
from os.path import join

def getnames (path):
	names = [];
	for root, _, filenames in walk(path):
		for filename in filenames:
			names.append((
				filename.split('.')[0],
				join(root, filename)))
	return names

with open("./require.js", "r") as f:
	out = f.read();

for file in getnames("./module"):
	print(file[1]);
	with open(file[1], "r") as f:
		out += f.read()

for file in getnames("./template"):
	print(f"./src/{file[0]}.js")
	with open(f"./src/{file[0]}.js", "r") as f:
		out += f.read()

with open("./system.js", "w") as f:
	f.write(out)
