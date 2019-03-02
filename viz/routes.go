package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

// TrackHandler - Handles track requests
func TrackHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("TrackHandler:", err)
		return
	}

	var tid string

	for {
		msgType, p, err := conn.ReadMessage()
		if err != nil {
			log.Println("TrackHandler ReadMessage:", err)
			continue
		}

		msg := fmt.Sprintf("%s", p)
		if msg == "done" {
			break
		}

		tid = msg
		trackStr := LookupTID(tid)

		if err := conn.WriteMessage(msgType, []byte(trackStr)); err != nil {
			log.Println("TrackHandler WriteMessage:", err)
			continue
		}
	}

	conn.Close()
}

// GraphHandler - Haldes graph requests
func GraphHandler(w http.ResponseWriter, r *http.Request) {
	graph, err := ioutil.ReadFile("../data/similar_pairs.txt")
	if err != nil {
		log.Println("GraphHandler:", err)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write(graph)
}
