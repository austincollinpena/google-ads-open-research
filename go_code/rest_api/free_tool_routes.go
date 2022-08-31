package rest_api

import (
	"encoding/json"
	"github.com/austincollinpena/google-ads-open-research/go_code/business_logic/free_tools"
	"github.com/austincollinpena/google-ads-open-research/go_code/ops/error_reporting"
	"github.com/austincollinpena/google-ads-open-research/go_code/ops/validate"
	"github.com/go-chi/chi/v5"
	"github.com/pkg/errors"
	"io"
	"net/http"
	"net/mail"
)

func freeToolRoutes() *chi.Mux {
	router := chi.NewRouter()
	router.Post("/ngram", Ngram)
	return router
}

func Ngram(w http.ResponseWriter, r *http.Request) {
	readBody, err := io.ReadAll(r.Body)
	defer r.Body.Close()
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "reading body ngram"))
		w.WriteHeader(400)
		return
	}
	var n free_tools.NgramArgs
	err = json.Unmarshal(readBody, &n)
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "parsing struct body"))
		w.WriteHeader(400)
		return
	}
	err = validate.AppValidator.Struct(n)
	if err != nil {
		APIErr(w, r, err.Error())
		return
	}
	var ngramStruct []free_tools.NgramUpload
	err = ProcessCSVUpload(r, "csv", &ngramStruct)
	if err != nil {
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
