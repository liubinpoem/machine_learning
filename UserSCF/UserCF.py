#coding=utf-8

#利用movielens数据进行推荐
from math import sqrt


class UserCF(object):
    def __init__(self,u_file,m_file):
        self.user_file=u_file;
        self.movie_file=m_file;
        self.prefer,self.movies=self.LoadData()
        self.unions=self.MovieUsersPair()
        self.CalMatch()

    #首先读取用户评分文件，形成<用户id，<电影id,评分>>的键值对
    #再读取电影文件，形成<电影id，电影名称>的键值对
    def LoadData(self):
        print "正在载入数据"
        try:
            f=open(self.user_file,"r")
            prefer={}
            # 读取掉第一行的列名称
            line=f.readline()
            line=f.readline()
            while line:
                line=f.readline()
                items=line.split(",")
                if len(items) is 4:
                    if prefer.has_key(items[0]):
                        val=prefer.get(items[0])
                        val.update({items[1]:items[2]})
                        prefer.update({items[0]:val})
                    else:
                        prefer.update({items[0]:{items[1]:items[2]}})
        finally:
            f.close()

        try:
            f=open(self.movie_file,"r")
            movies={}
            # 读取第一行的列名称
            line = f.readline()
            line = f.readline()
            while line:
                line = f.readline()
                items = line.split(",")
                if len(items) is 3:
                    movies.update({items[0]:items[1]})
        finally:
            f.close()
        print "载入数据完成！"
        return prefer,movies

    #对每部电影形成<电影id，set(users)>的键值对,这样在之后计算相似度时，只需搜索有共同喜好的用户，再进行计算
    def MovieUsersPair(self):
        movie_user_pair={}
        for userid,prefer_dict in self.prefer.iteritems():
            for movie_id,rate in prefer_dict.iteritems():
                if movie_user_pair.has_key(movie_id):
                    user_set=movie_user_pair.get(movie_id)
                    user_set.add(userid)
                    movie_user_pair.update({movie_id:user_set})
                else:
                    user_set=set()
                    user_set.add(userid)
                    movie_user_pair.update({movie_id:user_set})
        return movie_user_pair

    # 寻找与目标用户有交集的用户
    def FindUnionUsers(self, object_user):
        union_users={}
        for movie_id,user_list in self.unions.iteritems():
            if object_user in user_list:
                for user in user_list:
                    if user!=object_user:
                        union_users[user]=1
        return union_users

    #计算目标用户相关用户的相关性，并进行排序匹配
    def CalMatch(self):
        object_user='1'
        users=self.FindUnionUsers(object_user)
        for user in users:
            self.SimPearson(object_user,user)

    #计算两个用户的皮尔逊相关性系数
    def SimPearson(self,user_1,user_2):
        sim={}

        #查找双方都评价过的项
        for item in self.prefer[user_1]:
            if item in self.prefer[user_2]:
                sim[item]=1

        n=len(sim)

        if n is 0:
            print "zero error"
            return

        #求两个向量的偏好之和
        sum1=sum((float)(self.prefer[user_1][item]) for item in sim)
        sum2=sum((float)(self.prefer[user_2][item]) for item in sim)

        #求两个向量的各项的平方和
        sumSq1=sum(pow((float)(self.prefer[user_1][item]),2) for item in sim)
        sumSq2=sum(pow((float)(self.prefer[user_2][item]),2) for item in sim)

        #求两个向量乘积之和
        sumMulti=sum(((float)(self.prefer[user_1][item]))*((float)(self.prefer[user_2][item])) for item in sim)

        num1=sumMulti-sum1*sum2/n
        num2=sqrt(sumSq1-pow(sum1,2)/n)*sqrt(sumSq2-pow(sum2,2)/n)

        if num2!=0:
            print "similarity",abs(num1/num2)


















u_file="D:/GitHub/machine_learning/UserSCF/data/ratings.csv"
m_file="D:/GitHub/machine_learning/UserSCF/data/movies.csv"
uc=UserCF(u_file,m_file)
uc
