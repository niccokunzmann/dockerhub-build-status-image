#!/usr/bin/python3
"""

"""
import sys
import os
import requests
import json
from bottle import run, get, static_file, request, response, template


__version__ = "0.0.0"
__author__ = "Nicco Kunzmann"

API = "https://hub.docker.com/v2/repositories/{organization}/{repository}/buildhistory/?page_size=100"
DEFAULT_TAG = "latest"
DEFAULT_ORGANIZATION = "library"
DEFAULT_TEXT = "Docker"
SVG = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="72" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="a">
    <rect width="72" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#a)">
    <path fill="#555" d="M0 0h43v20H0z"/>
    <path fill="{color}" d="M43 0h29v20H43z"/>
    <path fill="url(#b)" d="M0 0h72v20H0z"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <a xlink:href="https://github.com/niccokunzmann/dockerhub-build-status-image"
      target="_blank">
    <text x="21.5" y="15" fill="#010101" fill-opacity=".3">{text}</text>
    <text x="21.5" y="14">{text}</text>
    <text x="56.5" y="15" fill="#010101" fill-opacity=".3">{status}</text>
    <text x="56.5" y="14">{status}</text>
    </a>
  </g>
</svg>
"""
HTML_OF_ROOT = """
<!DOCTYPE html>
<html>
    <head>
        <title>dockerhub-build-status-image</title>
        <style>body{padding: 0 25%;font-family: sans-serif;} code{font-size:90%;background-color:#ddd;}</style>
    </head>
    <body>
        <h1>dockerhub-build-status-image</h1><hr>
        <h2>Repository</h2>
        <p>Repository: <a href="https://github.com/niccokunzmann/dockerhub-build-status-image">niccokunzmann/dockerhub-build-status-image</a></p>
        <h2>Explaination</h2>
        <p>Show status badges of your dockerhub automated build in your README.md (like those for travis).<p>
        <h2>Example</h2>
        <ul>
            <li>
                <img src="https://camo.githubusercontent.com/2f41fa46f7e9b0f8f4116d1a27015e98d0a71ccd/68747470733a2f2f646f636b65726275696c646261646765732e7175656c6c746578742e65752f7374617475732e7376673f6f7267616e697a6174696f6e3d6e6963636f6b756e7a6d616e6e267265706f7369746f72793d646f636b65726875622d6275696c642d7374617475732d696d616765" alt="" data-canonical-src="https://dockerbuildbadges.quelltext.eu/status.svg?organization=niccokunzmann&amp;repository=dockerhub-build-status-image" style="max-width:100%;">
                <code>https://dockerbuildbadges.quelltext.eu/status.svg?organization=niccokunzmann&repository=dockerhub-build-status-image </code>
            </li>
        </ul>
        <a href="https://github.com/niccokunzmann/dockerhub-build-status-image/archive/master.zip"><h2>Download source code</h2></a>
    </body>
</html>
"""

@get('/source')
def static():
    return static_file(os.path.basename(__file__),
                       root=os.path.dirname(__file__))

def get_status(organization, repository, tag):
    url = API.format(organization=organization, repository=repository)
    while url:
        print("Requesting {}".format(url))
        status = requests.get(url)
        data = status.json()
        url = data["next"] # TODO: error handling
        results = data["results"] # TODO: error handling
        for build in results:
            if build["dockertag_name"] == tag: # TODO: error handling
               return build["status"] # TODO: error handling
    return None


@get("/build/<organization>/<repository>")
def get_build_status(organization, repository):
    tag = request.query.get("tag", DEFAULT_TAG)
    status = get_status(organization, repository, tag)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    if status is None:
        return {"request": "error", "description": "tag {} not found".format(tag)}
    return {"request": "ok", "status": status}

@get("/status.svg")
def get_svg():
    organization = request.query.get("organization", DEFAULT_ORGANIZATION)
    repository = request.query["repository"]
    tag = request.query.get("tag", DEFAULT_TAG)
    text = request.query.get("text", DEFAULT_TEXT)
    status = get_status(organization, repository, tag)
    response.content_type = "image/svg+xml"
    if status < 0:
        code = "error"
        color = "#c41"
    else:
        code = "ok"
        color = "#4c1"
    response.set_header('Cache-Control', 'max-age=3600')
    return SVG.format(color=color, text=text, status=code)

@get("/")
def get_root():
    return template(HTML_OF_ROOT)

def main():
    run(host='', port=80, debug=True)

if __name__ == "__main__":
    main()
