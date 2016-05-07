#!/usr/bin/python

DOCUMENTATION = '''
---
module: cran
short_description: Install R packages.
options:
  name:
    description:
      - The name of an R package.
    required: true
    default null
  state:
    description:
      - The state of module
    required: false
    choices: ['present', 'absent']
    default: present
  repo:
    description:
      - The repository
    required: false
    default: "http://cran.rstudio.com/"
'''

RSCRIPT = '/usr/bin/Rscript'

def get_installed_version(module):
	cmd = [RSCRIPT, '--slave', '--no-save', '--no-restore-history',
		'-e', 'cat(packageVersion("{name:}"))'.format(
			name = module.params['name']
		)]
	(rc, out, err) = module.run_command(cmd, check_rc=True)
	return out[1].strip() if not err else None


def install(module):
	cmd = [RSCRIPT, '--slave', '--no-save', '--no-restore-history',
		'-e', 'install.packages(pkgs="{name:}", repos="{repos:}")'.format(
			name = module.params['name'],
			repos = module.params['repo']
		)]
	module.run_command(cmd, check_rc=True)


def uninstall(module):
	cmd = [RSCRIPT, '--slave', '--no-save', '--no-restore-history',
		'-e', 'remove.packages(pkgs="{name:}")'.format(
			name = module.params['name']
		)]
	module.run_command(cmd, check_rc=True)


def main():
	module = AnsibleModule(
	    argument_spec = dict(
		state     = dict(default='present', choices=['present', 'absent']),
		name      = dict(required=True),
		repo      = dict(default='http://cran.rstudio.com/')
	    )
	)
	state   = module.params['state']
	changed = False

	if state == 'present':
		install(module)
		changed = True

	module.exit_json(changed=changed, name=module.params['name'])

from ansible.module_utils.basic import *
if __name__ == '__main__':
	main()
