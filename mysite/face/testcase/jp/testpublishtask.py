#！/usr/bin/env python
#coding:utf-8
__author__ = 'caryr'
import time,re,unittest
from ..ci.common.ParaTestCase import ParametrizedTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import functools
result_test_flag = False

# class SkipTest(Exception):
#     '''Raise this exception in a test to skip it.'''
# def skip_result_if_task_exist(func):
#     """
#     Conditionally skip a test.
#     """
#     print("my_skip")
#     def decorator(self,*args,**kwargs):
#         if(self.flag == False):
#             return func(self,*args,**kwargs)
#         else:
#             return SkipTest
#     return decorator

class TestPublish(ParametrizedTestCase):
    @classmethod
    def setUpClass(cls):
        cls.flag = False
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.driver.get("http://"+cls.para['ip'])
        cls.username = cls.driver.find_element_by_id("txtUserName")
        cls.password = cls.driver.find_element_by_id("txtPassword")
        cls.login_button = cls.driver.find_element_by_css_selector("input[value^='登    录']")
        # 进入超级管理员账号获取校级管理员
        cls.super_account = cls.para['ip'].split(':')[0]+'|mycos@admin'
        cls.username.send_keys(cls.super_account)
        cls.password.send_keys(cls.para['superpassword'])
        cls.login_button.click()
        close_list = cls.driver.find_elements_by_css_selector("button[i='close']")
        close_list[1].click()
        close_list[0].click()
        cls.driver.find_element_by_css_selector("div[class^='navList js_system']").click()
        cls.driver.find_element_by_css_selector("a[class^='js_system_role NoSemester']").click()
        cls.driver.switch_to.frame("iframeBody")
        cls.driver.find_element_by_css_selector("a[class^='member js_editrole'][data-name='学校管理员']").click()
        cls.driver.switch_to.default_content()
        manager_table = cls.driver.find_element_by_id("bodybinds")
        maneger_account = manager_table.find_element_by_css_selector("tr td+td").text
        close_button = cls.driver.find_element_by_css_selector("button[i='close']")
        close_button.click()
        cls.driver.find_element_by_css_selector("a[class^='js_goout']").click()
        # 进入校级管理员
        cls.username = cls.driver.find_element_by_id("txtUserName")
        cls.password = cls.driver.find_element_by_id("txtPassword")
        cls.login_button = cls.driver.find_element_by_css_selector("input[value^='登    录']")
        cls.username.send_keys(maneger_account)
        cls.password.send_keys(cls.para['password'])
        cls.login_button.click()
        close_list = cls.driver.find_elements_by_css_selector("button[i='close']")
        close_list[1].click()
        close_list[0].click()
        cls.help_close_div = cls.driver.find_element_by_css_selector("div[class^='helpInfo']")
        cls.help_close_span = cls.help_close_div.find_element_by_css_selector("span")
        cls.help_close_span.click()
