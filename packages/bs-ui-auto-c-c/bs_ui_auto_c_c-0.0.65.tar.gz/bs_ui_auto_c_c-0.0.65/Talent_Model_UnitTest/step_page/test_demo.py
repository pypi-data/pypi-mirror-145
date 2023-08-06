
from v5_components.page.modlues import *


def test_ghy(web_driver_initialize):
    """
    1
    """
    login('root600684@beisen.com', 'aa123456', web_driver_initialize)
    go_to_menu(web_driver_initialize, '人才模型')
    filter_item(web_driver_initialize, "文本框-人员单选")
    filter_item(web_driver_initialize, "文本框-人员单选",['管理员'],oper_type='advanced')
    filter_item(web_driver_initialize, "文本框-电子邮件",'331776297@qq.com')
    filter_item(web_driver_initialize, "文本框-电子邮件",oper_type='advanced')
    filter_item(web_driver_initialize, "文本框-URL",'www.xixi.com')
    filter_item(web_driver_initialize, "文本框-URL",oper_type='advanced')
    # filter_item(web_driver_initialize, "文本框-lookup")
    # filter_item(web_driver_initialize, "文本框-lookup", oper_type='advanced')
    # filter_item(web_driver_initialize, "单选框-单选框")
    # filter_item(web_driver_initialize, "单选框-单选框", oper_type='advanced')
    # filter_item(web_driver_initialize, "面板选择-树状选择框","大区")
    # filter_item(web_driver_initialize, "面板选择-树状选择框","大区",oper_type='advanced')
    # filter_item(web_driver_initialize, "面板选择-地区选择框-单选",[['四川省','内江市','威远县'],['天津市','河西区']])
    # filter_item(web_driver_initialize, "面板选择-地区选择框-单选",[['四川省','内江市','威远县'],['天津市','河西区']],oper_type='advanced')
    # filter_item(web_driver_initialize, "内容库-文本区", oper_type='advanced')
    # filter_item(web_driver_initialize, "自定义整数类型", )
    # filter_item(web_driver_initialize, "自定义整数类型", oper_type='advanced')
    # filter_item(web_driver_initialize, "自定义日期时间", ["20210504","20220101"])
    # filter_item(web_driver_initialize, "自定义日期时间", ["20210504","20220101"], oper_type='advanced')
    # filter_item(web_driver_initialize, "自定义日期类型",  ["20210504","20220101"])
    # filter_item(web_driver_initialize, "自定义日期类型", oper_type='advanced')
    # filter_item(web_driver_initialize, "自定义年月")
    # filter_item(web_driver_initialize, "自定义年月", ["2022/09", "2022/10"], oper_type='advanced')
    # filter_item(web_driver_initialize, "自定义时分")
    # filter_item(web_driver_initialize, "自定义时分", ['0922','1001'], oper_type='advanced')
    # filter_item(web_driver_initialize, "面板选择-树状选择框","大区",filter_type='advanced')
    # filter_item(web_driver_initialize, "面板选择-地区选择框-多选选",[['四川省','内江市','威远县'],['天津市','河西区']],filter_type='advanced')
    # filter_item(web_driver_initialize, "面板选择-地区选择框-单选",[['四川省','内江市','威远县'],['天津市','河西区']])
    # filter_item(web_driver_initialize, "自定义日期时间",["20210504","20220101"])
    # filter_item(web_driver_initialize, "自定义年月", ["2022/09", "2022/10"])
    # filter_item(web_driver_initialize, "自定义时分",['0922',''])
    # filter_item(web_driver_initialize, "自定义日期时间")
    # filter_item(web_driver_initialize, "自定义日期类型")
    # filter_item(web_driver_initialize, "单选框-单选框")
    # filter_item(web_driver_initialize, "文本框-lookup")
    # filter_item(web_driver_initialize, "文本框-部门单选")
    # filter_item(web_driver_initialize, "文本框-人员多选")
    # filter_item(web_driver_initialize, "文本框-人员单选")
    # filter_item(web_driver_initialize, "文本框-电子邮件")
    # filter_item(web_driver_initialize, "文本框-URL")
    # filter_item(web_driver_initialize, "名称", "人才模型")
    # filter_item(web_driver_initialize, "创建时间", **{'开始时间': '20211116', "截止时间": "20211216"})
    # filter_item(web_driver_initialize, "所有者", '管理员', '大区负责人')
    time.sleep(5)



