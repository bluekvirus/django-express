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

from ..apps import ExpressConfig

import logging
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

def parseModel(md):
    logger.debug("__package__:" + __package__)
    my_module = importlib.import_module('.models', md)
    print("my_module: " + str(my_module))
    for name, data in inspect.getmembers(my_module):
        if name == '__builtins__':
            continue
        if inspect.isclass(name):
            logger.debug("class@ %s" % name)
        # print('@@@@%s %s :' % (type(name), name), repr(data))
    # print('------------------List elements in %s:------------------------' %(my_module))
    ret = {}
    for element_name in dir(my_module):
        element = getattr(my_module, element_name)
        # if inspect.isclass(element) and isinstance(element, ModelBase):
        if inspect.isclass(element) and type(element) == ModelBase:
            vn, mkey, rmkey, name = '', '', '', ''
            mkey = element.__module__+ '.' + element.__name__
            logger.debug("%s: %s: %s" % (element_name, type(element), element.__module__+ '.' + element.__name__))
            ret[mkey] = {'relations': {}, 'fields': {}, 'name': element.__name__, 'mkey': mkey, 'verbose_name': element_name}
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
        elif inspect.ismodule(element):
            # logger.debug("%s: %s" % (element_name, type(element)))
            # logger.debug("module %s" % element_name)
            pass
        else:
            # logger.debug("%s: %s" % (element_name, type(element)))
            pass
    # logger.debug('  %s: %s' % (ret, type(ret)))
    # print('--------------end List elements in %s:------------------------' %(my_module))
    return ret

# Create your views here.
@require_GET
def models(rq):
    k = rq.GET.get('app')
    return JsonResponse(parseModel(k))

@require_GET
def apps(rq):
    # logger.debug(ExpressConfig.applist)
    return JsonResponse({'payload': ExpressConfig.applist})
