package config

import (
	"bytes"
	_ "embed"
	"github.com/spf13/viper"

	"log"
	"os"
)

var (
	//go:embed debug-env.yaml
	debugEnv []byte
	//go:embed prod-env.yaml
	prodEnv []byte
)

func EnvSetUp() {
	// Set config env to the name of the file you want to load
	var envFile []byte
	if os.Getenv("config") == "prod-env" {
		envFile = prodEnv
	} else {
		envFile = debugEnv
	}
	viper.SetConfigType("yaml")
	err := viper.ReadConfig(bytes.NewReader(envFile))
	if err != nil {
		log.Fatal(err)
	}
}
