module.exports = (req, res, next)=>
{
	res.fakeData = "";

	res.echo = (data)=>
	{
		if (typeof data === "object" ||
			typeof data === "array")
		{
			res.fakeData += JSON.stringify(data);
		}
		else
		{
			res.fakeData += data;
		}
	};
	next();
}
