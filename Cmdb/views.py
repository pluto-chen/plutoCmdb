from django.shortcuts import render,HttpResponse

# Create your views here.
import json
from Cmdb import core


def asset_report(request):

    if request.method == 'POST':
        report_handler = core.Asset(request)
        if report_handler.data_is_avlid():
            report_handler.data_input()
        print('要回复的内容----------->',report_handler.reply_msg)
        return HttpResponse(json.dumps(report_handler.reply_msg))

def asset_report_with_noid(request):

    if request.method == 'POST':
        report_handler = core.Asset(request)
        reply_data = report_handler.filter_with_projectname()
        print('要回复的内容----------->',reply_data)
        return HttpResponse(json.dumps(reply_data))
