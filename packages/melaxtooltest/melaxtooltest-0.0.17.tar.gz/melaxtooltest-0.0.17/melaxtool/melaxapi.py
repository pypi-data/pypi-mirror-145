#!/usr/bin/env python
# coding: utf-8

import base64
import json
import os

import requests

# from IPython.core. import display
from IPython.core.display import display


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst


class NoteBook:
    iframe = """
          <iframe
              width="{width}"
              height="{height}"
              src="{src}{params}"
              frameborder="0"
              allowfullscreen
          ></iframe>
          """

    def __init__(self, url: str, nlpurl: str, id: str, **kwargs):
        self.url = url
        self.nlpurl = nlpurl
        self.width = 1080
        self.height = 600
        if 'width' in kwargs:
            self.width = kwargs['width']

        if 'height' in kwargs:
            self.height = kwargs['height']

        self.params = {"token": id, "domain": self.url}

    def _repr_html_(self):
        if self.params:
            from urllib.parse import urlencode
            params = "?" + urlencode(self.params)
        else:
            params = ""

        return self.iframe.format(src=self.url + "/test-nlp",
                                  width=self.width,
                                  height=self.height,
                                  params=params)


class NlpResult:

    def getRawText(self):
        return self.data['content']

    def getRawTextLen(self):
        return len(self.data['content'])

    def getItemByType(self, type: str):
        if 'indexes' in self.data:
            return {key: value for key, value in self.data['indexes'].items() if type in value}

    def getAllSentence(self):
        return self.sentence[:]

    def getAllEntity(self):
        return self.entities[:]

    def getAllRelation(self):
        return self.relations[:]

    def __init__(self, code, msg, url=None, cache='no', dic={}):
        self.url = url
        self.data = dic
        self.code = code
        self.msg = msg
        self.cache = cache
        self.sentence = []
        self.entities = []
        self.relations = []

        if 'indexes' in self.data:
            self.parse()

    def parse(self):
        for item in self.getItemByType('Sentence').items():
            if item[1] and 'Sentence' in item[1]:
                self.sentence.extend([value for value in item[1]['Sentence'].values()])

        idxdict = {'': []}

        # sen = self.sentence[idx]
        idx = 0
        self.sentence[idx]['entities'] = []
        # sen['entities'] = []
        for item in self.getItemByType('Entity').items():
            if item[1] and 'Entity' in item[1]:
                tmplist = [value for value in item[1]['Entity'].values()]

                for en in tmplist:
                    while not (
                            self.sentence[idx]['begin'] <= en['begin'] and self.sentence[idx]['end'] >= en['end']):
                        idx += 1
                        self.sentence[idx]['entities'] = []

                    self.sentence[idx]['entities'].append(en)
                    self.entities.append(en)
                    idxdict[self.key(en)] = [len(
                        self.entities) - 1, idx]

        idx = 0
        if len(self.entities) == 0:
            return
        ent = self.entities[idx]
        ent['relations'] = []
        for item in self.getItemByType('Relation').items():
            if item[1] and 'Relation' in item[1]:
                tmplist = [value for value in item[1]['Relation'].values()]
                self.relations.extend(tmplist)
                for rel in tmplist:
                    key = self.key(rel['fromEnt'])
                    if key in idxdict:
                        if 'relations' in self.entities[idxdict[key][0]]:
                            self.entities[idxdict[key][0]]['relations'].append(rel)
                        else:
                            self.entities[idxdict[key][0]]['relations'] = [rel]
                    # if key in idxdict and 'entities' in self.sentence[idxdict[key][1]]:
                    #     for en in self.sentence[idxdict[key][1]]['entities']:
                    #         if en['begin'] == rel['fromEnt']['begin'] and en['end'] == rel['fromEnt']['end']:
                    #             if 'relations' in en:
                    #                 en['relations'].append(rel)
                    #             else:
                    #                 en['relations'] = [rel]

    def key(self, en: dict):
        return str(en['begin']) + '_' + str(en['end']) + '_' + str(en['semantic'])


class MelaxClient:

    def __init__(self, key_path: str = None):
        self.key_path = key_path
        if key_path is not None:
            # read file key
            key = read_key_file(key_path)
            if key is not None:
                key_obj = verify_key(key)
                self.key = key
                self.url = key_obj['url']
                self.nlpurl = key_obj['nlpurl']
                return
        key = os.environ.get("MELAX_TECH_KEY")
        if key is not None:
            key_obj = verify_key(key)
            self.key = key
            self.url = key_obj['url']
            self.nlpurl = key_obj['nlpurl']

    # def invoke(self, text: str):
    #     payload = "{\"input\":\"" + str(base64.b64encode(text.encode("utf-8")), "utf-8") + "\"}"
    #     rsp = requests.request('POST', self.url, data=payload, headers=headers(self.key))
    #     if rsp.status_code == 200:
    #         return {'status_code': 200, 'output': json.loads(json.loads(rsp.content)['output'])}
    #     return {'status_code': rsp.status_code, 'content': str(rsp.content, 'utf-8')}

    def invoke(self, text: str, pipeline: str, front=False):
        # payload = "{\"input\":\"" + str(base64.b64encode(text.encode("utf-8")), "utf-8") + "\"}"
        payload = {
            "text": text,
            "pipeline": pipeline,
            "cache": front,
            "frontFlag": front,
        }
        rsp = requests.request('POST', self.url + "/api/nlp", data=json.dumps(payload), headers=headers(self.key))
        if rsp.status_code == 200:
            nlprsp = json.loads(rsp.content)
            if nlprsp and 'code' in nlprsp and nlprsp['code'] == 200:
                # print_response(nlprsp['data'])
                return NlpResult(code=200, msg='', url=self.url, cache=nlprsp['data'].get('cache', 'no'),
                                 dic=json.loads(nlprsp['data']['output']))
            else:
                return NlpResult(nlprsp['code'], nlprsp['message'])

        return NlpResult(rsp.status_code, rsp.content)

    def visualization(self, text: str, pipeline: str, **kwargs):
        result = self.invoke(text, pipeline, True)
        # k = NoteBook(self.url, result.cache, **kwargs)
        # k._repr_html_()
        display(NoteBook(self.url, self.nlpurl, result.cache, **kwargs))


def read_key_file(key_path: str):
    with open(key_path, mode='r') as file_obj:
        content = file_obj.read().splitlines()[0]
        return content
    return None


def verify_key(key: str):
    key_tmp = key.split('.')[1]
    if len(key_tmp) % 4 != 0:
        key_tmp += (len(key_tmp) % 4) * '='
    return json.loads(base64.b64decode(key_tmp))


def headers(key):
    return {'Content-Type': 'application/json', 'x-api-key': "Bearer " + key}

# if __name__ == '__main__':
#     input = """
#     Admission Date:  [**2118-6-2**]       Discharge Date:  [**2118-6-14**]
#
# Date of Birth:                    Sex:  F
#
# Service:  MICU and then to [**Doctor Last Name **] Medicine
#
# HISTORY OF PRESENT ILLNESS:  This is an 81-year-old female
# with a history of emphysema (not on home O2), who presents
# with three days of shortness of breath thought by her primary
# care doctor to be a COPD flare.  Two days prior to admission,
# she was started on a prednisone taper and one day prior to
# admission she required oxygen at home in order to maintain
# oxygen saturation greater than 90%.  She has also been on
# levofloxacin and nebulizers, and was not getting better, and
# presented to the [**Hospital1 18**] Emergency Room.
# """
#
# client = MelaxClient('/Users/lvjian/key.txt')
# response = client.invoke(input, "clinical:3", True)
#
# print(len(response.getAllSentence()))
