# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imucal']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0',
 'packaging>=21.3,<22.0',
 'pandas>=1.1.3,<2.0.0',
 'typing-extensions>=3.7.4']

extras_require = \
{'calplot': ['matplotlib>=3.3.2,<4.0.0'], 'h5py': ['h5py>=2.10.0,<3.0.0']}

setup_kwargs = {
    'name': 'imucal',
    'version': '2.1.1',
    'description': 'A Python library to calibrate 6 DOF IMUs',
    'long_description': '# imucal\n![Test and Lint](https://github.com/mad-lab-fau/imucal/workflows/Test%20and%20Lint/badge.svg)\n[![codecov](https://codecov.io/gh/mad-lab-fau/imucal/branch/master/graph/badge.svg?token=0OPHTQDYIB)](https://codecov.io/gh/mad-lab-fau/imucal)\n[![Documentation Status](https://readthedocs.org/projects/imucal/badge/?version=latest)](https://imucal.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/imucal)](https://pypi.org/project/imucal/)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/imucal)\n[![DOI](https://zenodo.org/badge/307143332.svg)](https://zenodo.org/badge/latestdoi/307143332)\n\nThis package provides methods to calculate and apply calibrations for 6 DOF IMUs based on multiple different methods.\n\nSo far supported are:\n\n- Ferraris Calibration ([Ferraris1994](https://www.sciencedirect.com/science/article/pii/0924424794800316) / [Ferraris1995](https://www.researchgate.net/publication/245080041_Calibration_of_three-axial_rate_gyros_without_angular_velocity_standards))\n- Ferraris Calibration using a Turntable\n\n## Installation\n\n```\npip install imucal\n```\n\nTo use the included calibration GUI you also need [matplotlib](https://pypi.org/project/matplotlib/) (version >2.2).\nYou can install it using:\n\n```\npip install imucal[calplot]\n```\n\n## Quickstart\nThis package implements the IMU-infield calibration based on [Ferraris1995](https://www.researchgate.net/publication/245080041_Calibration_of_three-axial_rate_gyros_without_angular_velocity_standards).\nThis calibration method requires the IMU data from 6 static positions (3 axes parallel and antiparallel to the gravitation\nvector) for calibrating the accelerometer and 3 rotations around the 3 main axes for calibrating the gyroscope.\nIn this implementation, these parts are referred to as `{acc,gyr}_{x,y,z}_{p,a}` for the static regions and\n`{acc,gyr}_{x,y,z}_rot` for the rotations.\nAs example, `acc_y_a` would be the 3D-acceleration data measured during a static phase, where the **y-axis** was \noriented **antiparallel** to the gravitation vector.\n\nTo annotate a Ferraris calibration session that was recorded in a single go, you can use the following code snippet.  \n**Note**: This will open an interactive Tkinter plot. Therefore, this will only work on your local PC and not on a server or remote hosted Jupyter instance.\n\n```python\nfrom imucal import ferraris_regions_from_interactive_plot\n\n# Your data as a 6 column dataframe\ndata = ...\n\nsection_data, section_list = ferraris_regions_from_interactive_plot(\n    data, acc_cols=["acc_x", "acc_y", "acc_z"], gyr_cols=["gyr_x", "gyr_y", "gyr_z"]\n)\n# Save the section list as reference for the future\nsection_list.to_csv(\'./calibration_sections.csv\')  # This is optional, but recommended\n```\n\nNow you can perform the calibration:\n```python\nfrom imucal import FerrarisCalibration\n\nsampling_rate = 100 #Hz \ncal = FerrarisCalibration()\ncal_mat = cal.compute(section_data, sampling_rate, from_acc_unit="m/s^2", from_gyr_unit="deg/s")\n# `cal_mat` is your final calibration matrix object you can use to calibrate data\ncal_mat.to_json_file(\'./calibration.json\')\n```\n\nApplying a calibration:\n\n```python\nfrom imucal.management import load_calibration_info\n\ncal_mat = load_calibration_info(\'./calibration.json\')\nnew_data = pd.DataFrame(...)\ncalibrated_data = cal_mat.calibrate_df(new_data, acc_unit="m/s^2", gyr_unit="deg/s")\n```\n\nFor further information on how to perform a calibration check the \n[User Guides](https://imucal.readthedocs.io/en/latest/guides/index.html) or the\n[Examples](https://imucal.readthedocs.io/en/latest/auto_examples/index.html).\n\n## Further Calibration Methods\n\nAt the moment, this package only implements calibration methods based on Ferraris1994/95, because this is what we use to\ncalibrate our IMUs.\nWe are aware that various other methods exist and would love to add them to this package as well.\nUnfortunately, at the moment we can not justify the time investment.\n\nStill, we think that this package provides a suitable framework to implement other calibration methods with relative\nease.\nIf you would like to contribute such a method, let us know via [GitHub Issue](https://github.com/mad-lab-fau/imucal/issues), and we will try to help you as good\nas possible.\n\n## Citation\n\nIf you are using `imucal` in your scientific work, we would appreciate if you would cite or link the project:\n\n```\nKüderle, A., Roth, N., Richer, R., & Eskofier, B. M., \nimucal - A Python library to calibrate 6 DOF IMUs (Version 2.0.2) [Computer software].\nhttps://doi.org/10.5281/zenodo.56392388\n```\n\n## Contributing\n\nAll project management and development happens through [this GitHub project](https://github.com/mad-lab-fau/imucal).\nIf you have any issues, ideas, or any comments at all, just open a new issue.\nWe are always happy when people are interested to use our work and would like to support you in this process.\nIn particular, we want to welcome contributions of new calibration algorithms, to make this package even more useful for a wider audience.\n',
    'author': 'Arne Küderle',
    'author_email': 'arne.kuederle@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/imucal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
