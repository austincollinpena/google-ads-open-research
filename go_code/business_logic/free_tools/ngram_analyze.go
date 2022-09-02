package free_tools

import (
	"github.com/go-gota/gota/dataframe"
	"github.com/go-gota/gota/series"
	"github.com/rafatbiin/gongram"
	"regexp"
	"strings"
	"sync"
)

var RemoveAlphaNumeric = regexp.MustCompile(`[^A-Za-z0-9\s]`)

func GenerateNGrams(s []string) []string {
	var ngramList []string
	for _, val := range s {
		val = RemoveAlphaNumeric.ReplaceAllString(val, "")
		spaceCount := strings.Count(val, " ")
		// Handle single words
		if spaceCount == 0 {
			ngramList = append(ngramList, val)
		}
		for i := 1; i < 8; i++ {
			// avoid useless loops
			if i-1 > spaceCount {
				continue
			}
			// Error is essentially only for when the
			ngrams, _ := gongram.Generate(val, i)
			ngramList = append(ngramList, ngrams...)
		}
	}
	return ngramList
}

type StatColumnGetter struct {
	Name  string
	Index int
	Count int
}

type StatsMap map[string]FullStats

type FullStats struct {
	Clicks      float64
	Cost        float64
	Conversions float64
	ConvValue   float64
	Impr        float64
	TopImpr     float64
	AbsTopImpr  float64
	Appearances int
}

// StatsForDataframe
type StatsForDataframe struct {
	Clicks      float64
	Cost        float64
	Conversions float64
	ConvValue   float64
	Impr        float64
	TopImpr     float64
	AbsTopImpr  float64
	Appearances int
	SearchTerm  string
	Campaign    string
}

func GetNGramStats(df dataframe.DataFrame, grams []string, poolSize int, campaignName string) []StatsForDataframe {
	var SyncStatsMap sync.Map
	searchTerms := df.Col("SearchTerm").Records()

	if poolSize > 2500 {
		poolSize = 2500
	}

	semaphoreChannel := make(chan struct{}, poolSize)
	defer close(semaphoreChannel)
	wg := sync.WaitGroup{}

	for _, gram := range grams {
		wg.Add(1)
		semaphoreChannel <- struct{}{}
		gramCopy := gram
		go func() {
			ngramAnalysis(gramCopy, searchTerms, NgramAnalysisArgs{
				Clicks:      df.Col("Clicks").Float(),
				Cost:        df.Col("Cost").Float(),
				Conversions: df.Col("Conversions").Float(),
				ConvValue:   df.Col("ConversionValue").Float(),
				Impr:        df.Col("Impr").Float(),
				TopImpr:     df.Col("ImprTop").Float(),
				AbsTopImpr:  df.Col("ImprAbsTop").Float(),
			}, &SyncStatsMap)
			wg.Done()
			<-semaphoreChannel
		}()
	}

	wg.Wait()

	return TakeStatsMapToStruct(&SyncStatsMap, campaignName)
}

func TakeStatsMapToStruct(p *sync.Map, campaignName string) []StatsForDataframe {
	var n []StatsForDataframe
	p.Range(func(key, value interface{}) bool {
		searchterm := key.(string)
		stats := value.(FullStats)
		n = append(n, StatsForDataframe{
			Clicks:      stats.Clicks,
			Cost:        stats.Cost,
			Conversions: stats.Conversions,
			ConvValue:   stats.ConvValue,
			Impr:        stats.Impr,
			TopImpr:     stats.TopImpr,
			AbsTopImpr:  stats.AbsTopImpr,
			Appearances: stats.Appearances,
			SearchTerm:  searchterm,
			Campaign:    campaignName,
		})
		return true
	})
	return n
}

type NgramAnalysisArgs struct {
	Clicks      []float64
	Cost        []float64
	Conversions []float64
	ConvValue   []float64
	Impr        []float64
	TopImpr     []float64
	AbsTopImpr  []float64
}

func ngramAnalysis(gram string, searchTerms []string, ngramArgs NgramAnalysisArgs, SyncStatsMap *sync.Map) {

	for i := 0; i < len(searchTerms); i++ {
		//if strings.Contains(searchTerms[i], fmt.Sprintf("%s ", gram)) || strings.Contains(searchTerms[i], fmt.Sprintf("%s ", gram)) || searchTerms[i] == gram {
		if strings.Contains(searchTerms[i], gram) {
			value, valid := SyncStatsMap.Load(gram)
			if !valid {
				SyncStatsMap.Store(gram,
					FullStats{
						Clicks:      ngramArgs.Clicks[i],
						Cost:        ngramArgs.Cost[i],
						Conversions: ngramArgs.Conversions[i],
						ConvValue:   ngramArgs.ConvValue[i],
						Impr:        ngramArgs.Impr[i],
						TopImpr:     ngramArgs.TopImpr[i],
						AbsTopImpr:  ngramArgs.AbsTopImpr[i],
						Appearances: 1,
					})
			} else {
				asValue, _ := value.(FullStats)
				asValue.Clicks = ngramArgs.Clicks[i] + asValue.Clicks
				asValue.Cost = ngramArgs.Cost[i] + asValue.Cost
				asValue.Conversions = ngramArgs.Conversions[i] + asValue.Conversions
				asValue.ConvValue = ngramArgs.ConvValue[i] + asValue.ConvValue
				asValue.Impr = ngramArgs.Impr[i] + asValue.Impr
				asValue.TopImpr = ngramArgs.TopImpr[i] + asValue.TopImpr
				asValue.AbsTopImpr = ngramArgs.AbsTopImpr[i] + asValue.AbsTopImpr
				asValue.Appearances = asValue.Appearances + 1
				SyncStatsMap.Store(gram, asValue)
			}
		}
	}
}

// AddGramCount counts the number of spaces in a search terms and adds one
// this way, we can get the number of total grams in a given search term
func AddGramCount(df dataframe.DataFrame) dataframe.DataFrame {
	if len(df.Names()) == 0 {
		return df
	}
	searchTermIndex := IndexOf(df.Names(), "SearchTerm")
	s := df.Rapply(func(s series.Series) series.Series {
		searchTerm := s.Elem(searchTermIndex).String()
		count := strings.Count(searchTerm, " ") + 1
		return series.Ints(count)
	})
	df = df.Mutate(s.Col("X0")).Rename("GramCount", "X0")
	return df
}
