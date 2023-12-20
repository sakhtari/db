package layout

import (
	"encoding/xml"
	"io"
	"os"
)

type LayoutDefinition struct {
	DeviceType    int      `xml:"deviceType,attr"`
	DisplayWidth  int      `xml:"displayWidth,attr"`
	DisplayHeight int      `xml:"displayHeight,attr"`
	Layouts       []Layout `xml:"Layouts>Layout"`
}

type Layout struct {
	Name  string `xml:"name,attr"`
	Pages []Page `xml:"Pages>Page"`
}

type Page struct {
	Panels []Panel `xml:"Panels>Panel"`
}

type Panel struct {
	X      int    `xml:"x,attr"`
	Y      int    `xml:"y,attr"`
	Width  int    `xml:"width,attr"`
	Height int    `xml:"height,attr"`
	Texts  []Text `xml:"Texts>Text"`
}

type Text struct {
	Name         string `xml:"name,attr"`
	X            int    `xml:"x,attr"`
	Y            int    `xml:"y,attr"`
	Width        int    `xml:"width,attr"`
	Height       int    `xml:"height,attr"`
	FontList     string `xml:"fontlist,attr"`
	AlignX       string `xml:"alignX,attr"`
	AlignY       string `xml:"alignY,attr"`
	RotationType string `xml:"RotationType,attr"`
	Border       string `xml:"border,attr"`
}

func (layoutDef *LayoutDefinition) ReadLayout() error {
	// Open our xmlFile
	xmlFile, err := os.Open("../pdi_xml/layout_408.xml")
	// if we os.Open returns an error then return it
	if err != nil {
		return err
	}

	defer xmlFile.Close()
	// read our opened xmlFile as a byte array.
	xmlData, _ := io.ReadAll(xmlFile)
	err = xml.Unmarshal([]byte(xmlData), &layoutDef)

	return err
}
