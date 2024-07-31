from setuptools import setup, Extension
import os

project_root = os.path.dirname(os.path.abspath(__file__))

module = Extension('c_extensions.pdf_operations',
            sources=[os.path.join(project_root, 'c_extensions', 'pdf_operations.c')],
            include_dirs=['/usr/include/poppler'],
            libraries=['poppler'],
            extra_compile_args=['-std=c99'])

setup(name='pdf_operations',
    version='1.0',
    description='PDF operations in C',
    ext_modules=[module],
    packages=['c_extensions'])