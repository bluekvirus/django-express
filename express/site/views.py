from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.db.models.base import ModelBase
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import fields
from django.apps import apps
import os
import pprint
import inspect
import imp
import importlib
import queue

from ..apps import ExpressConfig

import logging
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
def parseModel(task):
    vn, mkey, rmkey, name, ret = '', '', '', '', {}
    element, element_name = task['obj'], task['vname']
    mkey = element.__module__+ '.' + element.__name__
    logger.debug("%s: %s: %s" % (element_name, type(element), element.__module__+ '.' + element.__name__))
    ret[mkey] = {'relations': {}, 'fields': {}, 'name': element.__name__, 'mkey': mkey, 'verbose_name': element_name}
    logger.debug(ret[mkey])
    for field in element._meta.get_fields():
        if field.auto_created:
            continue
        logger.debug('  %s: %s: %s' % (field, type(field), field.__class__.__name__))
        logger.debug('      auto_created: %s' % field.auto_created)
        logger.debug('      related_model: %s, is_relation: %s' % (str(field.related_model), field.is_relation))
        logger.debug('      many_to_many: %s, many_to_one: %s, one_to_one: %s' % (field.many_to_many, field.many_to_one, field.one_to_one))
        if type(field) == fields.related.ForeignKey:
            logger.debug('      !!! ForeignKey found: %s' %(field))
        logger.debug('  %s: %s' % (field.verbose_name, type(field.verbose_name)))
        if type(field.verbose_name) == str:
            vn = field.verbose_name
            name = str(field)
        else:
            vn = str(field.verbose_name)
            name = str(field)
        ret[mkey]['fields'][name] = {
            'name': name,
            'verbose_name': vn,
            'type': field.get_internal_type(),
            'related_model': ''
        }
        if field.related_model:
            aa =  ['many_to_many', 'many_to_one', 'one_to_one'][list(filter(lambda ix: ix[1], enumerate([field.many_to_many, field.many_to_one, field.one_to_one])))[0][0]]
            if type(field.related_model) ==  str:
                logger.debug((element.__module__+ '.' + field.related_model))
                rmkey = element.__module__+ '.' + field.related_model
                ret[mkey]['relations'][rmkey] = {
                    'related_model': rmkey,
                    'relation': aa
                }
                ret[mkey]['fields'][name]['related_model'] = rmkey
            else:
                rmkey = str(field.related_model)[len("<class '") : -2]
                logger.debug(str(field.related_model))
                logger.debug(rmkey)
                ret[mkey]['relations'][rmkey] = {
                    'related_model': rmkey,
                    'relation': aa
                }
                ret[mkey]['fields'][name]['related_model'] = rmkey
            # logger.debug('  %s, %s' % (field.related_model.__name__, aa))
    return ret

# Create your views here.
@require_GET
def models(rq):
    logger.debug("__package__:" + __package__)
    q = queue.Queue()
    k = rq.GET.get('app')
    mdls = importlib.import_module('.models', k)
    logger.debug("mdls: " + str(mdls))
    for name, data in inspect.getmembers(mdls):
        if name == '__builtins__':
            continue
        if inspect.isclass(name):
            logger.debug("class@ %s" % name)
        # print('@@@@%s %s :' % (type(name), name), repr(data))
    for element_name in dir(mdls):
        element = getattr(mdls, element_name)
        logger.debug(element_name)
        if inspect.isclass(element) and type(element) == ModelBase:
            mkey = element.__module__+ '.' + element.__name__
            logger.debug(mkey)
            q.put({'obj': element, 'mkey': mkey, 'vname': element_name})
        else:
            pass

    ret = {}
    while not q.empty():
        task = q.get()
        mkey = task['mkey']
        if mkey not in ret:
            mdMeta = parseModel(task)
            ret[mkey] = mdMeta[mkey]
            # logger.debug(mdMeta)
            for md in mdMeta[mkey]:
                for r in mdMeta[mkey]['relations']:
                    logger.debug(r)
                    if r not in ret:
                        pkg = '.'.join(r.split('.')[:-1])
                        cls = r.split('.')[-1]
                        logger.debug(pkg)
                        logger.debug(cls)
                        q.put({'obj': getattr(importlib.import_module('.'.join(r.split('.')[:-1])), r.split('.')[-1]), 'mkey': r, 'vname': r.split('.')[-1]})
    return JsonResponse(ret)

@require_GET
def apps(rq):
    # logger.debug(ExpressConfig.applist)
    return JsonResponse({'payload': ExpressConfig.applist})
