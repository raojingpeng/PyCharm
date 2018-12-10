#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/9 11:37
# @Author  : raojingpeng
# @File    : app.py.py

import os
from flask import Flask, render_template, flash

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


@app.route('/')
@app.route('/index')
def index():
    flash('Now in Home')
    return render_template('index.html')


@app.route('/leetcode')
def leetcode():
    flash('Now in Leetcode')
    return render_template('leetcode.html')
