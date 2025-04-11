package main

import "fmt"

func main() {
   var sum int = 17
   var count int = 5
   res := sum/count 
   var mean float32
   fmt.Printf("%d\n", res)
   mean = float32(sum)/float32(count)
   fmt.Printf("mean 的值为: %f\n",mean)
}