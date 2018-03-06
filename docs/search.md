Search uses the Haystack library in front of an Elastic Search backend.
It is important to pay attention to the versions of Haystack and ElasticSearch in use since
supported features and functionality can vary. As of this writing we're using
[`django-haystack==2.4.1`](http://django-haystack.readthedocs.io/en/v2.4.1/) and `Elasticsearch version: 2.4.6`

To easily get a local instance up and running:

`docker run --rm -p 9200:9200/tcp elasticsearch:2.4.6`

Once running, you can populate the index with:

`manage.py rebuild_index`

## Config

Refer to `HAYSTACK_CONNECTIONS` and `HAYSTACK_DEFAULT_OPERATOR` in the settings files.

 
## Search logic

Search gets executed as a `SearchFilter`. We are just passing the user input along 
to the search backend. The default query operator has been set to `'OR'` to help avoid 
unnecessary empty sets or document exclusions.

Many types of keyword searches and phrase matches should work well as is. Support for stemming and root words will be 
subject to the capabilities of the ElasticSearch configuration. In most cases work would probably 
have to be done on the search logic and ES config to achieve successful stemming/root matching. 

### Documents, Templates, Weighting/Boosting

The content that gets submitted for each content type is based on the templates in 
`templates/search/indexes/content`.  While haystack provides an option for boosting in the API, we're using
 the templates to boost some fields by declaring them multiple times. 
