package main

import (
	"bytes"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/divan/gorilla-xmlrpc/xml"
)

type Datatest struct {
	Who []byte
}

func XmlRpcCall(method string, args Datatest) (reply struct{ Message string }, err error) {
	buf, _ := xml.EncodeClientRequest(method, &args)

	resp, err := http.Post("http://localhost:1234/RPC2", "text/xml", bytes.NewBuffer(buf))
	if err != nil {
		return
	}
	defer resp.Body.Close()

	err = xml.DecodeClientResponse(resp.Body, &reply)
	return
}

func main() {
	/*
		t := Datatest{Who: "user 1"}
		//t := "serasdf"
		//t.Who = `asdfasdf

		reply, err := XmlRpcCall("HelloService.Say", t)
		if err != nil {
			log.Fatal(err)
		}

		log.Printf("Response: %s\n", reply.Message)
	*/
	xmlFile, err := os.Open("../pdi_xml/layout_408.xml")
	// if we os.Open returns an error then return it
	if err != nil {
		log.Fatal(err)
	}

	defer xmlFile.Close()
	// read our opened xmlFile as a byte array.
	xmlData, _ := io.ReadAll(xmlFile)

	t := Datatest{Who: xmlData}
	reply, err := XmlRpcCall("DisplayService.SetDisplayLayout", t)
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("Response: %s\n", reply.Message)

}
