//usr/bin/env go run $0 "$@"; exit

// https://gist.github.com/msoap/a9ee054f80a58b16867c
// Set first line (instead shebang): //usr/bin/env go run $0 "$@"; exit
// and run:
//    chmod 744 script.go
//    ./script.go 1 2

package main

import (
    "fmt"
    "os"
)

func main() {
    fmt.Println("Hello world!")
    cwd, _ := os.Getwd()
    fmt.Println("cwd:", cwd)
    fmt.Println("args:", os.Args[1:])
}
