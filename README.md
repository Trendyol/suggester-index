# Suggester Index

![](https://img.shields.io/badge/build-pass-success) ![](https://img.shields.io/badge/requirements-up%20to%20date-success) ![](https://img.shields.io/badge/elasticsearch-v6.4.3-blue) ![](https://img.shields.io/badge/language-turkish-blue)

This suggester project generate Turkish words for your Elastic Search fuzzy index.

## Getting Started

### Prerequisites

You will need interpreter for **Python** and **pip3** the standard package manager for Python

For installing Python and pip with Homebrew:

```
brew install python3
```

### Installing

A step by step series of examples that tell you how to get a development env running

Clone repository with this command:

```
git clone https://github.com/Trendyol/suggester-index.git
```

Go to project file and install all requirements with pip3:

```
pip3 install requirements.txt 
```

#### Set variables before run the script:

Each document indexed is associated with a _type (Mapping Type). 
The value of the _type field is accessible in queries, aggregations, scripts, and when sorting 
Set target index document type like:

```
export DOC_TYPE = "keywords"
```

Set post target Elasticsearch one of the data node url like:

```
export TARGET_ES_URL = "10.1.50.10:9200"
```

Set get source Elasticsearch one of the data node url:

```
export SOURCE_ES_URL = "10.1.50.10:9200"
```

Index is how Elasticsearch represents data. In Elasticsearch, a Document is the unit of search and index. 
An index consists of one or more Documents.
Set target index name:

```
export TARGET_INDEX = "fuzzyKeywords"
```

Set source index name:

```
export SOURCE_INDEX = "productIndex"
```

Product name attribute of source example:

```json
 "hits" : {
    "total" : 1234,
    "max_score" : 1.0,
    "hits" : 
      {
        "_index" : "indexName",
        "_type" : "type",
        "_id" : "1234567",
        "_score" : 1.0,
        "_source" : {
          "name" : "Kadın Gri Melanj T-Shirt"
        }
      }
```

Set source name attribute:

```
export SOURCE_ATTRIBUTE = "name"
```

## Running the script

#### After the set variable then we can run generateFuzzyKeyword.py class:

```
python ./getFuzzyKeywords.py
```

After running the script, the words aggregate the dictionary and Elasticsearch source directory.
Then separates the word and deletes special characters and numbers, then trims. 
After performing these operations script write the words keywords.json file then script reads this file and post it to the target index of Elasticsearch.

## Making Docker image
To make docker image this project you can run this command:

```
docker build -t suggester-index .
```

After docker image created, we can set the variables and run the docker container::

```
docker run -e DOC_TYPE="keyword" -e TARGET_ES_URL="10.1.50.10:9200" -e SOURCE_ES_URL="http://10.1.50.10:9200" -e SOURCE_INDEX="productIndex" -e TARGET_INDEX="fuzzyKeywords" -e SOURCE_ATTRIBUTE="name" suggester-index
```

Or you can run the docker image we have prepared for you:

```
docker run -e DOC_TYPE="keyword" -e TARGET_ES_URL="10.1.50.10:9200" -e SOURCE_ES_URL="http://10.1.50.10:9200" -e SOURCE_INDEX="productIndex" -e TARGET_INDEX="fuzzyKeywords" -e SOURCE_ATTRIBUTE="name" trendyol/suggester-index
```

## Contributing
Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/suggester-index)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/suggester-index)
5. Open a Pull Request

Please don't forget to check our commit message styles as we want to have consistency across our commit logs.

## Acknowledgments

* [ElasticSearch 6.4](https://www.elastic.co/guide/en/elasticsearch/reference/6.4/index.html "ElasticSearch")

* [Suggester-Index Docker Hub Page](https://hub.docker.com/r/trendyol/suggester-index "Suggester-Index Docker Hub Page")

## License

```
Copyright 2019 Trendyol.com

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```