#!/usr/bin/env node

//Небольшой скрипт для рендеринга шаблона рассылки и проверки

var
    jade = require('jade'),
    fs = require('fs');

var
    template = '/home/uranuz/projects/videobase/interface/jade/mail/week_newsletter.jade',
    dataFile = '/home/uranuz/projects/videobase/data.json',
    outputFile = '/home/uranuz/projects/videobase/letter.html';

fs.readFile(dataFile, function(err, data) {
    if(err) throw err;

    var json = JSON.parse(data);
    var context = json.context;

    var html = jade.renderFile(template, context);

    fs.writeFile(outputFile, html, function(err) {
       if(err) throw err;
       console.log('Template successfully rendered into: ', outputFile);
    });
});

