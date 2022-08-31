package rest_api

import (
	"github.com/austincollinpena/google-ads-open-research/go_code/ops/config"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/rs/cors"
	"github.com/spf13/viper"
	"log"
	"net/http"
	"time"
)

func Routes() *chi.Mux {
	router := chi.NewRouter()
	router.Use(
		middleware.Compress(5),
		middleware.Heartbeat("/health-check"),
		middleware.Recoverer,
		cors.New(cors.Options{
			AllowedOrigins:   viper.GetStringSlice("allowedOrigins"),
			AllowCredentials: true,
			Debug:            true,
			//AllowedHeaders:   []string{"Content-Type", "Sentry-Trace", "X-CSRF-Token"},
			AllowedHeaders: []string{"*"},
			MaxAge:         300,
			ExposedHeaders: []string{"*"},
			AllowedMethods: []string{"GET", "PATCH", "POST"},
		}).Handler,
		middleware.RedirectSlashes,
	)
	router.Route("/v1", func(r chi.Router) {
		r.Mount("/api/group", freeToolRoutes())
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
	}
	err := s.ListenAndServe()
	if err != nil {
		log.Fatal(err)
	}
}
