#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2022/3/22 5:45 下午
@Desc    :  toolbox line.
"""
import ast
import time
import datetime
import jmespath
import urllib.parse

from airtest.core.api import log, assert_equal
from deepdiff import DeepDiff


def diff(expect, actual, complete=True, exclude_paths=None) -> dict:
    """
    analysis diff result
    old new
    :param expect: expect
    :param actual: actual
    :param complete: match type, match complete or include, default complete.
    :param exclude_paths: parameter whitelist is empty by default.
    :return: {'result': True, 'data': {}}
    :Example:
        >>> {'result': True, 'data': {'dictionary_item_added': [root['data']]}}
    """
    exclude_paths = set([f"root['{path}']" for path in str(exclude_paths).split(',')])
    if len(exclude_paths) == 0:
        exclude_paths = None

    if not isinstance(expect, dict):
        expect = ast.literal_eval(expect)
    if not isinstance(actual, dict):
        actual = ast.literal_eval(actual)

    compare_results = DeepDiff(expect, actual, view='text', ignore_order=True,
                               exclude_paths=exclude_paths).to_dict()
    if not complete:
        if compare_results.get("values_changed"):
            result = False
        else:
            result = True
    else:
        if compare_results.get("dictionary_item_added") or compare_results.get(
                "dictionary_item_removed") or compare_results.get("values_changed") or compare_results.get(
                "iterable_item_added") or compare_results.get("iterable_item_removed"):
            result = False
        else:
            result = True

    return {'result': result, 'data': compare_results}


def extract(expressions, data):
    """
    extract the value you want！
    help documentation >>> https://jmespath.org/tutorial.html
    :param expressions: jsonpath expressions
    :param data: data dict
    :return: the value you want
    :Example:
        >>> test_dict = {"a": {"b": {"c": {"d": "value"}}}}
        >>> result = extract(expressions='a.b.c.d', data = test_dict)
        >>> print(result)
        >>> # value
    """
    _data = jmespath.search(expressions, data)
    return _data


def timestamp():
    """
    timestamp tool
    :return:
    """
    return int(round(time.time() * 1000))


def datetime_strife(fmt="%Y-%m-%d_%H-%M-%S"):
    """
    format datetime tool
    :param fmt: %Y-%m-%d_%H-%M-%S
    :return:
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(seconds=1.0):
    """
    sleep time
    :param seconds:
    :return:
    """
    time.sleep(seconds)


def target(target_url, sign='stag=', index=1) -> dict:
    """
    the value you want！
    :param index: default 1
    :param sign: split flag
    :param target_url: encoded string
    :return: the value you want！
    """
    stag = ast.literal_eval(str(urllib.parse.unquote(target_url).split(sign)[index]))

    return stag


def assert_diff(result: dict):
    """
    Assert two values are equal
    :param result:
    :raise AssertionError: if assertion
    :return: None
    """
    # Report step
    log(arg=result['data'], desc='Diff result')

    # Assertion
    assert_equal(True, result['result'], "Diff result")


def search(start_time, end_time, api, types):
    """

    :param types: request or response
    :param start_time: 13-bit, millisecond timestamp, 1648545731537.
    :param end_time: default current timestamp, 1648645731537
    :param api: interface name.
    :return: interface information list.
    :Example:
        >>> search_data = search(start_time=1648545731537, end_time=1648645731537, api='/api/test', types='request')
        >>> print(search_data)
        >>> # [{'invokedBy': 'open'}]
    """
    from garbevents.db import proxy_data
    data_collection = proxy_data.query(
        f"select {types} from proxy where timestamps between {start_time} and {end_time} "
        f"and api == '{api}';")

    res = []
    for data in data_collection:
        for d in data:
            res.append(ast.literal_eval(d))
    return res
