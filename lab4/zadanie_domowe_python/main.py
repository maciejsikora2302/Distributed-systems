import pykka
from enum import Enum
from random import randint, random
from time import sleep, time
from tinydb import TinyDB, Query
import os
from threading import Lock

class Status(Enum):
    OK = 1
    BATTERY_LOW = 2
    PROPULSION_ERROR = 3
    NAVIGATION_ERROR = 4

class SatelliteAPI(object):
    def getStatus(self, satelite_index):
        try:
            sleep(0.1 + randint(0, 400)/1000)
        except Exception as e:
            print(f"Exception {e} occured while waiting for status.")
        p = random()
        if (p<0.8): return Status.OK
        if (p<0.9): return Status.BATTERY_LOW
        if (p<0.95): return Status.NAVIGATION_ERROR
        return Status.PROPULSION_ERROR

class SpaceStation(pykka.ThreadingActor):
    def __init__(self, dispatcher=None, name=None, db=None, db_lock = None):
        super().__init__()
        self.dispatcher = dispatcher
        self.name = name
        self.request_id = 0
        self.db = db
        self.lock = db_lock

    def next_id(self):
        self.request_id += 1
        return self.request_id
    
    def send_request(self, req_first_sat_id, req_range, req_timeout):
        print(f"Station({self.name}) is sending a request number {self.request_id+1}, first satelite = {req_first_sat_id}, request range = {req_range}, timeout = {req_timeout}")
        start = time()
        response = self.dispatcher.request(self.next_id(), req_first_sat_id, req_range, req_timeout).get()
        query_id, satelite_status, response_in_time = response.check_status().get()
        stop = time()
        response.stop()
        db_satelite = Query()
        print(f"Station({self.name}) -> query_if = {query_id}, time to get response = {int((stop-start)*1000)}ms, percent of not timeouted satelites = {response_in_time}%")
        
        self.lock.acquire()
        for satelite_id, stat in satelite_status:
            print(f"Station({self.name}) --> Satelite({satelite_id}) returned status = {stat}")
            
            query_search = self.db.search(db_satelite.id == satelite_id)
            # print(f"QUERY SEARCH = {query_search}, query_search[fail_count] = {query_search[0]['fail_count']}")
            self.db.update({"fail_count": query_search[0]["fail_count"]+1}, db_satelite.id == satelite_id)
        self.lock.release()

    def print_data_base(self):
        for item in self.db:
            print(item)
        # return self.satelliteAPI.getStatus(int(message))

    def get_fails_of_satelite(self, satelite_id):
        satelite = Query()
        fail_count = self.db.search(satelite.id == satelite_id)[0]['fail_count']
        if fail_count > 0:
            print(f"Station({self.name}) => Query for satelite id {satelite_id}, fail count = {fail_count}")


class Dispatcher(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()

    def request(self, query_id, first_sat_id, req_range, timeout):
        tmp_ref = Requestor.start(query_id, first_sat_id, req_range, timeout).proxy()
        # tmp_ref.check_status()
        # tmp_ref.stop()
        return tmp_ref #(1, [(1, Status.OK)], 100)

class Requestor(pykka.ThreadingActor):
    def __init__(self, query_id, first_sat_id, req_range, timeout):
        super().__init__()
        self.query_id = query_id
        self.first_sat_id = first_sat_id
        self.range = req_range
        self.timeout = timeout
    
    def check_status(self):
        future_res = []
        for i in range(self.first_sat_id, self.first_sat_id + self.range):
            pom = RequestorSubprocess.start(timeout = 300).proxy()
            future_res.append((i, pom.api_get_status(), pom))

        # print(future_res)
        error_map = []
        ok_stat = 0
        for i, res, pom in future_res:
            time_ms, stat = res.get()
            pom.stop()
            if stat != Status.OK and time_ms != "TIMEOUT": error_map.append((i, stat))
            elif time_ms != "TIMEOUT": ok_stat += 1
        # time_ms, stat = pom.api_get_status().get()
        # pom.stop()
        # print(responses)

        return (self.query_id, error_map, int((ok_stat / self.range )* 100))#(1, [(1, Status.OK)], 100)

class RequestorSubprocess(pykka.ThreadingActor):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout/1000
    def api_get_status(self):
        try:
            comm = Communicator.start().proxy()
            start = time()
            stat = comm.api_call.getStatus(7777).get(timeout=self.timeout)
            end = time()
            comm.stop()
            return (int((end-start)*1000), stat)
        except Exception as e:
            comm.stop()
            return ("TIMEOUT", None)

class Communicator(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()
        self.api_call = pykka.traversable(SatelliteAPI())


#Proxy is a mechanism in pykka that build an abstraction over Actor model to lets you access inner values in Actor Model conventions 
#(every querry to atribute is packet into actor ask model)

db_name = "db.json"
START = time()

try:
    os.remove(f"./{db_name}")
except Exception as e:
    pass
open(f"./{db_name}", "w+").close()

db = TinyDB(db_name)
for satelite_id in range(100, 200):
    db.insert({"id": satelite_id, "fail_count": 0})

db_lock = Lock()

main_dispatcher = Dispatcher().start().proxy()

stations = [
    SpaceStation.start(dispatcher = main_dispatcher, name = "Station-Alfa", db = db, db_lock = db_lock).proxy(),
    SpaceStation.start(dispatcher = main_dispatcher, name = "Station-Beta", db = db, db_lock = db_lock).proxy(),
    SpaceStation.start(dispatcher = main_dispatcher, name = "Station-Gamma", db = db, db_lock = db_lock).proxy()
]


requests = []
number_of_requests_per_station = 2
for i in range(len(stations)*number_of_requests_per_station):
    requests.append(stations[i%len(stations)].send_request(req_first_sat_id=100, req_range=randint(1,51), req_timeout=300))

for req in requests:
    req.get()

sleep(1)

for sat_id in range(100,200):
    stations[0].get_fails_of_satelite(sat_id).get()

for station in stations:
    station.stop()
main_dispatcher.stop()
END = time()
print(f"All actors stopped. Time of work = {int((END-START)*1000)}ms")