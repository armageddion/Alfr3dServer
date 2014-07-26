var http = require("http");
var fs = require("fs");

console.log("Starting...");

var config = JSON.parse(fs.readFileSync("/home/alfr3d/alfr3d.js/alfr3dconf.json"));
var host = config.host;
var port = config.port;

var server = http.createServer(function(request, response){
	console.log("Received request: "+request.url);
	fs.readFile("/var/www"+request.url, function(error,data){
		console.log("reading file "+"/var/www"+request.url);
		if (error){
			response.writeHead(404, {"Content-type":"text/plain"});
			response.end("Sorry, the page was not found");
		}
		else{
			response.writeHead(200, {"Content-type":"text/html"});
			response.end(data);
		}
	})
});

server.listen(port,host,function(){
	console.log("Listening "+ host + ":" + port);

});

fs.watchFile("alfr3dconf.json", function(){
	console.log("configurations have been changed...")
	config = JSON.parse(fs.readFileSync("alfr3dconf.json"));
	server.close();
	host = config.host;
	port = config.port;
	server.listen(port,host,function(){
		console.log("Now listening "+ host + ":" + port);

	});	
});