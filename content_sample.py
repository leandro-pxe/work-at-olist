from calls_api.calls.models import CallRecord

source_phone = '99988526423'
destination_phone = '9993468278'

datas =[
{'call_id': 70, 'started_at': '2016-02-29T12:00:00Z', 'ended_at': '2016-02-29T14:00:00Z'},
{'call_id': 71, 'started_at': '2017-12-12T15:07:13Z', 'ended_at':  '2017-12-12T15:14:56Z'},
{'call_id': 72, 'started_at': '2017-12-12T22:47:56Z', 'ended_at':  '2017-12-12T22:50:56Z'},
{'call_id': 73, 'started_at': '2017-12-12T21:57:13Z', 'ended_at':  '2017-12-12T22:10:56Z'},
{'call_id': 74, 'started_at': '2017-12-12T04:57:13Z', 'ended_at':  '2017-12-12T06:10:56Z'},
{'call_id': 75, 'started_at': '2017-12-12T21:57:13Z', 'ended_at':  '2017-12-13T22:10:56Z'},
{'call_id': 76, 'started_at': '2017-12-12T15:07:58Z', 'ended_at':  '2017-12-12T15:12:56Z'},
{'call_id': 77, 'started_at': '2018-02-28T21:57:13Z', 'ended_at':  '2018-03-01T22:10:56Z'}
]

for data in datas:
    CallRecord.objects.create(
        type='START',
        date_register=data['started_at'],
        call_id=data['call_id'],
        source=source_phone,
        destination=destination_phone,
    )
    CallRecord.objects.create(
        type='END',
        date_register=data['ended_at'],
        call_id=data['call_id'],
    )
