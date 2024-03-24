import threading
import time

from common import math_polygon as _math_polygon
from common import mongo_db_crud as _mongo_db_crud
import date_time
from event import event as _event
from event import user_event as _user_event
from event import user_weekly_event as _user_weekly_event
import log
import mongo_db

def SearchNear(lngLat: list, maxMeters: float, title: str = '', limit: int = 250, skip: int = 0, withAdmins: int = 1,
    type: str = ''):
    query = {
        'location': {
            '$nearSphere': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': lngLat,
                },
                '$maxDistance': maxMeters,
            }
        },
    }
    sortKeys = "dayOfWeek,startTime"
    ret = _mongo_db_crud.Search('weeklyEvent', {'title': title, 'type': type}, limit = limit, skip = skip, query = query,
        sortKeys = sortKeys)
    userIds = []
    # Calculate distance
    # May also be able to use geoNear https://stackoverflow.com/questions/33864461/mongodb-print-distance-between-two-points
    for index, item in reversed(list(enumerate(ret['weeklyEvents']))):
        ret['weeklyEvents'][index]['xDistanceKm'] = round(_math_polygon.Haversine(item['location']['coordinates'],
            lngLat, units = 'kilometers'), 3)
        if withAdmins:
            for userId in item['adminUserIds']:
                if userId not in userIds:
                    userIds.append(userId)

    if len(userIds) > 0 and withAdmins:
        listKeyVals = { '_id': userIds }
        fields = { "firstName": 1, "lastName": 1, "email": 1, }
        users = _mongo_db_crud.Search('user', listKeyVals = listKeyVals, fields = fields, limit = limit * 10)['users']
        usersIdMap = {}
        for user in users:
            usersIdMap[user['_id']] = user
        for indexEvent, event in enumerate(ret['weeklyEvents']):
            if 'adminUsers' not in ret['weeklyEvents'][indexEvent]:
                ret['weeklyEvents'][indexEvent]['adminUsers'] = []
            for userId in event['adminUserIds']:
                user = usersIdMap[userId] if userId in usersIdMap else {}
                ret['weeklyEvents'][indexEvent]['adminUsers'].append(user)

    return ret

def GetById(weeklyEventId: str, withAdmins: int = 1):
    ret = _mongo_db_crud.GetById('weeklyEvent', weeklyEventId)
    if withAdmins:
        userIds = []
        for userId in ret['weeklyEvent']['adminUserIds']:
            if userId not in userIds:
                userIds.append(userId)
        listKeyVals = { '_id': userIds }
        fields = { "firstName": 1, "lastName": 1, "email": 1, }
        users = _mongo_db_crud.Search('user', listKeyVals = listKeyVals, fields = fields)['users']
        usersIdMap = {}
        for user in users:
            usersIdMap[user['_id']] = user
        ret['weeklyEvent']['adminUsers'] = []
        for userId in ret['weeklyEvent']['adminUserIds']:
            user = usersIdMap[userId] if userId in usersIdMap else {}
            ret['weeklyEvent']['adminUsers'].append(user)
    return ret

def Save(weeklyEvent: dict):
    if 'timezone' not in weeklyEvent or weeklyEvent['timezone'] == '':
        weeklyEvent['timezone'] = date_time.GetTimezoneFromLngLat(weeklyEvent['location']['coordinates'])
    return _mongo_db_crud.Save('weeklyEvent', weeklyEvent)

def Remove(weeklyEventId: str):
    query = { 'weeklyEventId': weeklyEventId }
    events = mongo_db.find('event', query)['items']
    eventIds = []
    for event in events:
        eventIds.append(event['_id'])
    mongo_db.delete_many('userEvent', { 'eventId': { '$in': eventIds } })

    mongo_db.delete_many('event', { 'weeklyEventId': weeklyEventId })
    # TODO - end stripe subscription
    mongo_db.delete_many('userWeeklyEvent', { 'weeklyEventId': weeklyEventId })
    return _mongo_db_crud.RemoveById('weeklyEvent', weeklyEventId)

def CheckRSVPDeadline(weeklyEventId: str, now = None):
    ret = { 'valid': 1, 'message': '' }
    weeklyEvent = mongo_db.find_one('weeklyEvent', {'_id': mongo_db.to_object_id(weeklyEventId)})['item']
    retCheck = _event.GetNextEventStart(weeklyEvent, now = now)
    # See if deadline passed.
    if retCheck['rsvpDeadlinePassed']:
        # See if this is the first time passed (most recent event is still this week's event).
        sortObj = { 'start': -1 }
        currentEvent = mongo_db.find('event', {'weeklyEventId': weeklyEvent['_id']}, sort_obj = sortObj)['items'][0]
        if currentEvent['start'] == retCheck['thisWeekStart']:
            _user_event.CheckAddHostsAndAttendees(currentEvent['_id'], fillAll = 1)
            _user_weekly_event.AddWeeklyUsersToEvent(weeklyEvent['_id'], now = now)
    return ret

def CheckAllRSVPDeadlines(now = None):
    query = { 'priceUSD': { '$gt': 0 } }
    weeklyEvents = mongo_db.find('weeklyEvent', query)['items']
    log.log('info', 'weekly_event.CheckAllRSVPDeadlines', str(len(weeklyEvents)), 'weekly events')
    for weeklyEvent in weeklyEvents:
        CheckRSVPDeadline(weeklyEvent['_id'], now = now)
    return None

def CheckRSVPDeadlineLoop(timeoutMinutes = 15):
    log.log('info', 'weekly_event.CheckRSVPDeadlineLoop starting')
    thread = None
    while 1:
        if thread is None or not thread.is_alive():
            thread = threading.Thread(target=CheckAllRSVPDeadlines, args=())
            thread.start()
        time.sleep(timeoutMinutes * 60)
    return None
