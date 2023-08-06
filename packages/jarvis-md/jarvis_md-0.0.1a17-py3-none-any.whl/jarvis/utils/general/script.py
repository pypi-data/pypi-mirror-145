import os, time

def create_script(cmd, env=None, name=None, shell='/bin/bash', output_dir='./', check=False, verbose=True, **kwargs):
    """
    Method to automate creation of shell scripts spanning permutation of ENV variables

    EXAMPLES

    # create(..., env={'CUDA_VISIBLE_DEVICES': '0:4'})
    # create(..., env={'CUDA_VISIBLE_DEVICES': '0,2:4'})
    # create(..., env={'CUDA_VISIBLE_DEVICES,JARVIS_SPLIT': '0:4'})
    # create(..., env={'CUDA_VISIBLE_DEVICES': '0:4', 'JARVIS_SPLIT': '0:4'})

    """
    # --- Create list of env permutations
    permutations = ['']
    ranges = lambda x : range(int(x.split(':')[0]), int(x.split(':')[1])) if ':' in x else [x]

    # --- Parse env
    if type(env) is str:
        env = {e.split('=')[0]: e.split('=')[1] for e in env.split(';')}

    for ks, vs in env.items():

        # --- Create permutations of current key-value pair
        ks = ks.split(',')
        vs = vs.split(',')
        vs = [v for v_ in vs for v in ranges(v_)]
        es = [''.join(['\nexport {}={}'.format(k, v) for k in ks]) for v in vs]

        # --- Add to permutations for all other existing pairs
        permutations = ['{}{}'.format(p, e) for p in permutations for e in es]

    # --- Create output dir
    name = name or '{}-{}'.format(os.environ['HOME'].split('/')[-1], time.strftime('%Y%m%d-%H%M%S'))

    output_dir = output_dir or './'
    if output_dir[-1] != '/':
        output_dir += '/'

    if not check:
        os.makedirs(output_dir, exist_ok=True)

    for n, env in enumerate(permutations):

        fname = '{}{}-{:04d}.sh'.format(output_dir, name, n) if len(permutations) > 1 else '{}{}.sh'.format(output_dir, name)

        if verbose:
            print('=' * 120)
            print('Creating file: {}'.format(fname), end='')
            print(env)
            print(cmd)

        if not check:

            # --- Write file
            with open(fname, 'w') as f:
                
                f.write('#!{}\n'.format(shell))
                f.write('{}\n'.format(env))
                f.write('{}'.format(cmd))

            # --- Change permissions
            os.chmod(fname, 0x0755)
