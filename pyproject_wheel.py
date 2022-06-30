import sys
import subprocess
import os


def build_wheel(*, wheeldir, stdout=None):
    command = (
        sys.executable,
        '-m', 'pip',
        'wheel',
        '--wheel-dir', wheeldir,
        '--no-deps',
        #'--use-pep517',
        #'--no-build-isolation',
        '--disable-pip-version-check',
        '--no-clean',
        #'--progress-bar', 'off',
        '--verbose',
        '.',
    )
    cp = subprocess.run(command, stdout=stdout)
    return cp.returncode


if __name__ == '__main__':
    # lhh - bug in rhel8's python-wheel causes TMPDIR usage to go
    # into an infinite loop
    os.unsetenv('TMPDIR')
    sys.exit(build_wheel(wheeldir=sys.argv[1]))
