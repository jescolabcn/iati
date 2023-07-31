import smtplib


from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


class mysmtp(smtplib.SMTP):
    def sendmail(self, from_addr, to_addrs, msg, mail_options=[],rcpt_options=[]):
        self.ehlo_or_helo_if_needed()
        esmtp_opts = []
        if self.does_esmtp:
            if self.has_extn('size'):
                esmtp_opts.append("size=%d" % len(msg))
            for option in mail_options:
                esmtp_opts.append(option)

        (code, resp) = self.mail(from_addr, esmtp_opts)
        if code != 250:
            self.rset()
            raise smtplib.SMTPSenderRefused(code, resp, from_addr)
        senderrs = {}
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        for each in to_addrs:
            (code, resp) = self.rcpt(each, rcpt_options)            
            senderrs[each] = (code, resp)
        (code, resp) = self.data(msg)
        senderrs["data"] = (code, resp)
        if code != 250:
            self.rset()
            raise smtplib.SMTPDataError(code, resp)
        return senderrs