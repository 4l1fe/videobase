#!/bin/bash
for conv in $(ls configs/*.ini.example| pyp "p.replace('.example','')");
do
cp $conv.example $conv
done;
