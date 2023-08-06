# -*- coding: UTF-8 -*-
import smtplib
import os.path
from loguru import logger
import email.mime.multipart
import email.mime.text
import email.mime.base
import traceback

mail_host = "smtp.exmail.qq.com"  # 使用的邮箱的smtp服务器地址
mail_port = 465
mail_user = "huzhiming@bixin.cn"  # 用户名
mail_pass = "fRDf8G3VJFfSXicr"  # 密码
pre_title = "Monkey测试报告"
mail_postfix = "@bixin.cn"  # 邮箱的后缀


class Mail(object):
    """[summary]

    Arguments:
        object {[type]} -- [description]

    Returns:

    """

    def sendMail(self,
                 content: str,
                 toMailList: list = None,
                 title: str = pre_title,
                 attchFilepath: str = None,
                 host: str = mail_host,
                 port: int = mail_port,
                 username: str = mail_user,
                 password: str = mail_pass,
                 isHtml: bool = False):
        """[summary]
        邮件发送功能
        导入包后通过使用Mail().sendMail(.....)进行发送
        注意：需要使用时严禁使用循环语句，避免大批量发送导致发送邮箱被禁用
        Arguments:
            title {[String]} -- [主题]
            content {[String]} -- [邮件内容]
            toMailList {[String]} -- [收件人列表]

        Keyword Arguments:
            attchFilepath {[String]} -- [附件路径] (default: {None})
            host {[String]} -- [发送方伺服地址] (default: {mail_host})
            username {[String]} -- [发送方邮箱地址] (default: {mail_user})
            password {[String]} -- [发送方密码] (default: {mail_pass})

        Returns:
            [Boolean] -- [发送成功返回True，失败False]
        """
        toMailList = [receiver + mail_postfix for receiver in toMailList]
        # 登录
        server = smtplib.SMTP_SSL(host, port=port)
        server.login(username, password)  # 仅smtp服务器需要验证时
        # 构造MIMEMultipart对象做为根容器
        main_msg = email.mime.multipart.MIMEMultipart()
        # 构造MIMEText对象做为邮件显示内容并附加到根容器
        if isHtml:
            text_msg = email.mime.text.MIMEText(content, 'html', 'utf-8')
        else:
            text_msg = email.mime.text.MIMEText(content)
        main_msg.attach(text_msg)
        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)
        if attchFilepath is not None:
            try:
                # 读入文件内容并格式化 [方式2]
                data = open(attchFilepath, 'rb')
                file_msg = email.mime.base.MIMEBase(maintype, subtype)
                file_msg.set_payload(data.read())
                data.close()
                email.Encoders.encode_base64(file_msg)  # 把附件编码
                # 设置附件头
                basename = os.path.basename(attchFilepath)
                file_msg.add_header('Content-Disposition',
                                    'attachment',
                                    filename=basename)  # 修改邮件头
                main_msg.attach(file_msg)
            except IOError:
                msg = "邮件发送失败，「{0}」路径下文件缺失".format(attchFilepath)
                logger.warning(msg)
                text_msg = email.mime.text.MIMEText("\n邮件发送失败，附件文件缺失，请联系相关开发检查附件路径及资源！")
                main_msg.attach(text_msg)
                return msg
        # 设置根容器属性
        main_msg['From'] = username
        main_msg['To'] = ";".join(toMailList)
        main_msg['Subject'] = title
        main_msg['Date'] = email.utils.formatdate()
        # 得到格式化后的完整文本
        fullText = main_msg.as_string()
        # 用smtp发送邮件
        try:
            server.sendmail(username, toMailList, fullText)
            msg = "邮件已经成功发送"
            logger.info(msg)
        except BaseException as e:
            msg = "发送失败，发送邮件中途错误"
            logger.error("{0}:{1}".format(msg, traceback.format_exc()))
            raise e
        finally:
            server.quit()
            return msg


if __name__ == '__main__':
    print("请确认现在在调试")
