#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 17:24:22 2017
@author: aj
This program queries Elasticsearch with each individual query and writes the retrieved results to an output file in the standard trec_eval format.
There are 30 query topics provided for which this program retrieves the search results. More information about this can be found here: http://trec-cds.appspot.com/2017.html
"""



import collections
from elasticsearch import Elasticsearch
from os import listdir
from os.path import join



def es_query(query, index_, queryFile):
       """
       This function is used to query Elasticsearch and write results to an output file.
       It receives a dictionary containing the extracted query terms from the extract_query_xml function. After querying Elasticsearch, the retrieved results are written to an output file in the standard trec_eval format.
       """
       
       try:
              #Store the disease name from the received dictionary in the variable named query
              
              #For a simple query without any customizations, uncomment the following line
              #res = es.search(index='ct', q=query, size=1000)['hits']['hits']
              #Current implementation uses a customized query with multi-match and post-filters in a manner deemed best possible for the current retrieval process. Comment the following query if you plan to use the simple query in the previous line.
              #We limit the retrieved results to 1000. The results are arranged in decreasing order of their assigned scores. We assign a rank to each result starting from 1 to 1000 based on decreasing scores. We normalize the score for each result based on the score of the first result with the maximum score.
              print("index_:", index_)
              res = es.search(index=index_, body={
                                          "query":
                                                 {"bool":
                                                        {"must":
                                                               {"multi_match":
                                                                      {"query":query, "type":"phrase_prefix", "fields":["brief_title","brief_summary","detailed_description","condition", "eligibility","keyword","mesh_term"]
                                                                      }
                                                               },
                                                         "should":
                                                                [
                                                                 {"term":{"eligibility" : "query"}},
                                                                 {"term":{"brief_summary" : "query"}},
                                                                 {"term":{"detailed_description" : "query"}},
                                                                 {"term":{"keyword" : "query"}},
                                                                ]
                                                        }
                                                 },
                                          "post_filter":
                                                 {"term":
                                                        {"gender":"all"}
                                                 }
                                          },
                                   size=1000
                     )['hits']['hits']
              
              
              #Write the retrieved results to an output file in the standard trec_eval format
              with open(join(output_path, queryFile + "_" + query + ".txt"), 'a') as op_file:
                     for i in res:
                            # op_file.write('Q' + str(tnum) + '\t{}\t{}\n'.format(i['_source']['nct_id'],rank_ctr,round(i['_score']/max_score,4)))
                            op_file.write(i['_source']['nct_id']+"\n")
                            
               
       except Exception as e:
              print("\nUnable to query/write!")
              print('Error Message:',e,'\n')
       
       return




if __name__ == '__main__':
       #Create connection to Elasticsearch listening on localhost port 9200. It uses the Python Elasticsearch API which is the official low-level client for Elasticsearch.
       try:
              es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
              
              input_path = "../data/queries/less_precision_queries"
              queryFiles = sorted(listdir(input_path))
              output_path = "../data/lowPrecisionqueriesResultBaseline"
              
              for queryFile in queryFiles:
                fp = open(join(input_path, queryFile), "r")
                queries = fp.readlines()
                fp.close()
                index_ = queries[0].strip()
                print(index_)
                queries = queries[1:]
                for query in queries:
                  print(query.strip())
                  es_query(query.strip(), index_, queryFile.split(".")[0].strip())
                print()


              	
              	

       except Exception as e:
              print('\nCannot connect to Elasticsearch!')
              print('Error Message:',e,'\n')
       #Call the function to start extracting the queries