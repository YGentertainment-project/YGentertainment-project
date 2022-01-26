from datetime import datetime

class Stats:
    def __init__(self):
        self.status = 'ready'
        self.item_count = 0
        self.start_time = datetime.fromtimestamp(0)
        self.finish_time = datetime.fromtimestamp(0)
        self.lastlog_time = datetime.fromtimestamp(0)
        self.log_count = dict.fromkeys(['ERROR', 'WARNING', 'INFO', 'DEBUG'], 0)
        self.res_count = {}
        self.err_count = {}
        
    def __str__(self):
        s = f'status: {self.status}\n'
        if self.status != 'ready':
            s += f'start_time: {self.start_time}\n'
        if self.status == 'finish':
            s += f'finish_time: {self.finish_time}\n'
        else :
            s += f'lastlog_time: {self.lastlog_time}\n'
        s += f'item_count: {self.item_count}\n'
        for x in self.res_count:
            s += f'response_count/{x}: {self.res_count[x]}\n'
        for x in self.log_count:
            s += f'log_count/{x}: {self.log_count[x]}\n'
        for x in self.err_count:
            s += f'err_count/{x}: {len(self.err_count[x])}\n'
        return s
    
    def to_dict(self):
        temp = {}
        temp['status'] = self.status
        temp['item_count'] = self.item_count
        temp['start_time'] = self.start_time.strftime('%Y-%m-%dT%H:%M:%S')
        temp['finish_time'] = self.finish_time.strftime('%Y-%m-%dT%H:%M:%S')
        temp['lastlog_time'] = self.lastlog_time.strftime('%Y-%m-%dT%H:%M:%S')
        temp['log_count'] = self.log_count
        temp['res_count'] = self.res_count
        temp['err_count'] = self.err_count
        return temp