$ cat ./upload_query.py
#!/opt/anaconda3/envs/py311/bin/python
from ragflow_sdk import RAGFlow, Session

def get_ids(dataset):
    documents = dataset.list_documents()
    return [document.id for document in documents]

api_key="ragflow-***"
url='http://node02.sinotech-eng.com:8080'
aid_name='GoogleCanlendarAid'

rag_object = RAGFlow(api_key=api_key,base_url=url)
dataset = rag_object.list_datasets(name="google_calendar_events")
dataset = dataset[0]
try:
    ids=get_ids(dataset)
    dataset.delete_documents(ids=ids)
except:
    print('nofile to delete')
with open('/nas2/kuang/MyPrograms/GoogleCalendarAPI/whole.csv', 'rb') as file:
    file_content = file.read()
dataset.upload_documents([{"displayed_name": "whole.csv", "blob": file_content}])
ids=get_ids(dataset)
dataset.async_parse_documents(ids)