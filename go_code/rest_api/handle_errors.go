package rest_api

import (
	"encoding/json"
	"net/http"
)

type ErrorMessage struct {
	Message string `json:"error_message"`
}

func APIErr(w http.ResponseWriter, r *http.Request, errMessage string) {
	w.WriteHeader(400)
	e := ErrorMessage{
		Message: errMessage,
	}
	message, _ := json.Marshal(e)
	w.Write(message)
	return
}
