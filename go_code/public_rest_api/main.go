package public_rest_api

import (
	"github.com/austincollinpena/google-ads-open-research/go_code/ops/config"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/gorilla/sessions"
	"github.com/markbates/goth/gothic"
	"github.com/rs/cors"
	"github.com/spf13/viper"
	"log"
	"net/http"
	"time"
)

func Routes() *chi.Mux {
	router := chi.NewRouter()
	router.Use(
		//middleware.Compress(5),
		middleware.Heartbeat("/health-check"),
		middleware.Recoverer,
		middleware.Logger,
		cors.New(cors.Options{
			AllowedOrigins: viper.GetStringSlice("allowedOrigins"),
			//AllowedOrigins:   []string{"*"},
			AllowCredentials: true,
			Debug:            true,
			AllowedHeaders:   []string{"*"},
			MaxAge:           30000,
			ExposedHeaders:   []string{"*"},
			AllowedMethods:   []string{"GET", "PATCH", "POST"},
		}).Handler,
		middleware.RedirectSlashes,
		//maxBytes,
	)
	router.Route("/v1", func(r chi.Router) {
		r.Mount("/api/free-tools", freeToolRoutes())
		r.Mount("/api/oauth", oauth())
		r.Mount("/api/user", user())
	})
	return router
}

func RunServer() {
	config.EnvSetUp()
	router := Routes()
	walkFunc := func(method string, route string, handler http.Handler, middlewares ...func(http.Handler) http.Handler) error {
		log.Printf("%s %s\n", method, route) // Walk and print out all routes
		return nil
	}
	gothic.Store = sessions.NewCookieStore([]byte("fake-sessions-store-to-stop-annoying-warning"))
	err := InitSecureCookie()
	if err != nil {
		log.Fatal(err)
	}
	if err := chi.Walk(router, walkFunc); err != nil {
		log.Panicf("Logging err: %s\n", err.Error()) // panic if there is an error
	}
	s := &http.Server{
		ReadHeaderTimeout: 10 * time.Second,
		ReadTimeout:       10 * time.Second,    //
		WriteTimeout:      30000 * time.Second, // 30000 seconds to give the client a response
		IdleTimeout:       10 * time.Second,
		Addr:              viper.GetString("serveServerFrom"),
		Handler:           router,
		MaxHeaderBytes:    5242880000,
	}

	err = s.ListenAndServe()
	if err != nil {
		log.Fatal(err)
	}
}
