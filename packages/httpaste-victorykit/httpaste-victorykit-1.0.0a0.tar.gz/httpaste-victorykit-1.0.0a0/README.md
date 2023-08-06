# httpaste - versatile HTTP pastebin

![](docs/_assets/images/favpng_parrot-royalty-free-cartoon.png)

httpaste is a pastebin application for easily pasting and retrieving data over
HTTP from shell environments and web browsers. It is inspired by [sprunge.us](http://sprunge.us)
and [ix.io](http://ix.io/), but focuses on extendability, advanced security, with little to
no trade-off to simplicity. It can be hosted through WSGI, CGI, Fast CGI, or
as a standalone evaluation server. It offers multiple storage backends, such as
a filesystem backend, SQLite backend, MySQL backend, or MongoDB backend.

All pastes are being encrypted on the fly and can only be retrieved by an
authorized user, either through knowing the paste id of a public paste, or
having authentication credentials, as well as the paste id of a private paste.
This makes httpaste ideal as a pastebin for sensitive environments such as the
Tor network. Authentication credentials are created on-the-fly and don’t  require a sign-up process.

httpaste supports output formatting for syntax highlighting (powered by
[pygments](https://pygments.org/)), as well as MIME type output manipulation, and input encoding.
Therefore httpaste can server as an anonymous object storage for small data.

Minute-based and ‘burn-after-read’ paste expiration are supported.

httpaste focuses on security through cryptography, making it a computationally intensive application.

# Get Started

## Install

```shell
$ python3 -m pip install httpaste-victorykit
$ httpaste --help
```

## Create Configuration

```shell
$ httpaste default-config --dump myconfig.ini
```

**NOTE**: The default configuration creates an in-memory SQLite backend, which is not
suitable for WWW deployments. Visit backend, for more
information on configuring the backend.

## Run a Local Evaluation Server

```shell
$ httpaste standalone --config myconfig.ini --port 8080
```

## Publish a Private Paste

```shell
$ echo 'My first private paste' | curl -F 'data=<-' -u myusername:mypassword http://localhost:8080/paste/private
http://localhost:8080/paste/private/UALUA9
```

**NOTE**: If the user does not exist, they will be created upon authentication.

## Retrieve a Private Paste

```shell
$ curl -u myusername:mypassword http://localhost:8080/paste/private/UALUA9
My first private paste
```

## Publish a Public Paste

```shell
$ echo 'My first public paste' | curl -F 'data=<-' http://localhost:8080/paste/public
http://localhost:8080/paste/public/X4L39J
```

## Retrieve a Public Paste

```shell
$ curl http://localhost:8080/paste/public/X4L39J
My first public paste
```

### Documentation

The documentation can be found under [https://victorykit.bitbucket.io/httpaste/](https://victorykit.bitbucket.io/httpaste/).

### Licensing

Copyright (C) 2021  Tiara Rodney (victoryk.it)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <[https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)>.

This program uses licensed third-party software.

### More Information


* [Architecture](ARCHITECTURE.md)


* [Contribution Guidelines](CONTRIBUTING.md)
