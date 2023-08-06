from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='uranium_image_cleanup',
      #Examples naming conventions
      #1.2.0.dev1  # Development release
      #1.2.0a1     # Alpha Release
      #1.2.0b1     # Beta Release
      #1.2.0rc1    # Release Candidate
      #1.2.0       # Final Release
      #1.2.0.post1 # Post Release
      #15.10       # Date based release
      #23          # Serial release
      version='0.9.0b4',
      description='Remove text/noise from grayscale uranium photos',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='image processing filtering ',
      project_urls={'Source': 'https://github.com/brienschmaltz/uranium_image_cleanup'},
      author='4120 Industries',
      author_email='schmaltz.6@wright.edu',
      license='MIT',
      install_requires=[
          'tqdm',
          'opencv-python',
          'numpy',
          'pillow'
      ],
      package_dir={'': 'src'},
      py_modules=["removeLabel"],
      packages=find_packages(where='src'),
      python_requires='>=2.7, <4',
      entry_points={  
        'console_scripts': [
            'uic=uranium_image_cleanup_package:main',
        ],
      },
      )