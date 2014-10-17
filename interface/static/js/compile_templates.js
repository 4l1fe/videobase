#!/usr/bin/env node

var
    jade = require("jade"),
    fs = require("fs"),
    templates = [
        '../tpl/cast-thumb.jade'
    ],
    options = {
        compileDebug: false,
        debug: false,
        pretty: false
    },
    codeStr = "window.mi_templates = {",
    i = 0,
    outFileName = "templates.js";

for( ; i < templates.length; i++)
{
    var nameWithExt = templates[i].split('/').slice(-1)[0];
    console.log(nameWithExt);
    var name = nameWithExt.split('.').slice(0,-1).join('.');

    var funcCode = jade.compileFileClient(templates[i], options);

    if( i !== 0 )
        codeStr += ',';
    codeStr += '"' + name + '":' + funcCode;
}

codeStr += "};";

fs.writeFile(outFileName, codeStr, function(err) {
    if(err) throw err;
    console.log('Rendered templates successfully saved into: ' + outFileName);
});