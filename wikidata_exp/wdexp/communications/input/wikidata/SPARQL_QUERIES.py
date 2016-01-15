__author__ = 'Dani'

#### Endpoint info

BASE_ENDPOINT_URL = "https://query.wikidata.org/sparql?format=json&query="

BASE_WIKIDATA_ENTITY_URL = "http://www.wikidata.org/entity/Q"
BASE_WIKIDATA_PROPERTY_URL = "http://www.wikidata.org/prop/direct/P"


#### Response PARAMS

TYPE_RESULT = "type"
VALUE_RESULT = "value"
URI_RESULT = "uri"



###############  QUERIES

### Incoming

QUERY_INCOMING = """PREFIX wikibase: <http://wikiba.se/ontology#>
                 PREFIX wd: <http://www.wikidata.org/entity/>
                 SELECT ?prop ?sub WHERE {{?sub ?prop wd:{} .
                 SERVICE wikibase:label {{bd:serviceParam wikibase:language "en" .}}}}"""

INCOMING_QUERY_PROP = "prop"
INCOMING_QUERY_ENTITY = "sub"


### Outcoming

QUERY_OUTCOMING = 'PREFIX wikibase: <http://wikiba.se/ontology#> ' \
                  'PREFIX wd: <http://www.wikidata.org/entity/>  ' \
                  'SELECT ?prop ?obj WHERE {{wd:{} ?prop ?obj . ' \
                  'SERVICE wikibase:label {{bd:serviceParam wikibase:language "en" .}}}}'

OUTCOMING_QUERY_PROP = "prop"
OUTCOMING_QUERY_ENTITY = "obj"



