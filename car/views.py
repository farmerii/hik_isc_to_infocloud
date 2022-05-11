# -*- coding: utf-8 -*-
import csv
import logging
import chardet
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import ParkCar, ParkUser, QunZu, CheZhu, TingGuanJia, YongHuXinXi, ZuZhiXinXi


def car_upload_view(request):
    # 初始化success返回页面提示数据,car_log_data为上传车辆信息时有重复数据，exception_log_data为错误信息
    car_log_data = []
    exception_log_data = []
    # 记录行号
    a = 0
    if request.method == 'GET':
        return render(request, 'car/car_upload.html')
    elif request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file'].read()
            # 跳过1行？
            # next(csv_file)
            # if not csv_file.name.endswith('.csv'):
            #     messages.error(request, '上传的文件不是CSV文件')
            #     return HttpResponseRedirect(reverse('car_upload'))
            # # 判断文件是否过大
            # if csv_file.multiple_chunks():
            #     messages.error(request, '上传的文件超过%2.fMB'%csv_file.size/(1000*1000))
            #     return HttpResponseRedirect(reverse('car_upload'))
            # 文件decode编码为UTF-8,并使用.replace('	', '')删除文件中不需要的空白字符，使用.replace('"', '')删除双引号
            # file_data = csv_file.read().decode('utf-8').replace('	', '').replace('"', '')
            # 自动判断CVS文件的编码格式
            file_encode = chardet.detect(csv_file)
            file_encoding = str(file_encode.get('encoding'))
            # print(file_encoding)
            # 使用自动判断出的编码格式,并使用.replace('	', '')删除文件中不需要的空白字符，使用.replace('"', '')删除双引号
            file_data = csv_file.decode(file_encoding).replace('	', '').replace('"', '')
            # 使用\n为行间分隔符
            lines = file_data.split('\n')
            # 循环所有数据并写入数据库中，如有错误显示出来
            for line in lines:
                # 行号
                a += 1
                # 前9行为非有效数据
                if not a < 10:
                    # 注意：csv文件中如有空白行将报IndexError('list index out of range')错误，所以要try一下
                    try:
                        # 使用逗号为字符间分隔符
                        fields = line.split(',')
                        # 判断数据库中是否已经有同样的工号
                        if not ParkCar.objects.filter(chepaihaoma=fields[0]):
                            try:
                                # 分割line后的fields是数组
                                # 注意：csv文件中如有空白行将报IndexError('list index out of range')错误，但可以继续运行下一行
                                ParkCar.objects.create(chepaihaoma=fields[0], miaosu=fields[5],
                                                       chezhuxingming=fields[6],
                                                       gonghao=fields[7])
                            except Exception as e1:
                                # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                                logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                                exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e1)])
                                messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                        else:
                            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                            logging.getLogger('django').error('用户工号重复：' + fields[0] + ' ' + fields[5])
                            # 将重复工号的信息加入user_log_data中
                            car_log_data.append([fields[0], fields[6], fields[7]])
                    except Exception as e2:
                        # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                        logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e2))
                        exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e2)])
                        messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e2))
        except Exception as e3:
            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
            logging.getLogger('django').error('上传文件错误：第' + str(a) + '行  ' + repr(e3))
            exception_log_data.append(['上传文件错误：' + '第' + str(a) + '行    ' + repr(e3)])
            messages.error(request, '上传文件错误：第' + str(a) + '行    ' + repr(e3))
        return render(request, 'car/car_success.html', locals())


def car_list_view(request):
    # 获取页面的查询字符串判断在某页，如无则置1
    page_num = request.GET.get('page', 1)
    # 在数据库中查询所有车辆信息
    cars = ParkCar.objects.all().order_by('id')
    # 初始化paginator，每页30条数据
    paginator = Paginator(cars, 30)
    # 初始化具体的页面对象，并将page_num转化为int型
    c_page = paginator.page(int(page_num))
    return render(request, 'car/car_list.html', locals())


def car_clear_view(request):
    ParkCar.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))


