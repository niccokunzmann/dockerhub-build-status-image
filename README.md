# dockerhub-build-status-image

![](https://dockerbuildbadges.quelltext.eu/status.svg?organization=niccokunzmann&repository=dockerhub-build-status-image)

Show status badges of your dockerhub automated build in your README.md (like those for travis).

Architecture
------------

- SVG image
  - pulls JS file
    - JS file includes list of status servers (since dockerhub does not allow crossorigin requests)
- status servers
  - form
    - a python package
    - a docker container (to use the badge :) )
    - a heroku deploy
  - may serve the svg file but better if they do not, to provide more fault tolerance, see the JS file

API
---

### Server

- `GET /build/<organnization>/<repository>`  
  `GET /build/<organnization>/<repository>?tag=<tag>`  
  Get the build status of an automated build.
  - `organization` is the dockerhub organization. Examples: `library` and `mariobehling`
  - `repository` is the repository in this organization. Examples: `nginx` and `loklak`
  - `tag` is optional, it is `latest` by default. Examples: `latest`
  
  Headers:
  - `Access-Control-Allow-Origin: *`
  
  Result:
  - In case the request had an error:  
    `{"request":"error","description":<text>}`  
    Where `text` is the error description.
  - In case all went fine:  
    `{"request":"ok", status:<build status>}`  
    The `build status` is
    - Negative for an error. Example: `-1`
    - Positive for success. Example: `1`
    - It gets taken like from [this example](https://hub.docker.com/v2/repositories/library/nginx/)
  
- `GET /source`  
  Get the source code.

- `GET /status.svg`  
  See [status.svg][status]

### status.svg
[status]: statussvg

Parameters:
- `organization` is the name of the dockerhub organization.
  If it is left out, it will be `library`.
- `repository` is the name of the repository. This must be given.
- `tag` is the name of the tag to use.
  If it is left out, it is `latest`.
- `text` is the text to show on the badge.
  If it is left out, it is `Docker`.
  
Examples:
- ![](https://dockerbuildbadges.quelltext.eu/status.svg?organization=niccokunzmann&repository=dockerhub-build-status-image)
  `https://dockerbuildbadges.quelltext.eu/status.svg?organization=niccokunzmann&repository=dockerhub-build-status-image`
- https://niccokunzmann.github.io/dockerhub-build-status-image/status.svg?organization=mariobehling&repository=loklak  
  If you have JavaScript enabled, this will ask for several servers.
  This is more fault in case servers go down.
  
Badge Servers
-------------

You can contribute a badge server to this list here and in [status.js](status.js):

- https://dockerbuildbadges.quelltext.eu/status.svg

Contribute
----------

As said, you can contribute a server or write your own - the API is open.
You can [solve issues](https://github.com/niccokunzmann/dockerhub-build-status-image/issues).

Keywords
--------

- status images for dockerhub automated builds
- build status badge for docker images
- svg badges

Reading
-------

- API
  - https://forums.docker.com/t/docker-hub-api-documentation/9091/3
  - https://hub.docker.com/v2/repositories/mariobehling/loklak/buildhistory/?page_size=100
  - https://hub.docker.com/v2/repositories/mariobehling/loklak/autobuild/
