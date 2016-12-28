# ClassRank prototype: Wikidata explorer

## Source code
The source code maintained in this repository consist on set of modules handy for exploring the content of Wikidata knowledge graph. Most of the code is a prototype of ClassRank algorithm, but some other features has been implemented. The code is structured by separate commands that have been sequentially executed to obtain the final results. Each command use to require an input file/URL and  an output path. Some commands consume the product of some other in a piped system. The following commands have been implemented:


- Count number of apparitions of each property in wikidata database. It works against a locally stored json dump.
- Extract description, labels and aliases for a given set of properties specified through a file. It works against an API
- Scrap Google Trends to find queries related with labels or alias of properties.
- Count number of n-grams apparitions (with different size of n) in AOL. It works using a local dump.
- COMPLETE


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
