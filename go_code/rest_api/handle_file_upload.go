package rest_api

import (
	"fmt"
	"github.com/jszwec/csvutil"
	"github.com/pkg/errors"
	"io"
	"net/http"
)

// ProcessCSVUpload a CSV from a request
func ProcessCSVUpload(r *http.Request, formKey string, targetStruct any) error {
	err := r.ParseForm()
	if err != nil {
		return errors.Wrap(err, "processing file")
	}
	content, _, err := r.FormFile(formKey)
	if err != nil {
		return errors.Wrap(err, fmt.Sprintf("reading file at %s"))
	}
	data, err := io.ReadAll(content)
	if err != nil {
		return errors.Wrap(err, "reading csv file")
	}
	err = csvutil.Unmarshal(data, &targetStruct)
	if err != nil {
		return errors.Wrap(err, "decoding csv file")
	}
	return nil
}
