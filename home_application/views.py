# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
import base64
import json

from blueking.component.shortcuts import get_client_by_request, logger
from common.mymako import render_mako_context, render_mako_tostring, render_json
from home_application.models import Script, OptLog


def home(request):
    """
    首页
    """
    client = get_client_by_request(request)
    biz_info = client.cc.get_app_list()
    script_info = Script.objects.all()
    script_list = [
        {
            'id': i.id,
            'script_name': i.script_name,
            'script_text': i.script_text,
            'script_input': i.script_input,
            'script_desc': i.script_desc
        }
        for i in script_info
    ]
    if biz_info.get("result"):
        biz_list = biz_info.get("data")
        param = {
            "app_id": biz_list[0].get("ApplicationID"),
            "field": "OSName"
        }
        biz_host_info = client.cc.get_host_list_by_field(param)
        if biz_host_info.get("result"):
            biz_host_list = []
            temp_biz_host_list = biz_host_info.get("data")
            for key in temp_biz_host_list:
                for host_info in temp_biz_host_list[key]:
                    host = {
                        "hostID": host_info["HostID"],
                        "hostIP": host_info["InnerIP"],
                        "hostOSType": key
                    }
                    biz_host_list.append(host)
    else:
        logger.error(u"请求业务列表失败：%s" % biz_info.get('message'))
        bk_biz_list = []
    return render_mako_context(request, '/home_application/index.html',
                               {"biz_list": biz_list, "biz_host_list": biz_host_list, "script_list": script_list})


def search_host(request):
    """
    获取业务下的主机
    """
    client = get_client_by_request(request)
    biz_id = request.GET.get("bk_biz_id")
    param = {
        "app_id": biz_id,
        "field": "OSName"
    }
    biz_host_info = client.cc.get_host_list_by_field(param)
    if biz_host_info.get("result"):
        biz_host_list = []
        temp_biz_host_list = biz_host_info.get("data")
        for key in temp_biz_host_list:
            for host_info in temp_biz_host_list[key]:
                host = {
                    "hostID": host_info["HostID"],
                    "hostIP": host_info["InnerIP"],
                    "hostOSType": key
                }
                biz_host_list.append(host)
    else:
        logger.error(u"请求业务机器列表失败：%s" % biz_host_info.get('message'))
        biz_host_list = []
    data = render_mako_tostring('/home_application/biz_host_table.html', {
        'biz_host_list': biz_host_list
    })

    return render_json({
        'result': True,
        'data': data
    })


def create_task(request):
    """
    创建查询任务
    """
    client = get_client_by_request(request)
    req = json.loads(request.body)
    biz_id = req.get("bk_biz_id")
    script_id = req.get("script_id")
    hosts = req.get("hosts")
    script = Script.objects.get(id=script_id)
    linux_host = []
    windows_host = []
    for host in hosts:
        if host.get("os_type") == "linux centos":
            linux_host.append({"ip": host.get("ip"), "source": 0})
        else:
            windows_host.append({"ip": host.get("ip"), "source": 0})
    if len(linux_host) != 0:
        param = {
            "app_id": biz_id,
            "content": base64.b64encode(script.script_text),
            "ip_list": linux_host,
            "type": 1,
            "account": "root",
        }
        job = client.job.fast_execute_script(param)
        if job.get("result"):
            OptLog.objects.create(
                biz=biz_id,
                script_id=script_id,
                task_id=job.get("data").get("taskInstanceId")
            )
    return render_json({"result": True, "data": {}})


def test_interface(request):
    return render_json({
        "result": True,
        "message": "hello",
        "data": "world"
    })
