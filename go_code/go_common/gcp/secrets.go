package gcp

import (
	secretmanager "cloud.google.com/go/secretmanager/apiv1"
	"context"
	_ "embed"
	"fmt"
	"github.com/pkg/errors"
	"google.golang.org/api/option"
	secretmanagerpb "google.golang.org/genproto/googleapis/cloud/secretmanager/v1"
)

var (
	//go:embed service_accounts/get-secrets.json
	AccessGCPSecrets []byte
)

// GetSecret gets a secret managed by google
func GetSecret(ctx context.Context, key string) (string, error) {
	opts := option.WithCredentialsJSON(AccessGCPSecrets)
	c, err := secretmanager.NewClient(ctx, opts)
	defer c.Close()
	if err != nil {
		return "", errors.Wrap(err, "creating getsecret client")
	}
	req := &secretmanagerpb.AccessSecretVersionRequest{
		Name: fmt.Sprintf("projects/708323219376/secrets/%s/versions/latest", key),
	}
	secret, err := c.AccessSecretVersion(ctx, req)
	if err != nil {
		return "", errors.Wrap(err, "executing getsecret request")
	}
	return string(secret.Payload.Data), nil
}
