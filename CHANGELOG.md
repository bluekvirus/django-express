Change Log
==========

0.3.0 (2017-02-10*)
-------------------
1. Changed default services mount point to `<full module path>/fn_name`;
2. Added Model decorator @serve, @serve_unprotected for default CRUD->api mappings;

working on ...

- refine @serve (+validation, +paging, +filter/sort)
- @url support for Model
- @schedule(period=, retry=)
- api listing (view, templates and static)
- @case(in=.json, out=.json) (shortcut)
- [optional] @permissions (uri/model, object)
- [optional] @task (celery)


0.2.5 (2017-01-29)
------------------
1. Added services autodiscovery;
2. Added basic decorators;
3. Added request and response delegators;
4. Added express flavored res.* apis;
5. Added express flavored req.* apis;
6. Added readme doc with version badges;
7. Fixed regression in res.download();
8. Fixed regression in @csrf;
9. Added req header access as dict;
10. Added django.urls.reverse() support;
11. Fixed the crlf-lf script issues on both Window and Linux/Mac;
12. Refined code examples and comments;
13. Fixed regression in res.redirect();
14. Added res.render() to use django templates;
