function getProjectURL ()
{
	const file = fs.readFileSync("./package.json");
	const package = JSON.parse(file);
	return package.repository.url;
}
