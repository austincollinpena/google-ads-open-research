package free_tools

//
//import (
//	"fmt"
//	"github.com/go-gota/gota/dataframe"
//	"github.com/go-gota/gota/series"
//	"regexp"
//	"strings"
//)
//
//// RunNGrams is the entrypoint for a python implementation of n grams
//func RunNGrams(n []NgramUpload) {
//	df := MarshallColumnsIntoNumbers(n, []string{"Impr", "Clicks", "Cost", "Conversions", "ConversionValue", "ImprTop", "ImprAbsTop"})
//	uniqueCampaignValues := getUniqueValuesFromSlice(df.Col("Campaign").Records())
//	uniqueSearchTerms := getUniqueValuesFromSlice(df.Col("SearchTerm").Records())
//	uniqueGrams := GetAllGrams(uniqueSearchTerms)
//	fmt.Println(uniqueSearchTerms, uniqueCampaignValues, uniqueGrams)
//}
//
//// GetAllGrams takes in a list and returns every known gram
//func GetAllGrams(s []string) []string {
//	var allGrams []string
//	for _, val := range s {
//		allNonUniqueGrams := getUniqueGrams(val)
//		allGrams = append(allGrams, allNonUniqueGrams...)
//	}
//	return allGrams
//}
//
//var MatchWordRegex = regexp.MustCompile(`[^\w\s]`)
//
//func getUniqueGrams(s string) []string {
//	return MatchWordRegex.Split(s, -1)
//}
//
//// dropNonNumericalElements drops anything that isn't a number
//func dropNonNumericalElements(e series.Element) series.Element {
//	str := e.Copy()
//	str.Set(strings.ReplaceAll(str.String(), ",", ""))
//	str.Set(strings.ReplaceAll(str.String(), " --", ""))
//	str.Set(strings.ReplaceAll(str.String(), "%", ""))
//	if str.String() == "" {
//		str.Set("0")
//	}
//	return str
//}
//
//// addCostColumns adds cost related columns
//func addCostColumns(df dataframe.DataFrame, names []string) {
//	for _, val := range names {
//		df.Capply()
//	}
//}
//
//// getUniqueValuesFromSlice takes any slice and returns the unique values
//func getUniqueValuesFromSlice[K comparable](vals []K) []K {
//	keys := make(map[K]bool)
//	list := []K{}
//	for _, e := range vals {
//		if _, val := keys[e]; !val {
//			keys[e] = true
//			list = append(list, e)
//		}
//	}
//	return list
//}
//
//// MarshallColumnsIntoNumbers takes a struct and a list of column names and returns a dataframe
//// with the correct data type
//func MarshallColumnsIntoNumbers(n []NgramUpload, colNames []string) dataframe.DataFrame {
//	df := dataframe.LoadStructs(n)
//	convertFromStringToInt := []string{"Impr", "Clicks", "Cost", "Conversions", "ConversionValue", "ImprTop", "ImprAbsTop"}
//	for _, val := range convertFromStringToInt {
//		colCopy := df.Col(val)
//		transMuted := colCopy.Map(dropNonNumericalElements)
//		df = df.Drop(val)
//		df = df.Mutate(series.New(transMuted.Records(), series.Float, val))
//	}
//	return df
//}
