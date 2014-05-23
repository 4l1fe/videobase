#!/usr/bin/env node
var zerorpc = require("zerorpc");
var jade = require('jade');

var tmpl_path = "../interface/jade/";
var renderers = {
        index: function(context) {return jade.renderFile(tmpl_path + 'page_index.jade', context)},
        film: function(context) {return jade.renderFile(tmpl_path + 'page_film.jade', context)},
        person: function(context) {return jade.renderFile(tmpl_path + 'page_person.jade', context)},
        register: function(context) {return jade.renderFile(tmpl_path + 'page_registration.jade', context)},
        user: function(context) {return jade.renderFile(tmpl_path + 'page_user.jade', context)},
        login: function(context) {return jade.renderFile(tmpl_path + 'page_login.jade', context)},
        playlist: function(context) {return jade.renderFile(tmpl_path + 'page_playlist.jade', context)},
        feed: function(context) {return jade.renderFile(tmpl_path + 'page_feed.jade', context)}
};

var server = new zerorpc.Server({
    render: function(json, reply){
        var data = JSON.parse(json);
        reply(null, renderers[data.template](data.context));
    }
});

server.on("error", function(error){
   console.error(error);
});

server.bind("tcp://*:4242");