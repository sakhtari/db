package content

type LayoutContent struct {
	Name  string `xml:"name,attr"`
	Pages []Page `xml:"Pages>Page"`
}

type Page struct {
	Texts []Text `xml:"Texts>Text"`
}

type Text struct {
	Name  string `xml:"name,attr"`
	Value string `xml:"value,attr"`
}
