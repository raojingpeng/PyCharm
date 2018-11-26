#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 11:34
# @Author  : raojingpeng
# @File    : app.py.py


from flask import Flask, request, redirect, session

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/hello/<name>')
def hello(name):
    return '<h1>Hello %s!</h1>' % name
