package free_tools

import (
	"bytes"
	"github.com/go-gota/gota/dataframe"
	"github.com/pkg/errors"
	"os"
)

// TODO: https://www.youtube.com/watch?v=4yjrdMUlckc
func SaveNGramData(df dataframe.DataFrame) error {
	df = df.Arrange(
		dataframe.RevSort("Cost"))
	var b bytes.Buffer
	err := df.WriteCSV(&b)
	if err != nil {
		return errors.Wrap(err, "writing to csv")
	}
	f, err := os.Create("./results.csv")
	if err != nil {
		return errors.Wrap(err, "ngram csv file create")
	}
	_, err = f.Write(b.Bytes())
	if err != nil {
		return errors.Wrap(err, "writing to file")
	}
	return nil
}
