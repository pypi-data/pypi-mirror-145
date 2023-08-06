# -*- coding: utf-8 -*-

'''
2021.1.10 15：56 实现redis作为网络池
概要：通过发布者这样的实现。

后期如何使用？
    1：安装redis  pip install aioredis==1.3.1 要安装这个版本的异步redis
    2：
        （1）继承这个类，
        （2）然后将url通过_addurl 添加进来
        （3）写一个接受返回结果的async函数
        （4）启动crawl_main方法
    3：可以更改参数
        指定redis_key/redis_db/_max_workers/_poptype = 'FIFO'  ##先进先出


案例：
from my_utils.redis_urlpool import RedisUrlPool
import asyncio

class GetFast(RedisUrlPool):
    def __init__(self):
        super(GetFast,self).__init__()
        self._redisKey = "BaiduList"   ##指定网络池的key
        self._max_workers = 2          ##开始多少个任务

    async def load_url(self):
        """加载url"""
        url_item = {"url":"https://www.baidu.com","backfunc":"parse_baidu"}
        await self._addurl(url_item)


    async def parse_baidu(self,r):
        """解析对应的回调函数"""
        print(r.keys())
        print("收到html长度：",len(r['html']))

    async def run(self):
        await self.load_url()     ##加载url
        await self.crawl_main()   ##启动爬虫程序


if __name__ == '__main__':
    baidu = GetFast()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(baidu.run())

'''

import traceback
import platform
import aiohttp
import aioredis
import asyncio
import cchardet
import time, json
import logging

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # 加上这一行


