#!/bin/python3
from os      import stat, mkdir, walk
from os.path import exists, join

if not exists("./src/"):
	mkdir("./src/")

def getnames (path):
	names = [];
	for root, _, filenames in walk(path):
		for filename in filenames:
			names.append((
				filename.split(".")[0],
				join(root, filename)))
	return names

def shouldBuild (source, temp):
	source = join("./src/", file[0] + ".js");
	temp   = file[1];

	if not exists(source):
		return True

	if stat(temp).st_mtime > stat(source).st_mtime:
		return True

	return False

def compileTemp (name, infile, outfile):
	with open(infile, "r") as f:
		temp = f.read()

	data  = f"async function {name} (req, res)\n"
	data += "{\n"

	buff    = ""
	escaped = False
	i       = 0
	templen = len(temp)
	while i < templen:
		if not escaped:
			if temp[i] == '<' and temp[i+1] == '?' and temp[i-1] != '\\':
				i      += 1
				escaped = True
				data   += f"\tres.echo(\"{buff}\");\n"
				buff    = ""
			elif not (temp[i] == '\\' and temp[i+1] == '<'):
				buff += temp[i] \
					.replace('\t', "\\t") \
					.replace('\n', "\\n") \
					.replace('\r', "") \
					.replace('"', "\\\"")
		else:
			if temp[i] == '?' and temp[i+1] == '>':
				i      += 1
				escaped = False
				data   += '\n'
			else:
				data += temp[i];
		i += 1

	if buff and not escaped:
		data += f"\tres.echo(\"{buff}\");\n"

	data += "}\n"
	data += f"module.exports.{name} = {name};\n\n"

	with open(outfile, "w") as f:
		f.write(data)

temps = getnames("./template")
for file in temps:
	source = join("./src/", file[0] + ".js");
	temp   = file[1];

	if (shouldBuild(source, temp)):
		compileTemp(file[0], temp, source)
		print(file[0], "\tCompiled")
	else:
		print(file[0], "\tNot Modified")

src = getnames("./src")
