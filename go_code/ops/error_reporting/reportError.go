package error_reporting

import "fmt"

// ReportError TODO make this meaningful
func ReportError(err error) {
	fmt.Println(err.Error())
}
