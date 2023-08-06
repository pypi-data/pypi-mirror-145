import os, pandas as pd, json, glob
from ...utils.general import *
from ...utils.general import tools as jtools

def load(csv=None, row=0, client='client.yml', **kwargs):
    """
    Method to load CSV file with training hyperparameters

    :params

      (str) csv        : CSV file with hyperparameter values
      (int) row        : row of CSV file to load 
      (str) project_id : name of project_id if relative paths should be expanded
      (str) version_id : name of version_id if relative paths should be expanded

    Note that while any CSV file format is compatible, the following columns are recommended:

    project_id | output_dir | _client                | fold | ...
    ------------------------------------------------------------------
    project_id | ./exp01-0    /path/to/client.yml      0
    project_id | ./exp01-1    /path/to/client.yml      1
    project_id | ./exp01-2    /path/to/client.yml      2
    ------------------------------------------------------------------

    The _client row typically contains the source TEMPLATE client.yml file. If both _client
    and output_dir columns are present, then the following OUTPUT client file is inferred:

      client = '{}/{}'.format(output_dir, client)

    If this OUTPUT client file exists, the '_client' column is changed to the new OUTPUT file.

    """
    # --- Extract ENVIRON variables if present 
    csv = os.environ.get('JARVIS_PARAMS_CSV', None) or csv
    row = int(os.environ['JARVIS_PARAMS_ROW']) if 'JARVIS_PARAMS_ROW' in os.environ else row

    if csv is None:
        printd('ERROR no *.csv found')
        return

    # --- Load row
    df = pd.read_csv(csv)

    # --- Format dict
    p = json.loads(df.iloc[row].to_json())

    # --- Convert relative path names if needed
    p = expand_paths(p=p, csv=csv)

    # --- Convert client path
    if type(p.get('_client', None)) is str and type(p.get('output_dir', None)) is str:
        client = '{}/{}'.format(p['output_dir'], client)
        if os.path.exists(client):
            p['_client'] = client

    return p

def expand_paths(p, csv=None):

    _id = jtools.parse_ids(**p)

    if _id['project'] is not None:
        paths = jtools.get_paths(_id['project'], _id['version'], alt_path=csv)
        root = paths.get('code', '')
        p = {k: v.format(root=root) if type(v) is str else v for k, v in p.items()}

        p['_id'] = _id
        p['_paths'] = paths

    return p

def create_script_jmodels(jmodels=None, name=None, csv=None, py=None, rows=None, output_dir='./', check=False, prefix=None, **kwargs):

    # --- Find *.csv file
    csv = find_files(jmodels, base=csv, exts=['csv'])

    # --- Find *.py/ipynb file
    py = find_files(jmodels, base=py, exts=['py', 'ipynb'])

    if py is None or csv is None:
        return

    # --- Load *.csv file
    df = pd.read_csv(csv)

    # --- Find command
    cmd = {
        'py': 'python',
        'ipynb': 'ipython'}.get(py.split('.')[-1], None)

    if cmd is None:
        printd('ERROR fname ext (*.{}) not recognized'.format(py.split('.')[-1]))
        return

    # --- Add command prefix
    if prefix is not None:
        cmd = prefix + '\n' + cmd
        cmd = cmd.replace('\\n', '\n')

    # --- Find rows
    if rows is None:
        rows = [i for i in range(df.shape[0])]

    elif type(rows) is str:
        ranges = lambda x : range(int(x.split(':')[0]), int(x.split(':')[1])) if ':' in x else [x]
        rows = rows.split(',')
        rows = [r for row in rows for r in ranges(row)]

    # --- Create ENV dictionary
    env = {
        'JARVIS_PATH_CONFIGS': jtools.find_configs_dir(alt_path=py),
        'JARVIS_PARAMS_CSV': csv}

    # --- Create name
    name = name or os.path.basename(py).split('.')[0]

    # --- Create scripts
    for n, row in df.iloc[rows].iterrows():

        row = expand_paths(p=row, csv=csv)
        env['JARVIS_PARAMS_ROW'] = str(n) 
        out = ' > {}/stdout 2>&1'.format(row['output_dir']) if 'output_dir' in row else ''
        CMD = '{} {}{}'.format(cmd, py, out)
        name_ = '{}-{:04d}'.format(name, n)

        if not check and 'output_dir' in row:
            os.makedirs(row['output_dir'], exist_ok=True)

        create_script(cmd=CMD, env=env, name=name_, output_dir=output_dir, check=check, **kwargs)

def find_files(jmodels, base, exts):

    base = base or ''

    for e in exts:
        fname = glob.glob('{}/*{}*.{}'.format(jmodels, base, e))

        if len(fname) > 1:
            flag = '-csv' if 'csv' in e else '-py'
            printd('ERROR more than one file of type *.{} found; please specify with {} flag'.format(e, flag))
            return

        if len(fname) == 1:
            return os.path.abspath(fname[0])

    printd('ERROR no {} file found'.format(exts))
