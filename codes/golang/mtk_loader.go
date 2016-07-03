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
    "sync"
    "time"
    "strings"
    "log"
    "encoding/hex"
    "github.com/jochenvg/go-udev"
    "github.com/tarm/serial"
    //_"github.com/mikepb/go-serial"
)

func serW(s *serial.Port, ss string) {
    hh, e := hex.DecodeString(ss)
    if e != nil {
        log.Fatal(e)
    }
    fmt.Printf("%x ->", hh)
    //n, err := s.Write([]byte("\x0a"))
    n, err := s.Write(hh)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(" count", n)
}

func serR(s *serial.Port) (ss string, e error) {
    buf := make([]byte, 128)
    n, err := s.Read(buf)
    if err != nil {
        log.Fatal(err)
    }
    //log.Printf("%q", buf[:n])
    //fmt.Printf("<- %x", buf[:n])
    fmt.Println("<-", hex.EncodeToString(buf[:n]))
    //fmt.Println("<-", fmt.Sprintf("%x", buf[:n]))

    return hex.EncodeToString(buf[:n]), err
}

func ser(ss string){
    fmt.Println("Using serial:", ss)

    c := &serial.Config{Name: ss, Baud: 115200}
    s, err := serial.OpenPort(c)
    if err != nil {
        log.Fatal(err)
    }

    //time.Sleep(time.Second/2)
    serW(s, "a0");       serR(s) // 5f
    serW(s, "0a");       serR(s) // f5
    serW(s, "50");       serR(s) // af
    serW(s, "05");       serR(s) // fa

    serW(s, "a2");       serR(s) // a2
    serW(s, "80010000"); serR(s) // 80010000
    serW(s, "00000001"); serR(s) // +

    serW(s, "a2");       serR(s) // a2
    serW(s, "80010008"); serR(s) // 80010008
    serW(s, "00000001"); serR(s) // +

    s.Close()
}

func main() {
    fmt.Println("Hello world!")
    cwd, _ := os.Getwd()
    fmt.Println("cwd:", cwd)
    fmt.Println("args:", os.Args[1:])

    // Create Udev and Monitor
    u := udev.Udev{}
    m := u.NewMonitorFromNetlink("udev")

    // Add filters to monitor
    //m.FilterAddMatchSubsystemDevtype("usb-serial", nil)
    //m.FilterAddMatchTag("systemd")

    // Create a done signal channel
    done := make(chan struct{})

    // Start monitor goroutine and get receive channel
    ch, _ := m.DeviceChan(done)

    // WaitGroup for timers
    var wg sync.WaitGroup
    wg.Add(3)
    go func() {
	fmt.Println("Started listening on channel")
	for d := range ch {
		//fmt.Println("Event:", 
                //            "\nSyspath:",  d.Syspath(),
                //            "\nAction:",   d.Action(),
                //            "\nDevtype:",  d.Devtype(),
                //            "\nSubsystem:", d.Subsystem())
                //fmt.Println("")
                if d.Action() == "add" {
                  if d.Subsystem() == "usb-serial" {
                    s  := strings.Split(d.Syspath(), "/")
                    ss := "/dev/" + s[len(s)-1]
                    //fmt.Println(ss)
                    //fmt.Println("")
                    ser(ss)
                  }
                }
	}
	fmt.Println("Channel closed")
	wg.Done()
    }()
    go func() {
	fmt.Println("Starting timer to update filter")
	<-time.After(20 * time.Second)
	fmt.Println("Removing filter")
	m.FilterRemove()
	fmt.Println("Updating filter")
	m.FilterUpdate()
	wg.Done()
    }()
    go func() {
	fmt.Println("Starting timer to signal done")
	<-time.After(20 * time.Second)
	fmt.Println("Signalling done")
	close(done)
	wg.Done()
    }()
    wg.Wait()
}

/*
// +build linux

package udev

import (
	"fmt"
	"runtime"
	"sync"
	"testing"
	"time"
)

func ExampleMonitor() {

	// Create Udev and Monitor
	u := Udev{}
	m := u.NewMonitorFromNetlink("udev")

}

func TestMonitorDeviceChan(t *testing.T) {
	u := Udev{}
	m := u.NewMonitorFromNetlink("udev")
	m.FilterAddMatchSubsystemDevtype("block", "disk")
	m.FilterAddMatchTag("systemd")
	done := make(chan struct{})
	ch, e := m.DeviceChan(done)
	if e != nil {
		t.Fail()
	}
	var wg sync.WaitGroup
	wg.Add(3)
	go func() {
		fmt.Println("Started listening on channel")
		for d := range ch {
			fmt.Println(d.Syspath(), d.Action())
		}
		fmt.Println("Channel closed")
		wg.Done()
	}()
	go func() {
		fmt.Println("Starting timer to update filter")
		<-time.After(2 * time.Second)
		fmt.Println("Removing filter")
		m.FilterRemove()
		fmt.Println("Updating filter")
		m.FilterUpdate()
		wg.Done()
	}()
	go func() {
		fmt.Println("Starting timer to signal done")
		<-time.After(4 * time.Second)
		fmt.Println("Signalling done")
		close(done)
		wg.Done()
	}()
	wg.Wait()

}

func TestMonitorGC(t *testing.T) {
	runtime.GC()
}
*/