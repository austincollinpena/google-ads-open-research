package gcp

import (
	"bytes"
	"encoding/json"
	"net/http"
	"sync"
	"time"
)

// SimulateTaskCreator Runs HTTP requests against a certain path
// Just like a task queue
func SimulateTaskCreator[T any](args []T, url string) error {
	semaphoreChannel := make(chan struct{}, 100)
	defer close(semaphoreChannel)
	wg := sync.WaitGroup{}
	var outsideError error
	for _, val := range args {
		wg.Add(1)
		semaphoreChannel <- struct{}{}
		argCopy := val
		go func() {
			c := http.Client{
				Timeout: 60 * time.Second,
			}
			asBytes, err := json.Marshal(argCopy)
			if err != nil {
				outsideError = err
			}
			req, err := http.NewRequest("POST", url, bytes.NewReader(asBytes))
			req.Header.Add("content-type", "application/json")
			if err != nil {
				outsideError = err
			}
			_, err = c.Do(req)
			if err != nil {
				outsideError = err
			}
			wg.Done()
			<-semaphoreChannel
		}()
	}
	wg.Wait()
	return outsideError
}
