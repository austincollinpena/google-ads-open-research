package free_tools

import (
	"encoding/json"
	"fmt"
	"github.com/austincollinpena/google-ads-open-research/go_code/go_common/gcp"
	"github.com/google/uuid"
	"github.com/pkg/errors"
	"github.com/spf13/viper"
)

// NGramServerArgs are what the Python server expects
type NGramServerArgs struct {
	FileName     string  `json:"filename"`
	RoasTarget   float64 `json:"roas_target"`
	FilterOnROAS bool    `json:"filter_on_roas"`
	Email        string  `json:"email"`
}

// QueueNGramAnalysis puts the n gram job in a Google Cloud Queue
func QueueNGramAnalysis(n NgramArgs, b []byte) error {
	fileName := fmt.Sprintf("%s-search-terms-%s", n.Email, uuid.NewString())
	err := gcp.SaveToGCP(b, fileName)
	if err != nil {
		return errors.Wrap(err, "uploading n gram to gcp")
	}
	ngramServerArgs := NGramServerArgs{
		FileName:     fileName,
		RoasTarget:   n.RoaSTarget,
		Email:        n.Email,
		FilterOnROAS: n.IsROASTarget,
	}

	argBody, err := json.Marshal(ngramServerArgs)
	if err != nil {
		return errors.Wrap(err, "could not marshal")
	}
	if viper.GetBool("prod") == true {
		_, err = gcp.CreateHTTPTaskWithToken("totemic-fact-361111", "us-central1", "queue-ngram-analysis", fmt.Sprintf("%s/ngram", viper.GetString("pythonAnalyticsServer")), "invoke-cloud-tasks@totemic-fact-361111.iam.gserviceaccount.com", argBody)
	} else {
		go gcp.SimulateTaskCreator([]NGramServerArgs{ngramServerArgs}, fmt.Sprintf("%s/ngram", viper.GetString("pythonAnalyticsServer")))
	}
	if err != nil {
		return errors.Wrap(err, "could not create task")
	}
	return nil
}
