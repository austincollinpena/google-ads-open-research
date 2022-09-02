package free_tools

import (
	"fmt"
	"github.com/go-gota/gota/dataframe"
	"github.com/go-gota/gota/series"
	"github.com/pkg/errors"
)

// RunNGrams is the entrypoint for a python implementation of n grams
func RunNGrams(n []NgramUpload) error {
	// TODO: Convert "imprtop" and "imprabstop" to absolute values
	df := MarshallColumnsIntoNumbers(n, []string{"Impr", "Clicks", "Cost", "Conversions", "ConversionValue", "ImprTop", "ImprAbsTop"})
	//df = df.Filter(dataframe.F{
	//	Colidx:     0,
	//	Colname:    "Impr",
	//	Comparator: series.Greater,
	//	Comparando: 3,
	//})

	// TODO: Debug
	// June 1 - Aug 31 the word "locksmith near me" shows up 40 times in the results but 222 times
	//
	// It should show 903 clicks but only shows 40
	// moving towards just a strings.contains approach, rather than the " " + strings.contains
	// I see all 903, problem is there are a ton of one words I need to change now

	df = addCostColumns(df, []string{"Conversions", "ConversionValue"})

	df = ConvertPercentToAbsValues(df, "Impr", []string{"ImprTop", "ImprAbsTop"})

	// Create the efficient column
	dfEffecient := df.Filter(dataframe.F{
		Colidx:     0,
		Colname:    "ConversionValue_cost",
		Comparator: series.Greater,
		Comparando: 2.0,
	})

	uniqueCampaignNames := getUniqueValuesFromSlice(df.Col("Campaign").Records())
	uniqueSearchTerms := getUniqueValuesFromSlice(df.Col("SearchTerm").Records())
	uniqueGrams := getUniqueValuesFromSlice(GenerateNGrams(uniqueSearchTerms))

	completedDF := dataframe.New(
		series.New([]string{""}, series.String, "SearchTerm"))

	// Loop through the campaigns
	for _, campaign := range uniqueCampaignNames {
		campaignOnlyDF := df.Filter(dataframe.F{
			Colidx:     0,
			Colname:    "Campaign",
			Comparator: series.Eq,
			Comparando: campaign,
		})
		campaignResults := GetNGramStats(campaignOnlyDF, uniqueGrams, len(uniqueGrams), campaign)
		campaignResultsDF := dataframe.LoadStructs(campaignResults)

		// get efficient values
		efficientCampaignDF := dfEffecient.Filter(dataframe.F{
			Colidx:     0,
			Colname:    "Campaign",
			Comparator: series.Eq,
			Comparando: campaign,
		})

		efficientCampaignResults := GetNGramStats(efficientCampaignDF, uniqueGrams, len(uniqueGrams), campaign)

		efficientCampaignResultsDF := dataframe.LoadStructs(efficientCampaignResults)

		efficientCampaignResultsDF, err := AppendNameToColumns(efficientCampaignResultsDF, []string{"SearchTerm", "Campaign"}, "_efficient")

		if err != nil {
			return errors.Wrap(err, "appending name to columns")
		}

		// nil sizes don't work
		if len(efficientCampaignResults) == 0 {
			continue
			completedDF = completedDF.Concat(campaignResultsDF)
		}

		joinedDF := campaignResultsDF.LeftJoin(efficientCampaignResultsDF, "SearchTerm")

		joinedDF = joinedDF.Drop("Campaign_1")

		// TODO: Sometimes effecient seems to fail and nil concats make the whole thing nil

		completedDF = completedDF.Concat(joinedDF)

	}
	completedDF = AddGramCount(completedDF)
	err := SaveNGramData(completedDF)
	if err != nil {
		return err
	}
	return nil
}

// addCostColumns adds cost related columns for arbitrary strings
// it assumes that the cost column is named "Cost"
func addCostColumns(df dataframe.DataFrame, names []string) dataframe.DataFrame {
	//for _, name := range names {
	//	df = df.Mutate(series.New(make([]float64, df.Nrow()), series.Float, fmt.Sprintf("%s_cost", name)))
	//}
	for _, name := range names {
		nameIndex := IndexOf(df.Names(), name)
		costIndex := IndexOf(df.Names(), "Cost")
		//conversionCostIndex := IndexOf(df.Names(), fmt.Sprintf("%s_cost", name))
		s := df.Rapply(func(s series.Series) series.Series {
			cost := s.Elem(costIndex).Float()
			nameValue := s.Elem(nameIndex).Float()
			if cost == 0 || nameValue == 0 {
				return series.Floats(0)
			}
			value := series.Floats(nameValue / cost)
			return value
		})
		df = df.Mutate(s.Col("X0")).Rename(fmt.Sprintf("%s_cost", name), "X0")
		//df = df.Mutate(df.Col("X0"))
	}
	return df
}

// ConvertPercentToAbsValues takes something like top IS % and then gets that abs value
// So a top IS of 12% on an impression count of 100 would return 12.
func ConvertPercentToAbsValues(df dataframe.DataFrame, key string, names []string) dataframe.DataFrame {
	for _, name := range names {
		nameIndex := IndexOf(df.Names(), name)
		costIndex := IndexOf(df.Names(), key)
		//conversionCostIndex := IndexOf(df.Names(), fmt.Sprintf("%s_cost", name))
		s := df.Rapply(func(s series.Series) series.Series {
			cost := s.Elem(costIndex).Float()
			nameValue := s.Elem(nameIndex).Float()
			if cost == 0 || nameValue == 0 {
				return series.Floats(0)
			}
			value := series.Floats(nameValue * cost)
			return value
		})
		df = df.Drop(name)
		df = df.Mutate(s.Col("X0")).Rename(name, "X0")
	}
	return df
}
