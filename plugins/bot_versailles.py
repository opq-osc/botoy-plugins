import random

from botoy.decorators import equal_content, ignore_botself
from botoy.sugar import Text

__name__ = "凡尔赛语录"
__doc__ = "凡尔赛语录：发送凡尔赛"

setences = (
    "今天，我的姐妹说要开跑车来接我下班，我说不要，打工人怎么能用跑车下班？家里已经帮我包了一辆公车了",
    "看到我朋友圈的步数，朋友问，你今天去跑马拉松了吗？其实没有，我就是绕着自己的庄园散了个步",
    "哎，烦死了，每天上班这么晚，下班还这么早",
    "今天，给女朋友发红包的时候！不小心把金额输成电话号码了，居然还成功了，害得我又少了一个月的零花钱",
    "用了好多年手机，我才知道原来手机没电了可以充电不用买新的，还有前两天又去换车，4s店才告诉我原来汽车是可以加油的",
    "为什么凡尔赛就是装逼的意思？凡尔赛宫就在我家隔壁，我经常去做客",
    "香奈儿太不好用了还是用爱马仕买菜装的多",
    "每天的食材不都有专门的人员送到后厨吗?",
    "哎，也想看看平民的生活",
    "我家保姆用海蓝之谜你说她是不是有点小奢侈?",
    "烦人，每次去厨房拿点吃的都要走断腿，太远了。",
    "最大的遗憾就是因为保送错过了一生一次的高考经历",
    "真烦，我都说了不要吃鲍鱼龙虾了就不能给我一份方便面嘛",
    "今天去珠宝店看了看价格700w我弱弱的回去买我的兰博基尼算了",
    "说出来挺不好意思，我是今天才知道原来鸡蛋 有壳，以前都是管家剥好给我吃，一直以为鸡蛋都是白白软软的。",
    "以前我是不会去商场买的，我觉得会比较贵，然后还要看标签。现在基本上不太需要看标签了，因为我收入还比较高",
    "最近去试完衣服顺路回家都买几捧玫瑰，老公突然就说要买一个带院子的房子，种满玫瑰叫园丁专门打理，但是玫瑰看久了也一般啊",
    "上次开私飞回巴黎，正好遇到伟霆，一直跟着我，还跟我要微信 号，都无语了， 我就这一个微信号 ，给你了我用啥啊，真的感到很困扰",
    "被某先生气死，明明是自己懒不去洗车，落了一层灰被写了字，他倒还好意思舔着脸问我：宝贝，是不是不喜欢?宝贝，怎么老是不开总放着",
    "今早我们家的园丁被我开除了，因为透过望远镜看到50公里以外正在工作的他竟然穿着今年阿玛尼的春装。拜托，这都要2020年冬天了喂",
    "每天就大鱼大肉胡吃海塞，是个人就腻啊!还有家里的珠宝首饰太多了!堆得屋子乱难收拾，请了三十多个丫鬟都收拾不过来。为什么?因为屋子太大了呗",
    "我说想吃橘子了 我小舅就把他万亩橘园都送给了我 说我想吃多少吃多少。我说 唉 好苦恼啊 这我怎么能吃的完呢?他说：吃不完就卖了 这百八千万当我的嫁妆了",
    "之前心血来潮想申请几个学校试试，就随便申了几个，布朗、斯坦福、南加大、西北、埃默里……除了梦校哈佛还是差一点，但幸好西北收留了我这个five，做人还是要学会知足啊!毕竟知足常乐嘛",
    "去小区里的驿站取快递，老板突然把我拦下，要把她侄子介绍给我，缠着给我看照片，是个185帅哥，还一直跟我说家庭条件有多好。我问为啥是我，老板说你身材又高挑长得又漂亮，别人我都不给他介绍的。旁边都是看戏的大爷大妈们，起哄让我赶紧加他微信，我吓得落荒而逃了",
    "刚刚上班被老板骂，用昨天刚到的iPhone 12 Pro Max 512G给先森发了条消息：“好难哦，被老板骂了，我不想上班了。” 大概15分钟，都快下班了他还没有理我，我已经有点生气了。突然他从背后环绕住我：“我在。” 先森收购公司，正好只要15分钟",
    "吃到腻的大鱼大肉、多到乱的珠宝首饰、三十多个丫鬟也收拾不过来的屋子",
    "哎，烦死了，每天上班这么晚，还下班这么早",
    "老公竟然送了我一辆粉红的兰博基尼，这颜色选的也太直男了吧，哎，怎么跟他说我不喜欢这个颜色呢？",
    "你们啊，三句话离不开赚钱，搞得我好像缺钱似的",
    "作为程序员没有在公司加过班，我总觉得自己缺了点什么",
)


@ignore_botself
@equal_content("凡尔赛")
def receive_group_msg(_):
    Text(random.choice(setences))
