
var servers = ["http://localhost"];



function escapeHtml(unsafe) {
  // from http://stackoverflow.com/a/6234804/1320237
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}


function getQueryParams() {
  var qs = document.location.search;
  // from http://stackoverflow.com/a/1099670/1320237
  qs = qs.split("+").join(" ");

  var params = {}, tokens,
      re = /[?&]?([^=]+)=([^&]*)/g;

  while (tokens = re.exec(qs)) {
    params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
  }
  return params;
}

var parameters = getQueryParams();

function request_from_server(server) {
  var url = server + "/build/" + parameters.organization + "/" + parameters.repository;
  if (parameters.tag) {
    url += "?tag=" + tag;
  }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var result = JSON.parse(this.responseText)
        status_arrived(url, result);
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

function status_arrived(url, status) {
  if (status.request != "ok") {
    console.error(url + " error: " + status.description);
    return
  }
  if (status.status < 0) {
      set_text("status", "error")
      set_text("status-shadow", "error")
  } else {
      set_text("status", "ok")
      set_text("status-shadow", "ok")
  }
}

function set_text(id, text) {
  var element = document.getElementById(id);
  element.innerHTML = escapeHtml(text);
}

if (parameters.text) {
  set_text("name", parameters.text)
  set_text("name-shadow", parameters.text)
}

if (!parameters.organization) {
  parameters.organization = "library";
}

if (!parameters.repository) {
  console.error("There is no repository parameter. Please read the documentation.");
  set_text("name", "read the picture documentation")
  set_text("name-shadow", "read the picture documentation")
}

for (var i = 0; i < servers.length; i += 1) {
  var server = servers[i];
  request_from_server(server);
}
