package validate

import "github.com/go-playground/validator/v10"

// AppValidator uses a single instance of Validate, so it caches struct info
var AppValidator *validator.Validate

func init() {
	AppValidator = validator.New()
}
