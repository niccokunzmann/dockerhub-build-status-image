# dockerhub-build-status-image
Status images for your dockerhub automated build (like those for travis)

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

- `GET /build/<organnization>/<repository>`  
  `GET /build/<organnization>/<repository>?tag=<tag>`  
  Get the build status of an automated build.
  - `organization` is the dockerhub organization. Examples: `library` and `mariobehling`
  - `repository` is the repository in this organization. Examples: `nginx` and `loklak`
  - `tag` is optional, it is `latest` by default. Examples: `latest`
  
  The build status is
  - Negative for an error. Example: `-1`
  - Positive for success. Example: `1`
  - It gets taken like from [this example](https://hub.docker.com/v2/repositories/library/nginx/)
  
  Headers:
  - `Access-Control-Allow-Origin: *`
- `GET /source`  
  Get the source code.

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
