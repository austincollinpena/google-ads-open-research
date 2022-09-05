package free_tools

import (
	"fmt"
	"github.com/go-gota/gota/dataframe"
	"github.com/go-gota/gota/series"
	"github.com/pkg/errors"
	"strings"
)

// MarshallColumnsIntoNumbers takes a struct and a list of column names and returns a dataframe
// with the correct data type
func MarshallColumnsIntoNumbers(n []NgramUpload, colNames []string) dataframe.DataFrame {
	df := dataframe.LoadStructs(n)
	for _, val := range colNames {
		colCopy := df.Col(val)
		transMuted := colCopy.Map(dropNonNumericalElements)
		df = df.Drop(val)
		df = df.Mutate(series.New(transMuted.Records(), series.Float, val))
	}
	return df
}

// AppendNameToColumns
func AppendNameToColumns(df dataframe.DataFrame, ignoreCols []string, suffix string) (dataframe.DataFrame, error) {
	if len(df.Names()) == 0 {
		return df, nil
	}
	var newNames []string
NameLoop:
	for _, val := range df.Names() {
		for _, ignore := range ignoreCols {
			if val == ignore {
				newNames = append(newNames, val)
				continue NameLoop
			}
		}
		newNames = append(newNames, fmt.Sprintf("%s_%s", val, suffix))
	}
	err := df.SetNames(newNames...)
	if err != nil {
		return dataframe.DataFrame{}, errors.Wrap(err, "failed to set up dataframe")
	}
	return df, nil
}

func IndexOf[T comparable](collection []T, el T) int {
	for i, x := range collection {
		if x == el {
			return i
		}
	}
	panic(fmt.Sprintf("Could not find index for %T", el))
	return -1
}

// dropNonNumericalElements drops anything that isn't a number
func dropNonNumericalElements(e series.Element) series.Element {
	str := e.Copy()
	str.Set(strings.ReplaceAll(str.String(), ",", ""))
	str.Set(strings.ReplaceAll(str.String(), " --", ""))
	str.Set(strings.ReplaceAll(str.String(), "%", ""))
	if str.String() == "" {
		str.Set("0")
	}
	return str
}

// getUniqueValuesFromSlice takes any slice and returns the unique values
func getUniqueValuesFromSlice[K comparable](vals []K) []K {
	keys := make(map[K]bool)
	list := []K{}
	for _, e := range vals {
		if _, val := keys[e]; !val {
			keys[e] = true
			list = append(list, e)
		}
	}
	return list
}