class RedisUrlPool():
    def __init__(self,host, db=0, password="", port=6379):
        # url_item只能支持这些key
        __url_keys = ["url", 'count', "backfunc", "method", "info", "proxy", "data", "headers", "timeout", "debug", "binary", "oargs", ]
        self.__url_keys = set(__url_keys)
        self.__host = host
        self.__db = db
        self.__password = password
        self.__port = port
        self._max_workers = 8  ##允许创建多少个并发的任务
        self._now_workers = 0  ##现在剩余的并发任务
        ##当这个url的count请求次数3次，将不再下载url，  # 在返回的r对象绑定一个is_stop=1属性，需要自己去处理这个属性
        self._DropUrlCount = 3
        ##可以指定网络池的在redis中的key
        self._redisKey = 'testli'
        self._poptype = 'FIFO'  ##定义取网络请求池的 规则先进先出【】
        self._url_retry = True
        self.__init_logger()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._redisConnect())

    def __init_logger(self) -> logging:
        """
        :description: 创建logging手柄用于打印信息
        """
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

    async def _redisConnect(self):
        """
        :description: 创建链接池
        :param: minsize 链接池的最小数量
        :param: maxsize 链接池的最大数量
        :param: encoding 指定返回的response decoding.
        :param: create_connection_timeout：链接超时定为4秒
        """
        try:
            self.redis_pool = await aioredis.create_pool('redis://{0}:{1}'.format(self.__host, self.__port), minsize=2, maxsize=6,
                                                         db=self.__db, encoding='utf8', create_connection_timeout=4, password=self.__password)
        except Exception as e:
            logging.error("创建redis池失败，退出程序")
            raise

    async def _addurl(self, item):
        '''添加url到redis中去'''
        item_key = set(item.keys())
        ##以下的几个cookie/redirected_url/status/html是返回的结果，如果重新进入网络池，先删除
        item.pop('cookie') if "cookie" in item_key else None
        item.pop('redirected_url') if "redirected_url" in item_key else None
        item.pop('status') if "status" in item_key else None
        item.pop('html') if "html" in item_key else None
        nullset = self.__url_keys - set(item.keys())

        # 传入的url_item是url_key的子集
        if item_key.issubset(self.__url_keys) or (not nullset):
            with await self.redis_pool as conn:  # low-level redis connection
                value = json.dumps(item, ensure_ascii=False)
                await conn.execute('rpush', self._redisKey, value)
                conn.close()
        else:
            print('添加的url_item，不符合定义')
            exit(886)

    async def _popurl(self, popcount=1):
        """
        :description: 一次性取多少条请求出来
        :param: popcount：pop出来的数量
        """
        popurls = []
        for i in range(popcount):
            with await self.redis_pool as conn:  # low-level redis connection
                ##判断是先进先出，还是先进后出
                pop_type = "rpop" if self._poptype == 'FIFO' else "lpop"
                url_item = await conn.execute(pop_type, self._redisKey, encoding='utf8')
                if url_item is None:
                    break
                url_item = json.loads(url_item)
                popurls.append(url_item)
                conn.close()
        return popurls

    @property
    async def url_count(self):
        '''输出url一共在数据库有多少个'''
        with await self.redis_pool as conn:
            result = await conn.execute('llen', self._redisKey)
            return result

    def pre_crawal_patch(self, url_item):
        '''封装url_item'''
        _headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        new_url_item = {}
        new_url_item['headers'] = url_item.get('headers') if url_item.get('headers') else _headers
        new_url_item['info'] = url_item.get('info') if url_item.get('info') else ""
        new_url_item['proxy'] = url_item.get('proxy') if url_item.get('proxy') else ""
        new_url_item['timeout'] = url_item.get('timeout') if url_item.get('timeout') else 10
        new_url_item['url'] = url_item.get('url') if url_item.get('url') else ""
        new_url_item['oargs'] = url_item.get('oargs') if url_item.get('oargs') else ""
        new_url_item['data'] = url_item.get('data') if url_item.get('data') else ""
        new_url_item['method'] = url_item.get('method') if url_item.get('method') else "GET"
        new_url_item['count'] = url_item.get('count') if url_item.get('count') else 0
        new_url_item['binary'] = url_item.get('binary') if url_item.get('binary') else False
        new_url_item['debug'] = url_item.get('debug') if url_item.get('debug') else False
        new_url_item['backfunc'] = url_item.get('backfunc') if url_item.get('backfunc') else ""
        return new_url_item

    async def crawl_patch(self, url_item):
        '''页面下载'''
        print(url_item.get('info')) if url_item.get('info') else None
        #############获取url_item的参数进行组装##############
        nui = self.pre_crawal_patch(url_item=url_item)
        nui['redirected_url'] = url_item['url']
        if nui.get('count', 0) == self._DropUrlCount:
            print("丢弃这个url")
            return None

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method=nui['method'], url=nui['url'], ssl=False, proxy=nui['proxy'],
                                           data=nui['data'], timeout=nui['timeout'], headers=nui['headers']) as rep:
                    status = rep.status
                    if status == 200:
                        if nui['binary']:
                            nui['html'] = await rep.content.read()
                        else:
                            content = await rep.content.read()
                            encoding = cchardet.detect(content)['encoding']
                            nui['html'] = content.decode(encoding)
                        nui['status'] = status
                        nui['redirected_url'] = rep.url
                        nui['cookie'] = rep.cookies
                    else:
                        if nui['binary']:
                            nui['html'] = b''
                        else:
                            nui['html'] = ''
                        nui['status'] = 0
                        nui['redirected_url'] = rep.url
                        nui['cookie'] = ''
                        nui['count'] = nui.get('count', 0) + 1
                    ##返回封装的返回报文
                    return nui
            except Exception as e:
                if nui.get('debug'):
                    traceback.print_exc()

                if nui['binary']:
                    nui['html'] = b''
                else:
                    nui['html'] = ''
                nui['status'] = 0
                nui['redirected_url'] = nui['url']
                nui['cookie'] = ''
                nui['count'] = nui.get('count', 0) + 1
                return nui

    async def crawl_process(self, url_item):
        rep_r = await self.crawl_patch(url_item)
        func_name = url_item.get('backfunc')
        if rep_r.get('html'):
            # 反射执行回调函数
            if func_name:
                func = getattr(self, func_name)
                try:
                    await func(rep_r)
                except Exception as e:
                    print("当前的url_item:", rep_r)
                    exit('回调函数出错,请检查')
        else:
            ##如果不存在则说明本次请求失败,判断是否要重新放入网络池
            if self._url_retry:
                await self._addurl(rep_r)
            self._now_workers -= 1
            return
        self._now_workers -= 1

    async def crawl_main(self):
        '''启动crawl_main之前，要确保网络池当中url存在'''
        url_count = await self.url_count
        print("一共要处理：%s" % url_count, '个URL')
        while 1:
            if url_count == 0:
                print("网络池没有要下载的url，退出循环")
                self.redis_pool.close()
                break
            pop_count = self._max_workers - self._now_workers
            popurls = await self._popurl(popcount=pop_count)
            tasks = []
            for url_item in popurls:
                corotinue = asyncio.create_task(self.crawl_process(url_item))
                tasks.append(corotinue)
                self._now_workers += 1
            else:
                await asyncio.wait(tasks)
            url_count = await self.url_count
            if url_count == 0:
                print("网络池没有要下载的url，退出循环")
                self.redis_pool.close()
                await self.redis_pool.wait_closed()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    obj = RedisUrlPool(port=6381, password="abcde")
    url_item = {"url": "www.baidu.com"}

    obj._addurl(url_item)

    # url_item = {"url":"www.baidu.com"}
    # popurls = loop.run_until_complete(obj.url_count)
    # print(popurls)

    # result = obj.table.find()
    # for i in result:
    #     print(i)
    # item_url = {"url":'https://www.baidu.com'}
    # obj.insert_pool(item_url)
    # print(obj.count_pool)
    # obj.pop_pool()