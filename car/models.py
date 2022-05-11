from django.db import models

# Create your models here.
from django.db import models


class ParkUser(models.Model):
    chezhuxingming = models.CharField('车主姓名', max_length=50)
    xingbie = models.CharField('性别', max_length=1)
    zuzhilujing = models.CharField('组织路径', max_length=100)
    zhengjianleixing = models.CharField('证件类型', max_length=10)
    zhengjianhaoma = models.CharField('证件号码', max_length=18)
    gonghao = models.CharField('工号', max_length=20)
    shoujihaoma = models.CharField('手机号码', max_length=15)
    is_active = models.BooleanField('是否活动', default=True)

    class Meta:
        db_table = 'ParkUser'


class ParkCar(models.Model):
    chepaihaoma = models.CharField('车牌号码', max_length=12)
    chepaileixing = models.CharField('车牌类型', max_length=10)
    chepaiyanse = models.CharField('车牌颜色', max_length=8)
    cheliangleixing = models.CharField('车辆类型', max_length=10)
    cheliangyanse = models.CharField('车辆颜色', max_length=10)
    miaosu = models.CharField('描述', max_length=100)
    chezhuxingming = models.CharField('车主姓名', max_length=50)
    gonghao = models.CharField('工号', max_length=20)
    is_active = models.BooleanField('是否活动', default=True)

    class Meta:
        db_table = 'ParkCar'


class QunZu(models.Model):
    cg_id = models.CharField('群组ID', max_length=100)
    indexcode = models.CharField('代码', max_length=100)
    cg_name = models.CharField('群组名称', max_length=100)
    remark = models.CharField('备注', max_length=100)
    create_time = models.CharField('新建时间', max_length=100)
    update_time = models.CharField('修改时间', max_length=100)

    class Meta:
        db_table = 'QunZu'


class CheZhu(models.Model):
    v_id = models.CharField('用户ID', max_length=100)
    v_plate_no = models.CharField('车牌号码', max_length=100)
    v_plate_type = models.CharField('车牌类型', max_length=100)
    v_plate_color = models.CharField('车牌颜色', max_length=100)
    v_vehicle_type = models.CharField('车辆类型', max_length=100)
    v_vehicle_color = models.CharField('车辆颜色', max_length=100)
    v_vehicle_card = models.CharField('车辆ID', max_length=100)
    v_person_id = models.CharField('车主ID', max_length=100)
    v_vehicle_group = models.CharField('群组ID', max_length=100)
    v_description = models.CharField('备注', max_length=100)
    v_create_time = models.CharField('新建时间', max_length=100)
    v_update_time = models.CharField('修改时间', max_length=100)

    class Meta:
        db_table = 'CheZhu'


class TingGuanJia(models.Model):
    chepaihaoma = models.CharField('车牌号码', max_length=20)
    cheweihao = models.CharField('车位号', max_length=20)
    tingchekumingcheng = models.CharField('停车库名称', max_length=50)
    kaishishijian = models.CharField('开始时间', max_length=50)
    jiesushijian = models.CharField('结束时间', max_length=50)
    chepaizuzhilujing = models.CharField('车牌所属组织路径', max_length=100)
    chepaileixing = models.CharField('车牌类型', max_length=20)
    chepaiyanse = models.CharField('车牌颜色', max_length=10)
    cheliangleixing = models.CharField('车辆类型', max_length=20)
    cheliangyanse = models.CharField('车辆颜色', max_length=20)
    miaosu = models.CharField('描述', max_length=100)
    chezhuxingming = models.CharField('车主姓名', max_length=50)
    xinbie = models.CharField('性别', max_length=4)
    chezhuzuzhilujing = models.CharField('车主所属组织路径', max_length=100)
    gonghao = models.CharField('工号', max_length=50)
    shoujihao = models.CharField('手机号', max_length=20)
    qunzumingcheng = models.CharField('群组名称', max_length=50)
    xinjianshijian = models.CharField('新建时间', max_length=50, default='')
    xiugaishijian = models.CharField('修改时间', max_length=50, default='')

    class Meta:
        db_table = 'TingCheGuanJia'  # 停车管家


class YongHuXinXi(models.Model):
    yonghuID = models.CharField('用户ID', max_length=50)
    yonghuming = models.CharField('用户姓名', max_length=20)
    shoujihaoma = models.CharField('手机号码', max_length=20)
    zuzhiID = models.CharField('组织ID', max_length=50)
    yonghumingpinyin = models.CharField('用户名拼音', max_length=50)
    xinjianshijian = models.CharField('用户建立时间', max_length=50)
    xiugaishijian = models.CharField('用户修改时间', max_length=50)

    class Meta:
        db_table = 'YongHuXinXi'  # 用户信息


class ZuZhiXinXi(models.Model):
    zuzhiID = models.CharField('zuzhiID', max_length=50)
    zuzhimingcheng = models.CharField('组织名称', max_length=50)

    class Meta:
        db_table = 'ZuZhiXinXi'  # 群组信息
