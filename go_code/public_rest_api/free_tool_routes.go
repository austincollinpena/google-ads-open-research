package public_rest_api

import (
	"encoding/json"
	"github.com/austincollinpena/google-ads-open-research/go_code/business_logic/free_tools"
	"github.com/austincollinpena/google-ads-open-research/go_code/ops/error_reporting"
	"github.com/austincollinpena/google-ads-open-research/go_code/ops/validate"
	"github.com/go-chi/chi/v5"
	"github.com/pkg/errors"
	"net/http"
	"net/mail"
)

func freeToolRoutes() *chi.Mux {
	router := chi.NewRouter()
	router.Post("/ngram", Ngram)
	return router
}

func Ngram(w http.ResponseWriter, r *http.Request) {
	err := r.ParseMultipartForm(52428800000000000)
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "parsing form"))
		APIErr(w, r, err.Error())
		return
	}
	stringifiedArgs := r.Form.Get("args")
	var n free_tools.NgramArgs
	err = json.Unmarshal([]byte(stringifiedArgs), &n)
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "parsing struct body"))
		APIErr(w, r, err.Error())
		return
	}
	err = validate.AppValidator.Struct(n)
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "validating"))
		APIErr(w, r, err.Error())
		return
	}
	csvData, err := ProcessCSVUpload(r, "csvData")
	if err != nil {
		APIErr(w, r, err.Error())
		return
	}
	err = free_tools.QueueNGramAnalysis(n, csvData)
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "queue ngram"))
		APIErr(w, r, err.Error())
		return
	}
}

func validMailAddress(address string) (string, bool) {
	addr, err := mail.ParseAddress(address)
	if err != nil {
		return "", false
	}
	return addr.Address, true
}
