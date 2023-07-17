#!/bin/python3
from os      import stat
from os.path import exists

if exists("./router.js"):
	if stat("./routes").st_mtime < stat("./router.js").st_mtime:
		print("Not modified");
		exit(0)

with open("./routes", "r") as f:
	data = f.read()

out = """const system = require("./system.js");

module.exports = (app, conf)=>
{
"""
print("METHOD\tROUTE\tPage");
for route in data.split("\n"):
	if route:
		section = route.split(" ")
		print("\t".join(section))

		out += f"\tapp.{section[0].lower()}(\"{section[1]}\", "
		out += "(req, res)=>\n{"
		out += f"\tsystem.{section[2]}(req, res)\n"
		out += "\tres.send(res.fakeData);\n"
		out += "});\n";

out += "}\n"

with open("./router.js", "w") as f:
	f.write(out);
