from pymilvus import connections
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection
import random


class Milvus:
    _HOST = '114.116.221.131'
    _PORT = '19530'
    collection = None
    def __init__(self):
        self._HOST = '114.116.221.131'
        self._PORT = '19530'
        self.collection = self.get_milvus_collection('O2E')
        self.collection.load()

    def get_milvus_connection(self):
        '''建⽴Milvus连接'''
        connections.connect(
            alias="default", host= self._HOST, port=self._PORT
    )
    def create_milvus_collection(self):
        '''创建 collection'''
        milvus_id = FieldSchema(
            name="milvus_id",
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True
        )
        paper_id = FieldSchema(
            name="paper_id",
            dtype=DataType.INT64,
        )
        vector = FieldSchema(
            name="vector",
            dtype=DataType.FLOAT_VECTOR,
            dim=100
        )
        schema = CollectionSchema(
            fields=[milvus_id, paper_id, vector],
            description="O2E"
        ) 
        collection_name = "O2E"
        collection = Collection(
            name=collection_name,
            schema=schema,
            using='default',
            # shards_num=2,
            # consistency_level="Strong"
        )
    def get_milvus_collection(self, name):
        '''获取指定collection'''
        collection = Collection(name)
        return collection
    def milvus_insert(self, collection_name, data, partition_name=None):
        ''' 插⼊数据。
        param: collection_name: collection名称
        param: partition_name: partition名称
        param: data: 待插⼊的数据，list-like(list, tuple)
        return: Milvus⽣成的ids
        '''
        # collection = self.get_milvus_collection(collection_name)
        res = self.collection.insert(partition_name=partition_name, data=data)
        ids = res.primary_keys # 这个id是由Milvus⽣成的，⼤家注意要和论⽂id对应起来保存
        return ids
    def milvus_search(self, collection_name, query_vectors, topk, expr=None):
        ''' 查询相关向量。
        param: collection_name: collection名称
        param: partition_names: partition名称列表
        param: query_vectors: 待查询的数据，list-like(list, tuple) 
        param: topk: 每个query返回的最相似个数
        param: expr: 条件表达式
        return: ids_list, (list,list)
        '''
        # collection = self.get_milvus_collection(collection_name)
        # collection.load()
        res = self.collection.search(
            # partition_names=partition_names,
            data=query_vectors,
            anns_field="vector",
            limit=topk,
            expr=expr,
            param={"metric_type": "IP", "params": {"nprobe": 10}} 
        )
        ids_list = []
        for item in res:
            ids = []
            for p in item:
                ids.append(p.id)
            ids_list.append(ids)
        return ids_list
    def milvus_get_by_id(self, collection_name, id):
        '''根据id获取数据'''
        # collection = self.get_milvus_collection(collection_name)
        # collection.load()
        res = self.collection.query("milvus_id == {}".format(id), output_fields=["vector"])
        # print(res)
        for item in res:
            print(item)
    def paper_get_by_id(self, collection_name, id):
        '''根据id获取数据'''
        # collection = self.get_milvus_collection(collection_name)
        # collection.load()
        res = self.collection.query("milvus_id == {}".format(id), output_fields=["paper_id"])
        print(res)
        return res