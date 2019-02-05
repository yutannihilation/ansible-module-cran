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
    default: "https://cran.rstudio.com/"
'''

RSCRIPT = 'Rscript'

def get_installed_version(module):
	cmd = [RSCRIPT, '--slave', '--no-save', '--no-restore-history',
		'-e', 'p <- installed.packages(); cat(p[p[,1] == "{name:}",3])'.format(
			name = module.params['name']
		)]
	(rc, stdout, stderr) = module.run_command(cmd, check_rc=False)
	return stdout.strip() if rc == 0 else None


def install(module):
	cmd = [RSCRIPT, '--slave', '--no-save', '--no-restore-history',
		'-e', 'install.packages(pkgs="{name:}", repos="{repos:}")'.format(
			name = module.params['name'],
			repos = module.params['repo']
		)]
	(rc, stdout, stderr) = module.run_command(cmd, check_rc=True)
	return stderr


def uninstall(module):
	cmd = [RSCRIPT, '--slave', '--no-save', '--no-restore-history',
		'-e', 'remove.packages(pkgs="{name:}")'.format(
			name = module.params['name']
		)]
	(rc, stdout, stderr) = module.run_command(cmd, check_rc=True)
	return stderr


def main():
	module = AnsibleModule(
	    argument_spec = dict(
		state     = dict(default='present', choices=['present', 'absent']),
		name      = dict(required=True),
		repo      = dict(default='https://cran.rstudio.com/')
	    )
	)
	state   = module.params['state']
	name    = module.params['name']
	changed = False
	version = get_installed_version(module)

	if state == 'present' and not version:
		stderr = install(module)
		version = get_installed_version(module)
		if not version:
			module.fail_json(msg='Failed to install {name:}: {err:}'.format(name = name, err  = stderr, version = version))
		changed = True

	elif state == 'absent' and version:
		stderr = uninstall(module)
		version = get_installed_version(module)
		if version:
			module.fail_json(msg='Failed to install {name:}: {err:}'.format(name = name, err  = stderr))
		changed = True

	module.exit_json(changed=changed, name=name, version=version)


from ansible.module_utils.basic import *
if __name__ == '__main__':
	main()
