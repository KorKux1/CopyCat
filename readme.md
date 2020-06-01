# 😺 CopyCat Scraper

It's a scraper for products from the Amazon, Linio and Falabella websites.

<p align="center">

<a href="https://github.com/KorKux1/CopyCat/pulls">
<img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome"/></a>

<a href="https://github.com/KorKux1/CopyCat/blob/master/LICENSE">
<img alt="GitHub license" src="https://img.shields.io/github/license/KorKux1/CopyCat?label=license"/></a>

<a href="https://github.com/KorKux1/CopyCat/graphs/contributors">
<img src="https://img.shields.io/github/contributors-anon/korkux1/copycat" alt="GitHub contributors"/></a>

<a href="https://github.com/KorKux1/CopyCat/issues">
<img alt="GitHub issues" src="https://img.shields.io/github/issues/KorKux1/CopyCat"></a>

<a href="https://github.com/KorKux1/CopyCat/network">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/KorKux1/CopyCat"></a>

<a href="https://github.com/KorKux1/CopyCat/stargazers">
<img alt="GitHub stars" src="https://img.shields.io/github/stars/KorKux1/CopyCat"></a>

<img alt="GitHub language count" src="https://img.shields.io/github/languages/count/KorKux1/CopyCat">

</p>

## Requirements
* Languages: 
<img alt="python" src="https://img.shields.io/badge/python-3.7-green"> 
* Libraries: Flask, Selenium, requests, bs4
* Others: Bootstrap

## Screenshots

![Index](resources/screen1.jpg)

## Setup (Developer Mode)

Clone repository 

`git clone https://github.com/KorKux1/CopyCat.git`

Enter the folder

`cd CopyCat`

Create a virtual enviroment
`py -m venv env`

Install Libraries

`pip install -r requirements.txt`

Verify
`pip freeze`

On Linux
> set environment variables
> Entry point `export FLASK_APP=main.py`
> Secret Key `export SECRET_KEY="your key"`

On Windows
> set environment variables
> Entry point `set $env:FLASK_APP='main.py'`
> Secret Key `set $env:SECRET_KEY="your key"`

Run server
`flask run`

For enable debug mode
Windows `set $env:FLASK_DEBUG=1`
Linux `export FLASK_DEBUG=1`

## Usage

1. Go to `http://127.0.0.1:5000/`

2. In the top search bar type the product you want to search, press enter.

## License
MIT License

---
⌨️ with the ❤️ by KorKux 😊






