# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiotrap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tiotrap',
    'version': '0.3.3',
    'description': 'Helper For Capturing Text IO Streams like stdout, stderr',
    'long_description': '## TextIOTrap\n\nSimple class for trapping / capturing Python Text IO streams like from `subprocess.popen`, `pexpect`, `sys.stderr` and others; enabling the capture output of or dropping streams with cross platform `DEVNULL` helper. \n\n### Installation\n\n```\npython3 -m pip install tiotrap\n```\n\n\n### Usage\n\nThis tool contains one class `TextIOTrap` and a helper `DEVNULL`.\n\n\n### Examples\n\n#### (Ex1) Use `TextIOTrap` to capture stdout of a chatty process using `store` option:\n```python3\n_stdout_bk = sys.stdout # Store original stdout\nttrap = tiotrap.TextIOTrap(store=True)\n\ntry:\n    sys.stdout = ttrap # Map stdout to tiotrap\n    print("TEST1")\n    # call some chatty functions()\n    print("TEST2")\n\nfinally:\n    sys.stdout = _stdout_bk # Restore stdout\n```\nOutput of print:\n```\ncaptured logs:\nTEST1\n<chatty outputs here>\nTEST2\n```\n\n\n#### (Ex2) Use `TextIOTrap` to capture stdout using `write_handler` option:\n```python3\naTrap = []\n_stdout_bk = sys.stdout\ntry:\n    sys.stdout = tiotrap.TextIOTrap(write_handler=lambda s: aTrap.append(s))\n    print("TEST1")\n    print("TEST2")\n\nfinally:\n    sys.stdout = _stdout_bk\n# print adds extra \\n end so remove with rstrip()\nprint(f"aTrap:\\n{\'\'.join(aTrap).rstrip()}\\n~end~\\n")\n```\n\nOutput of print:\n```\naTrappedStdout = [\'TEST1\', \'TEST2\']\n```\nYou can substitute lambda with a function or method call to handle `writes` with your own code.\n\n\n\n#### (Ex3) Use `TextIOTrap` grab output `pexpect` call :\n```python3\nttrap = tiotrap.TextIOTrap(store=True)\n\np = pexpect.spawn(\'ls -la\')\np.logfile = ttrap\np.expect(pexpect.EOF)\n\nprint(f"`ls -la` cmd output:\\n{ttrap.entries()}\\n~")\n```\n\nOutput of print:\n```\nls output:\n<full directory listing here of cwd>\n```\n\nOther uses of `TextIOTrap`:\n* Output the stdout of a `subprocess.popen` call in real time to a secondary log file\n* ...\n\n\n#### (Ex4) Use `TextIOTrap` grab output `pexpect` call :\n```python3\nttrap = tiotrap.TextIOTrap(store=True)\n\np = pexpect.spawn(\'ls -la\')\np.logfile = ttrap\np.expect(pexpect.EOF)\n\nprint("ls -la` cmd output (as was written):")\nfor write in ttrap:\n    print(write)\n```\nOutput: Similar to Ex4\n\n\n#### (Ex5) Use `DEVNULL` to drop all output of a TextIO Stream\n```python3\n_stdout_bk = sys.stdout\n\ntry:\n    sys.stdout = tiotrap.DEVNULL\n    print("THIS WILL NOT PRINT")\n\nfinally:\n    sys.stdout = _stdout_bk\n\nprint("THIS WILL PRINT")\n```\nThis DEVNULL is very simple implementation and is fully cross platform unlike someother DEVNULL implementations.\n\n\nNote:` TextIOTrap` has been set up to be compatible with the standard methods for a Text IO streams. I\'ll be glad to update if any edge cases are discovered.\n',
    'author': 'Timothy C. Quinn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/tiotrap/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