def user_upload_view(request):
    # 初始化success返回页面提示数据,user_log_data为上传用户信息时有重复数据，exception_log_data为错误信息
    user_log_data = []
    exception_log_data = []
    # 记录行号
    a = 0
    if request.method == 'GET':
        return render(request, 'car/user_upload.html')
    elif request.method == 'POST':
        try:
            # request.FILES['csv_file'].read()在同一函数中只能执行一次
            csv_file = request.FILES['csv_file'].read()
            # 跳过1行？
            # next(csv_file)
            # if not csv_file.name.endswith('.csv'):
            #     messages.error(request, '上传的文件不是CSV文件')
            #     return HttpResponseRedirect(reverse('user_upload'))
            # # 判断文件是否过大
            # if csv_file.multiple_chunks():
            #     messages.error(request, '上传的文件超过%2.fMB'%csv_file.size/(1000*1000))
            #     return HttpResponseRedirect(reverse('user_upload'))
            # 自动判断CVS文件的编码格式
            file_encode = chardet.detect(csv_file)
            print(file_encode)
            file_encoding = str(file_encode.get('encoding'))
            print(file_encoding)
            # 使用自动判断出的编码格式,并使用.replace('	', '')删除文件中不需要的空白字符，使用.replace('"', '')删除双引号
            file_data = csv_file.decode(file_encoding).replace('	', '').replace('"', '')
            print(file_data)
            # 使用\n为行间分隔符
            lines = file_data.split('\n')
            # 循环所有数据并写入数据库中，如有错误显示出来
            for line in lines:
                a += 1
                # 前8行为非有效数据
                if not a < 9:
                    try:
                        # 注意：csv文件中如有空白行将报IndexError('list index out of range')错误，所以要try一下
                        # 使用逗号为字符间分隔符
                        fields = line.split(',')
                        # 记录行号
                        # 判断数据库中是否已经有同样的工号
                        if not ParkUser.objects.filter(gonghao=fields[5]):
                            try:
                                # 分割line后的fields是数组
                                ParkUser.objects.create(chezhuxingming=fields[0], zuzhilujing=fields[2],
                                                        gonghao=fields[5],
                                                        shoujihaoma=fields[6])
                            except Exception as e1:
                                # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                                logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                                exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e1)])
                                messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                        else:
                            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                            logging.getLogger('django').error('用户工号重复：' + fields[0] + ' ' + fields[5])
                            # 将重复工号的信息加入user_log_data中
                            user_log_data.append([fields[0], fields[5]])
                    except Exception as e2:
                        # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                        logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e2))
                        exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e2)])
                        messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e2))
        except Exception as e3:
            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
            logging.getLogger('django').error('上传文件错误：第' + str(a) + '行  ' + repr(e3))
            exception_log_data.append(['上传文件错误：' + '第' + str(a) + '行    ' + repr(e3)])
            messages.error(request, '上传文件错误：第' + str(a) + '行    ' + repr(e3))
            pass
        # 处理完成后转到完成页面并显示错误信息
        return render(request, 'car/user_success.html', locals())


def user_list_view(request):
    # 获取页面的查询字符串判断在某页，如无则置1
    page_num = request.GET.get('page', 1)
    # 在数据库中查询所有车主信息
    users = ParkUser.objects.all().order_by('id')
    # 初始化paginator，每页30条数据
    paginator = Paginator(users, 30)
    # 初始化具体的页面对象，并将page_num转化为int型
    c_page = paginator.page(int(page_num))
    return render(request, 'car/user_list.html', locals())


def user_clear_view(request):
    ParkUser.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))