def test_ghy_03(web_driver_initialize):
    """
    1
    """
    login('root600684@beisen.com', 'aa123456', web_driver_initialize)
    go_to_menu(web_driver_initialize, '人才模型')
    button_click(web_driver_initialize, "//div[@class='button-list clearfix  ']", "新增")
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{'人才模型': '指定名称',})
    form_button_click(web_driver_initialize, "保存")



def test_ghy_04(web_driver_initialize):
    """
    1
    """
    login('root600684@beisen.com', 'aa123456', web_driver_initialize)
    go_to_menu(web_driver_initialize, '人才模型')
    button_click(web_driver_initialize, "//div[@class='button-list clearfix  ']", "新增")
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list)
    # option_form(web_driver_initialize, fields_to_operate_on_list,**{'富文本类型':None,'内容库-富文本':None,'文本框-lookup':None,'文本框-人员单选':None,'文本框-人员多选':None,'文本框-公式':None,'文本框-电子邮件':None,'文本框-URL':None,'文本框-整数':None,'文本框-小数':None,'面板选择-树状选择框':None,'面板选择-地区选择框-多选选':None,'面板选择-地区选择框-单选':None,
    #     '自定义日期类型':'19951014','自定义日期时间':'19951014','自定义时分':'1014','自定义年月':'1995/10',
    #                                                               '文件上传-文件上传':None,'文件上传-图片上传':None,
    #                                                                 '文件上传-多文件上传':None,
    #                                                               '文件上传-多图片上传':None,
    #                                                               '多选框-复选框':['金','土'],
    #                                                              '人才模型':'哈哈哈',
    #                                                               '单选框-是否':'是',
    #                                                               '单选框-单选框':'飞机'})
    form_button_click(web_driver_initialize, "保存")

def test_add_talent_model(web_driver_initialize):
    """
    新增人才模型
    """

    go_to_menu(web_driver_initialize, '人才模型')
    list_button_click(web_driver_initialize, '新增')
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{'人才模型': '自动新增人才模型5'})
    form_button_click(web_driver_initialize, '保存')
    enter_iframe(web_driver_initialize, '//*[@class="round-pattern-tips-title"]')
    value = web_driver_initialize.find_element_by_xpath('//*[@class="round-pattern-tips-title"]').text
    data = web_driver_initialize.global_instance.get('case_data_dict').add_talent_model_date
    expected_results = data.get('预期结果')
    pytest_assume(web_driver_initialize, expected_results, value, '自动创建活动，页面显示添加成功')


def test_delete_talent_model(web_driver_initialize):
    """
    删除人才模型
    """
    go_to_menu(web_driver_initialize, '人才模型')
    click_check_index(web_driver_initialize, 1)
    list_button_click(web_driver_initialize, '删除')
    secondary_confirmation_button_click(web_driver_initialize, '是')
    explicit_waiting(web_driver_initialize, '//*[@class="round-pattern-tips-title"]',
                     element_attribute={'key': 'innerText', 'value': '删除成功'})
    value = web_driver_initialize.find_element_by_xpath('//*[@class="round-pattern-tips-title"]').text
    data = web_driver_initialize.global_instance.get('case_data_dict').delete_talent_model_date
    expected_results = data.get('预期结果')
    pytest_assume(web_driver_initialize, expected_results, value, '自动创建活动，页面显示删除成功')


