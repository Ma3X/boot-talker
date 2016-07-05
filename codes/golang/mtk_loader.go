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
    "github.com/abiosoft/ishell"
    //_"github.com/mikepb/go-serial"
)

const CLR_0 = "\x1b[30;1m"
const CLR_R = "\x1b[31;1m"
const CLR_G = "\x1b[32;1m"
const CLR_Y = "\x1b[33;1m"
const CLR_B = "\x1b[34;1m"
const CLR_M = "\x1b[35;1m"
const CLR_C = "\x1b[36;1m"
const CLR_W = "\x1b[37;1m"
const CLR_N = "\x1b[0m"

func if_err() {
    fmt.Println("error open serial port: ")
    fmt.Println("for full reset serial device you must reload drivers:")
    fmt.Println("                                   ")
    fmt.Println("   cat /proc/tty/drivers           ")
    fmt.Println("   lsmod | grep usbserial          ")
    fmt.Println("   sudo modprobe -r pl2303 qcaux   ")
    fmt.Println("   sudo modprobe -r usbserial      ")
    fmt.Println("                                   ")
}

func serW(s *serial.Port, ss string) {
    hh, e := hex.DecodeString(ss)
    if e != nil {
        log.Fatal(e)
    }
    fmt.Printf("%x "+CLR_R+"->"+CLR_N, hh)
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
    fmt.Println(CLR_G+"<-"+CLR_N, hex.EncodeToString(buf[:n]))
    //fmt.Println("<-", fmt.Sprintf("%x", buf[:n]))

    return hex.EncodeToString(buf[:n]), err
}

func serB(s *serial.Port) {
        serW(s, "a2");       serR(s) // a2
        serW(s, "00000000"); serR(s) // A0010000
        serW(s, "00000004"); serR(s) // +
                             serR(s)
        serW(s, "a2");       serR(s) // a2
        serW(s, "00000004"); serR(s) // A0010004
        serW(s, "00000004"); serR(s) // +
                             serR(s)
        serW(s, "a2");       serR(s) // a2
        serW(s, "00000008"); serR(s) // A0010008
        serW(s, "00000004"); serR(s) // +
                             serR(s)
        serW(s, "a2");       serR(s) // a2
        serW(s, "0000000C"); serR(s) // A0010000
        serW(s, "00000004"); serR(s) // +
                             serR(s)
        serW(s, "a2");       serR(s) // a2
        serW(s, "00000010"); serR(s) // A0010000
        serW(s, "00000004"); serR(s) // +
                             serR(s)
        serW(s, "a2");       serR(s) // a2
        serW(s, "00000014"); serR(s) // A0010004
        serW(s, "00000004"); serR(s) // +
                             serR(s)
        serW(s, "a2");       serR(s) // a2
        serW(s, "00000018"); serR(s) // A0010008
        serW(s, "00000004"); serR(s) // +
                             serR(s)
        serW(s, "a2");       serR(s) // a2
        serW(s, "0000001C"); serR(s) // A0010000
        serW(s, "00000004"); serR(s) // +
                             serR(s)
}

func ser(ss string){
    fmt.Println("Using serial:", ss)

    c := &serial.Config{Name: ss, Baud: 115200}
    s, err := serial.OpenPort(c)
    if err != nil {
        log.Fatal(err)
    }

    //time.Sleep(time.Second/2)

    // swap-char-gaming ("dress code")
    serW(s, "a0");       serR(s) // 5f
    serW(s, "0a");       serR(s) // f5
    serW(s, "50");       serR(s) // af
    serW(s, "05");       serR(s) // fa

    // checking mcu model
    mcu := "unknown"
    // ckeck N1: in 0x80010008
    if mcu == "unknown" {
      fmt.Println("check software register in address:", "0x80010008")
      serW(s, "a2");       serR(s) // a2
      serW(s, "80010008"); serR(s) // A0000004
      serW(s, "00000001"); serR(s) // +
               res, _   := serR(s)
      switch res {
      case "6235":
        mcu = "mt6235"
        fmt.Println("mcu is:"+CLR_Y, mcu, CLR_N)

        serW(s, "a2");       serR(s) // a2
        serW(s, "80010000"); serR(s) // 80010000
        serW(s, "00000001"); serR(s) // +
        fmt.Println("5:",mcu)
                             serR(s)
        fmt.Println("6:",mcu)
      case "6253":
        mcu = "mt6253"
        fmt.Println("mcu is:"+CLR_Y, mcu, CLR_N)

        serW(s, "a2");       serR(s) // a2
        serW(s, "80010000"); serR(s) // 80010000
        serW(s, "00000001"); serR(s) // +
                             serR(s)
      default:
        fmt.Println("check not found in 0x80010008")
      }
    }

    // ckeck N2: in 0xA0000008
    if mcu == "unknown" {
      fmt.Println("check software register in address:", "0xA0000008")
      serW(s, "a2");       serR(s) // a2
      serW(s, "A0000008"); serR(s) // A0000008
      serW(s, "00000001"); serR(s) // +
               res, _   := serR(s)
      switch res {
      case "6261":
        mcu = "mt6261x"
        fmt.Println("mcu is:"+CLR_Y, mcu, CLR_N)

        serW(s, "a2");       serR(s) // a2
        serW(s, "A0000000"); serR(s) // A0000000
        serW(s, "00000001"); serR(s) // +
                             serR(s)
      default:
        fmt.Println("check not found in 0xA0000008")
      }
    }

    // block watchdog timer
    watchdog := "on"
    switch mcu {
      case "mt6235","mt6253":
        serW(s, "a1");       serR(s) // a1
        serW(s, "80030000"); serR(s) // 80030000
        serW(s, "00000001"); serR(s) // 00000001
        serW(s, "2200");     serR(s) // 2200
        watchdog = "off"
      default:
        fmt.Println(CLR_R+"no find watchdog"+CLR_N)
    }

    if watchdog == "off" {
        // create new shell.
          // by default, new shell includes 'exit', 'help' and 'clear' commands.
          shell := ishell.New()

          // display welcome info.
          shell.Println(CLR_G+"interactive shell"+CLR_N+" for "+CLR_Y+mcu+CLR_N)

          // register a function for "greet" command.
          shell.Register("greet", func(args ...string) (string, error) {
            name := "Stranger"
            if len(args) > 0 {
                name = strings.Join(args, " ")
            }
            return "Hello "+name, nil
          })

          // register a function for "read" command.
          shell.Register("read", func(args ...string) (string, error) {
            //name := "Stranger"
            //if len(args) > 0 {
            //    name = strings.Join(args, " ")
            //}

            // read first memory address
            serB(s)

            return "Success", nil
          })

          // start shell
          shell.Start()
    }

    s.Close()
}

func main() {
    fmt.Println("Working with UART port as MediaTek MCU")
    fmt.Println("")
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