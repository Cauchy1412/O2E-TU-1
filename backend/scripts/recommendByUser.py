import json
import numpy as np

class recommender:
    '''
    users：用户集
    k：表示得出最相近的k的近邻
    n：表示需要推荐的物品数，如不够则随机从微知识库里挑选一些
    '''
    def __init__(self, users, k=3, n=10):
        self.k = k
        self.n = n
        self.users = users
        # 对 user 的标签向量进行归一化
        for instance in self.users:
            self.users[instance]['tag_favor'] = self.normalize(self.users[instance]['tag_favor'])

    def normalize(self, x):
        '''
        将标签向量归一化，使得各分量之和为1，以避免造成新用户由于缺乏偏好数据本身标签向量就要比老用户小
        hope this work!
        '''
        total = np.sum(x)
        x = np.array(x) / total
        return x

    def euclideanDistence(self, x, y):
        '''
        用于计算标签向量之间的距离
        x, y：标签向量
        '''
        return np.linalg.norm(x-y)
        
    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.users:
            if instance != username:
                distance = self.euclideanDistence(self.users[username]['tag_favor'], self.users[instance]['tag_favor'])
                distances.append((instance, distance))

        distances.sort(key=lambda tuple: tuple[1])
        return distances
    
    #推荐算法的主体函数
    def recommend(self, username):
        '''
        实际的时候，可以直接使用 id
        '''
        #存储微知识id以及对应的权重，设成字典是为了方便下面的加权重
        recommendations = {}
        #计算出user与所有其他用户的相似度，返回一个list
        nearest = self.computeNearestNeighbor(username)
        # print nearest
        print('nearest: ', nearest)
        userFavor = self.users[username]['micro_knowledge']
        # print userRatings
        totalDistance = 0.0
        #得住最近的k个近邻的总距离
        for i in range(min(self.k, len(nearest))):
            totalDistance += nearest[i][1]
        if totalDistance==0.0:
            totalDistance=1.0
            
        #将与user最相近的k个人中user没有看过的书推荐给user，并且这里又做了一个分数的计算排名
        for i in range(min(self.k, len(nearest))):
        #第i个人的与user的相似度，转换到[0,1]之间
        #这个weight算得过于草率
            weight = 1 - nearest[i][1] / totalDistance
        
        #第i个人的name
            name = nearest[i][0]
        
        #第i个用户的发布或者收藏
            neighborFavor = self.users[name]['micro_knowledge']
        
            for knowledge in neighborFavor:
                if knowledge not in userFavor:
                    if knowledge not in recommendations:
                        recommendations[knowledge] = weight # 这里的权重当前仅考虑了当前用户与邻居的相似度，之后还可以考虑 knowledge 自身的点赞数、收藏数等
                    else:
                        recommendations[knowledge] = (recommendations[knowledge]+ weight)
            
        recommendations = list(recommendations.items()) # 转化成 (id, weight) tuple 的数组
        
        #做了一个排序
        recommendations.sort(key=lambda tuple: tuple[1], reverse=True)
        recommendations = list(map(lambda tuple: tuple[0], recommendations))
        # 若推荐数目不足 n，则进行填充
        if len(recommendations) < self.n:
        # 随机选一些微知识进行填充，如果可以的话，可以按照用户的标签向量作为依据，进行选取
        # 这里将使用随机数进行模拟
            for i in range(self.n - len(recommendations)):
                recommendations.append(np.random.randint(0, 1000))
        return recommendations[:self.n]
            
if __name__ == '__main__':
    with open('./scripts/userData.json', 'r') as json_file:
        user = json.load(json_file)
        r = recommender(user, k=5, n=10)
        res = r.recommend('user1')
        print(res)
    
