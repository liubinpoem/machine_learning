#coding=utf-8

#利用movielens数据进行推荐
from math import sqrt


class UserCF(object):
    def __init__(self,u_file,m_file):
        self.user_file=u_file;
        self.movie_file=m_file;
        self.prefer,self.movies=self.LoadData()
        self.unions=self.MovieUsersPair()

    #首先读取用户评分文件，形成<用户id，<电影id,评分>>的键值对
    #再读取电影文件，形成<电影id，电影名称>的键值对
    def LoadData(self):
        print "正在载入用户评分数据!\n------------------"
        try:
            f=open(self.user_file,"r")
            prefer={}
            # 读取掉第一行的列名称
            line=f.readline()
            line = f.readline()
            while line:
                items=line.split(",")
                if prefer.has_key(items[0]):
                    val=prefer.get(items[0])
                    val.update({items[1]:items[2]})
                    prefer.update({items[0]:val})
                else:
                    prefer.update({items[0]:{items[1]:items[2]}})
                line = f.readline()
        finally:
            pass

        try:
            print "正在载入产品数据!\n------------------"
            f=open(self.movie_file,"r")
            movies={}
            # 读取第一行的列名称
            line = f.readline()
            line = f.readline()
            while line:
                items = line.split(",")
                movies.update({items[0]:items[1]})
                line = f.readline()
        finally:
            pass

        print "载入数据完成!\n------------------"
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

    #计算目标用户相关用户的相关性，并进行排序,将得到的最相关的K个用户返回
    def CalMatch(self,object_user,K=10):
        similar_users={}
        users=self.FindUnionUsers(object_user)
        for user in users:
            sim=self.SimPearson(object_user,user)
            if sim!=2:
                similar_users.update({user:sim})
        #排序相关性的结果
        similar_users=sorted(similar_users.iteritems(),key=lambda d:d[1],reverse=True)
        if len(similar_users)>K:
            similar_users=similar_users[0:K]

        #for user,similarity in similar_users:
        #   print user,similarity
        return similar_users

    #计算两个用户的皮尔逊相关性系数
    def SimPearson(self,user_1,user_2):
        sim={}

        #查找双方都评价过的,或者购买过的项
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
            #print "similarity:",user_1+"\t"+user_2+"\t",abs(num1/num2)
            return abs(num1/num2)
        else:
            return 2

    #计算推荐度,从相似用户中,推荐该用户没有评分过的项
    def CalPopularity(self,object_user,K=20):
        items={}
        similar_users=self.CalMatch(object_user)
        #将所有相关用户评价过的商品列入字典
        for user,rate in similar_users:
            similar_user_items=self.prefer[user]
            for item in similar_user_items:
                if not self.prefer[object_user].has_key(item):
                    items[item]=0

        #计算目标用户对未打过分的项的喜欢的可能性
        for item in items:
            for user,rate in similar_users:
                if self.prefer[user].has_key(item):
                    items[item]=items[item]+rate*(float)(self.prefer[user][item])
        items=sorted(items.iteritems(),key=lambda d:d[1],reverse=True)

        #输出推荐
        if len(items)>K:
            recommend_items=items[0:K]
        else:
            recommend_items=items
        #for movieid,popularity in recommend_items:
        #    print movieid+"\t",popularity,"\t",self.movies[movieid]
        return recommend_items

    #
    def Recommend(self,object_users):
        print "正在计算推荐产品!\n------------------"
        recommend_list={}
        for object_user in object_users:
            recommend_items=self.CalPopularity(object_user)
            list={}
            for movie_id,popularity in recommend_items:
                list.update({movie_id:self.movies[movie_id]})
            recommend_list.update({object_user:list})

        recommend_list=sorted(recommend_list.iteritems(),key=lambda d:d[0],reverse=False)
        for user,movies in recommend_list:
            print "\n用户",user,"的推荐列表:"
            for item in movies.iteritems():
                print "\t",item[0],item[1]

        print "\n产品推荐完成!"

    #计算推荐列表的准确度
    def CalAccuracy(self,user,recommend_list):
        sum=0

#u_file="D:/GitHub/machine_learning/UsersCF/data/ratings.csv"
u_file="../UsersCF/data/ratings.csv"
#m_file="D:/GitHub/machine_learning/UsersCF/data/movies.csv"
m_file="../UsersCF/data/movies.csv"
uc=UserCF(u_file,m_file)
uc.Recommend(["100"])