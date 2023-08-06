
from airflow.models import BaseOperator
from airflow.providers.zeppelin.PythonUtils import PythonUtils
from airflow.providers.zeppelin.hooks.ZeppelinHook import ZeppelinHook


class ZeppelinOperator(BaseOperator):
    # template_fields = (attributes_to_be_rendered_with_jinja)
    def __init__(self, note_id, params=None, conn_id=ZeppelinHook.default_conn_name,
                 paragraph_id=None, status_sleep=5, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.zeppelin_task_id=kwargs['task_id']
        self.conn_id = conn_id
        self.note_id = note_id
        self.paragraph_id = paragraph_id
        self.params = params
        self.status_sleep = status_sleep

    def execute(self, context: 'Context') -> None:
        self.log.info('ZeppelinOperator[%s] Transfer Zeppelin Notebook[%s] using Connect[%s].', self.zeppelin_task_id, self.note_id, self.conn_id)
        if not self.paragraph_id :
            zeppelin_hook = ZeppelinHook(zeppelin_conn_id=self.conn_id,note_id=self.note_id,paragraph_id=self.paragraph_id,params=self.params,status_sleep=self.status_sleep)
            zeppelin_hook.run_notebook_paragraph()
            zeppelin_hook.wait_for_notebook_paragraph_to_execute()
        else:
            zeppelin_hook = ZeppelinHook(zeppelin_conn_id=self.conn_id,note_id=self.note_id,params=self.params,status_sleep=self.status_sleep)
            zeppelin_hook.run_notebook_all_paragraph()
        self.log.info('ZeppelinOperator[%s] Transfer Zeppelin Notebook[%s] using Connect[%s] finished.', self.zeppelin_task_id, self.note_id, self.conn_id)

    def __str__(self):
        return '{"task_id":"' + PythonUtils.NoneDefaultVale(self.zeppelin_task_id,'') + \
               '","conn_id":"' + PythonUtils.NoneDefaultVale(self.conn_id, '') + \
               '","note_id":"' + PythonUtils.NoneDefaultVale(self.note_id, '') + \
               '","paragraph_id":"' + PythonUtils.NoneDefaultVale(self.paragraph_id, '') + \
               '","params":"' + PythonUtils.NoneDefaultVale(self.params, '') + '"}';
