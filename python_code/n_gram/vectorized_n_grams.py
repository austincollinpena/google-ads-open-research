from collections import defaultdict
import spacy
from spacy.tokens import DocBin
from spacy.matcher import PhraseMatcher

from generate_fake import generate_fake_terms

# Thanks to @miike, who is Mike Robins on the Measure slack
# If I revisit a python implementation I will use this

docs, match_terms = generate_fake_terms(10000, 20000)
lookup = {item['Search term']: item['Clicks'] for item in docs} # lookup from term => number of clicks

nlp = spacy.blank('en')

counts = defaultdict(int)

def inc_clicks(matcher, doc, i, matches):
    # callback increments the 'clicks' counter when a term match is found in a document
    m, _, _ = matches[i]
    counts[m] += lookup[str(doc)] # increment total clicks for this term

matcher = PhraseMatcher(nlp.vocab) # create a new phrase matcher using the vocab from all documents
for term in match_terms:
    matcher.add(term, [nlp.make_doc(term)], on_match=inc_clicks)

for doc in docs:
    doc = nlp.make_doc(doc['Search term'])
    matches = matcher(doc) # find term matches in the document

# print in the order of counts (you can optionally sort this)
for hash, clicks in counts.items():
    print(nlp.vocab.strings[hash], clicks) # resolve hashes to strings