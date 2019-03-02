package main

import (
	"bufio"
	"log"
	"os"
	"strings"
)

var library map[string]string

// LoadLibrary - Load the library
func LoadLibrary() {
	library = make(map[string]string)

	f, err := os.Open("/Users/samlerner/Documents/Spotify/library.csv")
	if err != nil {
		log.Fatal("LoadLibrary:", err)
	}

	r := bufio.NewReader(f)

	var line string
	err = nil

	for err == nil {
		byteN := []byte("\n")
		line, err = r.ReadString(byteN[0])
		terms := strings.Split(line, ",")

		if len(terms) < 3 {
			break
		}

		artist := terms[0]
		tid := terms[1]
		title := terms[2]

		artist = strings.Trim(artist, "'\n")
		title = strings.Trim(title, "'\n")

		library[tid] = strings.Join([]string{title, artist}, ":")
	}
}

// LookupTID - Looks up the TID
func LookupTID(tid string) string {
	mdStr := library[tid]
	return strings.Join([]string{tid, mdStr}, ":")
}
