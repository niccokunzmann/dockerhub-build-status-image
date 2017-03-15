#!/usr/bin/python3
"""

"""
import sys
import os
import requests
import json
from bottle import run, get, static_file, request, response


__version__ = "0.0.0"
__author__ = "Nicco Kunzmann"

API = "https://hub.docker.com/v2/repositories/{organization}/{repository}/buildhistory/?page_size=100"
DEFAULT_TAG = "latest"

@get('/source')
def static():
    return static_file(os.path.basename(__file__),
                       root=os.path.dirname(__file__))

@get("/build/<organization>/<repository>")
def get_status(organization, repository):
    url = API.format(organization=organization, repository=repository)
    tag = request.query.get("tag", DEFAULT_TAG)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    while url:
        status = requests.get(url)
        data = status.json()
        url = data["next"] # TODO: error handling
        results = data["results"] # TODO: error handling
        for build in results:
            if build["dockertag_name"] == tag: # TODO: error handling
               status = build["status"] # TODO: error handling
               return {"request": "ok", "status": status}
    return {"request": "error", "description": "tag {} not found".format(tag)}

def main():
    run(host='', port=80, debug=True)

if __name__ == "__main__":
    main()