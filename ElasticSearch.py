'''
11/26/17
New Version of Elastic Search
'''
## I probably dont need all of these. just have them here for future functions / methods
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import client
from elasticsearch import helpers
from requests_aws4auth import AWS4Auth
import argparse
import json
import requests
import sys
import copy

class ES_Client:
    
    '''
    Expects: aws_access_code and aws_secret_code
    Does: Initializes new instance of ES_Client class
    Returns: does not return anything
    '''
    def __init__(self,aws_access_code, aws_secret_code):
        self.es = None
        self.client = None

        host = 'search-bueventshowcase-2vvvoxbm5u73pdzuqois4u2aru.us-east-2.es.amazonaws.com'
        awsauth = AWS4Auth( aws_access_code, aws_secret_code, 'us-east-2', 'es')
        try:
                #this is hard coded
                self.indexName = 'defaultevents'
                self.es = Elasticsearch(
                      hosts=[{'host': host, 'port': 443}],
                      http_auth=awsauth,
                      use_ssl=True,
                      verify_certs=True,
                      connection_class=RequestsHttpConnection) 
                self.client = client.IndicesClient(self.es)    
        except:
                print ("Connection to Elasticsearch host %s failed.",es)
                
    '''
    Expects: the label of the index in AWS Elasticsearch cluster that you would like to delete
    Does: Deletes all the nodes inside a given index and the index itself fro the cluster
    Returns: Does not return anything
    '''
    def index_delete( self, indexLabel):
       try: 
                if self.client != None and self.client.exists(index=indexLabel):
                    self.client.delete(index=indexLabel)
                    print('OK 200')
       except Exception as e:
                print ('Error 500: '+str(type(e)))

    '''
    Expects: Input the label of the node you wish to delete from event index
    Does: Deletes individual Nodes from a given index
    Returns: Does not return anything
    '''
    def delete_node(self, nodeLabel):
        try:
            if self.client != None and self.client.exists(index=self.indexName):
                self.es.delete(index=self.indexName, doc_type="event",id=int(nodeLabel))
                print('200 OK')
        except Exception as e:
            print ('500 error: '+str(type(e)))
            
    '''
    Expects: Doc / list of events you would like to send to ES cluster
    Does: performs a deep copy on each event object and
          adds to docL[] if its mapping matches the template
          mapping r0. performs bulk insert on docL to send
          all valid events to the event index 
    Returns:Does not return anything
    '''
    def send_events_to_ES(self, eventList):
        r0   = { '_op_type': "",
                 '_index':self.es,
                 '_type':"",
                 '_id':int,
                 'eventName':"", 'organizer': "",'participants':"",'description':"",'tags':[],'registrationRequired':bool,'location':"",'address':'','city':'','zipCode':"",'startTime':"",'endTime':"",'duration':int,'cost':int,'minCost':int,'maxCsot':int,'refundPolicy':bool,'subOrganizers':"",'sponsors':""}        
        docL = []
        for event in eventList:
            print("Sending Event: ",event)
            try:
                entry=copy.deepcopy(r0)
                for key in r0:

                    if key in event:
                        entry[key]=event.get(key)
                docL.append(entry)
            except:
                print ('error that prevents sending event to stic')
        print(docL)
        self._bulk_insert( docL )

    '''
    Expects: an Input of the list of events you would like to send to event index
    Does: adds multiple nodes to the default index
    Returns: does not return anything
    '''
    def _bulk_insert(self, eventList):
        try:
            helpers.bulk(client=self.es, actions=eventList,stats_only=True)
            print('200 OK')
        except elasticsearch.ElasticsearchException as e:
            print ('500 error: '+str(type(e)))
            
    '''
    Expects: The index of the node you want to search
    Does: Gets node information based on NodeIndex ID
    Returns: All event information for specified event 
    '''
    def get_info(self, nodeIndex):
        try:
            if self.client !=None and self.client.exists(index=self.indexName):
                return self.es.get(index=self.indexName, id=int(nodeIndex))
        except elasticsearch.ElasticsearchException  as e:
            print ('500 error: '+str(type(e)))
    '''
    Expects: No input expected
    Does: Counts the number of nodes in our cluster
    Returns: The number of events in our existing event index
    '''
    def _count(self):
        try:
            return self.es.count(index=self.indexName)
        except elasticsearch.ElasticsearchException as e:
            print ('500 error: '+str(type(e)))
    
    '''
    Expects: The query input (criteria) you want to search under
    Does: Searches through all events to find events that match query input
    Returns: A list of nodes that match the query. Will return " no Matches!" if no matches were found
    '''
    def description_search(self, criteria):
        try:
            if self.client !=None and self.client.exists(index=self.indexName):
                return self.es.search(index=self.indexName, doc_type='event', q=criteria)
        except elasticsearch.ElasticsearchException as e:
            print ('Elastic bulk send error: '+str(type(e)))
        
    def index_create(self):
        try:
            self.client.create(index=self.indexName)
            print('200 OK')
        except elasticsearch.ElasticsearchException as e:
            print ('500 error: '+str(type(e)))
        


        

