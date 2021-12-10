#coding=utf-8

from alibabacloud_imageseg20191230.client import Client as imageseg20191230Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_imageseg20191230 import models as imageseg_20191230_models
import oss2
import os
import requests
import json
import time
from itertools import islice
import urllib.request
from aliyunsdkcore.client import AcsClient
from aliyunsdkimageseg.request.v20191230.SegmentHDBodyRequest import SegmentHDBodyRequest
# from aliyunsdkimageseg.request.v20191230.RefineMaskRequest import RefineMaskRequest

class Sample:
    def __init__(self):
        pass
    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> imageseg20191230Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'imageseg.cn-shanghai.aliyuncs.com'
        return imageseg20191230Client(config)


auth = oss2.Auth('****', '*********')
#client = Sample.create_client('LTAI5t99ssG7EPSeiVn6scJB', 'W2Yr6pLQ3cruVaiJm2j9a0WHYIaPdd')
client = AcsClient('****', '****', 'cn-shanghai')
bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com',
                     '1803151818-sum')
image_names = []
url_list = []
file = open('local2net.txt', 'w', encoding='utf-8')
count = 0
MaskPath = 'E:\\MyDate_Deeplearning\\1803151818_sum\\'
finished = os.listdir(MaskPath)
print(len(finished))
for imgname in islice(oss2.ObjectIterator(bucket), 10000):
    img = imgname.key
    checkname = img[0:-4] + ".png"
    print(checkname)
    if checkname not in finished:
        image_names.append(img)
        print("cur image name: ", img)
        url = bucket.sign_url('GET', img, 60)
        url_list.append(url)
        file.writelines(img + " " + url + '\n')

        # segment_hdsky_request = imageseg_20191230_models.SegmentHDSkyRequest(
        #     image_url=url
        # )

        request = SegmentHDBodyRequest()
        request.set_ImageURL(url)
        response = client.do_action_with_exception(request)
        print(type(response))
        dict_res = eval(str(response, 'utf-8'))
        print(dict_res['Data']['ImageURL'])
        mask_url = dict_res['Data']['ImageURL']
        #print(response.body.data.image_url)
        urllib.request.urlretrieve(
            mask_url,
            MaskPath + imgname.key[:-4] + ".png")
        file.writelines(img + " " + mask_url + '\n')
        count = count + 1
        print("count: ", count)
# E:\Nubia\sky_extend\building_optimization
file.close()
