#!/usr/bin/env node

var zerorpc = require("zerorpc");
var jade = require('jade');
var path = require('path');

// Setup paths directories
var current_path = path.dirname(require.main.filename);
var tmpl_path = path.join(current_path, "../interface/jade");

// Setup renders
var renderers = {
    index: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_index.jade'), context)},
    film: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_film.jade'), context)},
    person: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_person.jade'), context)},
    register: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_register.jade'), context)},
    user: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_user.jade'), context)},
    login: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_login.jade'), context)},
    playlist: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_playlist.jade'), context)},
    feed: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_feed.jade'), context)},
    search: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_search.jade'), context)},
    profile: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_account.jade'), context)}
};

var server = new zerorpc.Server({
    render: function(json, reply) {
        var data = JSON.parse(json);
        var html = null;
        try {
            html = renderers[data.template](data.context);
        } catch(e) {
            console.log(e)
        }

        reply(null, html);
    }
});

server.on("error", function(error) {
   console.log(error);
});

server.bind("tcp://*:4242");
