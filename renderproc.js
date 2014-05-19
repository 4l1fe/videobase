#!/usr/bin/env node

var buf = '';
var jade = require('jade')

process.stdin.setEncoding('utf8');
process.stdin.on('data', function(chunk) {
    data = JSON.parse(chunk);
    tmpl_path = 'interface/jade/';
    renderers = {
        index: function(context) {return jade.renderFile(tmpl_path + 'page_index.jade', context)},
        film: function(context) {return jade.renderFile(tmpl_path + 'page_film.jade', context)},
        person: function(context) {return jade.renderFile(tmpl_path + 'page_person.jade', context)},
        register: function(context) {return jade.renderFile(tmpl_path + 'page_registration.jade', context)},
        user: function(context) {return jade.renderFile(tmpl_path + 'page_user.jade', context)},
        login: function(context) {return jade.renderFile(tmpl_path + 'page_login.jade', context)},
        playlist: function(context) {return jade.renderFile(tmpl_path + 'page_playlist.jade', context)}
    }

    console.log(renderers[data.template](data.context));
});
