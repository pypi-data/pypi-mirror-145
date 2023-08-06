from setuptools import setup, find_packages
from setuptools.command.install import install as _install

VERSION = '0.3.10'
DESCRIPTION = 'FFAST: Fast Fourier Analysis for Sentence embeddings and Tokenisation'
LONG_DESCRIPTION = 'Fast and lightweight NLP pipeline for ML tasks: powerful tokeniser and (model-free) sentence embeddings using Fast Fourier transforms, power means, positional encoding and Wordnet or Poincare Embeddings'

class DownloadWordnet(_install):
    def run(self):
        self.do_egg_install()
        from nltk import download
        download('wordnet')
        download('stopwords')

setup(
    name="ffast",
    version=VERSION,
    author="Mohammed Terry-Jack",
    author_email="<mohammedterryjack@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    setup_requires = ['nltk'],
    cmdclass={'download_wordnet': DownloadWordnet},
    include_package_data=True,
    package_data={'':['poincare/poincare.txt']},
    install_requires=['nltk', 'jellyfish', 'Unidecode', 'numpy', 'scipy'],
    keywords=['python', 'embedding', 'tokenisation', 'fast fourier', 'nlp', 'nlu', "poincare", "wordnet", "lite", "fast", "sentence encoder"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)