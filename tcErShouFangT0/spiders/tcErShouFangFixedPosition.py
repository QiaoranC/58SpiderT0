# -*- coding: utf-8 -*-
import scrapy
import re
# from redis import Redis
import redis
from scrapy_redis.spiders import RedisSpider

# error系列
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from scrapy.loader import ItemLoader
from scrapy.http import Request
from urllib import parse
import logging

from tcErShouFangT0.items import Tcershoufangt0Item

#log文件===========================================================================
import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='../logFixedPosition.txt',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)
#=================================================================================
logger = logging.getLogger()
r = redis.StrictRedis(host='106.75.166.130', port=6379, db=0, password='v5e7r8o4n4i9c0a9')

class TcershoufangSpider(RedisSpider):
    name = 'tcErShouFangFixedURLs'
    # allowed_domains = ['58.com']
    # start_urls = ['http://58.com/']
    # a = Redis()
    # a.delete("tcErShouFangStart_URL")
    # a.lpush("tcErShouFangStart_URL", 'http://la.58.com')
    # start_urls = ['http://la.58.com']
    redis_key = 'tcErShouFang:Start_URL'
    # r = redis.StrictRedis(host='106.75.166.130', port=6379, db=0, password='v5e7r8o4n4i9c0a9')
    
    
    def parse(self, response):
        cityList = {
          "安徽":{"合肥":"hf|837","芜湖":"wuhu|2045","蚌埠":"bengbu|3470","阜阳":"fy|2325","淮南":"hn|2319","安庆":"anqing|3251","宿州":"suzhou|3359","六安":"la|2328","淮北":"huaibei|9357","滁州":"chuzhou|10266","马鞍山":"mas|2039","铜陵":"tongling|10285","宣城":"xuancheng|5633","亳州":"bozhou|2329","黄山":"huangshan|2323","池州":"chizhou|10260","巢湖":"ch|10229","和县":"hexian|10892","霍邱":"hq|11226","桐城":"tongcheng|11296","宁国":"ningguo|5645","天长":"tianchang|10273"},
          "福建":{"福州":"fz|304","厦门":"xm|606","泉州":"qz|291","莆田":"pt|2429","漳州":"zhangzhou|710","宁德":"nd|7951","三明":"sm|2048","南平":"np|10291","龙岩":"ly|6752","武夷山":"wuyishan|10761","石狮":"shishi|296","晋江":"jinjiangshi|297","南安":"nananshi|293","龙海":"longhai|713"},
          "广东":{"深圳":"sz|4","广州":"gz|3","东莞":"dg|413","佛山":"fs|222","中山":"zs|771","珠海":"zh|910","惠州":"huizhou|722","江门":"jm|629","汕头":"st|783","湛江":"zhanjiang|791","肇庆":"zq|901","茂名":"mm|679","揭阳":"jy|927","梅州":"mz|9389","清远":"qingyuan|7303","阳江":"yj|2284","韶关":"sg|2192","河源":"heyuan|10467","云浮":"yf|10485","汕尾":"sw|9449","潮州":"chaozhou|10461","台山":"taishan|11263","阳春":"yangchun|8566","顺德":"sd|8716","惠东":"huidong|725","博罗":"boluo|726","海丰":"haifengxian|9444"},
          "广西":{"南宁":"nn|845","柳州":"liuzhou|7133","桂林":"gl|1039","玉林":"yulin|2337","梧州":"wuzhou|2046","北海":"bh|10536","贵港":"gg|6770","钦州":"qinzhou|2335","百色":"baise|10513","河池":"hc|2340","来宾":"lb|10552","贺州":"hezhou|10549","防城港":"fcg|10539","崇左":"chongzuo|10524"},
          "贵州":{"贵阳":"gy|2015","遵义":"zunyi|7620","黔东南":"qdn|9363","黔南":"qn|10492","六盘水":"lps|10506","毕节":"bijie|10564","铜仁":"tr|10417","安顺":"anshun|7468","黔西南":"qxn|10434","仁怀":"renhuaishi|7628"},
          "甘肃":{"兰州":"lz|952","天水":"tianshui|8601","白银":"by|10304","庆阳":"qingyang|10475","平凉":"pl|7154","酒泉":"jq|10387","张掖":"zhangye|10454","武威":"wuwei|10448","定西":"dx|10322","金昌":"jinchang|7428","陇南":"ln|10415","临夏":"linxia|7112","嘉峪关":"jyg|10362","甘南":"gn|10343"},
          "海南":{"海口":"haikou|2053","三亚":"sanya|2422","五指山":"wzs|9952","三沙":"sansha|13722","琼海":"qionghai|10136","文昌":"wenchang|9984","万宁":"wanning|10022","屯昌":"tunchang|10044","琼中":"qiongzhong|10064","陵水":"lingshui|10184","东方":"df|10250","定安":"da|10303","澄迈":"cm|10331","保亭":"baoting|10367","白沙":"baish|10380","儋州":"danzhou|10394"},
          "河南":{"郑州":"zz|342","洛阳":"luoyang|556","新乡":"xx|1016","南阳":"ny|592","许昌":"xc|977","平顶山":"pds|1005","安阳":"ay|1096","焦作":"jiaozuo|3266","商丘":"sq|1029","开封":"kaifeng|2342","濮阳":"puyang|2346","周口":"zk|933","信阳":"xy|8694","驻马店":"zmd|1067","漯河":"luohe|2347","三门峡":"smx|9317","鹤壁":"hb|2344","济源":"jiyuan|9918","明港":"mg|8541","鄢陵":"yanling|9123","禹州":"yuzhou|979","长葛":"changge|9344","灵宝":"lingbaoshi|9307","杞县":"qixianqu|7389","汝州":"ruzhou|1010","项城":"xiangchengshi|935","偃师":"yanshiqu|7121","长垣":"changyuan|5936"},
          "黑龙江":{"哈尔滨":"hrb|202","大庆":"dq|375","齐齐哈尔":"qqhr|5853","牡丹江":"mdj|3489","绥化":"suihua|6718","佳木斯":"jms|6776","鸡西":"jixi|7289","双鸭山":"sys|9837","鹤岗":"hegang|9061","黑河":"heihe|9862","伊春":"yich|9773","七台河":"qth|9848","大兴安岭":"dxal|9878"},
          "湖北":{"武汉":"wh|158","宜昌":"yc|858","襄阳":"xf|891","荆州":"jingzhou|3479","十堰":"shiyan|2032","黄石":"hshi|1734","孝感":"xiaogan|3434","黄冈":"hg|2299","恩施":"es|2302","荆门":"jingmen|2296","咸宁":"xianning|9617","鄂州":"ez|9709","随州":"suizhou|9656","潜江":"qianjiang|9669","天门":"tm|9517","仙桃":"xiantao|9736","神农架":"snj|9605","宜都":"yidou|864","汉川":"hanchuan|3439","枣阳":"zaoyang|896"},
          "湖南":{"长沙":"cs|414","株洲":"zhuzhou|1086","益阳":"yiyang|10198","常德":"changde|872","衡阳":"hy|914","湘潭":"xiangtan|2047","岳阳":"yy|821","郴州":"chenzhou|5695","邵阳":"shaoyang|2303","怀化":"hh|5756","永州":"yongzhou|2307","娄底":"ld|9481","湘西":"xiangxi|10219","张家界":"zjj|6788","醴陵":"liling|1091"},
          "河北":{"石家庄":"sjz|241","保定":"bd|424","唐山":"ts|276","廊坊":"lf|772","邯郸":"hd|572","秦皇岛":"qhd|1078","沧州":"cangzhou|652","邢台":"xt|751","衡水":"hs|993","张家口":"zjk|3328","承德":"chengde|6760","定州":"dingzhou|8398","馆陶":"gt|8706","张北":"zhangbei|11201","赵县":"zx|9048","正定":"zd|3198","迁安市":"qianan|284","任丘":"renqiu|656","三河":"sanhe|776","武安":"wuan|577","雄安新区":"xionganxinqu|111234","燕郊":"lfyanjiao|12730","涿州":"zhuozhou|428"},
          "江苏":{"苏州":"su|5","南京":"nj|172","无锡":"wx|93","常州":"cz|463","徐州":"xz|471","南通":"nt|394","扬州":"yz|637","盐城":"yancheng|613","淮安":"ha|968","连云港":"lyg|2049","泰州":"taizhou|693","宿迁":"suqian|2350","镇江":"zj|645","沭阳":"shuyang|5772","大丰":"dafeng|11279","如皋":"rugao|397","启东":"qidong|400","溧阳":"liyang|469","海门":"haimen|399","东海":"donghai|2147","扬中":"yangzhong|649","兴化":"xinghuashi|699","新沂":"xinyishi|478","泰兴":"taixing|696","如东":"rudong|402","邳州":"pizhou|477","沛县":"xzpeixian|11349","靖江":"jingjiang|698","建湖":"jianhu|618","海安":"haian|401","东台":"dongtai|615","丹阳":"danyang|648","宝应县":"baoyingx|14451","灌南":"guannan|2150","灌云":"guanyun|2148","姜堰":"jiangyan|697","金坛":"jintan|468","昆山":"szkunshan|16","泗洪":"sihong|5958","泗阳":"siyang|5959"},
          "江西":{"南昌":"nc|669","赣州":"ganzhou|2363","九江":"jj|2247","宜春":"yichun|5709","吉安":"ja|2364","上饶":"sr|10120","萍乡":"px|2248","抚州":"fuzhou|10134","景德镇":"jdz|2360","新余":"xinyu|10115","鹰潭":"yingtan|3209","永新":"yxx|11077","乐平":"lepingshi|9048"},
          "吉林":{"长春":"cc|319","吉林":"jl|700","四平":"sp|10171","延边":"yanbian|3184","松原":"songyuan|2315","白城":"bc|5918","通化":"th|10159","白山":"baishan|10179","辽源":"liaoyuan|2501","公主岭":"gongzhuling|10171"},
          "辽宁":{"沈阳":"sy|188","大连":"dl|147","鞍山":"as|523","锦州":"jinzhou|2354","抚顺":"fushun|5722","营口":"yk|5898","盘锦":"pj|2041","朝阳":"cy|10106","丹东":"dandong|3445","辽阳":"liaoyang|2038","本溪":"benxi|5845","葫芦岛":"hld|10088","铁岭":"tl|6729","阜新":"fx|10097","庄河":"pld|3306","瓦房店":"wfd|3279"},
          "宁夏":{"银川":"yinchuan|2054","吴忠":"wuzhong|9962","石嘴山":"szs|9971","中卫":"zw|9951","固原":"guyuan|2421"},
          "内蒙古":{"呼和浩特":"hu|811","包头":"bt|801","赤峰":"chifeng|6700","鄂尔多斯":"erds|2037","通辽":"tongliao|10015","呼伦贝尔":"hlbe|10039","巴彦淖尔市":"bycem|10070","乌兰察布":"wlcb|9993","锡林郭勒":"xl|2408","兴安盟":"xam|9976","乌海":"wuhai|2404","阿拉善盟":"alsm|10083","海拉尔":"hlr|2043"},
          "青海":{"西宁":"xn|2052","海西":"hx|9902","海北":"haibei|9917","果洛":"guoluo|9936","海东":"haidong|9909","黄南":"huangnan|9896","玉树":"ys|9888","海南":"hainan|10574"},
          "山东":{"青岛":"qd|122","济南":"jn|265","烟台":"yt|228","潍坊":"wf|362","临沂":"linyi|505","淄博":"zb|385","济宁":"jining|450","泰安":"ta|686","聊城":"lc|882","威海":"weihai|518","枣庄":"zaozhuang|961","德州":"dz|728","日照":"rizhao|3177","东营":"dy|623","菏泽":"heze|5632","滨州":"bz|944","莱芜":"lw|2292","章丘":"zhangqiu|8680","垦利":"kl|11313","诸城":"zc|9146","寿光":"shouguang|369","龙口":"longkou|233","曹县":"caoxian|5638","单县":"shanxian|5636","肥城":"feicheng|690","高密":"gaomi|371","广饶":"guangrao|627","桓台":"huantaixian|7335","莒县":"juxian|3180","莱州":"laizhou|235","蓬莱":"penglai|237","青州":"qingzhou|367","荣成":"rongcheng|522","乳山":"rushan|520","滕州":"tengzhou|967","新泰":"xintai|689","招远":"zhaoyuan|3325","邹城":"zoucheng|455","邹平":"zouping|946"},
          "山西":{"太原":"ty|740","临汾":"linfen|5669","大同":"dt|6964","运城":"yuncheng|5653","晋中":"jz|8854","长治":"changzhi|6921","晋城":"jincheng|3350","阳泉":"yq|8760","吕梁":"lvliang|3222","忻州":"xinzhou|3453","朔州":"shuozhou|9871","临猗":"linyixian|9193","清徐":"qingxu|10908"},
          "陕西":{"西安":"xa|483","咸阳":"xianyang|7453","宝鸡":"baoji|2044","渭南":"wn|5733","汉中":"hanzhong|3163","榆林":"yl|5942","延安":"yanan|8973","安康":"ankang|3157","商洛":"sl|9854","铜川":"tc|9832","神木":"shenmu|5944"},
          "四川":{"成都":"cd|102","绵阳":"mianyang|1057","德阳":"deyang|2373","南充":"nanchong|2378","宜宾":"yb|2380","自贡":"zg|6745","乐山":"ls|3237","泸州":"luzhou|2372","达州":"dazhou|9799","内江":"scnj|5928","遂宁":"suining|9688","攀枝花":"panzhihua|2371","眉山":"ms|9704","广安":"ga|2381","资阳":"zy|6803","凉山":"liangshan|9717","广元":"guangyuan|9749","雅安":"ya|9687","巴中":"bazhong|9811","阿坝":"ab|9817","甘孜":"ganzi|9764","安岳":"anyuexian|6806","广汉":"guanghanshi|8719","简阳":"jianyangshi|6805","仁寿":"renshouxian|9706"},
          "新疆":{"乌鲁木齐":"xj|984","昌吉":"changji|8582","巴音郭楞":"bygl|9530","伊犁":"yili|9472","阿克苏":"aks|9499","喀什":"ks|9326","哈密":"hami|7452","克拉玛依":"klmy|2042","博尔塔拉":"betl|9529","吐鲁番":"tlf|9475","和田":"ht|9489","石河子":"shz|9551","克孜勒苏":"kzls|9519","阿拉尔":"ale|9539","五家渠":"wjq|9562","图木舒克":"tmsk|9559","库尔勒":"kel|7168","阿勒泰":"alt|18837","塔城":"tac|18845"},
          "西藏":{"拉萨":"lasa|2055","日喀则":"rkz|9615","山南":"sn|9576","林芝":"linzhi|9646","昌都":"changdu|9648","那曲":"nq|9618","阿里":"al|9678","日土":"rituxian|9682","改则":"gaizexian|9684"},
          "云南":{"昆明":"km|541","曲靖":"qj|2389","大理":"dali|2398","红河":"honghe|2394","玉溪":"yx|2040","丽江":"lj|2392","文山":"ws|2395","楚雄":"cx|2393","西双版纳":"bn|2397","昭通":"zt|9409","德宏":"dh|9437","普洱":"pe|9444","保山":"bs|2390","临沧":"lincang|9422","迪庆":"diqing|9432","怒江":"nujiang|9462"},
          "浙江":{"杭州":"hz|79","宁波":"nb|135","温州":"wz|330","金华":"jh|531","嘉兴":"jx|497","台州":"tz|403","绍兴":"sx|355","湖州":"huzhou|831","丽水":"lishui|7921","衢州":"quzhou|6793","舟山":"zhoushan|8481","乐清":"yueqingcity|13950","瑞安":"ruiancity|13951","义乌":"yiwu|12291","余姚":"yuyao|5333","诸暨":"zhuji|357","象山":"xiangshanxian|6738","温岭":"wenling|408","桐乡":"tongxiang|502","慈溪":"cixi|5334","长兴":"changxing|834","嘉善":"jiashanx|14357","海宁":"haining|500","德清":"deqing|835","东阳":"dongyang|536","安吉":"anji|836","苍南":"cangnanxian|7579","临海":"linhai|407","永康":"yongkang|537","玉环":"yuhuan|409"},
          "其他":{"香港":"hk|2050","澳门":"am|9399","台湾":"tw|2051","北京":"bj|8728","上海":"sh|2258","天津":"tj|2258","重庆":"cq|2258"}
                } 
                       
        provinceList = {"安徽","福建","广东","广西","贵州","甘肃","海南","河南","黑龙江","湖北","湖南","河北","江苏","江西","吉林","辽宁","宁夏","内蒙古","青海","山东","山西","陕西","四川","新疆","西藏","云南","浙江","其他"}

        for provinceName in provinceList:
            for cityName in cityList[provinceName]: #http://zw.58.com/shangpu/
                #个人出租 二手房 求租 短租
                cityAddressC = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/chuzu/"
                cityAddressQ = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/qiuzu/"
                cityAddressD = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/duanzu/"
                cityAddressE = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/ershoufang/"
                
                #写字楼 
                cityAddressX0 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/zhaozu/pve_1092_0/"
                cityAddressX1 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/zhaozu/pve_1092_1/"
                cityAddressX2 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/zhaozu/pve_1092_2/"
                cityAddressX3 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/zhaozu/pve_1092_3/"
                
                #商铺 
                cityAddressS0 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/shangpucz/"
                cityAddressS1 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/shangpuqz/"
                cityAddressS2 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/shangpucs/"
                cityAddressS3 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/shangpuqg/"
                cityAddressS4 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/shengyizr/"
                
                #厂房 
                cityAddressF0 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/changfang/b1/"
                cityAddressF1 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/changfang/b2/"
                cityAddressF2 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/changfang/b3/"
                cityAddressF3 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/changfang/b4/"
                cityAddressF4 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/changfang/b5/"
                
                #车位 
                cityAddressK0 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cheku/b1/"
                cityAddressK1 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cheku/b2/"
                cityAddressK2 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cheku/b3/"
                cityAddressK3 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cheku/b4/"
                cityAddressK4 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cheku/b5/"

                #仓库 
                cityAddressH0 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cangkucf/b1/"
                cityAddressH1 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cangkucf/b2/"
                cityAddressH2 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cangkucf/b3/"
                cityAddressH3 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cangkucf/b4/"
                cityAddressH4 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/cangkucf/b5/"
                                
                #土地 
                cityAddressT0 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/tudi/b1/"
                cityAddressT1 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/tudi/b2/"
                cityAddressT2 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/tudi/b3/"
                cityAddressT3 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/tudi/b4/"
                cityAddressT4 = "http://" + cityList[provinceName][cityName].split("|")[0] + ".58.com/tudi/b5/"

                yield Request(cityAddressQ, callback=self.Q_Region, errback=self.errback_httpbin)
                yield Request(cityAddressD, callback=self.D_Region, errback=self.errback_httpbin)
                yield Request(cityAddressE, callback=self.E_Region, errback=self.errback_httpbin)

                yield Request(cityAddressX0, callback=self.X_Region, errback=self.errback_httpbin)
                yield Request(cityAddressX1, callback=self.X_Region, errback=self.errback_httpbin)
                yield Request(cityAddressX2, callback=self.X_Region, errback=self.errback_httpbin)
                yield Request(cityAddressX3, callback=self.X_Region, errback=self.errback_httpbin)

                yield Request(cityAddressS0, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressS1, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressS2, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressS3, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressS4, callback=self.S_Region, errback=self.errback_httpbin)

                yield Request(cityAddressF0, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressF1, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressF2, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressF3, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressF4, callback=self.S_Region, errback=self.errback_httpbin)            

                yield Request(cityAddressK0, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressK1, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressK2, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressK3, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressK4, callback=self.S_Region, errback=self.errback_httpbin)  

                yield Request(cityAddressH0, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressH1, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressH2, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressH3, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressH4, callback=self.S_Region, errback=self.errback_httpbin)  

                yield Request(cityAddressT0, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressT1, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressT2, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressT3, callback=self.S_Region, errback=self.errback_httpbin)
                yield Request(cityAddressT4, callback=self.S_Region, errback=self.errback_httpbin)  
    #一级区域=====================================================================================================
    #出租房 city+prov+commer
    def C_Region(self, response):
        TargetURL = response.url
        urlTestforSub = response.xpath('//dl[contains(@class,"secitem secitem_fist")]//@href')[1].extract()
        if urlTestforSub:
            yield Request(parse.urljoin(response.url, urlTestforSub), callback=self.C_subRegion, errback=self.errback_httpbin)
        else:
            logger.info("V's No available region in %s" % TargetURL)
            
    #求租 city
    def Q_Region(self, response):
        urlWhole = response.url
        r.lpush('58House:FixedPosition', urlWhole)        
        
    #短租 city+prove(judge)
    def D_Region(self, response):
        urlWhole = response.url
        next_url = response.xpath('//*[contains(@class,"next")]//@href').extract()
        #不存在下一页时,保存城市url        
        if next_url:
            #当页面最大值为70页时,才保存区域url
            MaxPage = int(response.xpath('//div[@class="pager"]/a[last()-1]//text()').extract_first())
            if MaxPage == 70:
                urls = response.xpath('//div[@class="relative"]/dl[@class="secitem"][1]/dd//@href')[1:]
                for url in urls.extract():
                    fullURL = parse.urljoin(response.url, url)
                    r.lpush('58House:FixedPosition', fullURL)
            #不到70页,保存城市url
            else:
                r.lpush('58House:FixedPosition', urlWhole)
        else:
            r.lpush('58House:FixedPosition', urlWhole)
               
    #二手房 city+prov+commer
    def E_Region(self, response):
        TargetURL = response.url
        urlTestforSub = response.xpath('//div[@class="filter-wrap"]/dl[1]//@href')[1].extract()
        if urlTestforSub:
            yield Request(parse.urljoin(response.url, urlTestforSub), callback=self.E_subRegion, errback=self.errback_httpbin)
        else:
            logger.info("V's No available region in %s" % TargetURL)   
    
    #写字楼 
    def X_Region(self, response):
        urlWhole = response.url
        next_url = response.xpath('//*[contains(@class,"next")]//@href').extract()
        if next_url:
            MaxPage = int(response.xpath('//div[@class="pager"]/a[last()-1]//text()').extract_first())
            if MaxPage == 70:
                urlTestforSub = response.xpath('//dl[@class="secitem"][1]/dd//@href')[1].extract()
                yield Request(parse.urljoin(response.url, urlTestforSub), callback=self.X_subRegion, errback=self.errback_httpbin)    
            else:
                r.lpush('58House:FixedPosition', urlWhole)
        else:
            r.lpush('58House:FixedPosition', urlWhole)
            
    #商铺 厂房 车位 仓库 土地
    def S_Region(self, response):
        urlWhole = response.url
        next_url = response.xpath('//*[contains(@class,"next")]//@href').extract()
        if next_url:
            MaxPage = int(response.xpath('//div[@class="pager"]/a[last()-1]//text()').extract_first())
            if MaxPage == 70:
                urlTestforSub = response.xpath('//div[@class="filter-wrap"]/dl[1]//@href')[1].extract()
                yield Request(parse.urljoin(response.url, urlTestforSub), callback=self.S_subRegion, errback=self.errback_httpbin)    
            else:
                r.lpush('58House:FixedPosition', urlWhole)
        else:
            r.lpush('58House:FixedPosition', urlWhole)
    #===============================================================================================================

    #二级区域=====================================================================================================
    #出租房 
    def C_subRegion(self, response):
        urls1 = response.xpath('//dl[contains(@class,"secitem secitem_fist")]//@href')[1:]
        urls2 = response.xpath('//div[contains(@class,"arealist")]//@href')
        if urls2:
            for url1 in urls1.extract():
                yield Request(parse.urljoin(response.url, url1), callback=self.C_subRegionR, errback=self.errback_httpbin)
        else:
            for url1 in urls1.extract():
                fullURL = parse.urljoin(response.url, url1)
                r.lpush('58House:FixedPosition', fullURL)                        
    
    #二手房 
    def E_subRegion(self, response):
        urlsRegionOnly = response.xpath('//div[@class="filter-wrap"]/dl[1]//@href')[1:]
        urlsNoSubway = response.xpath('//dl[@class="secitem secitem-no-subway"]//@href')
        urlsWithSubway = response.xpath('//div[@id="qySelectSecond"]//@href')
        if urlsNoSubway or urlsWithSubway:
            for url in urlsRegionOnly.extract():
                yield Request(parse.urljoin(response.url, url), callback=self.E_subRegionR, errback=self.errback_httpbin)
        else:
            for url in urlsRegionOnly.extract():
                fullURL = parse.urljoin(response.url, url)
                r.lpush('58House:FixedPosition', fullURL)
                 
    #写字楼 
    def X_subRegion(self, response):
        urls1 = response.xpath('//dl[@class="secitem"][1]/dd//@href')[1:]
        next_url = response.xpath('//*[contains(@class,"next")]//@href').extract()
        if next_url:
            MaxPage = int(response.xpath('//div[@class="pager"]/a[last()-1]//text()').extract_first())            
            urls2 = response.xpath('//div[@id="qySelectSecond"]//@href')
            if MaxPage == 70 and urls2:
                for url1 in urls1.extract():
                    yield Request(parse.urljoin(response.url, url1), callback=self.X_subRegionR, errback=self.errback_httpbin) 
            else:
                for url1 in urls1.extract():
                    fullURL = parse.urljoin(response.url, url1)
                    r.lpush('58House:FixedPosition', fullURL) 
        else:
            for url1 in urls1.extract():
                fullURL = parse.urljoin(response.url, url1)
                r.lpush('58House:FixedPosition', fullURL)  
    
    #商铺 厂房 车位 仓库
    def S_subRegion(self, response):
        next_url = response.xpath('//*[contains(@class,"next")]//@href').extract()
        urls1 = response.xpath('//div[@class="filter-wrap"]/dl[1]//@href')[1:]
        if next_url:
            MaxPage = int(response.xpath('//div[@class="pager"]/a[last()-1]//text()').extract_first())            
            urls2 = response.xpath('//dl[@class="secitem secitem-fist"]//@href')
            if MaxPage == 70 and urls2:
                for url1 in urls1.extract():
                    yield Request(parse.urljoin(response.url, url1), callback=self.S_subRegionR, errback=self.errback_httpbin)    
            else:
                for url1 in urls1.extract():
                    fullURL = parse.urljoin(response.url, url1)
                    r.lpush('58House:FixedPosition', fullURL) 
        else:
            for url1 in urls1.extract():
                fullURL = parse.urljoin(response.url, url1)
                r.lpush('58House:FixedPosition', fullURL)    
    #===============================================================================================================

    #二级区域获得===============================================================================================================
    def C_subRegionR(self, response):
        urls = response.xpath('//div[contains(@class,"arealist")]//@href')
        TargetURL = response.url
        if urls:
            for url in urls.extract():
                fullURL = parse.urljoin(response.url, url)
                r.lpush('58House:FixedPosition', fullURL) 
        else:
            r.lpush('58House:FixedPosition', TargetURL) 
            logger.debug("V's no subRegion in C %s" % TargetURL)
            
    def E_subRegionR(self, response):
        urlsNoSubway = response.xpath('//dl[@class="secitem secitem-no-subway"]//@href')
        urlsWithSubway = response.xpath('//div[@id="qySelectSecond"]//@href')
        TargetURL = response.url
        if urlsNoSubway:
            for url in urlsNoSubway.extract():
                fullURL = parse.urljoin(response.url, url)
                r.lpush('58House:FixedPosition', fullURL) 
        elif urlsWithSubway:        
            for url in urlsWithSubway.extract():
                fullURL = parse.urljoin(response.url, url)
                r.lpush('58House:FixedPosition', fullURL) 
        else:
            r.lpush('58House:FixedPosition', TargetURL)
            logger.debug("V's no subRegion in E %s" % TargetURL)
                
    def X_subRegionR(self, response):
        urls = response.xpath('//div[@id="qySelectSecond"]//@href')
        TargetURL = response.url
        if urls:
            for url in urls.extract():
                fullURL = parse.urljoin(response.url, url)
                r.lpush('58House:FixedPosition', fullURL) 
        else:
            r.lpush('58House:FixedPosition', TargetURL)
            logger.debug("V's no subRegion in X %s" % TargetURL)

    def S_subRegionR(self, response):
        urls = response.xpath('//dl[@class="secitem secitem-fist"]//@href')
        TargetURL = response.url
        if urls:
            for url in urls.extract():
                fullURL = parse.urljoin(response.url, url)
                r.lpush('58House:FixedPosition', fullURL) 
        else:
            r.lpush('58House:FixedPosition', TargetURL)
            logger.debug("V's no subRegion in S %s" % TargetURL)

#Error===================================================================================================================

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("V's Occur HttpError on %s", response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("V's Occur DNSLookupError on %s", request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("V's Occur TimeoutError on %s", request.url)
#========================================================================================================================





