from setuptools import setup, Extension
import os

project_root = os.path.dirname(os.path.abspath(__file__))

module = Extension('c_extensions.pdf_operations',
                 sources=[os.path.join(project_root, 'c_extensions', 'pdf_operations.c')],
                 include_dirs=[os.path.join(project_root, 'external', 'pdf_lib', 'include')],
                 libraries=['pdfparser'])

setup(name='pdf_operations',
    version='1.0',
    description='PDF operations in C',
    ext_modules=[module],
    packages=['c_extensions'])