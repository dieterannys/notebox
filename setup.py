from setuptools import setup, find_packages

setup(
    name='notebox',
    version='0.1.0',
    packages=find_packages('.'),
    description='',
    install_requires=[
        "pandas",
        "prompt_toolkit",
        "pytz",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "todoist",
        "ripgrepy",
        "iterfzf",
        "PyYAML",
        # Tests
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'notebox=notebox.repl:main',
        ]
    }
)
