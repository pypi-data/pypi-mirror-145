import sys
import time
import requests

from airflow.hooks.base import BaseHook
from airflow.providers.zeppelin.Zeppelin import Zeppelin

class ZeppelinHook(BaseHook):
    conn_name_attr = 'zeppelin_conn_id'
    default_conn_name = 'zeppelin_default'
    conn_type = 'zeppelin'
    hook_name = 'Zeppelin'

    def __init__(self,note_id, params, status_sleep, paragraph_id=None, zeppelin_conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.zeppelin_conn_id = zeppelin_conn_id
        self.host = None
        self.port = None
        self.password = None
        self.db = None
        self.protocol = None
        self.note_id = note_id
        self.paragraph_id = paragraph_id
        self.params = params
        self.status_sleep = status_sleep
        self.zeppelin_url = self.get_ZepplineUrl()
        self.zeppelin = None;
        self.get_notebook()
        self.log.info('using zeppelin url:%s', self.zeppelin_url)

    def get_ZepplineUrl(self):
        conn = self.get_connection(self.zeppelin_conn_id)
        self.host = conn.host
        self.port = conn.port
        self.password = None if str(conn.password).lower() in ['none', 'false', ''] else conn.password
        self.db = conn.schema
        self.protocol = None if str(conn.extra_dejson.get('protocol')).lower() in ['none', ''] else str(conn.extra_dejson.get('protocol')).lower()
        if str(conn.schema).lower() in ['http', 'https'] :
            self.protocol = str(conn.schema).lower()
        if self.protocol is None :
            self.protocol = 'http'

        # check for ssl parameters in conn.extra
        ssl_arg_names = [
            "ssl",
            "ssl_cert_reqs",
            "ssl_ca_certs",
            "ssl_keyfile",
            "ssl_cert_file",
            "ssl_check_hostname",
        ]
        ssl_args = {name: val for name, val in conn.extra_dejson.items() if name in ssl_arg_names}
        self.log.debug(
            'Initializing zeppelin object for ConnectId "%s" on %s:%s:%s',
            self.zeppelin_conn_id,
            self.host,
            self.port,
            self.db,
        )
        return self.protocol+'://'+self.host+':'+str(self.port)

    def get_notebook(self):
        """Call API to Get notebook INfo."""
        try:
            g = requests.get('{0}/api/notebook/{1}'.format(self.zeppelin_url, self.note_id))
            if g.status_code == 200:
                if g.json()['status'] == 'OK':
                    print('Get Notebook is send access.')
                    tmpZeppelin = Zeppelin(note_id = self.note_id)
                    tmpZeppelin.name = g.json()['body']['name']
                    tmpZeppelin.path = g.json()['body']['path']
                    tmpZeppelin.paragraphs = g.json()['body']['paragraphs']
                    self.zeppelin = tmpZeppelin
                else:
                    print('Get Notebook failed. ')
                    sys.exit(1)

            elif g.status_code == 500:
                print('Notebook is still busy executing. Checking again in 60 seconds...')
                sys.exit(1)

            else:
                print('ERROR: Get Book Unexpected return code: {}'.format(g.status_code))
                sys.exit(1)
            
        except KeyError as e:
            print(e)

    def run_notebook_all_paragraph(self):
        print('[run_notebook_all_paragraph] Run Zeppelin Notebook[{}][{}]'.format(self.note_id, self.zeppelin.name))
        for paragraph in self.zeppelin.paragraphs :
            paragraph.setdefault('title','None')
            self.run_paragraph(paragraph_id=paragraph['id'], paragraph_title= paragraph['title'])
            self.wait_paragraph_execute(paragraph_id=paragraph['id'], paragraph_title= paragraph['title'], status_sleep = self.status_sleep)

    def run_notebook(self):
        """Call API to execute notebook."""
        try:
            s = requests.post('{0}/api/notebook/job/{1}'.format(self.zeppelin_url, self.note_id))
            self.log.info('Run Notebook Zeppelin Url:%s', s.url)
            if s.status_code == 200:
                if s.json()['status']=='OK':
                    print('Notebook[%s][%s] is send access.' %(self.zeppelin.note_id,self.zeppelin.name))
                else:
                    print('Notebook is send false. ')
                    sys.exit(1)
            elif s.status_code == 500:
                print('ERROR: Unexpected return code: {}'.format(s.status_code))
                sys.exit(1)
            else:
                print('ERROR: Run Notebook Unexpected return code: {}'.format(s.status_code))
                sys.exit(1)
        except KeyError as e:
            print(e.__cause__)
            sys.exit(1)

    def wait_for_notebook_to_execute(self):
        """Wait for notebook to finish executing before continuing."""
        while True:
            r = requests.get('{0}/api/notebook/job/{1}'.format(self.zeppelin_url, self.note_id))
            if r.status_code == 200:
                try:
                    data = r.json()['body']['paragraphs']
                    if all(paragraph['status'] in ['FINISHED','READY'] for paragraph in data):
                        print('Paragraphs RunStatus:')
                        for paragraph in r.json()['body']['paragraphs']:
                            print(paragraph)
                        break
                    elif (paragraph['status'] in ['ERROR'] for paragraph in data):
                        print('Paragraphs RunStatus:')
                        for paragraph in r.json()['body']['paragraphs']:
                            print(paragraph)
                        sys.exit(1)
                    else:
                        print('Paragraphs RunningStatus:')
                        for paragraph in r.json()['body']['paragraphs']:
                            print(paragraph)
                    time.sleep(self.status_sleep)
                    continue
                except KeyError as e:
                    print(e)
                    print(r.json())
            elif r.status_code == 500:
                print('Notebook is still busy executing. Checking again in 60 seconds...')
                time.sleep(60)
                continue
            else:
                print('ERROR: Unexpected return code: {}'.format(r.status_code))
                sys.exit(1)

    def get_executed_notebook(self):
        """Return the executed notebook."""
        r = requests.get('{0}/api/notebook/job/{1}'.format(
            self.zeppelin_url, self.note_id))
        if r.status_code == 200:
            for paragraph in r.json()['body']['paragraphs']:
                print(paragraph)
        else:
            print('ERROR: Could not get executed notebook.', file=sys.stderr)
            sys.exit(1)

    def run_notebook_paragraph(self):
        """Call API to execute notebook on paragraph."""
        try:
            p = requests.post('{0}/api/notebook/job/{1}/{2}'.format(self.zeppelin_url, self.note_id, self.paragraph_id))
            self.log.info('Run Zeppelin Notebook paragraph Url:%s', p.url)
            if p.status_code == 200:
                if p.json()['status'] == 'OK':
                    print('Notebook[%s][%s] paragraph[%s] is send access.' % (self.note_id, self.zeppelin.name, self.paragraph_id))

                else:
                    print('Notebook[%s][%s] paragraph[%s] is send false. ' % (self.note_id, self.zeppelin.name, self.paragraph_id))
                
            elif p.status_code == 500:
                print('ERROR: Unexpected return code: {}'.format(p.status_code))
                sys.exit(1)
            else:
                print('ERROR: Unexpected return code: {}'.format(p.status_code))
                sys.exit(1)
            
        except KeyError as e:
            print(e.__cause__)
            sys.exit(1)

    def wait_for_notebook_paragraph_to_execute(self):
        """Wait for notebook paragraph to finish executing before continuing."""
        while True:
            c = requests.get('{0}/api/notebook/job/{1}/{2}'.format(self.zeppelin_url, self.note_id, self.paragraph_id))
            if c.status_code == 200:
                try:
                    if c.json()['status'] == 'OK':
                        if c.json()['body']['status'] in ['FINISHED' ,'READY'] :
                            print('Paragraph RunStatus:')
                            print(c.json()['body'])
                            break
                        elif c.json()['body']['status'] in ['ERROR'] :
                            print('Paragraph Error:')
                            print(c.json()['body']['errorMessage'])
                            sys.exit(1)
                        else:
                            print('Paragraphs RunningStatus:')
                            print(c.json()['body'])
                            time.sleep(self.status_sleep)
                            continue
                    else:
                        print('Notebook Paragraph[%s] getState failed.')
                        sys.exit(1)
                except KeyError as e:
                    print(e.__cause__)
                    sys.exit(1)

            elif c.status_code == 500:
                print('Notebook is still busy executing. Checking again in 60 seconds...')
                time.sleep(60)
                continue

            else:
                print('ERROR: Unexpected return code: {}'.format(c.status_code))
                sys.exit(1)

    def run_paragraph(self, paragraph_id, paragraph_title):
        """Call API to execute notebook on paragraph."""
        try:
            p = requests.post('{0}/api/notebook/job/{1}/{2}'.format(self.zeppelin_url, self.note_id, paragraph_id))
            # print('Run Zeppelin Notebook paragraph Url:{}'.format( p.url))

            if p.status_code == 200:
                if p.json()['status'] == 'OK':
                    print('Notebook[%s][%s] paragraph[%s] [%s] is send access.' % (self.note_id, self.zeppelin.name, paragraph_id, paragraph_title))

                else:
                    print('Notebook[%s][%s] paragraph[%s] [%s] is send false. ' % (self.note_id, self.zeppelin.name, paragraph_id, paragraph_title))

            elif p.status_code == 500:
                print('ERROR: Unexpected return code: {}'.format(p.status_code))
                sys.exit(1)
            else:
                print('ERROR: Unexpected return code: {}'.format(p.status_code))
                sys.exit(1)

        except KeyError as e:
            print(e.__cause__)
            sys.exit(1)

    def wait_paragraph_execute(self,paragraph_id, paragraph_title, status_sleep=2):
        """Wait for notebook paragraph to finish executing before continuing."""
        while True:
            c = requests.get('{0}/api/notebook/job/{1}/{2}'.format(self.zeppelin_url, self.note_id, paragraph_id))
            if c.status_code == 200:
                try:
                    if c.json()['status'] == 'OK':
                        if c.json()['body']['status'] in ['FINISHED' ,'READY'] :
                            print('Paragraph RunStatus:')
                            print(c.json()['body'])
                            break
                        elif c.json()['body']['status'] in ['ERROR'] :
                            print('Paragraph Error:')
                            print(c.json()['body']['errorMessage'])
                            sys.exit(1)
                        else:
                            time.sleep(status_sleep)
                            continue
                    else:
                        print('Notebook Paragraph[{}] Title[{}] getState failed.'.format(paragraph_id, paragraph_title))
                        sys.exit(1)
                except KeyError as e:
                    print(e.__cause__)
                    sys.exit(1)

            elif c.status_code == 500:
                print('Notebook is still busy executing. Checking again in 60 seconds...')
                time.sleep(60)
                continue

            else:
                print('ERROR: Unexpected return code: {}'.format(c.status_code))
                sys.exit(1)