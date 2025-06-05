import cfg

import adtdatasources.es

import extract_kpi2

def dis():
    no = '0001744489-24-000276'
    search_metric = "Average Monthly Revenue Per Paid Subscriber"
    r = adtdatasources.es.ES(cfg.es_index).query_phrase(search_metric,'text',filter={'filename':no})

    df_metrics = extract_kpi2.extract_kpi(search_metric, [d['text'] for d in r])

def dis2():
    search_metric = "Average Monthly Revenue Per Paid Subscriber"
    r = adtdatasources.es.ES(cfg.es_index).query_phrase(search_metric,'text',filter={'meta.symbol':'DIS','meta.date_fiscal':'2024-09-28'})

    df_metrics = extract_kpi2.extract_kpi(search_metric, [d['text'] for d in r])

def adbe():
    no = '0000796343-25-000059'
    search_metric = "Revenue by geographic area"
    # search_metric = "GMV"
    r = adtdatasources.es.ES(cfg.es_index).query_phrase(search_metric, 'text', filter={'filename': no})
    df_metrics = extract_kpi2.extract_kpi(search_metric, [d['text'] for d in r])

    search_metric = "Subscription revenue by segment"
    r = adtdatasources.es.ES(cfg.es_index).query_phrase(search_metric, 'text', filter={'filename': no})
    df_metrics = extract_kpi2.extract_kpi(search_metric, [d['text'] for d in r])
    a=1


def bkng():
    no = '0001075531-25-000024'
    search_metric = "global average daily rates ADRs "
    # search_metric = "GMV"
    r = adtdatasources.es.ES(cfg.es_index).query_phrase(search_metric, 'text', filter={'filename': no})

    df_metrics = extract_kpi2.extract_kpi(search_metric, [d['text'] for d in r])
