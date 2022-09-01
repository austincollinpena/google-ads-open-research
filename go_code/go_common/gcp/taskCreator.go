package gcp

import (
	cloudtasks "cloud.google.com/go/cloudtasks/apiv2"
	"context"
	"fmt"
	taskspb "google.golang.org/genproto/googleapis/cloud/tasks/v2"
)

// CreateHTTPTaskWithToken constructs a task with a authorization token
// and HTTP target then adds it to a Queue.
func CreateHTTPTaskWithToken(projectID string, locationID string, queueID string, url string, email string, body []byte) (*taskspb.Task, error) {
	// Create a new Cloud Tasks client instance.
	// See https://godoc.org/cloud.google.com/go/cloudtasks/apiv2
	ctx := context.Background()
	client, err := cloudtasks.NewClient(ctx)
	if err != nil {
		return nil, fmt.Errorf("NewClient: %v", err)
	}
	defer client.Close()

	// Build the Task queue path.
	// Example:    projects/adevo-339913/locations/us-east1/queues/start-ad-tests-two
	// From logs:  projects/adevo-339913/locations/us-east1/queues/start-ad-tests-two
	queuePath := fmt.Sprintf("projects/%s/locations/%s/queues/%s", projectID, locationID, queueID)
	// Build the Task payload.
	// https://godoc.org/google.golang.org/genproto/googleapis/cloud/tasks/v2#CreateTaskRequest
	req := &taskspb.CreateTaskRequest{
		Parent: queuePath,

		Task: &taskspb.Task{

			// https://godoc.org/google.golang.org/genproto/googleapis/cloud/tasks/v2#HttpRequest
			MessageType: &taskspb.Task_HttpRequest{

				HttpRequest: &taskspb.HttpRequest{
					HttpMethod: taskspb.HttpMethod_POST,
					Url:        url,
					Body:       body,
					Headers: map[string]string{
						"Content-type": "application/json",
					},
					AuthorizationHeader: &taskspb.HttpRequest_OidcToken{
						OidcToken: &taskspb.OidcToken{
							ServiceAccountEmail: email,
						},
					},
				},
			},
		},
	}

	// Add a payload message if one is present.
	req.Task.GetHttpRequest().Body = body

	createdTask, err := client.CreateTask(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("cloudtasks.CreateTask: %v", err)
	}

	return createdTask, nil
}
