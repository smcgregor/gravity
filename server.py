#!/usr/bin/env python
''' Generic Interface for MDPs to MDPVis; 
    output format supported = json '''
import sys
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from urlparse import urlparse, parse_qs
from FireGirlOptimizer import *

#
# Return data
#
def get_initialize(query):
    """Function returns a set of name:value pairs describing which
    controls/options will be available on the web visualization.

    General return value format as follows:
    {
    "reward": [
    {"name": "Discount",  "description":"The per-year discount", "current_value": 1, "max": 1, "min": 0, "units": "-"},
    {"name": "Board Feet",  "description":"The number of dollars per board foot for wood", "current_value": 10, "max": 100, "min": 0, "units": "$"},
    {"name": "Suppression Fixed Cost",  "description":"How much it costs to suppress a fire regardless of size.", "current_value": 1000, "max": 1000000, "min": 0, "units": "$"},
    {"name": "Suppression Marginal Cost",  "description":"How much it costs per hectare of burnt land to suppress a fire.", "current_value": 500, "max": 10000, "min": 0, "units": "$"},
    {"name": "Old Growth Value",  "description":"How much every hectare of old growth trees are valued.", "current_value": 100, "max": 100000, "min": 0, "units": "$"},
    {"name": "Forested Mountain Bike Trail",  "description":"The number of dollars each mountain bike trail is worth.", "current_value": 10, "max": 1000, "min": 0, "units": "$"}
    ],
    "transition": [
    {"name": "Number of Fires Per Year",  "description":"The total number of separate fires experiences per year.", "current_value": 1, "max": 1, "min": 1, "units": ""},
    {"name": "Fire spread rate",  "description":"The feet per hour spread of wildfires, normalized to wind.", "current_value": 10, "max": 10, "min": 10, "units": ""}
    ],
    "policy": [
    {"name": "Wind Speed",  "description":"for each kilometer per hour", "current_value": 0.8, "max": 10000, "min": -10000, "units": ""},
    {"name": "Humidity",  "description":"for each percent relative humidity", "current_value": -0.12, "max": 10000, "min": -10000, "units": ""},
    {"name": "Day",  "description":"for each day of the fire season", "current_value": -0.15, "max": 10000, "min": -10000, "units": ""},
    {"name": "Constant",  "description":"the intercept", "current_value": 9, "max": 10000, "min": 10000, "units": ""}
    ]
    }
    """
    # Hailey todo: return an object following the spec Sean Provides

    return_val = {
            "reward": [
                        {"name": "Discount",
                         "description":"The per-year discount",
                         "current_value": 1, "max": 1, "min": 0, "units": "-"},
                        {"name": "Suppression Fixed Cost",
                         "description":"cost per day of suppression",
                         "current_value": 500, "max": 999999, "min": 0, "units": "$"},
                        {"name": "Suppression Variable Cost",
                         "description":"cost per hectare of suppression",
                         "current_value": 500, "max": 999999, "min": 0, "units": "$"}
                        ],
            "transition": [
                         {"name": "Harvest Percent",
                          "description": "timber harvest rate as a percent of annual increment",
                          "current_value": 0.95, "max": 1, "min": 0, "units": "%"},
                         {"name": "Minimum Timber Value",
                          "description":"the minimum timber value required before harvest is allowed",
                          "current_value": 50, "max":9999, "min": 0, "units": "$"},
                         {"name": "Slash Remaning",
                          "description": "the amount of fuel load (slash) left after a harvest",
                          "current_value": 10, "max":9999, "min": 0, "units": "-"},
                         {"name": "Fuel Accumulation",
                          "description": "the amount of fuel load that accumulates each year",
                          "current_value": 2, "max":9999, "min": 0, "units": "-"},
                         {"name": "Suppression Effect",
                          "description": "the reduction in fire spread rate as the result of suppression",
                          "current_value": 0.5, "max":1, "min": 0, "units": "%"}
                         ],
            "policy": [
                        {"name": "Constant",
                         "description":"for the intercept",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Date",
                         "description":"for each day of the year",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Days Left",
                         "description":"for each day left in the year",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name":"Temperature",
                         "description":"for air temperature at the time of an ignition",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Wind Speed",
                         "description":"for wind speed at the time of an ignition",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Timber Value",
                         "description":"for the timber value at an ignition location",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Timber Value 8",
                         "description":"for the average timber value in the 8 neighboring stands",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Timber Value 24",
                         "description":"for the average timber value in the 24 neighboring stands",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Fuel Load",
                         "description":"for the fuel load at an ignition location",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Fuel Load 8",
                         "description":"for the average fuel load in the 8 neighboring stands",
                         "current_value": 0, "max": 10, "min":-10, "units": ""},
                        {"name": "Fuel Load 24",
                         "description":"for the average fuel load in the 24 neighboring stands",
                         "current_value": 0, "max": 10, "min":-10, "units": ""}

                      ]
                }

    return return_val

