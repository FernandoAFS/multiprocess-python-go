package main

import (
    "strconv"
    "os"
    "sync"
    "math"
    "time"
    "fmt"
)

func strLen(s string) int {
	return len(s)
}

func strLenRef(s *string) int {
	return len(*s)
}

func genStrL(n int64) string {
    t0 := time.Now()
	s := make([]rune, n)
	for i := range s {
		s[i] = '1'
	}
    res := string(s)
    dt := time.Now().Sub(t0).Nanoseconds()
    fmt.Printf("%f dt\n", float64(dt) / math.Pow(10, 9))
    return res
}

func worker(f func()) <-chan struct{}{
    c := make(chan struct{})
    go func(){
        f()
        close(c)
    }()
    return c
}

func merge(in ...<-chan struct{}){
   var wg sync.WaitGroup
 
   wg.Add(len(in))
   for _, c := range in {
       go func(){
           // WAIT FOR CHANNEL TO CLOSE
           for range(c){
           }
           wg.Done()
       }()
   }
   wg.Wait()
}


func mainSp() {
    strL := int64(math.Pow(10, 8))
	N := 50

	s := genStrL(strL)
	for i := 0; i < N; i++ {
		strLen(s)
	}
}


const N = 1000
var strL = int64(math.Pow(10, 8))

func mpVal(nProc int64) {

	s := genStrL(strL)

    chArg := make(chan string)

    // producer
    go func(){
        for i:=0; i<N; i++{
            chArg <- s
        }
        close(chArg)
    }()

    var wg sync.WaitGroup
    wg.Add(int(nProc))

    for i:=0; i<int(nProc); i++{
        go func(){
            for s := range(chArg){
                strLen(s)
            }
            wg.Done()
        }()
    }
    wg.Wait()
}

func mpRef(nProc int64) {

	s := genStrL(strL)

    chArg := make(chan *string)

    // producer
    go func(){
        for i:=0; i<N; i++{
            chArg <- &s
        }
        close(chArg)
    }()

    var wg sync.WaitGroup
    wg.Add(int(nProc))

    for i:=0; i<int(nProc); i++{
        go func(){
            for s := range(chArg){
                strLenRef(s)
            }
            wg.Done()
        }()
    }
    wg.Wait()
}

func main() {

	kind := os.Args[1]
    if kind == "sp"{
        mainSp()
        return
    }

    nProc, err := strconv.ParseInt(os.Args[2], 10, 64)
    if err != nil{
        panic(err)
    }

    if kind == "mpVal"{
        mpVal(nProc)
        return
    }

    if kind == "mpRef"{
        mpRef(nProc)
        return
    }
    panic("first argument must be sp, mpVal or mpRef")
}
