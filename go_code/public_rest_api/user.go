package public_rest_api

import (
	"encoding/json"
	"github.com/austincollinpena/google-ads-open-research/go_code/ops/error_reporting"
	"github.com/go-chi/chi/v5"
	"github.com/pkg/errors"
	"net/http"
	"time"
)

func user() *chi.Mux {
	router := chi.NewRouter()
	router.Get("/check-auth", CheckAuth)
	return router
}

type CheckAuthResponse struct {
	Email             string `json:"email"`
	TimeLeftInSeconds int64  `json:"timeLeftInSeconds"`
	IsValid           bool   `json:"isValid"`
}

func CheckAuth(w http.ResponseWriter, r *http.Request) {
	c := CheckAuthResponse{
		Email:             "",
		TimeLeftInSeconds: 0,
		IsValid:           false,
	}
	if cookie, err := r.Cookie("googleAdsOpenResearchSession"); err == nil {
		value := UserAuthCookie{}
		err = sc.Decode("googleAdsOpenResearchSession", cookie.Value, &value)
		if err != nil {
			w.WriteHeader(500)
			return
		}
		c = CheckAuthResponse{
			Email:             value.Email,
			TimeLeftInSeconds: value.UTCTimeValidUntil - time.Now().Unix(),
			IsValid:           true,
		}

	}
	asJSON, err := json.Marshal(c)
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "marshalling json check auth"))
		w.WriteHeader(500)
		return
	}
	w.Write(asJSON)
	w.WriteHeader(200)
}
