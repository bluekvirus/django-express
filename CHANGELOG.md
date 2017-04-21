Change Log
==========

0.3.2+ (2017-03-24*)
-------------------
1. Changed default services mount point to `<app_name>/<fn_name>`;
2. Added Model decorator @serve, @serve_unprotected for default CRUD->api mappings;
3. Added @url support for Model;
4. Refined @serve* for Model (+paging, +filter/sort);
5. Added services.url(noprefix=False) in addition to services.urls for per app service registration;
6. Added dummy mongodb (pymongo) backend for using django.db.connections['mongo'] directly;
7. Added ?db='DB' in @serve(-ed apis) for multiple db selection support;
8. Changed relative @url services mount point to `<app_name>/<url>`; 

working on ...

- @methods to replace the need to use generic views in Django;
- @cors and CORS middleware (mode: all/regex, tagged-only);
- @Model.signals.event for faster signal hook-up with fn;
- @permissions (uri/model, object) and ModelObjectBackend auth backend, (link m-m [ObjectPermission, object.pk] to user/group as object_permissions);
- refine @serve* (+validation);
- api listing (view, templates and static);
- @case(in=.json, out=.json) (shortcut);
- [optional] @task (asgi channel_layer/workers), live result notify;
- [optional] @schedule(period=, retry=), this indicates it is a @task;


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
