ansible-module-cran
=========

An ansible module to install/uninstall R packages

Requirements
------------

- R


Installation
------------

   ansible-galaxy install yutannihilation.cran


Example Playbook
----------------

    - hosts: localhost
      roles:
        - { role: yutannihilation.cran }
      tasks:
        - name: install R pakcages
          cran: name={{ item }} state=present
          with_items:
            - dplyr
            - ggplot2
            - purrr
            - tidyr

License
-------

MIT
