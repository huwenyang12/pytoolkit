import email
import imaplib
import time
from pathlib import Path
from email.header import decode_header,make_header

class MailMonitor:
    def __init__(self,email_addr,password,imap_server,imap_port=993,download_dir="attachments"):
        self.email_addr = email_addr
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True,exist_ok=True)


    def check(self,subject_keywords=None,attachment_keywords=None):
        """检查未读邮件并下载附件"""
        mail = imaplib.IMAP4_SSL(self.imap_server,self.imap_port)
        mail.login(self.email_addr,self.password)
        mail.select("INBOX")
        _,data = mail.search(None,"UNSEEN")
        downloaded = []
        for mail_id in data[0].split():
            _,msg_data = mail.fetch(mail_id,"(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            subject = self._decode_header(msg.get("Subject",""))
            if not self._match(subject,subject_keywords):
                continue
            files = self._save_attachments(msg,attachment_keywords)
            if files:
                downloaded.extend(files)
                mail.store(mail_id,"+FLAGS","\\Seen")
        mail.logout()
        return downloaded


    def listen(self,interval=30,subject_keywords=None,attachment_keywords=None):
        """持续监听邮箱"""
        while True:
            try:
                self.check(subject_keywords,attachment_keywords)
            except (imaplib.IMAP4.error,OSError) as e:
                print(f"邮件监听异常: {e}")
            time.sleep(interval)


    def _save_attachments(self,msg,attachment_keywords=None):
        """保存邮件附件"""
        files = []
        for part in msg.walk():
            filename = part.get_filename()
            if not filename:
                continue
            filename = self._decode_header(filename)
            if not self._match(filename,attachment_keywords):
                continue
            path = self.download_dir/Path(filename).name
            path.write_bytes(part.get_payload(decode=True))
            files.append(str(path))
        return files

    @staticmethod
    def _match(value,keywords):
        if not keywords:
            return True
        return any(keyword in value for keyword in keywords)

    @staticmethod
    def _decode_header(value):
        if not value:
            return ""
        return str(make_header(decode_header(value)))
    


if __name__ == "__main__":
    monitor = MailMonitor(
        email_addr="hwy0821@yeah.net",
        password="xxxxxxxxx",
        imap_server="imap.yeah.net",
        download_dir="attachments",
    )
    files = monitor.check("巡检报告","基础资源")      # 单次检查
    print(files)