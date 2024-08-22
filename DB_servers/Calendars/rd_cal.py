#!/usr/bin/env /nas2/kuang/anaconda3/envs/py39/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
from datetime import datetime, timedelta, timezone
from pandas import DataFrame, concat
from oauth2client import client
from googleapiclient import sample_tools
from anthropic import Anthropic

cmd = "grep title /nas2/VuePressSrc/Sup.calendars/zh/E1/*md | grep -v READ | cut -d':' -f3"
cats = subprocess.check_output(cmd, shell=True).decode('utf8').strip('\n')
ICTcalendar_id = "25ae42ff6cf09e84f742882600ca7da7374bc357b97d9c8bffad8c3dcfa226d6@group.calendar.google.com"
id_dpt = {ICTcalendar_id: 'ICT'}

def main(ndays, calendar_id):
    service, _ = sample_tools.init(
        argv="", name="calendar", version="v3", doc=None,
        filename="/nas2/kuang/MyPrograms/GoogleCalendarAPI/calendar_sample.py",
        scope="https://www.googleapis.com/auth/calendar.readonly",
    )

    today = (datetime.now() + timedelta(days=-1)).replace(hour=9, minute=0)
    future_dates = [today + timedelta(days=i) for i in range(ndays + 1)]
    time_min = today.strftime('%Y-%m-%dT%H:%M:00Z')
    time_max = (today + timedelta(days=ndays)).strftime('%Y-%m-%dT%H:%M:00Z')

    try:
        calendar_list_entry = next((entry for entry in service.calendarList().list().execute()["items"]
                                     if entry["id"] == calendar_id), None)
        if calendar_list_entry:
            print(calendar_list_entry["summary"])
            events_result = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max).execute()
            events = events_result.get('items', [])

            if not events:
                return DataFrame()

            data = [process_event(e, future_dates) for e in events]
            df = DataFrame(data, columns=['datetime', 'length', 'category', 'event'])
            df['department'] = id_dpt[calendar_id]
            df['period'] = ndays
            df['group'] = calendar_list_entry["summary"]
            return df

    except client.AccessTokenRefreshError:
        print("The credentials have been revoked or expired, please re-run the application to re-authorize.")

def process_event(event, future_dates):
    if "recurrence" in event and "WEEKLY" in event["recurrence"][0]:
        return out_weekly(event["start"], event["end"], future_dates)
    else:
        return out_single(event["start"], event["end"])

def out_weekly(start_dict, end_dict, future_dates):
    start_time = datetime.fromisoformat(start_dict['dateTime']).replace(tzinfo=timezone(timedelta(hours=8)))
    end_time = datetime.fromisoformat(end_dict['dateTime'])
    hours_difference = (end_time - start_time).total_seconds() / 3600
    dh = f"({int(hours_difference)}H)"
    wd = start_time.weekday()
    rdays = [date for date in future_dates if date.weekday() == wd]
    return [(r.replace(microsecond=0).replace(tzinfo=timezone(timedelta(hours=8))), dh,
             r.strftime("%Y%b%d_%H:%M%a").lower() + dh) for r in rdays]

def out_single(start_dict, end_dict):
    if 'date' in start_dict:
        start_time = datetime.strptime(start_dict['date'], "%Y-%m-%d").replace(tzinfo=timezone(timedelta(hours=8)))
        return (start_time, "(1d)", start_time.strftime("%Y%b%d_%H:%M%a").lower() + "(1d)")
    else:
        start_time = datetime.fromisoformat(start_dict['dateTime']).replace(tzinfo=timezone(timedelta(hours=8)))
        end_time = datetime.fromisoformat(end_dict['dateTime'])
        hours_difference = (end_time - start_time).total_seconds() / 3600
        dh = f"({int(hours_difference)}H)"
        return (start_time, dh, start_time.strftime("%Y%b%d_%H:%M%a").lower() + dh)

def summ_cate(summ):
    api_key = "your-api-key-here"  # 將 API 金鑰移至環境變數或安全的配置檔中
    client = Anthropic(api_key=api_key)
    prompt = f"我會給你一個事件的摘要，請就其內容，將其歸類在{cats}等類中的某一類，請不要說明理由，直接給類別名稱即可。事件摘要: {summ}"
    return client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    ).content[0].text

if __name__ == "__main__":
    df0 = DataFrame()
    for calID in id_dpt:
        for ndays in [1, 7, 14, 31, 90]:
            df = main(ndays, calID)
            if not df.empty:
                df0 = concat([df0, df], ignore_index=True)

    df0.set_index('period').to_csv('whole.csv')
