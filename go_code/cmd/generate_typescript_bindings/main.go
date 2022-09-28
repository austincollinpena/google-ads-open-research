package main

import (
	"bytes"
	"github.com/austincollinpena/google-ads-open-research/go_code/public_rest_api"
	"github.com/skia-dev/go2ts"
	"log"
	"os"
)

func main() {
	generator := go2ts.New()
	generator.Add(public_rest_api.CheckAuthResponse{})
	var b bytes.Buffer
	err := generator.Render(&b)
	if err != nil {
		log.Fatal(err)
	}
	f, err := os.Create("./web-front-end/src/go-types.ts")
	if err != nil {
		log.Fatal(err)
	}
	_, err = f.Write(b.Bytes())
	if err != nil {
		log.Fatal(err)
	}
}
