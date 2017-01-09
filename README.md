# ClassRank prototype: Wikidata explorer

## Source code
The source code maintained in this repository consist on set of modules handy for exploring the content of Wikidata knowledge graph. The core of the code is a prototype of ClassRank algorithm, but some other features has been implemented. The code is structured by separate commands that have been sequentially executed to obtain different results. Each command use to require an input file/URL and  an output path. Some commands consume the product of some others in a piped system. The following commands have been implemented:


- Count number of apparitions of each property in Wikidata. It works against a locally stored JSON dump of the graph.
- Extract description, labels and aliases of a given set of properties specified through a file. It works against an API.
- Classify a set of input entities of a graph in roles according to the way they are being used. Possibilities: class, instance, both of them (in different triples) or none of them. It uses a SPARQL API.
- Ellaborate a sorted list of classes regarding their number of discovered isntances in a graph. It consumes a certain format of JSON file.
- Compute the ClassRank score of each discovered class in a graph. It used a locally stored JSON dump, a local file of PageRank scores and a list of class-pointers in excell (xlsx).
- Detect properties frequently used to point a certain set of input nodes. It can consume the Wikidata JSON dump or an alternative format of JSON file.
- Extract information (descrittion, labels, aliasas) of a given set of entities. It works against an API.
- Obtain the rank of a certain set of input entities in a sorted list of PageRank scores. It consumes a certain format of JSON file.
- Creates a simplified Wikidata graph in a format in which each line represents a triple and each line has two tokes: first for the subject and last for the object. Each token is the ID of a Wikidata element. It uses a locally stored dump of Wikidata.
- Sort a JSON file containing PageRank scores of Wikidata entities and filter all those elements with minimun score. It consumes a certain format of JSON file.
- Calculate PageRank scores of a graph. It consumes a local file of a simplified Wikidata graph (unlabelled edges).
- Compare several features of two json files containing sorted lists of entities (different criteria: ClassRank scores, PageRank scores, number of instances,..).
- It builds a subgraph formed by all those elements in a graph conected with an input set of nodes with paths of length 1 (incoming/outgoing/both edges). It works against a SPARQL API.

### Complementary sources
Some other commands have been implemented in order to complete the information of some elements in Wikidata graph using external sources, or to sufy the structure of some other sources in order to compare it with Wikidata.


- Scrap of Google Trends. The command scraps queries against Google Trends related with labels or aliases of Wikidata elements in order to find extra aliases. DON NOT EXECUTE WITHOUT THE EXPLICIT PERMISSION OF GOOGLE COMPANY.
- Parser of AOL dump. The command count the number of n-grams apparitions (with different size of n) in a query log released by AOL.


## Results of applying ClassRank on Wikidata
In this page we are also offering some dowloadables with the results of applying our prototype of ClassRank on Wikidata. Two sources has been used: Wikidata API () and a local dump of Wikidata graph, with date with date of 2016/10/26. The dump is no longer offered in Wikidata's site. In order to reproduce the experiment using the same source, contact the authors of this repository.

Most of the results are rankings of elements sorted by some kind of metric, In this page we are publishing slices ocntaining the most relevant elements for each ranking in each case. In order to get access to the full lists, contact the authors.

1. Class-pointers:
  1. [List of acepted/rejected properties in Excell](https://danifdezalvarez.github.io/wikidataExplorer/)

2. PageRank:
  1. [Top-1000 entities according to PageRank](https://danifdezalvarez.github.io/wikidataExplorer/)

3. ClassRank:
  1. [Top-1000 classes according to ClassRank. Set of class-pointers of list 1.i] (https://danifdezalvarez.github.io/wikidataExplorer/)
  2. [Top-1000 classes according to ClassRank. Set of class-pointers: {P31, P279}] (https://danifdezalvarez.github.io/wikidataExplorer/)

4. Instance counting:
  1. [Top-1000 classes according to instance cointing. Set of class-pointers of list 1.i] (https://danifdezalvarez.github.io/wikidataExplorer/)
  2. [Top-1000 classes according to instance counting. Set of class-pointers: {P31, P279}] (https://danifdezalvarez.github.io/wikidataExplorer/) 
