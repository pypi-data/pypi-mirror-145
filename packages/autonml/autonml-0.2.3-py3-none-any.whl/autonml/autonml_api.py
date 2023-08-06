# File: autonml_api.py 
# Author(s): Vedant Sanil
# Created: Wed Feb 17 11:49:20 EST 2022 
# Description:
# Acknowledgements:
# Copyright (c) 2022 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import os, json
import shutil
import subprocess
import pandas as pd

class AutonML(object):
    def __init__(self, input_dir, output_dir, timeout=2, numcpus=8):
        self.input_dir = os.path.abspath(input_dir)
        self.output_dir = os.path.abspath(output_dir)
        self.timeout = str(timeout)
        self.numcpus = str(numcpus)
        self.problemPath = os.path.join(self.input_dir, 'TRAIN', 'problem_TRAIN', 'problemDoc.json')
        self.rank_df = None

    def run(self):
        proc = subprocess.Popen(['autonml_main', self.input_dir, 
                                self.output_dir, self.timeout, self.numcpus,
                                self.problemPath], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        output, error = proc.communicate()
        if proc.returncode != 0:
            print(output)
            raise RuntimeError(error.decode())

    def get_run_id(self):
        # Get the most recent run
        run_dirs = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir)]
        output_dir = sorted(run_dirs, key=lambda x: os.path.getmtime(x), reverse=True)[0]

        return output_dir

    def rank_pipelines(self):
        # Get the most recent run
        output_dir = self.get_run_id()

        # Load evaluation metric
        problemDocDir = os.path.join(self.input_dir, 'TRAIN', 'problem_TRAIN', 'problemDoc.json')
        with open(problemDocDir, 'r') as f:
            problem_dict = json.load(f)
        metric = problem_dict['inputs']['performanceMetrics'][0]['metric']

        # Search through ranked pipelines and record scores
        pipe_dir = os.path.join(output_dir, 'pipelines_ranked')
        rank_dict = {'Rank':[], 'Pipeline ID':[], 'Pipeline Description':[], f'Metric: {metric}':[]}
        for f in os.listdir(pipe_dir):
            f_path = os.path.join(pipe_dir, f)
            with open(f_path, 'r') as f:
                f_dict = json.load(f)

            rank_dict['Rank'].append(int(f_dict['pipeline_rank']))
            rank_dict['Pipeline ID'].append(f_dict['id'])

            desc = ""
            for idx, s in enumerate(f_dict['steps']):
                if s['type'] == 'PRIMITIVE':
                    desc += s['primitive']['name']
                    if idx != len(f_dict['steps'])-1:
                        desc += ", "
            
            rank_dict['Pipeline Description'].append(desc)
            rank_dict[f'Metric: {metric}'].append(float(f_dict['pipeline_score']))

        rank_df = pd.DataFrame.from_dict(rank_dict)
        rank_df = rank_df.sort_values(by=['Rank'], ignore_index=True)
        self.rank_df = rank_df
        
        return rank_df.style.hide_index()
        