# 答题
    def answer_question(self,driver2):
        # 单选
        single_questions = driver2.find_elements_by_css_selector("dl[id^='subject'][stype='1']")
        for question in single_questions:
            if (not (question.get_attribute("style") == 'display: none;')):
                question.find_element_by_css_selector("a[class^='jqTransformRadio']").click()
                time.sleep(0.5)
        # 多选
        multi_questions = driver2.find_elements_by_css_selector("dl[id^='subject'][stype='2']")
        for question in multi_questions:
            if (not (question.get_attribute("style") == 'display: none;')):
                question.find_element_by_css_selector("a[class^='jqTransformCheckbox']").click()
        # 矩阵单选
        matrix_single_questions = driver2.find_elements_by_css_selector("dl[id^='subject'][stype='31']")
        for question in matrix_single_questions:
            if (not (question.get_attribute("style") == 'display: none;')):
                subjectitems = question.find_elements_by_css_selector("a[class^='jqTransformRadio']")
                for subjectitem in subjectitems:
                    subjectitem.click()
        # 填空和意见反馈
        text_questions = driver2.find_elements_by_css_selector("dl[id^='subject'][stype='3']")
        for question in text_questions:
            if (not (question.get_attribute("style") == 'display: none;')):
                question.find_element_by_css_selector("textarea[class^='option']").send_keys("填空题")
        # 打分题
        score_questions = driver2.find_elements_by_css_selector("dl[id^='subject'][stype='4']")
        for question in score_questions:
            if (not (question.get_attribute("style") == 'display: none;')):
                subjectitems = question.find_elements_by_css_selector("td[class^='score_bar']")
                for subjectitem in subjectitems:
                    subjectitem.click()
        # 矩阵打分
        matrix_score_questions = driver2.find_elements_by_css_selector("dl[id^='subject'][stype='34']")
        for question in matrix_score_questions:
            if (not (question.get_attribute("style") == 'display: none;')):
                subjectitems = question.find_elements_by_css_selector("td[class^='score_td']")
                for subjectitem in subjectitems:
                    subjectitem.find_element_by_css_selector("img").click()
        # 拖拉题
        drag_questions = driver2.find_elements_by_css_selector("dl[id^='subject'][stype='8']")
        for drag_question in drag_questions:
            subjectitems = drag_question.find_elements_by_css_selector("a[class^='slider-handle']")
            for subjectitem in subjectitems:
                driver2.execute_script("arguments[0].setAttribute('style', arguments[1]);", subjectitem,
                                           "left: 680px;")
        # 提交答卷
        driver2.find_element_by_id("next_button").click()
        time.sleep(2)
        return 1

    def create_question(self,flag=None):
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("li[stype^='1']").click()
        if(flag=='result'):
            time.sleep(2)
            subjectitem = self.driver.find_element_by_css_selector("div[class^='editOption']")
            ActionChains(self.driver).move_to_element(subjectitem).perform()
            set_score_a = self.driver.find_element_by_css_selector("a[class^='setScore']")
            #self.driver.execute_script("arguments[0].style.display='inline';",set_score_a)
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", set_score_a,
                                   "visibility: visible;")
            time.sleep(1)
            set_score_a.click()
            time.sleep(0.5)
            #self.driver.switch_to.default_content()
            score_form = self.driver.find_element_by_id("setscore_form")
            score_input = score_form.find_element_by_css_selector("ul li+li input")
            score_input.clear()
            score_input.send_keys("60")
            self.driver.find_element_by_id("setscoreForNotePerNext").click()
            #self.driver.switch_to.frame("iframeBody")
        self.driver.find_element_by_css_selector("li[stype^='2']").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("li[stype^='3']").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("li[stype^='4']").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("li[stype^='31']").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("li[stype^='34']").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("li[stype^='8']").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("li[stype^='5']").click()
        time.sleep(0.5)

    def direct_to_homepage(self):
        try:
            self.driver.refresh()
            self.driver.switch_to.alert.accept()
        except:
            pass
