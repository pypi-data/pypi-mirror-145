
#!/usr/bin/env python3

# File: create_d3m_dataset.py 
# Author(s): Saswati Ray
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import json
import argparse
import shutil
import os
from os.path import exists
from d3m.container import Dataset
from d3m.utils import fix_uri
from d3m.container.utils import save_container

basic_json_problem = {
  "about": {
    "problemID": "raw_problem",
    "problemName": "raw_problem",
    "problemVersion": "1.0",
    "problemSchemaVersion": "4.1.0",
    "taskKeywords": [
      "classification"
    ]
  },
  "inputs": {
    "data": [
      {
        "datasetID": "raw_dataset",
        "targets": [
          {
            "targetIndex": 0,
            "resID": "learningData",
            "colIndex": 18,
            "colName": "LABEL"
          }
        ]
      }
    ],
    "performanceMetrics": [
      {
        "metric": "f1Macro"
      }
    ]
  },
  "expectedOutputs": {
    "predictionsFile": "predictions.csv"
  }
}


# Get file formats for image/audio/video
def getFormat(t):
    if t == "image":
        return {"image/jpeg": ["jpeg", "jpg"]}
    elif t == "text":
        return {"text/plain": ["txt"]}
    elif t == "audio":
        return {
        "audio/wav": [
          "wav"
        ],
        "audio/aiff": [
          "aif",
          "aiff"
        ],
        "audio/flac": [
          "flac"
        ],
        "audio/ogg": [
          "ogg"
        ],
        "audio/mpeg": [
          "mp3"
        ]
      }
    else:
        return {
        "video/mp4": [
          "mp4"
        ]
      }

# Process task time series forecasting
def process_forecasting_task(TRAIN_DATASET_PATH, TEST_DATASET_PATH):
    time_column = input("Please enter column name for date/time column: ")
    grouping_column = input("Please enter column name for grouping/category column: ")

    for PATH in [TRAIN_DATASET_PATH, TEST_DATASET_PATH]:
        with open(PATH+'datasetDoc.json') as f:
            basic_json_dataset = json.load(f)
            columns = basic_json_dataset["dataResources"][0]["columns"]
            for c in columns:
                if c["colName"] == time_column:
                    c["role"].append("timeIndicator")
                    c["role"].append("attribute")
                    c["colType"] = "dateTime"
                elif c["colName"] == grouping_column:
                    c["role"].append("suggestedGroupingKey")
                    c["role"].append("attribute")
                    c["colType"] = "categorical"
        with open(PATH+'datasetDoc.json', "w") as jsonFile:
            json.dump(basic_json_dataset, jsonFile, indent=4)    

# Process task keywords for image, audio, video, text, timeSeries
def process_tasks(tasks, TRAIN_DATASET_PATH, TEST_DATASET_PATH):
    for t in tasks:
        # Multimedia datasets
        if t == "image" or t == "audio" or t == "video" or t == "text":
            trainMediaDir = input("Please enter directory name for TRAIN media files: ")  
            testMediaDir = input("Please enter directory name for TEST media files: ")
            image_column = input("Please enter column name for media files: ")
            media = {}
            media["resID"] = "0"
            media["resPath"] = "media/"
            media["resType"] = t
            media["resFormat"] = getFormat(t)
            media["isCollection"] = True

            for PATH in [TRAIN_DATASET_PATH, TEST_DATASET_PATH]: 
                with open(PATH+'datasetDoc.json') as f:
                    basic_json_dataset = json.load(f)
                columns = basic_json_dataset["dataResources"][0]["columns"]
                for c in columns:
                    if c["colName"] == image_column:
                        c["role"].append("attribute")
                        c["colType"] = "string"
                        c["refersTo"] = {"resID": "0", "resObject": "item"}
                basic_json_dataset["dataResources"].append(media)
                with open(PATH+'datasetDoc.json', "w") as jsonFile:
                    json.dump(basic_json_dataset, jsonFile, indent=4)
            shutil.copytree(trainMediaDir, TRAIN_DATASET_PATH+'media')
            shutil.copytree(testMediaDir, TEST_DATASET_PATH+'media')
        elif t == "timeSeries":
            trainTSDir = input("Please enter directory name for TRAIN TS files: ")
            testTSDir = input("Please enter directory name for TEST TS files: ")
            timeseries_column = input("Please enter column name for timeseries files: ")
            media = {}
            media["resID"] = "0"
            media["resPath"] = "timeseries/"
            media["resType"] = "timeseries"
            media["resFormat"] = {"text/csv": ["csv"]}
            media["isCollection"] = True
            media["columns"] = []
            media["columns"].append({"colIndex": 0, "colName": "time", "colType": "integer", "role": ["timeIndicator"]})

            for PATH in [TRAIN_DATASET_PATH, TEST_DATASET_PATH]:
                with open(PATH+'datasetDoc.json') as f:
                    basic_json_dataset = json.load(f)
                columns = basic_json_dataset["dataResources"][0]["columns"]
                for c in columns:
                    if c["colName"] == timeseries_column:
                        c["role"].append("attribute")
                        c["colType"] = "string"
                        c["refersTo"] = {"resID": "0", "resObject": "item"}
                basic_json_dataset["dataResources"].insert(0, media)
                with open(PATH+'datasetDoc.json', "w") as jsonFile:
                    json.dump(basic_json_dataset, jsonFile, indent=4)
            shutil.copytree(trainTSDir, TRAIN_DATASET_PATH+'timeseries')
            shutil.copytree(testTSDir, TEST_DATASET_PATH+'timeseries')
        elif t == "forecasting":
            process_forecasting_task(TRAIN_DATASET_PATH, TEST_DATASET_PATH)


