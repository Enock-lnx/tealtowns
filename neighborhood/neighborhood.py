import mongo_db
from common import mongo_db_crud as _mongo_db_crud
from event import event as _event
from event import weekly_event as _weekly_event
from shared_item import shared_item as _shared_item

def GetByUName(uName: str, withWeeklyEvents: int = 0, withSharedItems: int = 0,
    weeklyEventsCount: int = 3, sharedItemsCount: int = 3, maxMeters: float = 500,
    limitCount: int = 250, withUsersCount: int = 0, withUniqueEventUsersCount: int = 0, userId: str = '',
    minDateString: str = '', maxDateString: str = '', withFreePaidStats: bool = False):
    ret = _mongo_db_crud.GetByUName('neighborhood', uName)
    if '_id' not in ret['neighborhood']:
        ret['valid'] = 0
        ret['message'] = 'Neighborhood not found for ' + uName
        return ret

    neighborhoodId = ret['neighborhood']['_id']
    if userId:
        userNeighborhoods = _mongo_db_crud.Search('userNeighborhood', stringKeyVals = {'userId': userId})['userNeighborhoods']
        for userNeighborhood in userNeighborhoods:
            if neighborhoodId == userNeighborhood['neighborhoodId']:
                ret['neighborhood']['userNeighborhood'] = userNeighborhood

    lngLat = ret['neighborhood']['location']['coordinates']
    if withWeeklyEvents or withUniqueEventUsersCount:
        items = _weekly_event.SearchNear(lngLat, maxMeters, limit = limitCount)['weeklyEvents']
        ret['weeklyEventsCount'] = len(items)
        ret['weeklyEvents'] = items[slice(0, weeklyEventsCount)] if len(items) > weeklyEventsCount else items
        if withUniqueEventUsersCount:
            weeklyEventIds = []
            for item in items:
                weeklyEventIds.append(item['_id'])
            retAttending = _event.GetUsersAttending(weeklyEventIds = weeklyEventIds, minDateString = minDateString,
                maxDateString = maxDateString, withFreePaidStats = withFreePaidStats)
            ret['uniqueEventUsersCount'] = retAttending['uniqueUsersCount']
            ret['eventInfos'] = retAttending['eventInfos']
            if withFreePaidStats:
                ret['freeEventsCount'] = retAttending['freeEventsCount']
                ret['paidEventsCount'] = retAttending['paidEventsCount']
                ret['totalFreeEventUsersCount'] = retAttending['totalFreeEventUsersCount']
                ret['totalPaidEventUsersCount'] = retAttending['totalPaidEventUsersCount']
                ret['totalCutUSD'] = retAttending['totalCutUSD']
                ret['totalEventUsersCount'] = retAttending['totalEventUsersCount']
    if withUsersCount:
        items = mongo_db.find('userNeighborhood', {'neighborhoodId': neighborhoodId})['items']
        ret['usersCount'] = len(items)
    if withSharedItems:
        items = _shared_item.SearchNear(lngLat, maxMeters, limit = limitCount)['sharedItems']
        ret['sharedItemsCount'] = len(items)
        ret['sharedItems'] = items[slice(0, sharedItemsCount)] if len(items) > sharedItemsCount else items
    return ret

def SearchNear(stringKeyVals: dict = {}, locationKeyVals: dict = {}, limit: int = 25, skip: int = 0,
    withLocationDistance: int = 0, userId: str = ''):
    ret = _mongo_db_crud.Search('neighborhood', stringKeyVals = stringKeyVals,
        locationKeyVals = locationKeyVals, limit = limit, skip = skip,
        withLocationDistance = withLocationDistance)
    if userId:
        userNeighborhoods = _mongo_db_crud.Search('userNeighborhood', stringKeyVals = {'userId': userId})['userNeighborhoods']
        for index, neighborhood in enumerate(ret['neighborhoods']):
            neighborhoodId = neighborhood['_id']
            for userNeighborhood in userNeighborhoods:
                if neighborhoodId == userNeighborhood['neighborhoodId']:
                    ret['neighborhoods'][index]['userNeighborhood'] = userNeighborhood
                    break

    return ret
