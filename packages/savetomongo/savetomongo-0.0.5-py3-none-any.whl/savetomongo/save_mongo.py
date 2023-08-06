class save_mongo:
    # Define order to retrieve options from ClientOptions for __repr__.
    # No host/port; these are retrieved from TopologySettings.
    def __init__(self,data,collec,plex):
        """data为字典嵌套列表类型或者列表嵌套字典类型的数据，\n
        eg.
        data:
            sam={'a':[1,2,3,4],'b':[3,4,5,6]}
          or
            sam=[{'a':1,'b':3},{'a':2,'b':4}]


        两种类型：一、字典类型 二、列表类型
           collec为需要传入的mongodb数据库下的集合名（collection 或 tables）的变量  \n
             client = pymongo.MongoClient(host='127.0.0.1', port=27017)
             db = client['douyu']
             p = db['do']
             p即为collec
           plex为需要查重的键名，如若不查重，请赋值为False

           \n

            """
        self.data=data
        self.collec=collec
        self.plex=plex

        if data is None:
            raise TypeError("data must be an dict")
        if isinstance(self.data,list):
            self.save()
        if isinstance(self.data,dict):
            self.save_of_dict()

# collection
    def save(self):

        p=self.collec
        if not self.plex:
            result = p.insert(self.data)
        else:
            for i in range(len(self.data)):
                # 通过主键id查重 不存在插入 存在跳过
                try:
                    # 查重处理
                    key = p.find_one({"{}".format(self.plex): str(self.data[i]['{}'.format(self.plex)])}, {'{}'.format(self.plex): 1})
                    if key == None:
                        # print(key == None)
                        pass

                    # 是否有重复数据
                    repetition = key
                    # 重复
                    if repetition:
                        # print('跳过')
                        pass
                    else:
                        result = p.insert_one(self.data[i])
                        print(self.data[i])

                except Exception as error:
                    # 出现错误时打印错误日志
                    print(error, "jieshuyichang")

    # 查重,若存在数据则更新，不存在则插入
    def save_of_dict(self):
        k=[]
        p = self.collec
        for count in range(len(list(self.data.values())[0])):
            s = {}

            for key, values in self.data.items():
                s[key] = values[count]
            k.append(s)
        # print(k)
        if not self.plex:

            # for i in range(len(k)):
            #     print(k[i])
            #     p.insert(k)
            p.insert(k)
        else:
            # print(k)
            for i in range(len(k)):
                 p.update_one({'{}'.format(self.plex): k[i][self.plex]}, {'$set': k[i]},True)


