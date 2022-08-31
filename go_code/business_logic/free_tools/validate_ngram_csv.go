package free_tools

type NgramArgs struct {
	RoaSTarget int    `json:"roas_target" validate:"required"`
	Name       string `json:"name" validate:"required"`
	FileName   string `json:"file_name" validate:"required"`
	Email      string `json:"email" validate:"required,email"`
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
