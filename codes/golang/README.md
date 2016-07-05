Go Version Manager
https://github.com/moovweb/gvm
------------------------------------------------
GIT_SSL_NO_VERIFY=true bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
Cloning from https://github.com/moovweb/gvm.git to /home/user/.gvm
No existing Go versions detected
Installed GVM v1.0.22

Please restart your terminal session or to get started right away run
 `source /home/user/.gvm/scripts/gvm`

gvm install go1.4 -B
gvm use go1.4 [--default]
export GOROOT_BOOTSTRAP=$GOROOT
gvm install go1.6.2
------------------------------------------------

go get github.com/jochenvg/go-udev
go get github.com/jkeiser/iter
go get github.com/tarm/serial
go get github.com/abiosoft/ishell
go get golang.org/x/sys/unix
apt-get install libudev-dev

------------------------------------------------

Go bindings for libudev
https://github.com/jochenvg/go-udev
https://godoc.org/github.com/jochenvg/go-udev
https://golanglibs.com/top?q=go-udev
https://golanglibs.com/top?q=udev

Уменьшение накладных расходов для утилит на golang
https://habrahabr.ru/post/251271/

This has golang development environment with libudev
https://hub.docker.com/r/gernest/golang-udev/

------------------------------------------------

Run Go program as script
https://gist.github.com/msoap/a9ee054f80a58b16867c

goscript - run Go golang in scripts!
https://gist.github.com/steakknife/8311240

Run go programs as a service on major platforms.
https://github.com/ayufan/golang-kardianos-service

Пишем веб сервис на Go (часть первая)
https://habrahabr.ru/post/208680/

https://godoc.org/golang.org/x/sys/windows/svc

Windows Service with Go - the easy way
http://sanatgersappa.blogspot.ru/2013/07/windows-service-with-go-easy-way.html

------------------------------------------------
