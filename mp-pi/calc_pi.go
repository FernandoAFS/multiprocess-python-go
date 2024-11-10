
package main

import (
    "strconv"
    "os"
    "math"
    "sync"
)

// calculates pi iteratively through a number of iterations
func calculatePi(nIter int64) (float64){

    numerator := 0.0
    pi := 1.0

    for n := int64(0); n < nIter; n++{
        numerator = math.Sqrt(2.0 + numerator)
        pi= pi * (numerator / 2.0)
    }

    return (1.0 / pi) * 2.0
}

// Run pi 50 calculations (each taking 2s each). split the job between n
// processes
func mainMp(){
    nProc64, err := strconv.ParseInt(os.Args[1], 10, 64)
    if err != nil{
        panic(err)
    }

    N := 50

    chArg := make(chan int64)

    var wg sync.WaitGroup
    wg.Add(int(nProc64))

    // PRODUCER
    go func(){
        var nIter int64 = 8000000000
        n := 0
        for n < N{
            n++
            chArg <- nIter
        }
        close(chArg)
    }()

    // WORKERS
    for i:=0;i< int(nProc64); i++{
        go func(){
            for arg := range chArg{
                calculatePi(arg)
            }
            wg.Done()
        }()
    }
    wg.Wait()
}

// RUN PI CALCULATION THROUGH A GIVEN NUMBER OF ITERATIONS.
func mainSp(){
    nIter, err := strconv.ParseInt(os.Args[1], 10, 64)
    if err != nil{
        panic(err)
    }
    calculatePi(nIter)
}

func main(){
    // mainMp()
    mainSp()
}
