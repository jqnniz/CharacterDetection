#!/bin/bash
wget http://192.168.0.9:8000/static/style.css
mv style.css ./static/style.css

wget http://192.168.0.9:8000/static/script.js
mv script.js ./static/script.js

wget http://192.168.0.9:8000/templates/index.html
mv index.html ./templates/index.html

wget http://192.168.0.9:8000/templates/gallery.html
mv gallery.html ./templates/gallery.html
