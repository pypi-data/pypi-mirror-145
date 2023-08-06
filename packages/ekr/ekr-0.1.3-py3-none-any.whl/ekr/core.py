# -*- coding: utf-8 -*-

from typing import Union
from mkr import MicroKernel
from efr import EventFramework, EventStation, Worker, Event

class EventKernel(EventFramework):
    CLASSTYPE = type(EventStation)
    def __init__(self, plugin_dir_name='plugins', **kwargs):
        super(EventKernel, self).__init__(**kwargs)
        self.mkr = MicroKernel(self, plugin_dir_name)
        self.mkr.mkpm.start()
        # for mod in self.mkr.mods:
        #     self.login(mod.mname)

    # def start(self):
    #     """
    #     启动内核
    #     start kernel
    #     :return:
    #     """
    #
    #     super(EventKernel, self).start()


    def _get_mod_stations(self, name):
        code = self.mkr[name]
        # print(code)
        if code is None:
            return False

        stations = []
        for k in dir(code):
            if k[:2] != '__' and k[-2:] != '__':
                v = getattr(code, k)
                if type(v) != self.CLASSTYPE and isinstance(v, EventStation):
                    stations += [v]
        # print(stations)
        if not stations:
            filter = getattr(code, 'filter', None)
            respond = getattr(code, 'respond', None)
            if respond is None:
                return False

            stations += [EventStation(code.__name__, filter, respond)]
        return stations

    def login(self, workable: Union[EventStation, str], worker: Worker=None) -> bool:
        """
        注册事件工作站。当update时，alloter会用调用station.filter(事件)->bool来判断station是否响应此事件。如果station响应了事件，那么alloter会把事件传入该station的队列.
        成功返回True，失败返回False

        Register the event workstation. When updating, the alloter will call station Filter - > bool to determine whether the station responds to this event. If the station responds to an event, the alloter will pass the event into the queue of the station
        Returns true for success and false for failure
        :param workable: EventStation pass through Event Station to login it or mod name
        :param worker: Worker assign worker to this station
                _: None  # do not assign.
        :return: bool
        """
        if isinstance(workable, EventStation):

            return super(EventKernel, self).login(workable, worker)
        else:
            stations = self._get_mod_stations(workable)

            if stations is False:
                return False

            ret = True
            for station in stations:
                ret = ret and super(EventKernel, self).login(station, worker)
            return ret

    def logoff(self, workable: Union[EventStation, str]) -> bool:
        """
        注销工作站。成功或不存在station返回True，失败返回False
        Log off the eventstation. Successful or non-existent stations return true, while failure returns false
        :param workable: EventStation or mod name
        :return: bool
        """
        if isinstance(workable, EventStation):

            return super(EventKernel, self).logoff(workable)
        else:
            stations = self._get_mod_stations(workable)

            if stations is False:
                return False

            ret = True
            for station in stations:
                ret = ret and super(EventKernel, self).logoff(station)
            return ret

    def assign(self, worker: Worker, workable:Union[EventStation, str]) -> bool:
        """
        布置任务到worker
        assign task to worker
        :param worker: Worker  If worker is None, mean cancel the station's worker
        :param workable: 可工作对象, 除了可以是EventStation外, 还可以是一个mod的名称. 该mod需要提供一个EventStation对象或名为filter、respond的方法
        :return: bool
        """
        if isinstance(workable, EventStation):

            return super(EventKernel, self).assign(worker, workable)
        else:
            stations = self._get_mod_stations(workable)
            # print(stations)
            if stations is False:
                return False

            ret = True
            for station in stations:
                ret = ret and super(EventKernel, self).assign(worker, station)
            return ret

    def list(self):
        """
        获取已安装的插件
        get installed plugins
        :return: list
        """
        return self.mkr.list()




