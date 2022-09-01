package gcp

import (
	"bytes"
	"cloud.google.com/go/storage"
	"context"
	_ "embed"
	"fmt"
	"google.golang.org/api/option"
	"io"
)

var (
	//go:embed service_accounts/access-cloud-storage-buckets.json
	AccessCloudStorageBucketsServiceAccount []byte
)

// SaveToGCP saves bytes
func SaveToGCP(b []byte, path string) error {
	ctx := context.Background()
	opts := option.WithCredentialsJSON(AccessCloudStorageBucketsServiceAccount)
	Client, err := storage.NewClient(ctx, opts)
	if err != nil {
		return err
	}
	// Save it to the set destination
	wc := Client.Bucket("temporary-ads-data-storage").Object(fmt.Sprintf("%s", path)).NewWriter(ctx)
	if _, err := io.Copy(wc, bytes.NewReader(b)); err != nil {
		return err
	}
	if err := wc.Close(); err != nil {
		return err
	}
	return nil
}
