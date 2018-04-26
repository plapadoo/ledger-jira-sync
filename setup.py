from setuptools import setup, find_packages

setup(
    name="ledger-jira-sync",
    version="1.0",
    description="Tool for synchronizing JIRA work logs with ledger work logs",
    python_requires='>=2.7',
    entry_points={'console_scripts': ['ledger-jira-sync = ledger_jira_sync.__main__:main']},
    long_description='',
    classifiers=[
        'Programming Language :: Python :: 2',
    ],
    keywords='jira, ledger',
    url='https://github.com/plapadoo/ledger-jira-sync',
    author='plapadoo',
    author_email='middendorf@plapadoo.de',
    license='BSD3',
    packages=find_packages(),
    install_requires=['jira'],
    include_package_data=True,
    zip_safe=True)
