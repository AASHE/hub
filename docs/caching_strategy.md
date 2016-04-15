# AASHE Hub Caching Strategy

It looks like we'll have to go with a hybrid of template and queryset caching. Given the pagination, I'm thinking that queryset caching makes sense.

## Services

We'll use [memcached](https://memcached.org/) and pick up a caching service from heroku add-ons or maybe Amazon's ElasticCache.

## User Types

  - unauthenticated
  - authenticated
    - member
    - non-memeber
    
## Cache-able areas

All template caching should take place below the header.

### Homepage

Template caching. Cache it all, regardless of user-type.

### Toolkits

Toolkit tab: Template caching - keys: auth
Resources tab: Queryset caching - keys: GET params, auth
STARS tab: Template caching

### Content Types

Querset Caching. Keys: content-type, GET params, auth

### Search

Queryset Caching. Keys: GET params and auth

## Other ideas

It might be possible to invalidate caches on approval of new resources. This is really the only time that these pages will change. This might be as simple as finding a way to invalidate the relevant caches for a new resource, for example:

If a resource is part of a particular content type and tied to two sustainability topics, we could invalidate the caches for those toolkits and the content type. This would require having...

### Consistent cache naming

#### Topics

    topic_<topic_id>_toolkit_anon
    topic_<topic_id>_toolkit_nonmember
    topic_<topic_id>_toolkit_member
    topic_<topic_id>_resources_page<num>_anon      # excludes filters
    topic_<topic_id>_resources_page<num>_nonmember # excludes filters
    topic_<topic_id>_resources_page<num>_member    # excludes filters
    topic_<topic_id>_stars_data                    # all access levels for now
    
#### Content Types

    content_type_<name>_page<num>_anon
    content_type_<name>_page<num>_nonmember
    content_type_<name>_page<num>_member
    
## Issues?

  - Would it be possible to have other reasons for clearing the cache?
    - Maybe when a topic name is changed?
