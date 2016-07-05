package hktool

import (
    "fmt"
    "github.com/tarm/serial"

    "strings"
    "log"
    "encoding/hex"

    // "os"
    // "sync"
    // "time"
    // "path/filepath"
    // "github.com/jochenvg/go-udev"
    // https://godoc.org/github.com/tarm/serial
    // "github.com/tarm/serial"
    // "github.com/abiosoft/ishell"
    // https://godoc.org/github.com/mikepb/go-serial
    // goserial "github.com/mikepb/go-serial"

    //parent ".."
)
//import L "github.com/mikepb/go-serial/listports"

const CLR_0 = "\x1b[30;1m"
const CLR_R = "\x1b[31;1m"
const CLR_G = "\x1b[32;1m"
const CLR_Y = "\x1b[33;1m"
const CLR_B = "\x1b[34;1m"
const CLR_M = "\x1b[35;1m"
const CLR_C = "\x1b[36;1m"
const CLR_W = "\x1b[37;1m"
const CLR_N = "\x1b[0m"

func leftExt(s string, padStr string, pLen int) string{
    if len(s)>pLen {
        return s[len(s)-pLen:]
    }
    return strings.Repeat(padStr, pLen-len(s)) + s
}

func serW(s *serial.Port, ss string) {
    hh, e := hex.DecodeString(ss)
    if e != nil {
        log.Fatal(e)
    }
//    fmt.Printf("%x "+CLR_R+"->"+CLR_N, hh)
    //n, err := s.Write([]byte("\x0a"))
//    n, err := s.Write(hh)
    _, err := s.Write(hh)
    if err != nil {
        log.Fatal(err)
    }
//    fmt.Println(" count", n)
}

func serR(s *serial.Port) (ss string, e error) {
    buf := make([]byte, 128)
    n, err := s.Read(buf)
    if err != nil {
        log.Fatal(err)
    }
    //log.Printf("%q", buf[:n])
    //fmt.Printf("<- %x", buf[:n])
//    fmt.Println(CLR_G+"<-"+CLR_N, hex.EncodeToString(buf[:n]))
    //fmt.Println("<-", fmt.Sprintf("%x", buf[:n]))

    return hex.EncodeToString(buf[:n]), err
}

func serH(s *serial.Port, addr string, line string) (left8 string, right8 string) {
        addr = strings.ToLower(addr)
        line = strings.ToLower(line)

        serW(s, "a2");       res, err := serR(s) // a2
        if err != nil        { log.Fatal(err) }
        if res != "a2"       { fmt.Println("not return a2");       return }
        serW(s, addr);       res, err  = serR(s) // addr
        if err != nil        { log.Fatal(err) }
        if res != addr       { fmt.Println("not return", addr);    return }
        serW(s, "00000004"); res, err  = serR(s) // len
        if err != nil        { log.Fatal(err) }
        if res != "00000004" { fmt.Println("not return 00000004"); return }
                             res, err  = serR(s) // +
        if err != nil        { log.Fatal(err) }
        if len(res) != 16    { fmt.Println("not return 16 chars"); return }

        return res[:8], res[8:]

        //serW(s, "00000000"); res, err  = serR(s)
        //serW(s, "00000004"); res, err  = serR(s)
        //serW(s, "00000004"); res, err  = serR(s)
        //serW(s, "0000000C"); res, err  = serR(s)
        //serW(s, "00000010"); res, err  = serR(s)
        //serW(s, "00000014"); res, err  = serR(s)
        //serW(s, "00000004"); res, err  = serR(s)
        //serW(s, "00000018"); res, err  = serR(s)
        //serW(s, "00000004"); res, err  = serR(s)
        //serW(s, "0000001C"); res, err  = serR(s)
}

// for exporting use Uppercase first char into function/type/variable name!
func Read(s *serial.Port, args ...string) {

    addr := "00000000"
    if len(args) > 0 { addr = args[0] }
    addr  = leftExt(addr, "0", 8)

    //offs := "00000000"
    //if len(args) > 1 { offs = args[1] }
    //offs  = leftExt(offs, "0", 8)

    line := "00000000"
    if len(args) > 1 { line = args[1] }
    line  = leftExt(line, "0", 8)

    fmt.Println(CLR_Y+"read address:"+CLR_N, "0x"+addr)
    //fmt.Println(CLR_Y+"read  offset:"+CLR_N, "0x"+offs)
    fmt.Println(CLR_Y+"print  lines:"+CLR_N, "0x"+line)

    //parent.serB(s)
    l8, r8 := serH(s, addr, line)
    fmt.Println(l8, r8)

    fmt.Println("")
}
