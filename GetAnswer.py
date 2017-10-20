# -*- coding: utf-8 -*-
# filename: GetAnswer.py
import json
import os
import httplib, urllib, base64
import simplejson

knowledgebaseid = "bb5fa08b-3f70-4453-9da4-879e12657f84"
subscription_key = "285d4c7ef5d4430895df6fb82b8219c8"


def GetMethodStr(methodcode):
    return "POST"
    # raise Exception("invalid methcode")


def GetLQnaPairs(_list, maxnum):
    num = int(input("number of the QnaPairs:"))
    if num > maxnum:
        num = maxnum
    for i in range(num):
        question = input("enter the question:")
        answer = input("enter the answer:")
        _list.append({"answer": answer, "question": question})
    return


def Geturls(_list, maxnum):
    num = int(input("number of the urls:"))
    if num > maxnum:
        num = maxnum
    for i in range(num):
        url = input()
        _list.append(url)
    return


def GetAlterations(stat_str, altera):
    num = int(input())
    for i in range(num):
        word = input()
        altera_words = []
        while altera_word != '0':
            altera_words.append(altera_word)
            altera_word = input()
        altera.append({"word": word, "alterations": altera_words})
    return


def GetBody(methodcode, body, question_str):
    body["question"] = question_str
    body["top"] = 1
    return


def GetDetailUrl(methodcode):
    params = urllib.urlencode({})
    return "/qnamaker/v2.0/knowledgebases/%s/generateAnswer?%s" % (knowledgebaseid, params)


def get_answer_from_qnamaker(question_str): 
    methodcode = 5
    try:
        methodstr = GetMethodStr(methodcode)
    except Exception as e:
        print e
    headers = {}
    if methodstr != "DELETE" and methodstr != "GET":
        headers["Content-Type"] = "application/json"
    headers["Ocp-Apim-Subscription-Key"] = subscription_key
    body = {}
    GetBody(methodcode, body, question_str)
    try:
        coon = httplib.HTTPSConnection("westus.api.cognitive.microsoft.com")
        detailurl = GetDetailUrl(methodcode)
        coon.request(methodstr, detailurl, json.dumps(body), headers)
        response = coon.getresponse()
        data = response.read()
        # print type(data)
        data_dict = json.loads(data)
        output_answer = data_dict["answers"][0]["answer"]
        coon.close()
        return output_answer
    except Exception as e:
        print "Error"


class QnaMaker(object):
    def __init__(self):
        pass

    def get_answer(self, question_str):
        f = open("savedqna.txt", "r")
        savedqna = json.loads(f.read())
        print savedqna
        try:
            print "1"
            answer_str = savedqna[question_str]
        except Exception as e:
            print "2"
            answer_str = get_answer_from_qnamaker(question_str)
            f.close()
            if answer_str.encode("utf-8") == "No good match found in the KB":
                answer_str = "人家好像听不懂呢".decode("utf-8")
            else:
                f = open("savedqna.txt", "w")
                savedqna[question_str] = answer_str
                f.write(json.dumps(savedqna))
        finally:
            f.close()
            return answer_str.encode("utf-8")

