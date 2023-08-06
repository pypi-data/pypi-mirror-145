# -*- coding: utf-8 -*-
import traceback
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from pyelastices.utils import generate_record


class Client(Elasticsearch):
    def __init__(self, url, timeout=None, doc_type=None, **kwargs):
        super().__init__(url, **kwargs)
        self.url = url
        self.timeout = timeout
        self.doc_type = doc_type

        self._client = Elasticsearch(self.url, timeout=self.timeout)

    def connect(self):
        # assert self._client is None, "Elasticsearch is already running"
        self._client = Elasticsearch(self.url, timeout=self.timeout)

    def disconnect(self):
        assert self._client is not None, "Elasticsearch is not running"
        self.close()
        self._client = None

    def query(self, index, body, scroll="5m", size=1000):
        assert self._client is not None, "Connection is not acquired"

        try:
            sources = helpers.scan(
                client=self._client,
                query=body,
                scroll=scroll,
                index=index,
                size=size,
                doc_type=self.doc_type,
                timeout=self.timeout,
            )
            for source in sources:
                yield source["_source"]
            # return sources
        except:
            traceback.format_exc()
            return None

    def query_df(self, index, body, size=1000):
        """Get data from elasticsearch format into Dataframe"""

        data = self.query(index=index, body=body, size=size)

        return pd.DataFrame(data)

    def truncate_index(self, index):
        """Truncate index"""
        assert self._client is not None, "Connection is not acquired"

        body = {"query": {"match_all": {}}}
        self.delete_by_query(index=index, body=body)

    def write_df(self, df, index, doc_type, uid_name='indexId'):
        """Insert DataFrame into ElasticSearch

        :param df: the DataFrame, must contain the column 'indexId' for a unique identifier
        :param index: the ElasticSearch index
        :param doc_type: the ElasticSearch doc_type
        """
        assert self._client is not None, "Connection is not acquired"

        if not isinstance(df, pd.DataFrame):
            raise ValueError('df must be a pandas DataFrame')

        if not self.indices.exists(index=index):
            print('index does not exist, creating index')
            self.indices.create(index=index)

        if not uid_name in df.columns:
            raise ValueError('the uid_name must be a column in the DataFrame')

        if len(df[uid_name]) != len(set(df[uid_name])):
            message = 'the values in uid_name must be unique to use as an ElasticSearch _id'
            raise ValueError(message)
        self.uid_name = uid_name

        # The dataframe should be sorted by column name
        df = df.reindex(sorted(df.columns), axis=1)

        data = ({
            '_index': index,
            '_type': doc_type,
            '_id': record[uid_name],
            '_source': record
        } for record in generate_record(df))
        helpers.bulk(self._client, data)
