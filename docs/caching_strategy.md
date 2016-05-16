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

Toolkit tab: Template caching - varies on: auth, is_member
Resources tab: Queryset caching - varies on: GET params, auth, is_member
STARS tab: Template caching - varies on: none
  the STARS tab isn't super important, since it doesn't save a query, but it does cache the mardown conversion process

### Content Types

Querset Caching. Keys: content-type, GET params, auth

### Search

Queryset Caching. Keys: GET params and auth

### Specific Resources

Template Caching - on user.is_staff

### Additional Caches

#### Filters

Filter options are created for each session. These too should be cached,
but they will be nested caches, so they should use the shorter caching.

#### Footer HTML

This is pulled from the DB, so we can safely cache this too.

## Cache Policy

Generally, caching can go 12 hours. To keep this consistent, I'll use the `CACHE_TTL_LONG` var and add a context processor to ensure that it's available in each template.

## Invalidation

For now, I don't think we need to worry about invalidation for adding resources. If we have to we can simply clear the entire cache. Here are some thoughts anyway.

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
    - Why not just simply clear the entire cache?
  - Add the cache keys and cache times to templates for easy viewing
