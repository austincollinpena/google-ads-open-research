package free_tools

import (
	"encoding/json"
	"fmt"
	"github.com/austincollinpena/google-ads-open-research/go_code/go_common/gcp"
	"github.com/google/uuid"
	"github.com/jszwec/csvutil"
	"github.com/pkg/errors"
	"github.com/spf13/viper"
	"math/rand"
)

// NGramServerArgs are what the Python server expects
type NGramServerArgs struct {
	FileName   string  `json:"filename"`
	RoasTarget float64 `json:"roas_target"`
	Name       string  `json:"name"`
}

// QueueNGramAnalysis puts the n gram job in a Google Cloud Queue
func QueueNGramAnalysis(n NgramArgs, u []NgramUpload) error {
	b, err := csvutil.Marshal(u)
	if err != nil {
		return errors.Wrap(err, "marshalling ngram args")
	}
	fileName := fmt.Sprintf("%s-search-terms-%s", n.Email, uuid.NewString())
	err = gcp.SaveToGCP(b, fileName)
	if err != nil {
		return errors.Wrap(err, "uploading n gram to gcp")
	}
	ngramServerArgs := NGramServerArgs{
		FileName:   fileName,
		RoasTarget: n.RoaSTarget,
		Name:       fmt.Sprintf("%s-%s", n.Email, RandStringRunes(4)),
	}
	argBody, err := json.Marshal(ngramServerArgs)
	if err != nil {
		return errors.Wrap(err, "could not marshal")
	}
	if viper.GetBool("prod") == true {
		_, err = gcp.CreateHTTPTaskWithToken("totemic-fact-361111", "us-central1", "queue-ngram-analysis", fmt.Sprintf("%s/ngram", viper.GetString("pythonAnalyticsServer")), "invoke-cloud-tasks@totemic-fact-361111.iam.gserviceaccount.com", argBody)
	} else {
		err = gcp.SimulateTaskCreator([]NGramServerArgs{ngramServerArgs}, fmt.Sprintf("%s/ngram", viper.GetString("pythonAnalyticsServer")))
	}
	if err != nil {
		return errors.Wrap(err, "could not create task")
	}
	return nil
}

var letterRunes = []rune("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

func RandStringRunes(n int) string {
	b := make([]rune, n)
	for i := range b {
		b[i] = letterRunes[rand.Intn(len(letterRunes))]
	}
	word := string(b)
	// don't swear at the user
	badWords := []string{"FUCK", "SHIT", "DICK", "ARSE", "CUNT", "CRAP", "TWAT", "SLUT"}
	for _, w := range badWords {
		if word == w {
			return "WOOP"
		}
	}
	return word
}