def test_demo(web_driver_initialize):
    """
    新增人才模型
    """

    go_to_menu(web_driver_initialize, '人才模型')
    filter_item(web_driver_initialize, '名称', '管理高潜综合测评默认人才模型1')
    expected_results = '管理高潜综合测评默认人才模型1'
    actual_results = web_driver_initialize.find_elements_by_xpath(f'//*[@class="z-content-wrapper-fix"]/div/div/div/div[1]')[0].text
    pytest_assume(web_driver_initialize, expected_results, actual_results, '验证筛选出的内容为预期结果')
    print(1)


def test_dimension_add(web_driver_initialize):
    """
    维度分类-新增
    :param web_driver_initialize:
    :return:
    """
    go_to_menu(web_driver_initialize, '人才模型')
    list_button_click(web_driver_initialize, '新增')
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{'人才模型': '用于维度'})
    form_button_click(web_driver_initialize, '保存')
    time.sleep(3)
    go_to_data_details_by_field_name(web_driver_initialize, '人才模型', '用于维度')
    view_tab_button_click(web_driver_initialize, '维度分类')
    details_page_button_click(web_driver_initialize, '新增')
    time.sleep(2)
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{
        '维度分类': '自动测试分类',
        '计分规则': '平均值',
        '排序': 1
    })

    form_button_click(web_driver_initialize, '保存')
    time.sleep(3)

    view_tab_button_click(web_driver_initialize, '维度')
    details_page_button_click(web_driver_initialize, '新增')
    time.sleep(2)
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{
        '分类': '自动测试分类',
        '维度': '自动维度',
        '计分规则': '平均值',
        '排序': 1
    })

    form_button_click(web_driver_initialize, '保存')

    time.sleep(3)
    go_to_menu(web_driver_initialize, '人才模型')
    data_index = get_data_index(web_driver_initialize, '人才模型', '用于维度')
    click_check_index(web_driver_initialize, data_index)
    list_button_click(web_driver_initialize, '删除')
    secondary_confirmation_button_click(web_driver_initialize, '是')


def test_dimension_editor(web_driver_initialize):
    """
    维度分类-编辑
    :param web_driver_initialize:
    :return:
    """
    go_to_menu(web_driver_initialize, '人才模型')
    list_button_click(web_driver_initialize, '新增')
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{'人才模型': '用于维度'})
    form_button_click(web_driver_initialize, '保存')
    time.sleep(3)
    go_to_data_details_by_field_name(web_driver_initialize, '人才模型', '用于维度')
    view_tab_button_click(web_driver_initialize, '维度分类')
    details_page_button_click(web_driver_initialize, '新增')
    time.sleep(2)
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{
        '维度分类': '自动测试分类',
        '计分规则': '平均值',
        '排序': 1
    })

    form_button_click(web_driver_initialize, '保存')
    time.sleep(3)

    view_tab_button_click(web_driver_initialize, '维度')
    details_page_button_click(web_driver_initialize, '新增')
    time.sleep(2)
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{
        '分类': '自动测试分类',
        '维度': '自动维度',
        '计分规则': '平均值',
        '排序': 1
    })

    form_button_click(web_driver_initialize, '保存')
    time.sleep(3)
    data_index = get_data_index(web_driver_initialize, '维度', '自动维度')
    click_check_index(web_driver_initialize, data_index)
    details_page_button_click(web_driver_initialize, '编辑')
    time.sleep(2)
    fields_to_operate_on_list = get_form_view(web_driver_initialize)
    option_form(web_driver_initialize, fields_to_operate_on_list, **{
        '维度': '自动维度11',
    })

    form_button_click(web_driver_initialize, '保存')
    actual_results = web_driver_initialize.find_elements_by_xpath(
        f'//*[@class="z-content-wrapper-fix"]/div/div/div/div[1]')[0].text
    pytest_assume(web_driver_initialize, '自动维度11', actual_results, '校验维度新增成功')

    go_to_menu(web_driver_initialize, '人才模型')
    data_index = get_data_index(web_driver_initialize, '人才模型', '用于维度')
    click_check_index(web_driver_initialize, data_index)
    list_button_click(web_driver_initialize, '删除')
    secondary_confirmation_button_click(web_driver_initialize, '是')
