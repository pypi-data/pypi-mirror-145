
from setuptools import setup


setup(name="pycosh", version="0.0.0", description="correlated self-heterodyne (COSH) optical noise analyzer",
      packages=["pycosh"], url="https://github.com/MaodongGao/pycosh",
      install_requires=["numpy", "scipy", "matplotlib"],
      author="Zhiquan Yuan, Heming Wang, Peng Liu, Bohan Li, Boqiang Shen, Maodong Gao",
      author_email="mgao@caltech.edu"
      )
