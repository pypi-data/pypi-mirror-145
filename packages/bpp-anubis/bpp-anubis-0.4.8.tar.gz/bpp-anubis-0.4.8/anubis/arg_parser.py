import argparse


def parse_arguments():
    parser = argparse.ArgumentParser('Running in parallel mode')

    # parallelism
    parser.add_argument('--processes',       '-p',  required=True, default=1,  type=int)
    parser.add_argument('--env',             '-e',  required=True, type=str)

    # dir/file paths
    parser.add_argument('--feature_dir',     '-fd', required=True, default='features')
    parser.add_argument('--output_dir',      '-od', required=True, default='output')
    parser.add_argument('--result_file',     '-rf')
    parser.add_argument('--account_file',    '-af', required=True)
    parser.add_argument('--account_section', '-as')

    # direct behave arguments (every bpp QA project requires these)
    parser.add_argument('--browser',         '-br', required=False)
    parser.add_argument('--headless',        '-hd', required=False, action='store_true')
    parser.add_argument('--itags',           '-it', required=False, nargs='+')
    parser.add_argument('--etags',           '-et', required=False, default=[], nargs='+')
    parser.add_argument('--retry',           '-rt', required=False, default=1,  type=int)

    return parser.parse_known_args()
