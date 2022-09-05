package public_rest_api

import (
	"fmt"
	"github.com/pkg/errors"
	"io"
	"net/http"
)

// ProcessCSVUpload a CSV from a request
func ProcessCSVUpload(r *http.Request, formKey string) ([]byte, error) {
	err := r.ParseForm()
	if err != nil {
		return nil, errors.Wrap(err, "processing file")
	}
	content, _, err := r.FormFile(formKey)
	if err != nil {
		return nil, errors.Wrap(err, fmt.Sprintf("reading file at %s"))
	}
	data, err := io.ReadAll(content)
	if err != nil {
		return nil, errors.Wrap(err, "reading csv file")
	}
	return data, nil
}