# 即时性创建-回答-删除问卷

    @unittest.skip("instantaneity")
    def test_aa_create_instantaneity(self):
        #self.direct_to_homepage()
        self.driver.find_element_by_css_selector("div[class^='navList js_general']").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("a[class^='js_general_q NoSemester']").click()
        time.sleep(3)
        #self.frame1 = self.driver.find_element_by_id("iframepage")
        self.driver.switch_to.frame("iframepage")
        self.driver.find_element_by_css_selector("a[class^='add js_create']").click()
        #self.driver.find_element_by_css_selector("a[class^='jqTransformRadio jqTransformChecked']").click()
        self.driver.find_element_by_css_selector("input[class^='js_name']").send_keys("publishCRinstantaneity")
        self.driver.find_element_by_css_selector("a[class^='mr0 js_nextstep release']").click()
        #等待题型加载
        self.create_question()
        self.next_parent = self.driver.find_element_by_id("designSurvey")
        #等待下一步
        time.sleep(1)
        #self.next_step = self.next_parent.find_elements_by_css_selector("a")[3]
        #time.sleep(0.5)
        #self.next_step.click()
        #js = "var q=document.body.scrollTop=100000"
        #js_down = "window.scrollTo(0,80);"
        #js_top = "document.documentElement.scrollTop"
        #self.driver.execute_script(js_top)
        #ActionChains(self.driver).click(self.next_step).perform()
        self.driver.find_element_by_css_selector("a[class^='button fR ml15 release NoSemester']").click()
        #self.driver.find_element_by_css_selector("a[class^='jqTransformRadio']").click()
        self.driver.find_element_by_css_selector("a[class^='mr0 js_nextstep release']").click()
        #start_time =
        #plus 09-18-17:39
        time.sleep(2)
        self.driver.find_element_by_id("txtStart").send_keys("2016-09-18 17:30")
        self.driver.find_element_by_id("txtEnd").send_keys("2018-09-19 17:30")
        #self.driver.find_element_by_id("txtStart").click()
        #self.frame2 = self.driver.find_element_by_css_selector("iframe[name^='_my97DPFrame']")
        # self.driver.switch_to.default_content()
        # self.driver.switch_to.frame('_my97DPFrame')
        # start_time_set = self.driver.find_element_by_css_selector("td[class='Wselday']")
        # ActionChains(self.driver).move_to_element(start_time_set).click().perform()
        # self.driver.switch_to.default_content()
        #end_time =
        #self.driver.switch_to.frame('iframepage')
        #self.driver.find_element_by_id("txtEnd").click()
        # self.driver.switch_to.default_content()
        # self.driver.switch_to.frame('_my97DPFrame')
        # end_time_set = self.driver.find_element_by_css_selector("td[class='Wselday']")
        # ActionChains(self.driver).move_to_element(end_time_set).click().perform()
        # self.driver.switch_to.default_content()
        # self.driver.switch_to().frame("iframepage")
        time.sleep(1)
        self.driver.find_element_by_id("btnPublish").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_css_selector("a[class^='js_general_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        task_name_a_list = self.driver.find_elements_by_css_selector("a[class^='js_preview underline']")
        name_list = []
        for task_name_a in task_name_a_list:
            name_list.append(task_name_a.text)
        self.driver.switch_to.default_content()
        self.assertIn("publishCRinstantaneity",name_list)

    @unittest.skip("instantaneity")
    def test_ab_answer_instantaneity(self):
        self.direct_to_homepage()
        self.driver.find_element_by_css_selector("div[class^='navList js_general']").click()
        self.driver.find_element_by_css_selector("a[class^='js_general_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        link = self.driver.find_element_by_css_selector("a[data-title^='问卷链接']")
        link.click()
        link_text_obj = self.driver.find_element_by_id("txtLink")
        link = link_text_obj.text
        driver2 = webdriver.Chrome()
        driver2.implicitly_wait(10)
        driver2.get(link)
        self.answer_question(driver2)
        driver2.quit()
        self.driver.switch_to.default_content()
        time.sleep(4)
        self.driver.find_element_by_css_selector("a[class^='js_general_q NoSemester']").click()
        time.sleep(1)
        self.driver.switch_to.frame("iframepage")
        table_instantaneity = self.driver.find_element_by_id("queryresult")
        task_tr = table_instantaneity.find_element_by_css_selector("div table tbody tr")
        task_td = task_tr.find_elements_by_css_selector("td")
        task_answer_count = task_td[8].text
        self.driver.switch_to.default_content()
        self.assertEqual(task_answer_count,'1 ')

    @unittest.skip("instantaneity")
    def test_ac_delete_instantaneity(self):
        self.direct_to_homepage()
        self.driver.find_element_by_css_selector("div[class^='navList js_general']").click()
        self.driver.find_element_by_css_selector("a[class^='js_general_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        table_instantaneity = self.driver.find_element_by_id("queryresult")
        task_tr = table_instantaneity.find_element_by_css_selector("div table tbody tr")
        task_td = task_tr.find_elements_by_css_selector("td")
        if(task_td[2].text == 'publishCRinstantaneity'):
            ActionChains(self.driver).move_to_element(task_td[0]).click().perform()
            self.driver.find_element_by_css_selector("a[class^='js_batch_delete']").click()
            self.driver.switch_to.default_content()
            self.driver.find_element_by_css_selector("button[data-id^='ok']").click()
            self.direct_to_homepage()
            self.driver.find_element_by_css_selector("div[class^='navList js_general']").click()
            self.driver.find_element_by_css_selector("a[class^='js_general_q NoSemester']").click()
            self.driver.switch_to.frame("iframepage")
            task_name_a_list = self.driver.find_elements_by_css_selector("a[class^='js_preview underline']")
            name_list = []
            for task_name_a in task_name_a_list:
                name_list.append(task_name_a.text)
            self.driver.switch_to.default_content()
            if('' not in name_list):
                self.assertNotIn("publishCRinstantaneity",name_list)
            else:
                self.assertNotIn("",name_list)
        else:
            self.assertEqual("Not in list","Not in list")

    @unittest.skip("process")
    def test_ba_create_process(self):
        self.direct_to_homepage()
        self.driver.find_element_by_css_selector("div[class^='navList js_process']").click()
        self.driver.find_element_by_css_selector("a[class^='js_process_q NoSemester']").click()
        time.sleep(3)
        self.driver.switch_to.frame("iframepage")
        self.driver.find_element_by_css_selector("a[class^='add js_create']").click()
        self.driver.find_element_by_css_selector("input[class^='js_name']").send_keys("publishCRprocess")
        self.driver.find_element_by_css_selector("a[class^='mr0 js_nextstep release']").click()
        # 等待题型加载
        time.sleep(3)
        self.driver.find_element_by_css_selector("li[stype^='1']").click()
        self.next_parent = self.driver.find_element_by_id("designSurvey")
        time.sleep(1)
        self.next_step = self.next_parent.find_elements_by_css_selector("a")[3]
        ActionChains(self.driver).click(self.next_step).perform()
        self.driver.find_element_by_css_selector("a[class^='add respondentAdd btnAdd']").click()
        self.driver.switch_to.default_content()
        all_div = self.driver.find_element_by_css_selector("div[class^='clearfix']")
        time.sleep(1)
        all_div.find_element_by_css_selector("p span a").click()
        self.driver.find_element_by_css_selector("input[class^='dlgOK confirm'][value^='确定']").click()
        time.sleep(6)
        self.driver.switch_to.frame("iframepage")
        self.driver.find_element_by_id("btnSend").click()
        WebDriverWait(self.driver,10).until(lambda x:x.find_element_by_id("txtStart"))
        self.driver.find_element_by_id("txtStart").send_keys("2017-09-18 17:30")
        self.driver.find_element_by_id("txtEnd").send_keys("2018-09-19 17:30")
        self.driver.find_element_by_id("js_publish").click()
        #WebDriverWait(self.driver, 20).until(lambda x: x.find_element_by_css_selector("div[class^='main tip']"))
        time.sleep(12)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_css_selector("a[class^='js_process_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        task_name_a_list = self.driver.find_elements_by_css_selector("a[class^='js_preview underline']")
        name_list = []
        for task_name_a in task_name_a_list:
            name_list.append(task_name_a.text)
        self.driver.switch_to.default_content()
        self.assertIn("publishCRprocess", name_list)

    @unittest.skip("process")
    def test_bb_answer_process(self):
        self.direct_to_homepage()
        self.driver.find_element_by_css_selector("div[class^='navList js_process']").click()
        self.driver.find_element_by_css_selector("a[class^='js_process_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        table_instantaneity = self.driver.find_element_by_id("queryresult")
        task_tr = table_instantaneity.find_element_by_css_selector("div table tbody tr")
        task_td = task_tr.find_elements_by_css_selector("td")
        if(task_td[2].text == 'publishCRprocess'):
            task_tr.find_element_by_css_selector("a[data-title^='查看结果']").click()
            self.driver.find_element_by_css_selector("a[class^='toAddSearchHref'][data-title='查看结果']").click()
            task_student_ul = self.driver.find_element_by_css_selector("ul[class^='createNav setCollect chooseCreateMode js_nav']")
            task_student_ul.find_element_by_css_selector("li+li+li").click()
            self.driver.find_element_by_css_selector("a[class^='accomplish fL']").click()
            student_num_td = self.driver.find_element_by_id("bodybind").find_element_by_css_selector("tr td+td")
            student_num = student_num_td.text
#新开浏览器答题
        driver2 = webdriver.Chrome()
        driver2.implicitly_wait(10)
        driver2.get(self.para['ip'])
        username = driver2.find_element_by_id("txtUserName")
        password = driver2.find_element_by_id("txtPassword")
        login_button = driver2.find_element_by_css_selector("input[value^='登    录']")
        username.send_keys(student_num)
        password.send_keys("00606f295a45485ba63671b6f8612213@")
        login_button.click()
        close_list = driver2.find_element_by_css_selector("button[i='close']")
        close_list.click()
#新开的网页
        driver2.switch_to.frame("iframeBody")
        driver2.find_element_by_id("txtName").send_keys("publishCRprocess")
        time.sleep(0.5)
        driver2.find_element_by_id("btnName").click()
        time.sleep(1)
        driver2.find_element_by_css_selector("a[class='mcopen']").click()
        #link = driver2.find_element_by_css_selector("a[class^='mcopen underline']")
        #ActionChains(driver2).move_to_element(link).click().perform()
        #task_table = driver2.find_element_by_id("tblQuestion")
        #task_table.find_element_by_css_selector("a").click()
        driver2.switch_to.default_content()
        time.sleep(3)
        for window_index in driver2.window_handles:
            driver2.switch_to.window(window_index)
            if(driver2.title=='publishCRprocess'):
                self.answer_question(driver2)
                driver2.quit()
                break
#查看结果
        time.sleep(4)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_css_selector("a[class^='js_process_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        table_instantaneity = self.driver.find_element_by_id("queryresult")
        task_tr = table_instantaneity.find_element_by_css_selector("div table tbody tr")
        task_td = task_tr.find_elements_by_css_selector("td")
        task_answer_count = task_td[8].text
        self.driver.switch_to.default_content()
        pattern = re.compile(r"(\d)/")
        real_result = pattern.findall(task_answer_count)[0]
        self.assertEqual(real_result,'1')

    @unittest.skip("process")
    def test_bc_delete_process(self):
        self.direct_to_homepage()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("div[class^='navList js_process']").click()
        self.driver.find_element_by_css_selector("a[class^='js_process_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        table_instantaneity = self.driver.find_element_by_id("queryresult")
        task_tr = table_instantaneity.find_element_by_css_selector("div table tbody tr")
        task_td = task_tr.find_elements_by_css_selector("td")
        if(task_td[2].text == 'publishCRprocess'):
            ActionChains(self.driver).move_to_element(task_td[0]).click().perform()
            self.driver.find_element_by_css_selector("a[class^='js_batch_delete']").click()
            self.driver.switch_to.default_content()
            self.driver.find_element_by_css_selector("button[data-id^='ok']").click()
        self.driver.find_element_by_css_selector("a[class^='js_process_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        task_name_a_list = self.driver.find_elements_by_css_selector("a[class^='js_preview underline']")
        name_list = []
        for task_name_a in task_name_a_list:
            name_list.append(task_name_a.text)
        self.driver.switch_to.default_content()
        if('' not in name_list):
            self.assertNotIn("publishCRprocess",name_list)
        else:
            self.assertNotIn("",name_list)

    #@unittest.skip("result")
    def test_ca_judge_result_test(self):
        self.direct_to_homepage()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
        self.driver.find_element_by_css_selector("a[class^='js_result_q NoSemester']").click()
        time.sleep(1)
        self.driver.switch_to.frame("iframepage")
        task_tbody = self.driver.find_element_by_css_selector("tbody[class^='jqtransformdone']")
        task = task_tbody.find_elements_by_css_selector("tr td")
        if(len(task)>2):
            globals()['result_test_flag'] = True
            self.assertEqual("exist"," result task")
        else:
            self.assertEqual("test","test")

    #@unittest.skip("result")
    def test_cb_create_result_template(self):
        if(globals()['result_test_flag'] == True):
            self.assertTrue(False,"已有结果性评价任务")
        self.direct_to_homepage()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
        self.driver.find_element_by_css_selector("a[class^='js_result_t NoSemester']").click()
        self.driver.switch_to.frame("iframeBody")
        self.driver.find_element_by_css_selector("a[class^='add js_add']").click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_css_selector("input[class=' required js_name']").send_keys("TemplateCRresult")
        self.driver.find_element_by_css_selector("input[class^='js_ok confirm']").click()
        self.driver.switch_to.frame("iframeBody")
        templeta_table = self.driver.find_element_by_css_selector("tbody[class='jqtransformdone']")
        first_template_td = templeta_table.find_elements_by_css_selector("tr td")
        if(len(first_template_td)>2 and first_template_td[1].text=='TemplateCRresult'):
            first_template_td[2].find_element_by_css_selector('a').click()
            self.create_question(flag='result')
            design_button = self.driver.find_element_by_id("designSurvey")
            design_button.find_elements_by_css_selector("a")[2].click()
            templeta_table = self.driver.find_element_by_css_selector("tbody[class='jqtransformdone']")
            first_template_td = templeta_table.find_elements_by_css_selector("tr td")
            student_Q = first_template_td[2].find_element_by_css_selector('a').text
            self.assertEqual("编辑", student_Q)
        else:
            self.assertEqual("1","Create Template Fail")

    @unittest.skip("result")
    def test_cc_create_result(self):
        if(self.flag == True):
            self.assertTrue(False,"已有结果性评价任务")
        self.direct_to_homepage()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
        self.driver.find_element_by_css_selector("a[class^='js_result_q NoSemester']").click()
        time.sleep(3)
        self.driver.switch_to.frame("iframepage")
        self.driver.find_element_by_css_selector("a[class^='add js_createtask']").click()
        self.driver.find_element_by_css_selector("tr[class^='createTr']").click()
        self.driver.find_element_by_css_selector("input[class^='js_name']").send_keys("publishCRresult")
        self.driver.find_element_by_css_selector("a[class^='mr0 js_nextstep release']").click()
        #选择调查对象
        #WebDriverWait(self.driver,10).until(lambda x: x.find_element_by_css_selector("div[class^='filtrateShowChoose formStyle']"))
        #survey_obj = self.driver.find_element_by_css_selector("div[class^='filtrateShowChoose formStyle']")
        #self.driver.switch_to.default_content()
        time.sleep(2)
        survey_obj = self.driver.find_element_by_id("persontype")
        obj_list_p = survey_obj.find_elements_by_css_selector("div p")
        for obj in obj_list_p:
            if(obj.text.find("学生")+1):
                obj.find_element_by_css_selector("span a").click()
                break
        survey_filed = self.driver.find_element_by_id("tabheader")
        filed_list_p = survey_filed.find_elements_by_css_selector("div p")
        for filed in filed_list_p:
            if(filed.text.find("课程")+1):
                filed.find_element_by_css_selector("span a").click()
                break
        # 一键添加
        #self.driver.switch_to.frame("iframepage")
        self.driver.find_element_by_css_selector("a[class^='add respondentAdd btnAdd']").click()
        self.driver.switch_to.default_content()
        time.sleep(1)
        self.driver.find_element_by_css_selector("a[class='jqTransformCheckbox']").click()
        self.driver.find_element_by_css_selector("input[class^='dlgOK confirm']").click()
        time.sleep(3)
        self.driver.find_element_by_css_selector("input[class^='dlgCancel']").click()
        self.driver.switch_to.frame("iframepage")
        self.driver.find_element_by_id("btnNext").click()
        self.driver.find_element_by_css_selector("input[class^='js_ststartdate']").send_keys("2017-09-18 17:30")
        self.driver.find_element_by_css_selector("input[class^='js_stenddate']").send_keys("2018-09-18 17:30")
        # self.driver.find_element_by_css_selector("input[class^='js_thstartdate']").send_keys("2017-09-18 17:30")
        # self.driver.find_element_by_css_selector("input[class^='js_thenddate']").send_keys("2017-09-18 17:30")
        self.driver.find_element_by_id("js_publish").click()
        time.sleep(15)
        self.driver.switch_to.default_content()
        # self.driver.refresh()
        # self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
        self.driver.find_element_by_css_selector("a[class^='js_result_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        task_tbody = self.driver.find_element_by_css_selector("tbody[class^='jqtransformdone']")
        task = task_tbody.find_elements_by_css_selector("tr td")
        task_name = task[2].text
        self.driver.switch_to.default_content()
        self.assertEqual("publishCRresult", task_name)

    #@unittest.skip("result")
    def test_cd_answer_result(self):
        if(self.flag == True):
            self.assertTrue(False,"已有结果性评价任务")
        self.direct_to_homepage()
        self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
        self.driver.find_element_by_css_selector("a[class^='js_result_q NoSemester']").click()
        self.driver.switch_to.frame("iframepage")
        table_result = self.driver.find_element_by_id("resultData")
        task_tr = table_result.find_element_by_css_selector("table tbody tr")
        task_td = task_tr.find_elements_by_css_selector("td")
        if(task_td[2].text == 'publishCRresult'):
            task_tr.find_element_by_css_selector("a[data-title^='查看结果']").click()
            self.driver.find_element_by_css_selector("a[class^='toAddSearchHref'][data-title='查看学生结果']").click()
            task_student_ul = self.driver.find_element_by_css_selector("ul[class^='createNav setCollect chooseCreateMode js_nav']")
            task_student_ul.find_element_by_css_selector("li+li+li").click()
            self.driver.find_element_by_css_selector("a[class^='accomplish fL']").click()
            student_num_td = self.driver.find_element_by_id("bodybind").find_element_by_css_selector("tr td+td")
            student_num = student_num_td.text
            driver2 = webdriver.Chrome()
            driver2.implicitly_wait(10)
            driver2.get("http://"+self.para['ip'])
            username = driver2.find_element_by_id("txtUserName")
            password = driver2.find_element_by_id("txtPassword")
            login_button = driver2.find_element_by_css_selector("input[value^='登    录']")
            username.send_keys(student_num)
            password.send_keys("00606f295a45485ba63671b6f8612213@")
            login_button.click()
            close_list = driver2.find_element_by_css_selector("button[i='close']")
            close_list.click()
            # 新开的网页
            driver2.switch_to.frame("iframepage")
            driver2.find_element_by_id("txtName").send_keys("publishCRresult")
            driver2.find_element_by_id("btnName").click()
            time.sleep(2)
            driver2.find_element_by_css_selector("a[class^='mcopen underline']").click()
            driver2.switch_to.default_content()
            time.sleep(3)
            for window_index in driver2.window_handles:
                driver2.switch_to.window(window_index)
                if (driver2.title == 'publishCRresult'):
                    self.answer_question(driver2)
                    time.sleep(10)
                    break
            driver2.quit()
            self.driver.switch_to.default_content()
            time.sleep(8)
            self.driver.find_element_by_css_selector("a[class^='js_result_q NoSemester']").click()
            self.driver.switch_to.frame("iframepage")
            task_tbody = self.driver.find_element_by_css_selector("tbody[class^='jqtransformdone']")
            task = task_tbody.find_elements_by_css_selector("tr td")
            task_answer_count = task[4].text
            self.driver.switch_to.default_content()
            pattern = re.compile(r"(\d)/")
            real_result = pattern.findall(task_answer_count)[0]
            self.assertEqual(real_result, '1')
        else:
            self.assertEquals("have Task","No Task")

    @unittest.skip("result")
    def test_ce_delete_result(self):
        if(self.flag == True):
            self.assertTrue(False,"已有结果性评价任务")
        self.direct_to_homepage()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
        self.driver.find_element_by_css_selector("a[class^='js_result_q NoSemester']").click()
        time.sleep(2)
        self.driver.switch_to.frame("iframepage")
        task_tbody = self.driver.find_element_by_css_selector("tbody[class^='jqtransformdone']")
        task = task_tbody.find_elements_by_css_selector("tr td")
        task_name = task[2].text
        if(task_name=='publishCRresult'):
            task[0].find_element_by_css_selector("span a").click()
            self.driver.find_element_by_css_selector("a[class^='js_batchdelete']").click()
            self.driver.switch_to.default_content()
            self.driver.find_element_by_css_selector("button[data-id^='ok']").click()
        #self.driver.switch_to.default_content()
            self.direct_to_homepage()
            time.sleep(0.5)
            self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
            self.driver.find_element_by_css_selector("a[class^='js_result_q NoSemester']").click()
            self.driver.switch_to.frame("iframepage")
            task_tbody = self.driver.find_element_by_css_selector("tbody[class^='jqtransformdone']")
            task = task_tbody.find_elements_by_css_selector("tr td")
            if(len(task)>2):
                task_name = task[2].text
                self.driver.switch_to.default_content()
                if(task_name!=''):
                    self.assertNotEqual("publishCRresult",task_name)
                else:
                    self.assertNotEqual('',task_name)
            else:
                self.assertEqual('1','1')
        else:
            self.assertNotEqual("publishCRresult",task_name)

    #@unittest.skip("result")
    def test_cf_delete_template(self):
        if(self.flag == True):
            self.assertTrue(False,"已有结果性评价任务")
        self.direct_to_homepage()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
        self.driver.find_element_by_css_selector("a[class^='js_result_t NoSemester']").click()
        self.driver.switch_to.frame("iframeBody")
        templeta_table = self.driver.find_element_by_css_selector("tbody[class='jqtransformdone']")
        first_template_td = templeta_table.find_elements_by_css_selector("tr td")
        task_name = first_template_td[1].text
        if (task_name == 'TemplateCRresult'):
            first_template_td[0].find_element_by_css_selector("span a").click()
            self.driver.find_element_by_css_selector("a[class^='js_batchd_delete']").click()
            self.driver.switch_to.default_content()
            self.driver.find_element_by_css_selector("button[data-id^='ok']").click()
            # self.driver.switch_to.default_content()
            #检查成功删除没有
            self.direct_to_homepage()
            time.sleep(0.5)
            self.driver.find_element_by_css_selector("div[class^='navList js_result']").click()
            self.driver.find_element_by_css_selector("a[class^='js_result_t NoSemester']").click()
            self.driver.switch_to.frame("iframepage")
            task_tbody = self.driver.find_element_by_css_selector("tbody[class^='jqtransformdone']")
            task = task_tbody.find_elements_by_css_selector("tr td")
            if (len(task) > 2):
                task_name = task[1].text
                self.driver.switch_to.default_content()
                if (task_name != ''):
                    self.assertNotEqual("TemplateCRresult", task_name)
                else:
                    self.assertNotEqual('',task_name)
            else:
                self.assertEqual('0', '0')
        else:
            self.assertNotEqual("publishCRresult", task_name)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