# 导入数据库种的群组信息
def qunzu_upload_view(request):
    # 初始化success返回页面提示数据,user_log_data为上传用户信息时有重复数据，exception_log_data为错误信息
    qunzu_log_data = []
    exception_log_data = []
    # 记录行号
    a = 0
    if request.method == 'GET':
        return render(request, 'car/qunzu_upload.html')
    elif request.method == 'POST':
        try:
            # request.FILES['csv_file'].read()在同一函数中只能执行一次
            csv_file = request.FILES['csv_file'].read()
            # 跳过1行？
            # next(csv_file)
            # if not csv_file.name.endswith('.csv'):
            #     messages.error(request, '上传的文件不是CSV文件')
            #     return HttpResponseRedirect(reverse('user_upload'))
            # # 判断文件是否过大
            # if csv_file.multiple_chunks():
            #     messages.error(request, '上传的文件超过%2.fMB'%csv_file.size/(1000*1000))
            #     return HttpResponseRedirect(reverse('user_upload'))
            # 自动判断CVS文件的编码格式
            file_encode = chardet.detect(csv_file)
            print(file_encode)
            file_encoding = str(file_encode.get('encoding'))
            print(file_encoding)
            # 使用自动判断出的编码格式,并使用.replace('	', '')删除文件中不需要的空白字符，使用.replace('"', '')删除双引号
            file_data = csv_file.decode(file_encoding).replace('	', ',').replace('"', '')
            print(file_data)
            # 使用\n为行间分隔符
            lines = file_data.split('\n')
            # 循环所有数据并写入数据库中，如有错误显示出来
            for line in lines:
                a += 1
                # 前8行为非有效数据
                if not a < 1:
                    try:
                        # 注意：csv文件中如有空白行将报IndexError('list index out of range')错误，所以要try一下
                        # 使用tab为字符间分隔符
                        fields = line.split(',')
                        # 记录行号
                        # 判断数据库中是否已经有同样的群组ID
                        if not QunZu.objects.filter(cg_id=fields[0]):
                            try:
                                # 分割line后的fields是数组
                                QunZu.objects.create(cg_id=fields[0], indexcode=fields[1], cg_name=fields[2],
                                                     remark=fields[3], create_time=fields[4], update_time=fields[5])
                            except Exception as e1:
                                # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                                logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                                exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e1)])
                                messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                        else:
                            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                            logging.getLogger('django').error('群组ID重复：' + fields[0] + ' ' + fields[5])
                            # 将重复工号的信息加入user_log_data中
                            qunzu_log_data.append([fields[0], fields[4]])
                    except Exception as e2:
                        # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                        logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e2))
                        exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e2)])
                        messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e2))
        except Exception as e3:
            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
            logging.getLogger('django').error('上传文件错误：第' + str(a) + '行  ' + repr(e3))
            exception_log_data.append(['上传文件错误：' + '第' + str(a) + '行    ' + repr(e3)])
            messages.error(request, '上传文件错误：第' + str(a) + '行    ' + repr(e3))
            pass
        # 处理完成后转到完成页面并显示错误信息
        return render(request, 'car/qunzu_success.html', locals())


def qunzu_list_view(request):
    # 获取页面的查询字符串判断在某页，如无则置1
    page_num = request.GET.get('page', 1)
    # 在数据库中查询所有车主信息
    users = QunZu.objects.all().order_by('id')
    # 初始化paginator，每页30条数据
    paginator = Paginator(users, 30)
    # 初始化具体的页面对象，并将page_num转化为int型
    c_page = paginator.page(int(page_num))
    return render(request, 'car/qunzu_list.html', locals())


def qunzu_clear_view(request):
    QunZu.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))


# 导入数据库中的信息
def chezhu_upload_view(request):
    # 初始化success返回页面提示数据,user_log_data为上传用户信息时有重复数据，exception_log_data为错误信息
    chezhu_log_data = []
    exception_log_data = []
    # 记录行号
    a = 0
    if request.method == 'GET':
        return render(request, 'car/chezhu_upload.html')
    elif request.method == 'POST':
        try:
            # request.FILES['csv_file'].read()在同一函数中只能执行一次
            csv_file = request.FILES['csv_file'].read()
            # 跳过1行？
            # next(csv_file)
            # if not csv_file.name.endswith('.csv'):
            #     messages.error(request, '上传的文件不是CSV文件')
            #     return HttpResponseRedirect(reverse('user_upload'))
            # # 判断文件是否过大
            # if csv_file.multiple_chunks():
            #     messages.error(request, '上传的文件超过%2.fMB'%csv_file.size/(1000*1000))
            #     return HttpResponseRedirect(reverse('user_upload'))
            # 自动判断CVS文件的编码格式
            file_encode = chardet.detect(csv_file)
            print(file_encode)
            file_encoding = str(file_encode.get('encoding'))
            print(file_encoding)
            # 使用自动判断出的编码格式,并使用.replace('    ', '')删除文件中不需要的空白字符(空白符为4个空格)，使用.replace('"', '')删除双引号
            file_data = csv_file.decode(file_encoding).replace('	', ',').replace('"', '')
            print(file_data)
            # 使用\n为行间分隔符
            lines = file_data.split('\n')
            # 循环所有数据并写入数据库中，如有错误显示出来
            for line in lines:
                a += 1
                # 跳过前6行非有效数据
                if not a < 6:
                    try:
                        # 注意：csv文件中如有空白行将报IndexError('list index out of range')错误，所以要try一下
                        # 使用tab为字符间分隔符
                        fields = line.split(',')
                        # 记录行号
                        # 判断数据库中是否已经有同样的车牌号码
                        if not CheZhu.objects.filter(v_plate_no=fields[1]):
                            try:
                                # 分割line后的fields是数组
                                CheZhu.objects.create(v_id=fields[0], v_plate_no=fields[1], v_plate_type=fields[2],
                                                      v_plate_color=fields[3], v_vehicle_type=fields[4],
                                                      v_vehicle_color=fields[5], v_vehicle_card=fields[6],
                                                      v_person_id=fields[7],
                                                      v_vehicle_group=fields[8], v_description=fields[9],
                                                      v_create_time=fields[10],
                                                      v_update_time=fields[11])
                            except Exception as e1:
                                # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                                logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                                exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e1)])
                                messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                        else:
                            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                            logging.getLogger('django').error('车牌号码重复：' + fields[0] + ' ' + fields[5])
                            # 将重复工号的信息加入user_log_data中
                            chezhu_log_data.append([fields[1], fields[8]])
                    except Exception as e2:
                        # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                        logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e2))
                        exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e2)])
                        messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e2))
        except Exception as e3:
            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
            logging.getLogger('django').error('上传文件错误：第' + str(a) + '行  ' + repr(e3))
            exception_log_data.append(['上传文件错误：' + '第' + str(a) + '行    ' + repr(e3)])
            messages.error(request, '上传文件错误：第' + str(a) + '行    ' + repr(e3))
            pass
        # 处理完成后转到完成页面并显示错误信息
        return render(request, 'car/chezhu_success.html', locals())


