var http=require("http");
var fs=require('fs');
var server=http.createServer();
server.listen(8080,function(){
    console.log("server is ring port 8080")
})
var handRequest=function(req,res){
    console.log("当前请求是:"+req.url);
    var url = req.url
    res.writeHead(200,{
        'Content-Type':'text/html'
    });
    fs.readFile('index.html','utf8',function(err,data){
        if(err) throw err;
        res.end(data);
    });
};
server.on('request',handRequest)