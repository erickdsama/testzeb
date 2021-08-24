from elasticsearch import Elasticsearch


def connect_elasticsearch():
    es = Elasticsearch(hosts='http://192.168.3.6:9200', timeout=10)
    if es.ping():
        return es
    else:
        ...
    return es


es = connect_elasticsearch()