def chezhu_list_view(request):
    # 获取页面的查询字符串判断在某页，如无则置1
    page_num = request.GET.get('page', 1)
    # 在数据库中查询所有车主信息
    users = CheZhu.objects.all().order_by('id')
    # 初始化paginator，每页30条数据
    paginator = Paginator(users, 30)
    # 初始化具体的页面对象，并将page_num转化为int型
    c_page = paginator.page(int(page_num))
    return render(request, 'car/chezhu_list.html', locals())


def chezhu_clear_view(request):
    CheZhu.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))


def yonghuxinxi_upload_view(request):
    # 初始化success返回页面提示数据,user_log_data为上传用户信息时有重复数据，exception_log_data为错误信息
    yonghuxinxi_log_data = []
    exception_log_data = []
    # 记录行号
    a = 0
    if request.method == 'GET':
        return render(request, 'car/yonghuxinxi_upload.html')
    elif request.method == 'POST':
        try:
            # request.FILES['csv_file'].read()在同一函数中只能执行一次
            csv_file = request.FILES['csv_file'].read()
            # 跳过1行？
            # next(csv_file)
            # if not csv_file.name.endswith('.csv'):
            #     messages.error(request, '上传的文件不是CSV文件')
            #     return HttpResponseRedirect(reverse('user_upload'))
            # # 判断文件是否过大
            # if csv_file.multiple_chunks():
            #     messages.error(request, '上传的文件超过%2.fMB'%csv_file.size/(1000*1000))
            #     return HttpResponseRedirect(reverse('user_upload'))
            # 自动判断CVS文件的编码格式
            file_encode = chardet.detect(csv_file)
            print(file_encode)
            file_encoding = str(file_encode.get('encoding'))
            print(file_encoding)
            # 使用自动判断出的编码格式,并使用.replace('    ', '')删除文件中不需要的空白字符(空白符为4个空格)，
            # 使用.replace('"', '')删除双引号
            file_data = csv_file.decode(file_encoding).replace('	', ',').replace('"', '')
            print(file_data)
            # 使用\n为行间分隔符
            lines = file_data.split('\n')
            # 循环所有数据并写入数据库中，如有错误显示出来
            for line in lines:
                a += 1
                # 跳过前5行非有效数据
                if not a < 6:
                    try:
                        # 注意：csv文件中如有空白行将报IndexError('list index out of range')错误，所以要try一下
                        # 使用tab为字符间分隔符
                        fields = line.split(',')
                        # 记录行号
                        # 判断数据库中是否已经有同样的车牌号码
                        if not YongHuXinXi.objects.filter(yonghuID=fields[0]):
                            try:
                                # 分割line后的fields是数组
                                YongHuXinXi.objects.create(yonghuID=fields[0], yonghuming=fields[1],
                                                           shoujihaoma=fields[4], zuzhiID=fields[5],
                                                           yonghumingpinyin=fields[9],
                                                           xinjianshijian=fields[10], xiugaishijian=fields[11])
                            except Exception as e1:
                                # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                                logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                                exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e1)])
                                messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                        else:
                            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                            logging.getLogger('django').error('用户ID重复：' + fields[0] + ' ' + fields[1])
                            # 将重复工号的信息加入user_log_data中
                            yonghuxinxi_log_data.append([fields[0], fields[1]])
                    except Exception as e2:
                        # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                        logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e2))
                        exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e2)])
                        messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e2))
        except Exception as e3:
            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
            logging.getLogger('django').error('上传文件错误：第' + str(a) + '行  ' + repr(e3))
            exception_log_data.append(['上传文件错误：' + '第' + str(a) + '行    ' + repr(e3)])
            messages.error(request, '上传文件错误：第' + str(a) + '行    ' + repr(e3))
            pass
        # 处理完成后转到完成页面并显示错误信息
        return render(request, 'car/yonghuxinxi_success.html', locals())


