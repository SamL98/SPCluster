package main

import (
	"flag"
	"log"
	"net/http"
)

func main() {
	LoadLibrary()

	var addr = flag.String("addr", ":8080", "Application address.")
	flag.Parse()

	fs := http.FileServer(http.Dir("static"))
	http.Handle("/", fs)
	http.HandleFunc("/tracks", TrackHandler)
	http.HandleFunc("/connections", GraphHandler)

	log.Println("Starting server on", *addr)
	if err := http.ListenAndServe(*addr, nil); err != nil {
		log.Fatal("ListenAndServe:", err)
	}
}
