package free_tools

import (
	"github.com/jdkato/prose/tokenize"
	"github.com/jszwec/csvutil"
	"io"
	"log"
	"os"
	"strings"
	"testing"
)

func BenchmarkTokenizer(b *testing.B) {
	f, err := os.Open("./git-ignored-data/search_terms_6-1_8-31.csv")
	if err != nil {
		b.Fatal(err)
	}
	asBytes, err := io.ReadAll(f)
	if err != nil {
		b.Fatal(err)
	}
	var d []NgramUpload
	err = csvutil.Unmarshal(asBytes, &d)
	if err != nil {
		b.Fatal(err)
	}
	df := MarshallColumnsIntoNumbers(d, []string{"Impr", "Clicks", "Cost", "Conversions", "ConversionValue", "ImprTop", "ImprAbsTop"})
	values := df.Col("SearchTerm").Records()
	stringArray := strings.Join(values, " ")
	b.ResetTimer()
	b.ReportAllocs()
	for n := 0; n < b.N; n++ {
		tokenize.TextToWords(stringArray)
	}
}

func TestRunNGrams(t *testing.T) {
	f, err := os.Open("./git-ignored-data/search_terms_6-1_8-31.csv")
	if err != nil {
		t.Fatal(err)
	}
	asBytes, err := io.ReadAll(f)
	if err != nil {
		t.Fatal(err)
	}
	var d []NgramUpload
	err = csvutil.Unmarshal(asBytes, &d)
	if err != nil {
		t.Fatal(err)
	}
	err = RunNGrams(d)
	if err != nil {
		t.Fatal(err)
	}
}

//func BenchmarkMultipleBenchmarks(b *testing.B) {
//	b.Run("500", BenchmarkRunNGramsPoolSize)      // 48793627100 ns/o
//	b.Run("5000", BenchmarkRunNGramsPoolSize5000) // 44632524100 ns/o
//	b.Run("100", BenchmarkRunNGramsPoolSize100)   // 54191868000 ns/o
//}

// Only parallel on the ngram loop:
func BenchmarkRunNGramsPoolSize(b *testing.B) {
	f, err := os.Open("./git-ignored-data/search_terms_6-1_8-31.csv")
	if err != nil {
		log.Fatal(err)
	}
	asBytes, err := io.ReadAll(f)
	if err != nil {
		log.Fatal(err)
	}
	var d []NgramUpload
	err = csvutil.Unmarshal(asBytes, &d)
	if err != nil {
		log.Fatal(err)
	}
	b.ResetTimer()
	b.ReportAllocs()
	for n := 0; n < b.N; n++ {
		RunNGrams(d)
	}
}

//func BenchmarkRunNGramsPoolSize5000(b *testing.B) {
//	f, err := os.Open("./git-ignored-data/search_terms.csv")
//	if err != nil {
//		log.Fatal(err)
//	}
//	asBytes, err := io.ReadAll(f)
//	if err != nil {
//		log.Fatal(err)
//	}
//	var d []NgramUpload
//	err = csvutil.Unmarshal(asBytes, &d)
//	if err != nil {
//		log.Fatal(err)
//	}
//	b.ResetTimer()
//	b.ReportAllocs()
//	for n := 0; n < b.N; n++ {
//		RunNGrams(d)
//	}
//}
//
//func BenchmarkRunNGramsPoolSize100(b *testing.B) {
//	f, err := os.Open("./git-ignored-data/search_terms.csv")
//	if err != nil {
//		log.Fatal(err)
//	}
//	asBytes, err := io.ReadAll(f)
//	if err != nil {
//		log.Fatal(err)
//	}
//	var d []NgramUpload
//	err = csvutil.Unmarshal(asBytes, &d)
//	if err != nil {
//		log.Fatal(err)
//	}
//	b.ResetTimer()
//	b.ReportAllocs()
//	for n := 0; n < b.N; n++ {
//		RunNGrams(d)
//	}
//}
