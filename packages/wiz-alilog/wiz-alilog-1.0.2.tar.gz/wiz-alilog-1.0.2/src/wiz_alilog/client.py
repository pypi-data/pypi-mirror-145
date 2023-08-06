import time

from aliyun.log import GetHistogramsRequest, LogClient, GetLogsRequest


class AliLogClient(object):
    def __init__(self, endpoint, project, logstore, access_key_id, access_key, limit=10000):
        self.endpoint = endpoint
        self.project = project
        self.logstore = logstore
        self.access_key_id = access_key_id
        self.access_key = access_key
        self.limit = limit

    def _total_count(self, start_timestamp, end_timestamp, query):
        res3 = None
        while (res3 is None) or (not res3.is_completed()):
            req3 = GetHistogramsRequest(self.project, self.logstore, start_timestamp, end_timestamp, "", query)
            res3 = self.client.get_histograms(req3)
        return res3.get_total_count()

    def __enter__(self):
        self.client = LogClient(self.endpoint, self.access_key_id, self.access_key)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def query(self, start_timestamp, end_timestamp, query="", logstore=None):
        full_list = []
        total_count = self._total_count(start_timestamp, end_timestamp, query)
        total_count = min(total_count, self.limit) if self.limit > 0 else total_count
        if total_count == 0:
            return full_list
        log_line = min(3000, total_count)
        for offset in range(0, total_count, log_line):
            res4 = None
            for _ in range(0, 3):
                req4 = GetLogsRequest(self.project, self.logstore if not logstore else logstore, start_timestamp, end_timestamp, "", query, log_line,
                                      offset, False)
                res4 = self.client.get_logs(req4)
                if res4 is not None and res4.is_completed():
                    break
                time.sleep(1)
            if res4 is not None:
                for item in res4.get_body():
                    full_list.append(item)
        return full_list

    def mute_alert(self, alert_name, project=None, until=0):
        if until <= 0:
            return False
        try:
            r = self.client.get_alert(self.project if not project else project, alert_name)
            config = r.body
            config['configuration']['muteUntil'] = until
            r = self.client.update_alert(self.project if not project else project, config)
            return True
        except:
            return False
        
