from elasticsearch import Elasticsearch


def connect_elasticsearch():
    es = Elasticsearch(hosts='http://143.198.158.144:9200/', timeout=10)
    if es.ping():
        return es
    else:
        ...
    return es


es = connect_elasticsearch()
