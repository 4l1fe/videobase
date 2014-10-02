#!/usr/bin/env node

var zerorpc = require("zerorpc");
var jade = require('jade');
var path = require('path');
var util = require('util');

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
    profile: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_account.jade'), context)},
    reset_passwd: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_reset.jade'), context)},
    confirm_passwd: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_confirm_pwd.jade'), context)},
    confirm_email: function(context) {return jade.renderFile(path.join(tmpl_path, 'page_confirm_email.jade'), context)},
    week_newsletter: function(context) {return jade.renderFile(path.join(tmpl_path, 'mail/week_newsletter.jade'), context)},
    personal_newsletter: function(context) {return jade.renderFile(path.join(tmpl_path, 'mail/notice_feed_letter.jade'), context)}
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

var port = 4242;
var tcp_path = util.format("tcp://*:%s", port);

console.log(util.format("Render server started on %s port.", port));
server.bind(tcp_path);
