#!/usr/bin/env node

var zerorpc = require("zerorpc");
var jade = require('jade');

var tmpl_path = __dirname + "/../interface/jade/";
var renderers = {
    index: function(context) {return jade.renderFile(tmpl_path + 'page_index.jade', context)},
    film: function(context) {return jade.renderFile(tmpl_path + 'page_film.jade', context)},
    person: function(context) {return jade.renderFile(tmpl_path + 'page_person.jade', context)},
    register: function(context) {return jade.renderFile(tmpl_path + 'page_register.jade', context)},
    user: function(context) {return jade.renderFile(tmpl_path + 'page_user.jade', context)},
    login: function(context) {return jade.renderFile(tmpl_path + 'page_login.jade', context)},
    playlist: function(context) {return jade.renderFile(tmpl_path + 'page_playlist.jade', context)},
    feed: function(context) {return jade.renderFile(tmpl_path + 'page_feed.jade', context)},
    search: function(context) {return jade.renderFile(tmpl_path + 'page_search.jade', context)}
};

var server = new zerorpc.Server({
    render: function(json, reply) {
        var data = JSON.parse(json);
        try {
            repl = renderers[data.template](data.context)
        } catch(e) {
            console.log(e)
        }

        console.log("OK");
        reply(null, renderers[data.template](data.context));
    }
});

server.on("error", function(error) {
   console.log(error);
});

server.bind("tcp://*:4242");
