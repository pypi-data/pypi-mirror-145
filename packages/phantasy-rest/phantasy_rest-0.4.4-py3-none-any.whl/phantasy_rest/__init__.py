__name__ == 'phantasy_rest'
__version__ = '0.4.4'
__author__ = 'Tong Zhang <zhangt@frib.msu.edu>'
__doc__ = """RESTful API for PHANTASY"""


def run():
    """Start up the service."""
    import argparse
    import phantasy_rest
    import subprocess
    import shlex
    import sys
    import os
    pkg_path = phantasy_rest.__path__[0]

    parser = argparse.ArgumentParser(description="Start PHANTASY-REST service")
    parser.add_argument("action", nargs="?", help="Control action, start|stop")
    parser.add_argument("--config",
                        dest="config",
                        help="Path of the app configuration file")
    parser.add_argument("--print-config",
                        action="store_true",
                        help="Print out the default configurations")

    args = parser.parse_args(sys.argv[1:])

    if args.print_config:
        # print default configurations
        with open(os.path.join(pkg_path, "config.toml"), "r") as fp:
            print(fp.read())
        sys.exit(0)

    if args.action not in ('start', 'stop'):
        # service action
        print("A valid action (start or stop) must be provided.")
        parser.print_help()
        sys.exit(1)

    if args.config is not None:
        from phantasy_rest._get_conf import set_envs
        set_envs(args.config)

    if args.action == 'start':
        cmdline = f'gunicorn main:app --config _gconf.py'
    else:  # 'stop'
        from phantasy_rest._gconf import pidfile
        cmdline = f'kill `cat {pidfile}`'
    subprocess.run(cmdline, cwd=pkg_path, shell=True)
