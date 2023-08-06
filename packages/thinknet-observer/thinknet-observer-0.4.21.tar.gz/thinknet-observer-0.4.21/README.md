# thinknet-observer-python
---
เป็น library ที่รวบรวมเครื่องมือการทำ observaibility ตาม format ของบริษัท ด้วยภาษา python โดยมีเครื่องมือดังนี้

* metrics
* log 
* tracing

  
## Installation
```
pip install thinknet-observer
```

## Metrics
การเรียกใช้ metrics เพื่อให้ [prometheus](https://prometheus.io/) มาเก็บ (pull) โดยมีวิธีการใช้งานดังนี้:

### PrometheusMiddleware()
> เป็น Class ที่ return middleware สำหรับเก็บ default metrics

Example
```python
from thinknet_observer import PrometheusMiddleware

# Flask
app = Flask(__name__)
# FastAPI
app = FastAPI()

''' use middleware to collect default metrics '''
# singleprocess mode
middleware = PrometheusMiddleware(app) 
# multiprocess mode
middleware = PrometheusMiddleware(app, is_multiprocessing = True) 

# add exclude (optional)
list_exclude = [{"route": "/healthz"}]
middleware.add_exclude(list_exclude)

```

### extension

Module สำหรับสร้าง custom metrics โดยมีการเรียกใช้งานดังนี้

```python
from thinknet_observer import MetricCollector
```

โดย custom metrics มีฟังก์ชั่นการทำงาน 4 ประเภทดังนี้

#### MetricCollector.counter(name, description, label)

> เป็น class method สำหรับสร้าง metrics ประเภท counter ซึ่งสามารถเพิ่มค่าได้อย่างเดียว

Parameter
| name  | type | description |
| ---- | ---- | ---- | 
| name  | String  | ชื่อของ metrics
| description  | String  | description ของ metrics
| labels  | Array  | array of string labels ของ metrics [optional]

Example
```python
# no label
custom_counter = MetricCollector.counter("CUSTOM_COUNTER", "desc of CUSTOM_COUNTER")
custom_counter.inc(1) #เพิ่มค่า 1

# label
custom_counter_label = MetricCollector.counter("CUSTOM_COUNTER", "desc of CUSTOM_COUNTER", ["key1","key2"])
custom_counter_label.labels('value1', 'value2').inc(1)
```

#### MetricCollector.gauge(name, description, label)

> เป็น class method สำหรับสร้าง metric ประเภท gauge ซึ่งสามารถเพิ่ม/ลดค่าได้

Parameter
| name  | type | description |
| ---- | ---- | ---- | 
| name  | String  | ชื่อของ metrics
| description  | String  | description ของ metrics
| labels  | Array  | array of string labels ของ metrics [optional]

Example
```python
# no labels
custom_gauge = MetricCollector.gauge(
    "CUSTOM_GAUGE", "desc of CUSTOM_GAUGE",
)
custom_gauge.inc(1) #เพิ่มค่า 1
custom_gauge.dec(5) #ลดค่าลง 5 

#labels
custom_gauge_label = MetricCollector.gauge(
    "CUSTOM_GAUGE", "desc of CUSTOM_GAUGE", ["key1", "key2"]
)
custom_gauge_label.labels('value1', 'value2').inc(1)
custom_gauge_label.labels('value1', 'value2').dec(5)
```

#### MetricCollector.histogram(name, description,label, bucket)

> เป็น class method สำหรับสร้าง metric ประเภท histogram 

Parameter
| name  | type | description |
| ---- | ---- | ---- | 
| name  | String  | ชื่อของ metrics
| description  | String  | description ของ metrics
| labels  | Array  | array of string labels ของ metrics [optional]
| bucket | Array | array of bucket for histogram [optional]

Example
```python
# no labels
custom_histogram = MetricCollector.histogram(
    "CUSTOM_HISTOGRAM", "desc of CUSTOM_HISTOGRAM",
)
custom_histogram.observe(20)

# labels
custom_histogram = MetricCollector.histogram(
    "CUSTOM_HISTOGRAM", "desc of CUSTOM_HISTOGRAM", ["key1", "key2"]
)
custom_histogram.labels('value1', 'value2').observe(20)
```

#### MetricCollector.summary(name, description, label)

> เป็น class method สำหรับสร้าง metric ประเภท summary

Parameter
| name  | type | description |
| ---- | ---- | ---- | 
| name  | String  | ชื่อของ metrics
| description  | String  | description ของ metrics
| labels  | Array  | array of string labels ของ metrics [optional]

Example
```python
# no labels
custom_summary = MetricCollector.summary(
    "CUSTOM_SUMMARY", "desc of CUSTOM_SUMMARY"
)
custom_summary.observe(10)

# labels
custom_summary_label = MetricCollector.summary(
    "CUSTOM_SUMMARY", "desc of CUSTOM_SUMMARY", ["key1", "key2"]
)
custom_summary_label.labels('value1', 'value2').observe(10)
```

### multiprocess mode
กรณีรันเป็น multiprocess mode ให้เพิ่ม environment: PROMETHEUS_MULTIPROC_DIR ด้วย
```
PROMETHEUS_MULTIPROC_DIR=./prometheus_multiproc/ (folder for multiprocess metrics)
```

### using gunicorn (Flask)
กรณีรันด้วย gunicorn แบบ multiprocess mode  ให้เพิ่ม file: gunicorn.config.py ที่ root path ด้วย

```python
import os

from pathlib import Path
from multiprocessing import cpu_count
from os import environ
from prometheus_client import multiprocess
from thinknet_observer import clear_multiproc_dir

def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)

def max_workers():    
    return cpu_count()

clear_multiproc_dir()

```

ref: [https://github.com/prometheus/client_python](https://github.com/prometheus/client_python)


---
## Log

log ของ thinknet_observer มีทั้งหมดสามแบบ logging, analyzer และ cronlogger โดยใช้แตกต่างกันดังต่อไปนี้

### logging()
> เป็น class method สำหรับใช้ logging เราจะใช้เมื่อต้องการ log เพื่อแสดงข้อความเกี่ยวกับการทำงานของระบบ (มักใช้กับ project ที่เป็น Service) และข้อความนั้น ๆ เป็น String โดย Log ที่ได้จะแสดงข้อมูลดังต่อไปนี้


|Field Name|Description|
|----------|-----------|
|timestamp|เวลาที่ทำการสร้าง log โดยจะอยู่ใน Format %Y-%m-%dT%H:%M:%S|
|level|ระดับของ Log (สามารถอ่านเพิ่มเติม [log level](https://docs.python.org/3/library/logging.html#levels))
|message|ข้อความที่ต้องการจะแสดง|
|log.source|ที่มาต้นทางของ log นั้น ๆ|
|log.version|เวอร์ชั่นของ log|

**วิธีการเรียกใช้งาน**
``` Python
from thinknet_observer import Logger
# Create instance
log = Logger.logging()
# Generate Log
log.error(message= "Error Message")
# {'timestamp':'2022-03-30T13:28:22Z','level':'ERROR','message':'Error Message','log.source':'application','log.version':1}
```
### analyzer()
> log ประเภทนี้เหมือนกับประเภทก่อนหน้าแต่ในการรับ message จะสามารถรับ message ที่เป็น Json ได้ (มักใช้กับ project ที่เป็น Service)โดย Log ที่ได้จะแสดงข้อมูลดังต่อไปนี้

|Field Name|Description|
|----------|-----------|
|timestamp|เวลาที่ทำการสร้าง log โดยจะอยู่ใน Format %Y-%m-%dT%H:%M:%S|
|level|ระดับของ Log (สามารถอ่านเพิ่มเติม [log level](https://docs.python.org/3/library/logging.html#levels))
|message|ข้อความที่ต้องการจะแสดง
|log.source|ที่มาต้นทางของ log นั้น ๆ|
|log.version|เวอร์ชั่นของ log|

**ลักษณะของ message ที่ต้องการ log**

 ``` Python 
 {
    "httpStatus": 4xx, 5xx (int)[optional]
    "serviceCode": key ที่สามารถสื่อความหมายชัดเจน (string
    "description": message จริงๆของระบบ (ถ้าไม่มีค่อยกำหนดเอง) (string)
    "traceID": ได้จาก headers (string)
    "payload": Stringify({}) [optional]
  } 
 ```

**วิธีการเรียกใช้งาน**
``` Python
from thinknet_observer import Logger
# Create instance
analyzelog = Logger.analyzer()
# Generate Log
analyzelog.error(message= {"index": 0, "data": []})
# {'timestamp':'2022-03-30T13:28:22Z','level':'ERROR','message':'{"serviceCode": 0, "description": "error message"}','log.source':'analyzer','log.version':1}
```

#### cronlogger(version, repo_name, project_name, tags, service)
> เป็น class method ที่ log ที่ไว้สำหรับการให้ข้อมูลเพื่อแจ้งขั้นตอนของการทำงานของระบบ ณ ปัจจุบัน โดยใช้กับ script ที่รันในลักษณะ cron job เช่นการ ETL ข้อมูล โดยข้อมูลที่ log สร้างขึ้นจะมีรายละเอียดดังต่อไปนี้

Parameter
| name  | type | description |
|---|---|---|
|version| string | เลข version ของ script หรือ repo ซึ่งดึงมาจาก package.json|  
|repo_name| string | ชื่อของ repo นั้นๆ |
|project_name| string| ชื่อของ script ที่รัน ซึ่งดึงมาจาก package.json|
|tags| string | ค่า tagging [optional]|
|service| string or dict | script นี้เกี่ยวข้องกับ service ไหน [optional] |

Output:
|Field Name|Description|
|----------|-----------|
|@timestamp|เวลาที่ทำการสร้าง log โดยจะอยู่ใน Format %Y-%m-%dT%H:%M:%S|
|name|ชื่อของ repository ที่ใช้งานอยู่ ณ ปัจจุบัน|
|project|ชื่อของ project ที่ repository ที่ใช้งานอยู่ ณ ปัจจุบัน|
|status|สถานะ หรือขั้นตอนการทำงาน ณ ปัจจุบัน ได้แก่ start, running, error และ success|
|type|ประเภทของ log โดยในที่นี้จะเป็น log ประเภท cron|
|message|ข้อความที่ต้องการจะแสดง|
|tags|Tag ที่มีความเกี่ยวข้องกับ project โดยรับค่าเป็น string เช่น 'etl,testing' (optional)|
|service|service ที่มีความเกี่ยวข้องกับโปรเจค (optional)|
|_version|เวอร์ชั่นของ repository|

**วิธีการเรียกใช้งาน**
``` Python
from thinknet_observer import Logger
# Create instance
cronlog = Logger.cronlogger(version = "1", repo_name= "test", project_name= "testest")
# Generate Log
cronlog.error(message= "test message", extra={"status": "error"})
# {'name': 'test','project': 'testest','status': 'error','type': cron,'tags': ,'service': {},'@timestamp':'2022-03-30T13:28:22Z','message': 'test message','_version':1}
```

### Accesslog
---
accesslog เป็น log ที่ใช้กับ service เมื่อมีการส่ง request จะส่ง log กลับมา
อ่านวิธีการ configuration เพิ่มเติม https://pgjones.gitlab.io/hypercorn/how_to_guides/configuring.html

**ตัวอย่างการใช้งาน**
```Python
from src.thinknet_observer import _create_logger, AccessLogAtoms
from src.thinknet_observer import clear_multiproc_dir

hypercorn.logging._create_logger = _create_logger
hypercorn.logging.AccessLogAtoms = AccessLogAtoms
clear_multiproc_dir()
bind = environ.get("APP_HOST", "0.0.0.0") + ":" + environ.get("APP_PORT", "8080")
loglevel = "info"
accesslog = "-"
access_log_format = '{"remote-addr":"%(h)s","method" : "%(m)s" ,"url" : "%(U)s", "status" : %(s)s , "trace-id" : "%({trace-id}o)s", "res": "%({content-length}o)s" ,"user-agent" : "%(a)s" ,"timestamp" : "%(t)s" ,"response-time" : "%(M)s" , "referrer" : "%(f)s" , "log.source": "http","log.version": "1"}'
workers = int(environ.get("NUM_WORKER", max_workers()))
root_path = "/face-recognition-service"
```
