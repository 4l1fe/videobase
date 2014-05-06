#!/usr/bin/env node
var buf = '';
var jade = require('jade')

process.stdin.setEncoding('utf8');
process.stdin.on('data', function(chunk){

data = JSON.parse(chunk)
renderers =  {
    index: function(context){return jade.renderFile('interface/jade/page_index.jade',context)},
    film: function(context){return jade.renderFile('interface/jade/page_film.jade',context)},
    person: function(context){return jade.renderFile('interface/jade/page_person.jade',context)},
    register: function(context){return jade.renderFile('interface/jade/page_registration.jade',context)},
    user: function(context){return jade.renderFile('interface/jade/page_user.jade',context)}

    //film: jade.compile('include page_film',{filename:'interface/jade/film_test.jade'}),
    //person: jade.compile('include person',{filename:'interface/person_test.jade'})
}

console.log(renderers[data.template](data.context))
 });
