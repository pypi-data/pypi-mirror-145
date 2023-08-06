# __main__.py
import os
import json
import multiprocessing
from multiprocessing import Pool
import sys
from datetime import datetime
from pathlib import Path
import re

# custom
from . import account_splitter, feature_splitter, arg_parser, results
from .parallelizer import command_generator

ANUBIS_ASCII = ("""
                 ♡♡                                               
                ♡♡♡                                                 
              ♡♡ ♡♡♡♡                                               
         ♡♡♡♡♡♡♡♡♡♡♡♡                                               
                 ♡♡♡♡♡                                              
                  ♡♡♡♡♡                                             
               ♡♡♡♡♡♡♡♡♡                                            
              ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡        ♡♡♡♡♡♡                         
              ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡ ♡♡♡♡                     
              ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡                   
          ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡     ♡♡♡♡♡♡♡♡♡♡                  
♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡       ♡♡♡♡♡     ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡                 
                                                    ♡♡♡              
          POWERED BY ANUBIS                          ♡♡♡♡            
(and the power of love  Σ>―(〃°ω°〃)♡→)               ♡♡♡♡♡          
                                                      ♡♡♡♡♡         
                                                       ♡♡♡♡         
                                                        ♡♡     """)


def main():
    print(ANUBIS_ASCII)
    start = datetime.now()

    # parse arguments
    _known_args, _unknown_args = arg_parser.parse_arguments()

    # <editor-fold desc="--- Set up the output directories for the run">
    # create a dir that will contain results and be exported
    print('--- SETTING UP OUTPUT')
    if not os.path.isdir(_known_args.output_dir):
        print(f'\tThe run output should go to <{_known_args.output_dir}> but it doesn\'t exist (creating it now)')
        os.makedirs(_known_args.output_dir, exist_ok=True)
    else:
        print(f'\tSending the output of this run to <{_known_args.output_dir}>')

    aggregate_out_file = _known_args.result_file if _known_args.result_file else '.temp_results.json'

    if not os.path.isfile(aggregate_out_file):
        print(f'\tThe directory to store <{aggregate_out_file}> doesn\'t exist (creating it now)')
        agg_fp = Path(aggregate_out_file)
        agg_fp.parent.mkdir(parents=True, exist_ok=True)
    # </editor-fold>

    # set up the multiple processes
    multiprocessing.set_start_method('fork')
    pool = Pool(_known_args.processes)

    # <editor-fold desc="--- Set up the accounts for the run">
    # get account data available for parallel runs
    # the `accounts_data` list looks like this --> [(<run_name>, "user pass"), [<list of feature files>]]
    if _known_args.account_file and _known_args.account_section:
        print('\n--- PARSING ACCOUNTS')
        print(f'\tfile:    <{_known_args.account_file}>')
        print(f'\tsection: <{_known_args.account_section}>')
        accounts_data = account_splitter.get_accounts(_known_args.processes, _known_args.account_file, _known_args.account_section)
    elif _known_args.account_file:
        print('\n--- PARSING ACCOUNTS')
        print(f'\tfile:    <{_known_args.account_file}>')
        accounts_data = account_splitter.get_all_accounts_reader(_known_args.processes, _known_args.account_file)
    else:
        print('\n--- ACCOUNTS NOT SPECIFIED')
        print('\tusing timestamps, instead of accounts, for output file names')
        # create dummy account data just for the purpose of naming the runs
        accounts_data = [(re.sub(r'[-:.]', '', datetime.now().isoformat()), 'NONE NONE') for i in range(_known_args.processes)]
    # </editor-fold>

    # <editor-fold desc="--- Set up the features">
    # split the features and store as list
    print('\n--- GROUPING FEATURES & ACCOUNTS')
    print(f'\tfeature dir:   <{_known_args.feature_dir}>')
    print(f'\tincluded tags: <{",".join([t for t in _known_args.itags]) if _known_args.itags else "(none)"}>')
    print(f'\texcluded tags: <{",".join([t for t in _known_args.etags]) if _known_args.etags else "(none)"}>')
    if _known_args.account_section:
        feature_groups = feature_splitter.get_features(_known_args, accounts_data)
    else:
        feature_groups = feature_splitter.get_features_with_general_accounts(_known_args)

    # run all the processes and save the locations of the result files
    num_groups = len(feature_groups)
    print(f'\n--- RUNNING <{num_groups} PROCESS{"ES" * int(num_groups > 1)}>')
    result_files = pool.map(command_generator, feature_groups)
    # </editor-fold>

    # <editor-fold desc="--- Combine the results">
    res_string = None

    try:
        print('--- HANDLING RESULTS')
        # create the aggregate file and calculate pass/fail rate
        results.create_aggregate(files=result_files, aggregate_out_file=aggregate_out_file)

        with open(aggregate_out_file) as f:
            res = json.load(f)

        statuses = []
        for feature in res:
            if 'elements' in feature:
                for scenario in feature['elements']:
                    if scenario['type'] != 'background':
                        statuses.append(scenario['status'])

        passed = statuses.count('passed')
        failed = statuses.count('failed')
        res_string = f'{passed / (passed + failed) * 100:.2f}%'
    except Exception as e:
        if _known_args.result_file:
            print(f'There was an error combining results\n{e}')
        else:
            pass

    if not _known_args.result_file:
        os.remove(aggregate_out_file)
    # </editor-fold>

    end = datetime.now()

    # <editor-fold desc="extremely basic summary">
    print('\n===========♡𓃥♡ SUMMARY ♡𓃥♡===========')
    print(f'Env:       <{_known_args.env}>')
    print(f'Browser:   <{_known_args.browser}>') if _known_args.browser else None
    print(f'Results:   <{_known_args.result_file}>') if _known_args.result_file else None
    print(f'Pass Rate: <{res_string if res_string else "could not calculate"}>')
    print(f'Run Time:  <{(end - start)}>')
    print('=======================================')
    # </editor-fold>


if __name__ == '__main__':
    # run everything
    main()
    sys.exit(0)