if __name__ == '__main__':

    aws_access_code = input('Pass access')
    aws_secret_code = input("secret please:")
    EsTest = ES_Client(aws_access_code, aws_secret_code)

    # call andy's event
    eventList = [{  '_op_type':'index',
                    '_index':'defaultevents',
                    '_type':"event",
                    '_id':1,
                    'eventName':"testEvent1", 'organizer': "Tigran",'participants':"andy",'description':"first tiger input",'tags':[],'registrationRequired':True,'location':"GSU",'address':'near mugar','city':'Boston','zipCode':"02215",'startTime':"now",'endTime':"end",'duration':120,'cost':3,'minCost':0,'maxCost':3,'refundPolicy':False,'subOrganizers':"andy",'sponsors':"none"
                    },
                {  '_op_type':'index',
                    '_index':'defaultevents',
                    '_type':"event",
                    '_id':2,
                    'eventName':"testEvent1", 'organizer': "Tigran",'participants':"andy",'description':"first tiger input",'tags':[],'registrationRequired':True,'location':"GSU",'address':'near mugar','city':'Boston','zipCode':"02215",'startTime':"now",'endTime':"end",'duration':120,'cost':3,'minCost':0,'maxCost':3,'refundPolicy':False,'subOrganizers':"andy",'sponsors':"none"
                    },
                 {  '_op_type':'index',
                    '_index':'defaultevents',
                    '_type':"event",
                    '_id':3,
                    'eventName':"testEvent1", 'organizer': "Tigran",'participants':"andy",'description':"first tiger input",'tags':[],'registrationRequired':True,'location':"GSU",'address':'near mugar','city':'Boston','zipCode':"02215",'startTime':"now",'endTime':"end",'duration':120,'cost':3,'minCost':0,'maxCost':3,'refundPolicy':False,'subOrganizers':"andy",'sponsors':"none"
                    },
                {  '_op_type':'index',
                    '_index':'defaultevents',
                    '_type':"event",
                    '_id':4,
                    'eventName':"testEvent1", 'organizer': "Tigran",'participants':"andy",'description':"first tiger input",'tags':[],'registrationRequired':True,'location':"GSU",'address':'near mugar','city':'Boston','zipCode':"02215",'startTime':"now",'endTime':"end",'duration':120,'cost':3,'minCost':0,'maxCost':3,'refundPolicy':False,'subOrganizers':"andy",'sponsors':"none"
                    },
                 {  '_op_type':'index',
                    '_index':'defaultevents',
                    '_type':"event",
                    '_id':5,
                    'eventName':"testEvent1", 'organizer': "Tigran",'participants':"andy",'description':"first tiger input",'tags':[],'registrationRequired':True,'location':"GSU",'address':'near mugar','city':'Boston','zipCode':"02215",'startTime':"now",'endTime':"end",'duration':120,'cost':3,'minCost':0,'maxCost':3,'refundPolicy':False,'subOrganizers':"andy",'sponsors':"none"
                    }
                 ]
    while(True):
        action = input("what would you like to do? ")
        if action=='deleteIndex':
            indexLabel = input("index label please: ")	
            EsTest.index_delete(indexLabel)
        elif action =='deleteNode' :
            nodeLabel = input('node label please: ')
            EsTest.delete_node(nodeLabel)
        elif action == 'indexCreate':
            EsTest.index_create()
        elif action=='bulkInsert' :
            EsTest._bulk_insert(eventList)
        elif action=='getInfo' :
            nodeIndex = input("which node #? ")
            answer =EsTest.get_info(nodeIndex)
            print(answer)
        elif action=='count':
            print(EsTest._count())
        elif action=='sd' :
            criteria = input("what you looking for? ")
            solution=EsTest.description_search(criteria)
            print(solution)
        else:
            print("Unknown action:%s ",action)
        pass



