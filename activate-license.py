import requests
import sys
import os 
import pickle
import urllib3
import subprocess


LICENSE_FILE_PATH = '/config/bigip.license'
ACTIVATE_F5_URL = 'https://activate.f5.com/license/dossier.jsp'

def main_procedure():
    baskey =  sys.argv[1]
    dossier = get_dossier(baskey)


def get_dossier(basekey):
    result = subprocess.run(['get_dossier', '-b', basekey], input=None, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    dossier = result.stdout.decode('utf-8')
    return dossier

def activate_f5(dossier):
    license = ""
    return license

def write_license(license_file):
    with open(LICENSE_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(license_file)


if __name__ == '__main__':
    main_procedure()
