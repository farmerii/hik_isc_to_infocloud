前言：
1.目的：升级为停掌柜平台，需将原有平台中的信息导入到云平台中，单原有平台导出的人员数据和车辆数据无法完全匹配，且不包含群组信息，故开发此工具。
2.仅在ISC1.2版，PMS1.2.0260中使用正常，其他版本未做测试。
3.仅在业余时间学习了两个月的python和django，界面和程序都比较简陋，请见谅！
4.使用django 4.0.4版本开发

1.解压海康ISC平台备份的文件，找到allBackup_*****\pgdb\(平台IP地址)\pms_(平台pms版本号)_pmsdb_**********_1.sql

2.用winhex打开.sql文件

3.搜索并保存各类信息

3.1车辆群组信息
3.1.1搜索如下信息
--
-- Data for Name: tb_car_group; Type: TABLE DATA; Schema: public; Owner: pms_pmsdb_user
--
3.1.2再搜索数据结尾信息
\.
3.1.3将之间的信息复制并保存到.txt文件中
3.1.4车辆群组信息格式如下：
--
-- Data for Name: tb_car_group; Type: TABLE DATA; Schema: public; Owner: pms_pmsdb_user
--

COPY public.tb_car_group (cg_id, indexcode, cg_name, remark, create_time, update_time) FROM stdin;
f85ffeba-7aa1-11e9-a347-e3e145b8fca3	76df6b8bca1d49a198491107785b2f8b	外协货车	南区免费	2019-05-20 09:52:48.684	2019-08-16 14:30:20.04
**************************************************************************
**************************************************************************
\.

3.2车辆信息
3.2.1搜索如下信息
--
-- Data for Name: tb_vehicle_info; Type: TABLE DATA; Schema: public; Owner: pms_pmsdb_user
--
3.2.2再搜索数据结尾信息
\.
3.2.3将之间的信息复制并保存到.txt文件中
3.2.4车辆信息格式如下：
--
-- Data for Name: tb_vehicle_info; Type: TABLE DATA; Schema: public; Owner: pms_pmsdb_user
--

COPY public.tb_vehicle_info (v_id, v_plate_no, v_plate_type, v_plate_color, v_vehicle_type, v_vehicle_color, v_vehicle_card, v_person_id, v_vehicle_group, v_description, v_create_time, v_update_time) FROM stdin;
0c7880283465467ab3d99bcf4f8bb23d	赣******	0	0	1	1		b324d5c7c3414bc5a9a65d2c12e0d35a	cf1251a2-5a03-11e9-be3a-1b7ca20fd6f1	\N	2020-12-21 15:12:10.374	2020-12-21 15:12:10.374
**************************************************************************
**************************************************************************
\.

3.3组织路径信息
3.3.1搜索如下信息
--
-- Data for Name: tb_organizational; Type: TABLE DATA; Schema: public; Owner: pms_pmsdb_user
--
3.3.2再搜索数据结尾信息
\.
3.3.3将之间的信息复制并保存到.txt文件中
3.3.4组织路径信息格式如下：
--
-- Data for Name: tb_organizational; Type: TABLE DATA; Schema: public; Owner: pms_pmsdb_user
--

COPY public.tb_organizational (org_id, org_indexcode, org_name, org_parentid, org_data_vesion, org_path, org_dis_order) FROM stdin;
e10d72e6-165e-4ef2-be0b-1d1c8640f1ab	\N	***科	0ed89372-6034-43aa-b486-685529ac8023	\N	e10d72e6-165e-4ef2-be0b-1d1c8640f1ab,0ed89372-6034-43aa-b486-685529ac8023,4db7c89d-0ce6-4826-9146-6b71f037d81e,	346
**************************************************************************
**************************************************************************
\.

3.4车主信息
3.4.1搜索如下信息
--
-- Data for Name: tb_person; Type: TABLE DATA; Schema: public; Owner: pms_pmsdb_user
--
3.4.2再搜索数据结尾信息
\.
3.4.3将之间的信息复制并保存到.txt文件中
3.4.4车主信息格式如下：
--
-- Data for Name: tb_person; Type: TABLE DATA; Schema: public; Owner: pms_pmsdb_user
--

COPY public.tb_person (p_id, p_name, p_cert_type, p_cert_no, p_phone, p_orgid, p_face_url, p_age, p_sex, p_pinyin, p_create_time, p_update_time) FROM stdin;
371bdeb54a19418da7de08f3879309ee	张*萍	111	\N	158****8490	015d15f3-6855-4cf4-a2fe-d22c48e3a146	\N	\N	2	zhang***ping	2021-01-26 16:25:57.41	2021-01-26 16:25:57.41
**************************************************************************
**************************************************************************
\.

4.分别将保存的四个.txt文件上传到系统中，导入系统时会验证系统中是否已经有对应的信息，所以会花费较长时间，经测试4000+数据大概在十分钟以内。

5.点击合并车辆信息

6.下载所有合并后的信息

