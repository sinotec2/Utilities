


> 如果是一個flask或是Django 網頁的專案，使用者如果啟動需要計算資源的程序步驟，他們還是會需要等待在畫面上呢？還是會怎麼處理？

## 解題原則

在 Flask 或 Django 網站中，如果用戶啟動需要大量計算資源的任務，通常不會讓用戶在頁面上等待計算完成。相反，可以使用 Celery 等任務隊列系統將這些任務移到後台處理，並通過異步方式通知用戶任務的完成狀態。這通常通過以下幾個步驟來實現：

1. **提交任務**：當用戶啟動需要計算資源的任務時，這個任務會被提交到 Celery 任務隊列。這個過程是異步的，會立即返回一個任務 ID 給用戶。

2. **後台處理**：Celery worker 從任務隊列中取出任務並在後台處理。這樣，計算密集型任務不會阻塞主應用程式的執行。

3. **回應用戶**：在用戶提交任務後，網站可以立即回應一個確認訊息或顯示一個進度頁面，而不需要等待任務完成。

4. **通知任務狀態**：當任務完成後，可以通過以下方式通知用戶：
   - **輪詢**：用戶可以在前端通過定期向服務器發送請求來查詢任務狀態。
   - **WebSocket**：可以使用 WebSocket 來實時通知用戶任務狀態更新。
   - **電子郵件或其他通知方式**：可以通過電子郵件或其他通知系統（如短信、推送通知）告知用戶任務完成。

以下是一個簡單的實現示例：

### 1. 提交任務

在 Flask 或 Django 的視圖中，提交任務到 Celery：

```python
# views.py (Flask or Django)

from flask import Flask, request, jsonify
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def long_task():
    import time
    time.sleep(10)  # 模擬一個需要時間的計算任務
    return 'Task completed!'

@app.route('/start-task', methods=['POST'])
def start_task():
    task = long_task.apply_async()
    return jsonify({'task_id': task.id}), 202

@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)
```

### 2. 查詢任務狀態

前端可以通過 AJAX 請求定期查詢任務狀態：

```javascript
// main.js

function checkTaskStatus(taskId) {
    fetch(`/task-status/${taskId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.state === 'SUCCESS') {
                alert('Task completed: ' + data.result);
            } else {
                setTimeout(() => checkTaskStatus(taskId), 2000);
            }
        });
}

document.getElementById('start-task-btn').addEventListener('click', () => {
    fetch('/start-task', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            checkTaskStatus(data.task_id);
        });
});
```

這樣，用戶提交計算任務後，後台會處理這些任務，前端通過輪詢或其他方式獲取任務狀態，而不需要在頁面上等待計算完成。


## Flask 整合案例

你說得對，要將查詢任務狀態的 JavaScript 程式與 Flask 或 Django 網頁應用整合，需要更詳細的步驟。下面是一個更完整的示例，展示如何將這些部分無縫整合在一起。
假設我們有一個簡單的 Flask 應用：

### 1. 設置 Flask 和 Celery

```python
# app.py

from flask import Flask, request, jsonify, render_template
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def long_task():
    import time
    time.sleep(10)  # 模擬一個需要時間的計算任務
    return 'Task completed!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-task', methods=['POST'])
def start_task():
    task = long_task.apply_async()
    return jsonify({'task_id': task.id}), 202

@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. 創建 HTML 模板

在 `templates` 文件夾中創建一個 `index.html` 文件：

```html
<!-- templates/index.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Task Runner</title>
    <script>
        function checkTaskStatus(taskId) {
            fetch(`/task-status/${taskId}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.state === 'SUCCESS') {
                        document.getElementById('status').innerText = 'Task completed: ' + data.result;
                    } else {
                        setTimeout(() => checkTaskStatus(taskId), 2000);
                    }
                });
        }

        function startTask() {
            fetch('/start-task', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').innerText = 'Task started, checking status...';
                    checkTaskStatus(data.task_id);
                });
        }
    </script>
</head>
<body>
    <h1>Task Runner</h1>
    <button onclick="startTask()">Start Task</button>
    <p id="status">No task running.</p>
</body>
</html>
```

## Django 示例

假設我們有一個簡單的 Django 應用：

### 1. 設置 Django 和 Celery

在 `your_project/your_app/tasks.py` 中：

```python
# your_project/your_app/tasks.py

from celery import shared_task
import time

@shared_task
def long_task():
    time.sleep(10)  # 模擬一個需要時間的計算任務
    return 'Task completed!'
```

在 `your_project/your_app/views.py` 中：

```python
# your_project/your_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .tasks import long_task
from celery.result import AsyncResult

def index(request):
    return render(request, 'index.html')

def start_task(request):
    task = long_task.apply_async()
    return JsonResponse({'task_id': task.id}, status=202)

def task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return JsonResponse(response)
```

在 `your_project/your_app/urls.py` 中：

```python
# your_project/your_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start-task', views.start_task, name='start_task'),
    path('task-status/<task_id>/', views.task_status, name='task_status'),
]
```

### 2. 創建 HTML 模板

在 `your_project/your_app/templates/your_app` 文件夾中創建一個 `index.html` 文件：

```html
<!-- your_project/your_app/templates/your_app/index.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Task Runner</title>
    <script>
        function checkTaskStatus(taskId) {
            fetch(`/task-status/${taskId}/`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.state === 'SUCCESS') {
                        document.getElementById('status').innerText = 'Task completed: ' + data.result;
                    } else {
                        setTimeout(() => checkTaskStatus(taskId), 2000);
                    }
                });
        }

        function startTask() {
            fetch('/start-task', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').innerText = 'Task started, checking status...';
                    checkTaskStatus(data.task_id);
                });
        }
    </script>
</head>
<body>
    <h1>Task Runner</h1>
    <button onclick="startTask()">Start Task</button>
    <p id="status">No task running.</p>
</body>
</html>
```

這些示例展示了如何在 Flask 和 Django 中整合 Celery 後台任務處理和前端 JavaScript 來實現任務狀態查詢。用戶啟動任務後，前端會通過 AJAX 請求定期查詢任務狀態，並在任務完成時通知用戶。


