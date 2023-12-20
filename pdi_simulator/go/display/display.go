package main

import (
	"encoding/xml"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	rpc_xml "github.com/divan/gorilla-xmlrpc/xml"
	"github.com/gorilla/rpc"

	"layout"
)


// Define a struct for your service and the methods you want to expose via XML-RPC.
type DisplayService struct{}

type XMLLayout struct {
	XMLContent []byte
}

func (h *DisplayService) SetDisplayLayout(r *http.Request, args *XMLLayout, reply *struct{ Message string }) error {
	var layoutDef layout.LayoutDefinition
	xml.Unmarshal(args.XMLContent, &layoutDef)

	fmt.Printf("Device Type: %d\n", layoutDef.DeviceType)
	fmt.Printf("Display Width: %d\n", layoutDef.DisplayWidth)
	fmt.Printf("Display Height: %d\n", layoutDef.DisplayHeight)

	for _, layout := range layoutDef.Layouts {
		fmt.Printf("Layout Name: %s\n", layout.Name)
		for _, page := range layout.Pages {
			for _, panel := range page.Panels {
				fmt.Printf("Panel X: %d, Y: %d, Width: %d, Height: %d\n", panel.X, panel.Y, panel.Width, panel.Height)
				for _, text := range panel.Texts {
					fmt.Printf("Text Name: %s, X: %d, Y: %d, Width: %d, Height: %d, FontList: %s, AlignX: %s, AlignY: %s, RotationType: %s, Border: %s\n", text.Name, text.X, text.Y, text.Width, text.Height, text.FontList, text.AlignX, text.AlignY, text.RotationType, text.Border)
				}
			}
		}
	}

	reply.Message = "Success"
	return nil
}

func serveHTML(w http.ResponseWriter, r *http.Request) {
	htmlFile, err := os.Open("display/template/page.html")
	if err != nil {
		fmt.Printf("Error opening file: %v\n", err)
		return
	}
	defer htmlFile.Close()

	html, _ := io.ReadAll(htmlFile)
	w.Header().Set("Content-Type", "text/html")
	fmt.Fprint(w, string(html))
}

func main() {

	/*
		var layoutDef layout.LayoutDefinition
		err := (&layoutDef).ReadLayout()

		if err != nil {
			fmt.Printf("Error decoding XML: %v\n", err)
			return
		}
	*/
	// create a default route handler
	http.HandleFunc("/", func(res http.ResponseWriter, req *http.Request) {
		fmt.Fprint(res, "Hello: "+req.Host)
	})

	s := rpc.NewServer()
	xmlrpcCodec := rpc_xml.NewCodec()
	s.RegisterCodec(xmlrpcCodec, "text/xml")
	s.RegisterService(new(HelloService), "")
	s.RegisterService(new(DisplayService), "")

	http.Handle("/RPC2", s)
	http.HandleFunc("/display", serveHTML)

	log.Println("Starting XML-RPC server on localhost:5000/RPC2")
	log.Fatal(http.ListenAndServe(":5000", nil))
	log.Println("Server started...")

}