def yonghuxinxi_list_view(request):
    # 获取页面的查询字符串判断在某页，如无则置1
    page_num = request.GET.get('page', 1)
    # 在数据库中查询所有车主信息
    users = YongHuXinXi.objects.all().order_by('id')
    # 初始化paginator，每页30条数据
    paginator = Paginator(users, 30)
    # 初始化具体的页面对象，并将page_num转化为int型
    c_page = paginator.page(int(page_num))
    return render(request, 'car/yonghuxinxi_list.html', locals())


def yonghuxinxi_clear_view(request):
    YongHuXinXi.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))


def zuzhixinxi_upload_view(request):
    # 初始化success返回页面提示数据,user_log_data为上传用户信息时有重复数据，exception_log_data为错误信息
    zuzhixinxi_log_data = []
    exception_log_data = []
    # 记录行号
    a = 0
    if request.method == 'GET':
        return render(request, 'car/zuzhixinxi_upload.html')
    elif request.method == 'POST':
        try:
            # request.FILES['csv_file'].read()在同一函数中只能执行一次
            csv_file = request.FILES['csv_file'].read()
            # 跳过1行？
            # next(csv_file)
            # if not csv_file.name.endswith('.csv'):
            #     messages.error(request, '上传的文件不是CSV文件')
            #     return HttpResponseRedirect(reverse('user_upload'))
            # # 判断文件是否过大
            # if csv_file.multiple_chunks():
            #     messages.error(request, '上传的文件超过%2.fMB'%csv_file.size/(1000*1000))
            #     return HttpResponseRedirect(reverse('user_upload'))
            # 自动判断CVS文件的编码格式
            file_encode = chardet.detect(csv_file)
            print(file_encode)
            file_encoding = str(file_encode.get('encoding'))
            print(file_encoding)
            # 使用自动判断出的编码格式,并使用.replace('    ', '')删除文件中不需要的空白字符(空白符为4个空格)，
            # 使用.replace('"', '')删除双引号
            file_data = csv_file.decode(file_encoding).replace('	', ',').replace('"', '')
            print(file_data)
            # 使用\n为行间分隔符
            lines = file_data.split('\n')
            # 循环所有数据并写入数据库中，如有错误显示出来
            for line in lines:
                a += 1
                # 跳过前5行非有效数据
                if not a < 6:
                    try:
                        # 注意：csv文件中如有空白行将报IndexError('list index out of range')错误，所以要try一下
                        # 使用tab为字符间分隔符
                        fields = line.split(',')
                        # 记录行号
                        # 判断数据库中是否已经有同样的车牌号码
                        if not ZuZhiXinXi.objects.filter(zuzhiID=fields[0]):
                            try:
                                # 分割line后的fields是数组
                                ZuZhiXinXi.objects.create(zuzhiID=fields[0], zuzhimingcheng=fields[2])
                            except Exception as e1:
                                # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                                logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                                exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e1)])
                                messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e1))
                        else:
                            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                            logging.getLogger('django').error('用户ID重复：' + fields[0] + ' ' + fields[2])
                            # 将重复工号的信息加入user_log_data中
                            zuzhixinxi_log_data.append([fields[0], fields[2]])
                    except Exception as e2:
                        # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
                        logging.getLogger('django').error('错误信息：' + '第' + str(a) + '行    ' + repr(e2))
                        exception_log_data.append(['错误信息：' + '第' + str(a) + '行    ' + repr(e2)])
                        messages.error(request, '错误信息：' + '第' + str(a) + '行    ' + repr(e2))
        except Exception as e3:
            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
            logging.getLogger('django').error('上传文件错误：第' + str(a) + '行  ' + repr(e3))
            exception_log_data.append(['上传文件错误：' + '第' + str(a) + '行    ' + repr(e3)])
            messages.error(request, '上传文件错误：第' + str(a) + '行    ' + repr(e3))
            pass
        # 处理完成后转到完成页面并显示错误信息
        return render(request, 'car/zuzhixinxi_success.html', locals())


