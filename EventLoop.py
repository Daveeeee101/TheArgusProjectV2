import asyncio
import time
from datetime import datetime
from typing import Dict
import GraphQLData
import ujson
from Asset import Asset
from Event import Event
from Collection import Collection
import logging
import aiohttp

graphURL = "https://api.opensea.io/graphql/"


async def getEventsFromTime(collections: Dict[str, Collection], lastUpdatesDict: Dict[str, str], sess):
    query = 'EventHistoryPollQuery'
    header = GraphQLData.getHeader(query)
    eventHappened = False
    for eventType, dt in lastUpdatesDict.items():
        body = GraphQLData.getQuery(query, archetype=None,
                                    collections=[c for c in collections],
                                    chains=[],
                                    eventTypes=[eventType],
                                    eventTimestamp_Gt=dt,
                                    count=100,
                                    showAll=True)
        async with sess.post(url=graphURL, headers=header, data=body) as resp:
            response = await resp.text()
        updated = False
        for event in (Event(x['node']) for x in ujson.loads(response)['data']['assetEvents']['edges']):
            if event.badEvent:
                event.setEventSpecific('CANCEL_FALSE')
                continue
            collections[event.collection].updateEventHistory(event)
            print(event)
            eventHappened = True
            if not updated:
                lastUpdatesDict[eventType] = event.timestamp
                updated = True
    return lastUpdatesDict, eventHappened


async def getAssetsByCollection(sess, collection: str, maxAssetsPercent):
    cursor = None
    query = 'AssetSearchQuery'
    header = GraphQLData.getHeader(query)
    newAssets = []
    floorPrice = 1
    maxPrice = -1
    prevCount = -1
    while prevCount != 0 and maxPrice < floorPrice * maxAssetsPercent:
        body = GraphQLData.getQuery(query, assetOwner=None,
                                    chains=[],
                                    collection=None,
                                    collectionQuery=None,
                                    collectionSortBy=None,
                                    collections=[collection],
                                    count=32,
                                    cursor=cursor,
                                    includeHiddenCollections=None,
                                    isAutoHidden=None,
                                    isPrivate=None,
                                    paymentAssets=None,
                                    priceFilter=None,
                                    prioritizeBuyNow=True,
                                    query=None,
                                    rarityFilter=None,
                                    resultModel="ASSETS",
                                    safelistRequestStatuses=None,
                                    showContextMenu=False,
                                    sortAscending=True,
                                    sortBy="UNIT_PRICE",
                                    stringTraits=None,
                                    toggles='BUY_NOW')
        async with sess.post(url=graphURL, headers=header, data=body) as resp:
            response = await resp.text()
        count = 0
        for assetData in ujson.loads(response)['data']['query']['search']['edges']:
            data = assetData['node']
            newAssets.append(asset := Asset(openseaAssetData=data))
            logging.info('adding token %s to collection %s',
                         asset.assetId, collection)
            cursor = assetData['cursor']
            count += 1
        prevCount = count
        print(prevCount)
        floorPrice = newAssets[0].price
        maxPrice = newAssets[-1].price
        print(floorPrice)
        print(maxPrice)
    return newAssets


async def eventLoop(collections: Dict[str, Collection]):
    async with aiohttp.ClientSession() as sess:
        logging.info("Getting initial asset info...")
        for collection, obj in collections.items():
            logging.info("Getting asset info for %s", collection)
            newAssets = await getAssetsByCollection(sess, collection, 2)
            obj.addInitialAssets(newAssets)
        currTime = datetime.utcnow().replace(microsecond=0).isoformat()
        updateTimes = {'AUCTION_SUCCESSFUL': currTime, 'AUCTION_CANCELLED': currTime, 'AUCTION_CREATED': currTime}
        logging.info("starting event loop...")
        lastCheck = time.time()
        while True:
            updateTimes, eventHappened = await getEventsFromTime(collections, updateTimes, sess)
            logging.info("updated events")
            if time.time() > lastCheck + (60 * 30):
                logging.info("checking if assets match...")
                newAssets = await getAssetsByCollection(sess, collection, 1.5)
                currentAssets = obj.getAssetsFromFloor(1.5)
                differentAssetsOpenSea = set(x.assetId for x in newAssets).difference(set(x.assetId for x in currentAssets))
                differentAssetsMemory = set(x.assetId for x in currentAssets).difference(set(x.assetId for x in newAssets))
                for assetId in differentAssetsMemory:
                    logging.warning("asset from memory (%s) is not in opensea", assetId)
                for assetId in differentAssetsOpenSea:
                    logging.warning("asset from opensea (%s) is not in memory", assetId)
                lastCheck = time.time()
            await asyncio.sleep(5)

