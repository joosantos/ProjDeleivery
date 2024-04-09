const port = process.env.PORT || 3000;

// Log the value of VITE_API_URL
console.log(`VITE_API_URL is ${process.env.VITE_API_URL}`);

// wire up the module
const express = require("express");

// create server instance
const app = express();

// Import the history module (https://github.com/bripkens/connect-history-api-fallback)
// Used to return the index.html page independently of the url used (url/, url/htom, url/etc)
var history = require("connect-history-api-fallback");
app.use(history());

// bind the request to an absolute path or relative to the CWD
app.use(express.static("dist"));

// start the server
app.listen(port, () => console.log(`Listening on port ${port}`));