def zuzhixinxi_list_view(request):
    # 获取页面的查询字符串判断在某页，如无则置1
    page_num = request.GET.get('page', 1)
    # 在数据库中查询所有车主信息
    users = ZuZhiXinXi.objects.all().order_by('id')
    # 初始化paginator，每页30条数据
    paginator = Paginator(users, 30)
    # 初始化具体的页面对象，并将page_num转化为int型
    c_page = paginator.page(int(page_num))
    return render(request, 'car/zuzhixinxi_list.html', locals())


def zuzhixinxi_clear_view(request):
    ZuZhiXinXi.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))


def tingguanjia_view(request):
    # 初始化success返回页面提示数据,all_log_data为车牌信息时有重复数据
    all_log_data = []
    # 从CheZhu数据库中获取车辆信息
    cheliangxinxi = CheZhu.objects.all()
    # 获取车牌号
    for car in cheliangxinxi:
        # 获取此次循环的车牌号
        chepaihaoma = car.v_plate_no
        chezhuID = car.v_person_id
        # 获取此次循环的描述信息
        miaosu = car.v_description
        # 判断TingGuanJia数据表中是否已有此车牌号
        if not TingGuanJia.objects.filter(chepaihaoma=chepaihaoma):
            # 在数据库QunZu中获取群组名称
            for qunzuming in QunZu.objects.filter(cg_id=car.v_vehicle_group):
                qunzumingcheng = qunzuming.cg_name
            # 在数据库YongHuXinXi中获取车主姓名
            for chezhu in YongHuXinXi.objects.filter(yonghuID=chezhuID):
                chezhuxingming = chezhu.yonghuming
                shoujihaoma = chezhu.shoujihaoma
            for zuzhi in ZuZhiXinXi.objects.filter(zuzhiID=chezhu.zuzhiID):
                zuzhimingcheng = zuzhi.zuzhimingcheng
            for shijian in CheZhu.objects.filter(v_plate_no=chepaihaoma):
                xinjianshijian = shijian.v_create_time
                xiugaishijian = shijian.v_update_time

            # 写入数据库
            TingGuanJia.objects.create(chepaihaoma=chepaihaoma, qunzumingcheng=qunzumingcheng, miaosu=miaosu,
                                       chezhuxingming=chezhuxingming, chezhuzuzhilujing=zuzhimingcheng,
                                       chepaizuzhilujing=zuzhimingcheng, shoujihao=shoujihaoma,
                                       xinjianshijian=xinjianshijian, xiugaishijian=xiugaishijian)
        else:
            # 这里的django会对应到日志配置中的django日志器配置，并加载那段配置
            logging.getLogger('django').error('车牌号码重复：' + chepaihaoma)
            # 将重复工号的信息加入user_log_data中
            all_log_data.append([chepaihaoma])
    return render(request, 'car/all_success.html', locals())


def tingguanjia_clear_view(request):
    TingGuanJia.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))


def all_list_view(request):
    # 获取页面的查询字符串判断在某页，如无则置1
    page_num = request.GET.get('page', 1)
    # 在数据库中查询所有车主信息
    users = TingGuanJia.objects.all().order_by('xiugaishijian')
    # 初始化paginator，每页30条数据
    paginator = Paginator(users, 30)
    # 初始化具体的页面对象，并将page_num转化为int型
    c_page = paginator.page(int(page_num))
    return render(request, 'car/all_list.html', locals())


def all_download_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="all_info.csv"'
    all_info = TingGuanJia.objects.all()
    writer = csv.writer(response)
    writer.writerow(['车牌号码', '车位号', '停车库名称', '开始时间', '结束时间', '车牌所属组织路径', '车牌类型', '车牌颜色', '车辆类型',
                    '车辆颜色', '描述', '车主姓名', '性别', '车主所属组织路径', '工号', '手机号', '群组名称', '录入时间', '修改时间'])
    for info in all_info:
        writer.writerow([info.chepaihaoma, '', info.tingchekumingcheng, '', '', info.chepaizuzhilujing, '', '', '', '',
                         info.miaosu, info.chezhuxingming, '', info.chezhuzuzhilujing, '', info.shoujihao,
                         info.qunzumingcheng, info.xinjianshijian, info.xiugaishijian])
    return response
