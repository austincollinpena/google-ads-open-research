package public_rest_api

import (
	"context"
	"fmt"
	"github.com/austincollinpena/google-ads-open-research/go_code/go_common/gcp"
	"github.com/austincollinpena/google-ads-open-research/go_code/ops/error_reporting"
	"github.com/go-chi/chi/v5"
	"github.com/gorilla/securecookie"
	"github.com/markbates/goth"
	"github.com/markbates/goth/gothic"
	"github.com/markbates/goth/providers/google"
	"github.com/pkg/errors"
	"github.com/spf13/viper"
	"net/http"
	"time"
)

func oauth() *chi.Mux {
	router := chi.NewRouter()
	router.Get("/auth", Google)
	router.Get("/auth-callback-login", GoogleAuthCallbackSignIn)
	return router
}

func Google(w http.ResponseWriter, r *http.Request) {

	oauthClientID, err := gcp.GetSecret(r.Context(), "google_ads_oauth_client_id")
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "getting secret for oauth client id"))
		w.WriteHeader(500)
		return
	}

	oauthClientSecret, err := gcp.GetSecret(r.Context(), "google_ads_oauth_client_secret")
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "getting secret for oauth client secret"))
		w.WriteHeader(500)
		return
	}

	goth.UseProviders(
		google.New(
			oauthClientID,
			oauthClientSecret,
			"http://localhost:8075/v1/api/oauth/auth-callback-login",
			"https://www.googleapis.com/auth/adwords", "email"),
	)
	http.SetCookie(w, &http.Cookie{
		Name:  "redirect",
		Value: r.URL.Query().Get("final-url"),
	})

	r = r.WithContext(context.WithValue(context.Background(), "provider", "google"))
	gothic.BeginAuthHandler(w, r)
}

var sc *securecookie.SecureCookie

func InitSecureCookie() error {
	hashKey, err := gcp.GetSecret(context.Background(), "secure_cookie_hash_key")
	if err != nil {
		return errors.Wrap(err, "getting hash key on init secure cookie")
	}
	block, err := gcp.GetSecret(context.Background(), "secure_cookie_block_key")
	if err != nil {
		return errors.Wrap(err, "getting block key on init secure cookie")
	}
	sc = securecookie.New([]byte(hashKey), []byte(block))
	return nil
}

type UserAuthCookie struct {
	Email             string
	AccessToken       string
	UTCTimeValidUntil int64
}

// GoogleAuthCallbackSignIn is for signing in with Google oauth
func GoogleAuthCallbackSignIn(w http.ResponseWriter, r *http.Request) {
	r = r.WithContext(context.WithValue(context.Background(), "provider", "google"))
	user, err := gothic.CompleteUserAuth(w, r)
	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "goth complete user auth"))
		http.Redirect(w, r,
			fmt.Sprintf("%s/ad-intelligence/login", viper.GetString("domainToRedirectToAfterAuth")),
			301)
		return
	}

	state := gothic.GetState(r)

	err = setCookie(w, UserAuthCookie{
		Email:             user.Email,
		AccessToken:       user.AccessToken,
		UTCTimeValidUntil: time.Now().Unix() + (60 * 60),
	})

	if err != nil {
		error_reporting.ReportError(errors.Wrap(err, "save user details in rest route"))
		w.WriteHeader(500)
		return
	}
	finalURL := fmt.Sprintf("%s/free-tools/home", viper.GetString("domainToRedirectToAfterAuth"))
	if state != "" {
		finalURL = state
	}
	http.Redirect(w, r, finalURL, 301)
}

func setCookie(w http.ResponseWriter, u UserAuthCookie) error {
	encoded, err := sc.Encode("googleAdsOpenResearchSession", u)
	if err != nil {
		return errors.Wrap(err, "setting auth cookie")
	}
	cookie := &http.Cookie{
		Name:     "googleAdsOpenResearchSession",
		Value:    encoded,
		Path:     "/",
		MaxAge:   60 * 60, // Expires in one hour
		Secure:   false,
		HttpOnly: true,
		Domain:   viper.GetString("cookieDomain"),
	}
	http.SetCookie(w, cookie)
	return nil
}
