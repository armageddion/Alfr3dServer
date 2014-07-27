var http = require("http");
var fs = require("fs");
var spawn = require('child_process').spawn;

console.log("Starting...");

var config = JSON.parse(fs.readFileSync("/home/alfr3d/alfr3d.js/alfr3dconf.json"));
var host = config.host;
var port = config.port;

var server = http.createServer(function(request, response){
	console.log("Received request: "+request.url);
	if(request.url === '/hello'){		
		var shellcmd = spawn('../utilities/tts.sh', ["hello sir"]);
		response.writeHead(200, {"Content-type":"text/html"});
		response.end("Hello to you too!");
	}

	else if(request.url === '/blink'){		
		var shellcmd = spawn('../run/sendToArduino.py', ["Blink"]);
		response.writeHead(200, {"Content-type":"text/html"});
		response.end("Blink!");
	}

	else if(request.url === '/welcomehome'){		
		//var shellcmd = spawn("TODO", ["hello sir"]);
		response.writeHead(200, {"Content-type":"text/html"});
		response.end("Welcome Home!");
	}	

	else {
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
	}
});

server.listen(port,host,function(){
	console.log("Listening "+ host + ":" + port);

});

fs.watchFile("../config/alfr3dconf.json", function(){
	console.log("configurations have been changed...")
	config = JSON.parse(fs.readFileSync("alfr3dconf.json"));
	server.close();
	host = config.host;
	port = config.port;
	server.listen(port,host,function(){
		console.log("Now listening "+ host + ":" + port);

	});	
});