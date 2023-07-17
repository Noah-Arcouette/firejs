// Controller for the server

const fs      = require("fs");
const http    = require("http");
const express = require("express");

const compression = require("compression");
const helmet      = require("helmet");
const cors        = require("cors");
const rateLimit   = require("express-rate-limit");
const bodyParser  = require("body-parser");

const conf = require("./conf.json");

const app = express();

app.use(compression());
app.use(helmet());
app.use(helmet.contentSecurityPolicy({
	directives: conf.csp
}));
app.use(cors(conf.cors));
app.use(rateLimit(conf.rateLimit));
app.use(bodyParser.json(conf.bodyParser));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(require("./server/echo.js"));
app.use("/static/", express.static("./static/"));

require("./router.js")(app, conf);

// start server
const httpServer = http.createServer(app);
httpServer.listen(
	conf.http.port,
	conf.http.ip
);
console.log(`HTTP server on ${conf.http.ip}:${conf.http.port}`);