def get_rollouts(query):
    # Hailey todo: return an object following the spec Sean Provides
    """Generates FireGirl pathways and returns a host of data from their histories

    Returns in the form:
    [
    [{"variable name":"variable value", ...}, {"variable name":"variable value", ...}],
    [{"variable name":"variable value", ...}, {"variable name":"variable value", ...}],
    ...
    ]
    which is a list containing one element per pathway. Each element is itself a list of 
    dictionaries representing each year of a pathway's evolution, and containing pertanent 
    information about that year.

    """

    query = {
            "reward": {  "Discount": 1,
                         "Suppression Fixed Cost": 500, 
                         "Suppression Variable Cost": 500
                      },
                        
            "transition": {"Harvest Percent": 0.95,
                           "Minimum Timber Value": 50,
                           "Slash Remaning": 10,
                           "Fuel Accumulation": 2,
                           "Suppression Effect": 0.5
                          },
                         
            "policy": { "Constant": 0, 
                        "Date": 0,
                        "Days Left": 0,
                        "Temperature": 0,
                        "Wind Speed": 0,
                        "Timber Value": 0,
                        "Timber Value 8": 0,
                        "Timber Value 24": 0,
                        "Fuel Load": 0,
                        "Fuel Load 8": 0,
                        "Fuel Load 24": 0
                       }      
                }

    dict_reward = query["reward"]
    dict_transition = query["transition"]
    dict_policy = query["policy"] 

    pathway_count = 100
    years = 100
    start_ID = 0

    #generate 100 rollouts
    opt = FireGirlPolicyOptimizer()
    opt.setObjFn("J1")
    #opt.setObjFn("J2")
    opt.SILENT = True
    
    #setting policy...
    #This is brittle, and will not work directly with FireWoman data... or with future versions
    # of FireGirl if new features get added...
    pol = FireGirlPolicy()
    pol.setParams([dict_policy["Constant"],
                   dict_policy["Date"],
                   dict_policy["Days Left"],
                   dict_policy["Temperature"],
                   dict_policy["Wind Speed"],
                   dict_policy["Timber Value"],
                   dict_policy["Timber Value 8"],
                   dict_policy["Timber Value 24"],
                   dict_policy["Fuel Load"],
                   dict_policy["Fuel Load 8"],
                   dict_policy["Fuel Load 24"],
                  ])

    #setting the policy in the optimizer, which will pass it to each created pathway
    opt.setPolicy(pol)

    #creating landscapes
    opt.createFireGirlPathways(pathway_count,years,start_ID)

    #outermost list to collect one sub-list for each pathway, etc...
    return_list = []

    #parse the data needed...
    for pw in opt.pathway_set:
        #new ignition events list for this pathway
        year_values = []
        for ign in pw.ignition_events:

            #make a dictionary for the yearly totals (supp cost, harvest, etc...)
            totals = {}

            #fill the total's dictionary
            totals["Harvest Value"] = pw.getHarvest(pw.index(ign))
            totals["Suppression Cost"] = pw.getSuppressionCost(pw.index(ign))
            totals["Growth"] = pw.getGrowth(pw.index(ign))


            #get the dictionary representation of the ignition
            features = ign.getDictionary()

            #concatenate the dictionaries
            totals.update(features)

            #add this ignition event + year details to this pathway's list of dictionaries
            year_values.append(totals)


        #the events list for this pathway has been filled, so add it to the return list
        return_list.append(year_values)

    #done with all pathways

    return return_list

def get_state(query):
    # Hailey todo: return an object following the spec Sean Provides
    return {'todo':'get_state'}

def get_optimize(query):
    # Hailey todo: return an object following the spec Sean Provides
    return {'todo':'get_optimize'}

# Request Handlers
class Handler(BaseHTTPRequestHandler):

    #handle GET command
    def do_GET(self):
        parsedQuery = urlparse(self.path)
        path = parsedQuery[2]
        print("processing get request:" + path)
        queryString = parsedQuery[4]
        queryDict = parse_qs(queryString)# todo, send this to the get_rollouts function
        
        if path == "/initialize":
            ret = json.dumps(get_initialize(queryDict))
            self.request.sendall(ret)
        elif path == "/rollouts":
            ret = json.dumps(get_rollouts(queryDict))
            self.request.sendall(ret)
        elif path == "/state":
            ret = json.dumps(get_state(queryDict))
            self.request.sendall(ret)
        elif path == "/optimize":
            ret = json.dumps(get_optimize(queryDict))
            self.request.sendall(ret)
        else:
            # Serve the visualization's files
            try:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
        return

# Starting Server
#note that this potentially makes every file on your computer readable by the internet
def run(port=8000):

    print('http server is starting...')
    print('note that this could potentially make all your files readable over the internet')
    server_address = ('127.0.0.1', port) #ip and port of server
    httpd = HTTPServer(server_address, Handler)
    print('http server is running...listening on port %s' %port)
    httpd.serve_forever()

if __name__ == '__main__':
    from optparse import OptionParser
    op = OptionParser(__doc__)
    op.add_option("-p", default=8000, type="int", dest="port", 
                  help="port #")
    opts, args = op.parse_args(sys.argv)
    run(opts.port)