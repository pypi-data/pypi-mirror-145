import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='cogexquestgen',
      version='1.0.3',
      description='Question generator from any text',
      author='Forked Questgen Contributor: Jeff Myers',
      author_email='j3f9y.f@gmail.com',
      packages=['Questgen', 'Questgen.encoding', 'Questgen.mcq'],
      url="https://github.com/JeffMII/Questgen.ai",
      install_requires=[
            'torch==1.9.0',
            'transformers>=3.0.2, <=4.2.2',
            'pytorch_lightning>=0.8.1, <=0.8.4',
            'sense2vec==2.0.0',
            'strsim==0.0.3',
            'six>=1.15.0, <=1.16.0',
            'networkx>=2.4.0, <=2.6.3',
            'numpy==1.16.3',
            'scipy>=1.4.1, <=1.5.4',
            'scikit-learn>=0.22.1, <=1.0.2',
            'unidecode>=1.1.1, <=1.3.2',
            'future==0.18.2',
            'joblib>=0.14.1, <=1.1.0',
            'spacy>=3.0.0, <=3.2.1',
            'pytz>=2020.1, <=2021.3',
            'python-dateutil>=2.8.1, <=2.8.2',
            'boto3>=1.14.40, <=1.20.39',
            'flashtext==2.7',
            'pandas>=1.1.1, <=1.1.5',
            'nltk==3.6.3',
            'cogexpke==1.8.1'
      ],
      package_data={'Questgen': ['questgen.py', 'mcq.py', 'train_gpu.py', 'encoding.py']}
)