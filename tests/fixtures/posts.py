# coding: utf-8

from __future__ import unicode_literals, absolute_import, print_function

import textwrap

from envision.app import create_app
from envision.ext import db
from envision.models.user import User
from envision.models.post import Post


def add_users():
    items = [
        User.create('wangbo@example.com', 'foobar', is_active=True),
        User.create('h.shoucheng@example.com', 'foobar', is_active=True),
    ]
    db.session.add_all(items)
    return items


def add_posts():
    current_user = add_users()[0]
    current_post = Post.create(
        title='秋日登洪府滕王閣餞別序',
        slug='teng-wang-ge-xu',
        author=current_user,
        status=Post.Status.publish)
    content = textwrap.dedent('''\
        豫章故郡，洪都新府。星分翼軫，地接衡廬。襟三江而帶五湖，控蠻荊而引甌越。
        物華天寶，龍光射牛斗之墟；人傑地靈，徐孺下陳蕃之榻。雄州霧列，俊彩星馳。
        臺隍枕夷夏之交，賓主盡東南之美。都督閻公之雅望，棨戟遙臨；
        宇文新州之懿範，襜帷暫駐。十旬休暇，勝友如雲。千里逢迎，高朋滿座。
        騰蛟起鳳，孟學士之詞宗；紫電青霜，王將軍之武庫。家君作宰，路出名區。
        童子何知？躬逢勝餞。

        時維九月，序屬三秋。潦水盡而寒潭清，煙光凝而暮山紫。
        儼驂騑於上路，訪風景於崇阿。臨帝子之長洲，得仙人之舊館。
        層臺聳翠，上出重霄；飛閣流丹，下臨無地。鶴汀鳧渚，窮島嶼之縈廻；
        桂殿蘭宮，即岡巒之體勢。

        披繡闥，俯雕甍。山原曠其盈視，川澤纡其駭矚。閭閻撲地，鍾鳴鼎食之家；
        舸艦迷津，青雀黃龍之舳。雲銷雨霽，彩徹區明。
        落霞與孤鶩齊飛[2]，秋水共長天一色。漁舟唱晚，響窮彭蠡之濱；
        雁陣驚寒，聲斷衡陽之浦。

        遙襟甫暢，逸興遄飛。爽籟發而清風生，纖歌凝而白雲遏。
        睢園綠竹，氣凌彭澤之樽；鄴水朱華，光照臨川之筆。四美具，二難并。
        窮睇眄於中天，極娛遊於暇日。天高地迥，覺宇宙之無窮；
        興盡悲來，識盈虛之有數。望長安於日下，指吳會於雲間。
        地勢極而南溟深，天柱高而北辰遠。關山難越，誰悲失路之人；
        萍水相逢，盡是他鄉之客。懷帝閽而不見，奉宣室以何年？

        嗟乎！時運不齊，命途多舛。馮唐易老，李廣難封。屈賈誼於長沙，非無聖主；
        竄梁鴻於海曲，豈乏明時？所賴君子安貧，達人知命。老當益壯，寧移白首之心；
        窮且益堅，不墜青雲之志。酌貪泉而覺爽，處涸轍以猶懽。北海雖賒，扶搖可接；
        東隅已逝，桑榆非晚。孟嘗高潔，空餘報國之心；阮籍猖狂，豈效窮途之哭？

        勃三尺微命，一介書生，無路請纓，等終軍之弱冠；有懷投筆，慕宗慤之長風。
        捨簪笏於百齡，奉晨昏於萬里。非謝家之寶樹，接孟氏之芳鄰。
        他日趨庭，叨陪鯉對；今茲捧袂，喜托龍門。楊意不逢，撫凌雲而自惜；
        鍾期既遇，奏流水以何慚？

        嗚呼！勝地不常，盛筵難再。蘭亭已矣，梓澤丘墟。臨別贈言，幸承恩於偉餞；
        登高作賦，是所望於群公！敢竭鄙誠，恭疏短引。一言均賦，四韻俱成。
        請灑潘江，各傾陸海云爾。

        滕王高閣臨江渚，佩玉鳴鸞罷歌舞。畫棟朝飛南浦雲，珠簾暮捲西山雨。
        閒雲潭影日悠悠，物換星移幾度秋。閣中帝子今何在？檻外長江空自流！
    ''').rstrip()
    current_post.set_content(content, Post.ContentType.markdown)
    items = [
        current_post,
    ]
    db.session.add_all(items)
    return items


def main():
    with create_app().app_context():
        add_posts()
        db.session.commit()


if __name__ == '__main__':
    main()
