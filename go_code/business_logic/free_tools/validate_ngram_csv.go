package free_tools

type NgramArgs struct {
	RoaSTarget   float64 `json:"target" validate:"required"`
	Email        string  `json:"email" validate:"required,email"`
	IsROASTarget bool    `json:"isROASTarget"`
}

type NgramUpload struct {
	SearchTerm      string `csv:"Search term"`
	Campaign        string `csv:"Campaign"`
	AdGroup         string `csv:"Ad group"`
	Clicks          string `csv:"Clicks"`
	Impr            string `csv:"Impr."`
	Cost            string `csv:"Cost"`
	Conversions     string `csv:"Conversions"`
	ConversionValue string `csv:"Conv. value"`
	ImprTop         string `csv:"Impr. (Top) %"`
	ImprAbsTop      string `csv:"Impr. (Abs. Top) %"`
}
