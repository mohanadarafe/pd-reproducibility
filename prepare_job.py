'''
The following script prepares the MRI volume execution by:
- Creating necessary folders
- Creating JSON inputs for Boutiques
- Creating SLURM scripts for Compute Canada
'''

import utils

if __name__ == '__main__':
    utils.prepare_input()