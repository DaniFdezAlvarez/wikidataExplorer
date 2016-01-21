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
                 SERVICE wikibase:label {{bd:serviceParam wikibase:language "en" .}}}}LIMIT 5"""

INCOMING_QUERY_PROP = "prop"
INCOMING_QUERY_ENTITY = "sub"


### Outcoming

QUERY_OUTCOMING = """PREFIX wikibase: <http://wikiba.se/ontology#>
                  PREFIX wd: <http://www.wikidata.org/entity/>
                  SELECT ?prop ?obj WHERE {{wd:{} ?prop ?obj .
                  SERVICE wikibase:label {{bd:serviceParam wikibase:language "en" .}}}} LIMIT 5"""

OUTCOMING_QUERY_PROP = "prop"
OUTCOMING_QUERY_ENTITY = "obj"



#### query get classes (is instance)


QUERY_IS_INSTANCE = """PREFIX wikibase: <http://wikiba.se/ontology#>
                      PREFIX wd: <http://www.wikidata.org/entity/>
                      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                      SELECT ?obj ?a_prop WHERE {{ wd:{} ?a_prop ?obj .
                      FILTER (?a_prop IN (wdt:P31, wdt:P279))
                      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}}} """  # LIMIT 5

PARAM_ENTITY_IS_INSTANCE = "obj"


#### query get instances (has instance)

QUERY_HAS_INSTANCES = """PREFIX wikibase: <http://wikiba.se/ontology#>
                      PREFIX wd: <http://www.wikidata.org/entity/>
                      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                      SELECT ?sub ?a_prop WHERE {{ ?sub ?a_prop wd:{} .
                      FILTER (?a_prop IN (wdt:P31, wdt:P279 ))
                      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}}}"""  # LIMIT 5

PARAM_ENTITY_HAS_INSTANCES = "sub"




