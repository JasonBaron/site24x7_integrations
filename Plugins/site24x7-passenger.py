#!/usr/bin/env python

import json
import subprocess
import xml.etree.ElementTree as ET

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"
# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Define commands to pull data from passenger-status
CMDJSON = '. /etc/profile ~/.bashrc 2>&1 >/dev/null; passenger-status --show=server --no-header'
CMDXML = '. /etc/profile ~/.bashrc 2>&1 >/dev/null; passenger-status --show=xml --no-header'

def metricCollector():
    METRICS_UNITS = {}
    xDataParse = {}
    data = {}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT
    data['total_active_memory_bytes'] = 0
    METRICS_UNITS['total_active_memory_bytes'] = 'bytes'
    #Pull Json Data:
    try:
        j = subprocess.Popen(CMDJSON, stdout=subprocess.PIPE, close_fds=True, shell=True)
        pjson_output = j.communicate()[0]
        pjson_output = json.loads(pjson_output)
        thread_count = pjson_output['threads']
    except:
        data['status'] = 0
        data['msg'] = 'error while parsing {} output'.format(j)

    data['plugin_version'] = str(PLUGIN_VERSION) + str(thread_count)
    data['thread_count'] = thread_count
    METRICS_UNITS['threads'] = 'count'

    for key in pjson_output:
        if 'threads' in key:
            continue
        if key.startswith('thread'):
            try:
                data[str(key) + '_active_client_count'] = pjson_output[key]['active_client_count']
                METRICS_UNITS[str(key) + '_active_client_count'] = 'count'
                data[str(key) + '_client_accept_speed_1h'] = pjson_output[key]['client_accept_speed']['1h']['value']
                METRICS_UNITS[str(key) + '_client_accept_speed_1h'] = 'ms'
                data[str(key) + '_client_accept_speed_1m'] = pjson_output[key]['client_accept_speed']['1m']['value']
                METRICS_UNITS[str(key) + '_client_accept_speed_1m'] = 'ms'
                data[str(key) + '_peak_active_client_count'] = pjson_output[key]['peak_active_client_count']
                METRICS_UNITS[str(key) + '_peak_active_client_count'] = 'count'
                data[str(key) + '_request_begin_speed_1h'] = pjson_output[key]['request_begin_speed']['1h']['value']
                METRICS_UNITS[str(key) + '_request_begin_speed_1h'] = 'ms'
                data[str(key) + '_request_begin_speed_1m_value'] = pjson_output[key]['request_begin_speed']['1m']['value']
                METRICS_UNITS[str(key) + '_request_begin_speed_1m'] = 'ms'
                data[str(key) + '_total_clients_accepted'] = pjson_output[key]['total_clients_accepted']
                METRICS_UNITS[str(key) + '_total_clients_accepted'] = 'count'
                continue
            except:
                data['status'] = 0
                data['msg'] = 'error while parsing {} output'.format(key)

    #Pull XML Data:
    try:
        x = subprocess.Popen(CMDXML, stdout=subprocess.PIPE, close_fds=True, shell=True)
        pxml_output = x.communicate()[0]
        tree = ET.ElementTree(ET.fromstring(pxml_output))
        root = tree.getroot()
    except:
        data['status'] = 0
        data['msg'] = 'error while parsing {} output'.format(x)

    try:
        xDataParse = {}
        for ps in root.getiterator('process'):
            for psi in ps.iter():
                if psi.tag == 'process':
                    continue
                elif psi.tag == 'pid':
                    psiPID = psi.text
                    xDataParse[ psiPID ] = [{'pid': psiPID}]
                    xDataParse[ psiPID ][0].update({'pid': psiPID})
                    continue
                else:
                    try:
                        psiPID
                    except:
                        data['status'] = 0
                        data['msg'] = 'error while executing {} command'.format(psi)
                    else:
                        xDataParse[ psiPID ][0].update({psi.tag: psi.text})
                        continue
    except:
        data['status'] = 0
        data['msg'] = 'error while parsing {} output'.format(ps)

    try:
        for index, item in enumerate(xDataParse, start=1):
            for xDP in xDataParse[item]:
                data['thread' + str(index) + '_pid'] = xDP['pid']
                data['thread' + str(index) + '_active_memory'] = int(xDP['real_memory'])
                METRICS_UNITS['thread' + str(index) + '_active_memory'] = 'bytes'
                data['total_active_memory_bytes'] += int(xDP['real_memory'])
                data['thread' + str(index) + '_busyness'] = xDP['busyness']
                METRICS_UNITS['thread' + str(index) + '_busyness'] = 'count'
                data['thread' + str(index) + '_cpu'] = xDP['cpu']
                METRICS_UNITS['thread' + str(index) + '_cpu'] = '%'
                data['thread' + str(index) + '_uptime'] = xDP['uptime']
    except:
        data['status'] = 0
        data['msg'] = 'error while parsing {} output'.format(item)

    data['units'] = METRICS_UNITS
    return data

if __name__ == '__main__':
    print json.dumps(metricCollector(), indent=4, sort_keys=True)
