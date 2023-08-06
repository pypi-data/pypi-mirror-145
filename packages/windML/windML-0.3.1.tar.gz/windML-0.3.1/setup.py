from setuptools import setup, find_packages

VERSION = '0.3.1'
DESCRIPTION = 'WindML'
LONG_DESCRIPTION = 'Refreshingly Lightweight Machine Learning (using only numpy). models include conditional-character-RNN, Transformer and a Direct Feedback Alignment NN and other one-shot models like extreme learning machines or matrix factorisation retrieval-based classifiers (for a model-free alternative)'

setup(
    name="windML",
    version=VERSION,
    author="Mohammed Terry-Jack",
    author_email="<mohammedterryjack@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'extreme learning machine', 'direct feedback alignment', 'matrix factorisation', 'ml', 'machine learning', 'rnn', 'transformer', 'numpy', 'lite'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)