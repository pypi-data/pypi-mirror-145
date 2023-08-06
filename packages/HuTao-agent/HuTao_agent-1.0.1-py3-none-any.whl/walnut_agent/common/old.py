

'''旧版case,聊天页'''
import time
from walnut_agent.common import config


def test_a_massage(self):
    """消息页操作"""
    # start_app("com.yangle.xiaoyuzhou")
    poco = self.poco
    time.sleep(1)
    # 点击关注页
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/tvTitle").click()
    time.sleep(2)
    # 向上滑动一页
    poco.up()
    time.sleep(2)
    poco.find_element_by_Name("android.view.ViewGroup")[config.num].click()
    poco.find_element_by_Text("私信").click()
    # poco("com.yangle.xiaoyuzhou:id/et_chat").click()
    # # 发消息
    # poco(name="com.yangle.xiaoyuzhou:id/et_chat").set_text(texts[num])
    # poco(name="com.yangle.xiaoyuzhou:id/btnSend").click()
    # touch((100,100))
    # 点击表情
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/tvChangeKeyboard").click()
    # 选择表情
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/ivEmotion")[0].click()
    # 点击照片
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/btnSendImage").click()
    # 选择照片
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/media_thumbnail")[config.num].click()
    time.sleep(1)
    poco.find_element_by_Name("android.widget.TextView").click()
    time.sleep(1)
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/tv_next_step").click()
    time.sleep(2)
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/btnSendGift").click()
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/btnRewardSend").click()
    # 点击空白让礼物的浮层影藏
    poco.right()
    # 返回消息页，点击发送消息的用户
    # poco(name="com.yangle.xiaoyuzhou:id/toolbarButtonText").click()
    # poco(name="com.yangle.xiaoyuzhou:id/toolbarButtonText").click()
    # poco(name="com.yangle.xiaoyuzhou:id/toolbarButtonText").click()
    # poco(name="com.yangle.xiaoyuzhou:id/toolbarButtonText").click()
    # poco(text="消息").click()
    # poco("android.widget.LinearLayout").offspring("com.yangle.xiaoyuzhou:id/fl_main").child(
    #     "android.widget.FrameLayout").offspring("com.yangle.xiaoyuzhou:id/viewPager").offspring(
    #     "com.yangle.xiaoyuzhou:id/rlvConversationList").child("android.view.ViewGroup")[0].click()
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/et_chat").set_text(config.texts[config.num])
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/btnSend").click()
    time.sleep(1)
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/toolbarButtonText")[1].click()
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/swNotDisturb").click()
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/swTopMsg").click()
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/swDefriend").click()
    poco.find_element_by_Text("确定").click()
    # 举报屏蔽，举报损失测试账号
    # poco(text="举报").click()
    # time.sleep(10)
    # poco("android.widget.LinearLayout").offspring("com.yangle.xiaoyuzhou:id/content").child("android.widget.FrameLayout").offspring("com.yangle.xiaoyuzhou:id/refresh_layout_child_container").child("android.webkit.WebView").child("android.webkit.WebView").offspring("android.widget.ListView").child("android.view.View")[7].child("android.view.View")[1].click()
    # poco("com.yangle.xiaoyuzhou:id/refresh_layout").swipe([-0.1441, -0.4993])
    # poco("com.yangle.xiaoyuzhou:id/refresh_layout").swipe([0.0202, -0.3418])
    # # 点击同意平台内容
    # poco("android.widget.LinearLayout").offspring("com.yangle.xiaoyuzhou:id/content").child(
    #     "android.widget.FrameLayout").offspring("com.yangle.xiaoyuzhou:id/refresh_layout_child_container").child(
    #     "android.webkit.WebView").child("android.webkit.WebView").child("android.view.View").child(
    #     "android.view.View")[8].child("android.view.View")[0].child("android.view.View").click()
    # poco(text="提交").click()
    # poco(text="点击关闭").click()
    # time.sleep(2)
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/toolbarButtonText").click()
    time.sleep(1)
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/toolbarButtonText").click()
    time.sleep(1)
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/toolbarButtonText").click()

    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/toolbarButtonText").click()
    poco.find_element_by_Name("com.yangle.xiaoyuzhou:id/toolbarButtonText").click()
    poco.find_element_by_Text("我的").click()

    # 回到我的页面
    print("=====测试结束：完成发消息，表情，礼物，置顶，免打扰，拉黑，举报====")