# Create TRAIN and TEST directories. Creates d3mIndex column for each data file.
def create_directories(DATASET_PATH, PROBLEM_PATH, dataFileName, target_name, basic_json_problem):
    if exists(DATASET_PATH):
        shutil.rmtree(DATASET_PATH)
    if exists(PROBLEM_PATH):
        shutil.rmtree(PROBLEM_PATH)

    dataset = Dataset.load(fix_uri(dataFileName), dataset_id='raw_dataset')
    save_container(dataset, DATASET_PATH)

    colIndex = dataset['learningData'].columns.get_loc(target_name)
    basic_json_problem["inputs"]["data"][0]['targets'][0]['colIndex'] = colIndex
    
    os.makedirs(PROBLEM_PATH)
    with open(PROBLEM_PATH+"/problemDoc.json", "w") as jsonFile:
        json.dump(basic_json_problem, jsonFile, indent=4)
    with open(DATASET_PATH+'datasetDoc.json') as f:
        basic_json_dataset = json.load(f)
    basic_json_dataset["about"]["datasetSchemaVersion"] = "4.1.0"
    basic_json_dataset["about"]["datasetVersion"] = "1.0" 
    with open(DATASET_PATH+'datasetDoc.json', "w") as jsonFile:
        json.dump(basic_json_dataset, jsonFile, indent=4)

def main():
    # Available are the following parameters-
    # Metrics to use are - accuracy, f1Macro, f1Micro, rocAuc, rocAucMacro, rocAucMicro, 
    #                      rSquared, meanSquaredError, meanSquaredError, meanAbsoluteError, 
    #                      normalizedMutualInformation
    # Tasks to use are : video, linkPrediction, graphMatching, forecasting, classification, graph, semiSupervised, text, timeSeries, 
    #                    clustering, collaborativeFiltering, regression, audio, objectDetection, vertexNomination, communityDetection, image, 
    #                    vertexClassification

    # python create_d3m_dataset.py <dataFileName> <testDataFileName> <target> <metric> -t/--tasks
    # Sample command to use: python create_d3m_dataset.py data.csv data.csv Hall_of_Fame f1Macro -t classification -t tabular

    parser = argparse.ArgumentParser(description="Raw dataset specifications")
    parser.add_argument("dataFileName", type=str, help="dataset TRAIN filename")
    parser.add_argument("testDataFileName", type=str, help="dataset TEST filename")
    parser.add_argument("target", type=str, help="Target")
    parser.add_argument("metric", type=str, help="Metric")
    parser.add_argument('-t','--tasks', action='append', help='Task(s)', required=True)
    args = parser.parse_args()
    print(args)

    TRAIN_DATASET_PATH = './raw/TRAIN/dataset_TRAIN/'
    TRAIN_PROBLEM_PATH = './raw/TRAIN/problem_TRAIN/'
    TEST_DATASET_PATH = './raw/TEST/dataset_TEST/'
    TEST_PROBLEM_PATH = './raw/TEST/problem_TEST/'

    basic_json_problem["inputs"]["data"][0]['targets'][0]['colName'] = args.target
    basic_json_problem["inputs"]['performanceMetrics'][0]['metric'] = args.metric
    basic_json_problem["about"]['taskKeywords'] = []
    for t in args.tasks:
        basic_json_problem["about"]['taskKeywords'].append(t)
    
    print("Going to create TRAIN files!")
    create_directories(TRAIN_DATASET_PATH, TRAIN_PROBLEM_PATH, args.dataFileName, args.target, basic_json_problem)
    print("Going to create TEST files!")
    create_directories(TEST_DATASET_PATH, TEST_PROBLEM_PATH, args.testDataFileName, args.target, basic_json_problem)

    process_tasks(args.tasks, TRAIN_DATASET_PATH, TEST_DATASET_PATH)

if __name__=="__main__":
    main()
