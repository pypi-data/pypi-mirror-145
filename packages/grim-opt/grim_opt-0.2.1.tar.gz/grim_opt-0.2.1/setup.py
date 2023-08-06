# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grim_opt']

package_data = \
{'': ['*']}

install_requires = \
['OWSLib>=0.25.0,<0.26.0',
 'Pillow>=8.4.0,<9.0.0',
 'PyYAML>=6.0,<7.0',
 'Pyomo>=5.7.3,<6.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'basemap>=1.3.2,<2.0.0',
 'geojson>=2.5.0,<3.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'netCDF4>=1.5.6,<2.0.0',
 'networkx>=2.5.1,<3.0.0',
 'numpy>=1.21.5,<2.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pyproj>=3.0.1,<4.0.0',
 'pyshp>=2.1.3,<3.0.0',
 'scipy>=1.6.2,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['grim_opt = grim_opt.cli_app:main']}

setup_kwargs = {
    'name': 'grim-opt',
    'version': '0.2.1',
    'description': 'Greenfield Renewable energy source Investment Model',
    'long_description': '## Installation steps\n\n* OPTIONAL, only if plotting is necessary:\n  + Install the `libgeos` library and development headers\n  + In Ubuntu: `sudo apt install libgeos-dev`\n\n* Use `pip` to install the `grim` library and executable normally.\n  + Recommended: do it in a fresh virtual environment\n    - Create env: `python3 -m venv <chosen_venv_directory>`\n    - Activate env: `source <chosen_venv_directory>/bin/activate`\n\n* TBD: Conda environment file (handles geos dependency also)\n\n## Instructions for contributing to the project\n\n* This project uses `poetry` as its dependency management, virtualenv management and release (build) tool\n   + Install following the steps described in https://python-poetry.org/docs/#installation\n\n### Building a new version and releasing/uploading to PyPI\n\n* Building a (new) release and publishing it to PyPI:\n   1. Make an account on `https://pypi.org`. Ask (optional) for invitation to become project contributor on PyPI.\n   2. Add API token on the "account settings" page of PyPI (global scope for now)\n   3. Register the API token to be the one used by Poetry: `poetry config pypi-token.pypi "<your_api_token>"`\n   4. Do the actual contribution to the project 🙂\n   5. Run `poetry update` to get possible dependecy updates, and commit the updated `poetry.lock` file\n   6. Increment the package\'s version number in `pyproject.toml`\n   7. Build the package (wheel and source): `poetry build`. The built artifacts will be placed in the `dist` folder\n   8. Publish to PyPI: `poetry publish`\n\n\n### Contributing to documentation and build the docs\n\nTODO\n\n\n## Processing steps\n\n### Area per land cover per region \n* Module/function name: `land_cover.py`\n* Input data:\n  + `corine_land_cover`\n  + `polygons`\n* Outputs:\n  + `region_area_land_cover_classes`\n\n* From `region_area_land_cover_classes`, we aggregate (manually) into: `region_area_generation`\n\n### Optimize investment\n* Module/function name: `optimization.py`\n* Input data\n  + `region_area_generation`\n  + `electricity_demand`\n  + `electricity_gencap_factors_new_solar`\n  + `electricity_gencap_factors_new_wind`\n  + `electricity_gencap_existing`\n  + `electricity_transcap_connections`\n* Input parameters:\n  + Techno-economic: `parameters_techno_econ.xlsx`\n* Outputs (`{pct}` is the proportion of the overall generation capacity required to be renewable):\n  + One file for each value of `{pct}`: 0%, 20%, 50%, 80%, 100%\n    - `optimized_gencap_{pct}_renew`\n    - `optimized_transcap_{pct}_renew`\n\n### Post-processing / plotting\n* Module/function name:\n  + `plot_capacities_totals.py`\n* Input data:\n  + One file for each value of `{pct}`: 0%, 20%, 50%, 80%, 100%\n    - `optimized_gencap_{pct}_renew`\n    - `optimized_transcap_{pct}_renew`\n* Output:\n  + `plot_capacities_totals`\n\n* Module/function name:\n  + `plot_capacities_regions.py`\n* Input data:\n  + One file for each value of `{pct}`: 0%, 20%, 50%, 80%, 100%\n    - `optimized_transcap_{pct}_renew`\n* Output:\n  + `plot_capacities_regions`\n\n\n## File meaning, format and data description\n\n### `corine_land_cover`\n* netcdf file: Corine land cover data\n* out_shp: the size of the Corine land cover data. For example, (4721, 4412) means 4721 points in y dimension and 4412 points in x dimension.\n* r: radius of circles where the circle area will be excluded from the available points/land cover. It should be used in combination with "class_artificial_indices".\n* class_artificial_indices: a list contains grid codes from Corine land cover data which present centers of the cirlces. The grid codes could be found in file "clc_legend_new.xls". The default values are artificial surfaces. Detailed description of the Corine land cover classes could be found in: https://land.copernicus.eu/user-corner/technical-library/corine-land-cover-nomenclature-guidelines/html. \n* EPSG3035/EPSG4326 are parameters for EPSG coordinate systems. For example, the EPSG 3035 system is constructed as: EPSG3035 = pyproj.Proj("+init=EPSG:3035").  \n\n### `polygons`\n* geojson files: polygon data (in my case, I created the polygon data myself) \n\n### Optimization inputs\n* `electricity_demand`\n  + Demand data (for countries: can be obtained from `ENTSO-E`, but need to be cleaned). The data is in MWh, per node, per time step.\n* Wind and solar data\n  + Can be obtained from `renewable.ninja`, but need to be cleaned\n  + `electricity_gencap_factors_new_solar`.  The data is unitless between 0 - 1, per node, per time step.\n  + `electricity_gencap_factors_new_wind`.  The data is unitless between 0 - 1, per node, per time step.\n\n* `electricity_gencap_existing`\n  + existing generation data. The data is in MW, per node, per technology.\n* `electricity_transcap_connections`\n  + line data (transmission capacities of inter-region connections). The data shows the details of the lines. In my case, both ends of the lines are represented by region numbers. The regions numbers can be found in file "region_numbered.csv" \n* `techno_economic_parameters.xlsx`\n  + techno-economic data\n\n### `region_area_land_cover_classes`\n* csv file (matrix): for each land cover class, for each region, the area (m2). \n\n### `region_area_generation`\n* Some manual calculations are done, for summation and suitability factors.\n  + Per column, the area in km2\n\n### `optimization`\n* sets\n  + N: number of nodes. \n  + FL: number of lines.\n  + G: all generation technologies.\n  + SC: storage conversion. S = SC\n  + S: storage technologies. S = SC\n  + RES: renewable energy technologies. Subset of G\n  + VRES: variable renewable energy technologies. Subset of RES.\n  + Non-VRES: non-variable renewable energy technologies. G-VRES.\n  + T = time steps\n  + T2 =time steps excluding the first time step  \n* parameters.\n  + capacity_density_onshore: capacity density for onshore wind turbines (MW/km2)\n  + capacity_density_solar: capacity density for solar PV (MW/km2)\n  + lol: value of lost load (euros/MWh)\n  + R: number of time steps. Used in combination with T, T2. \n  + CT: cost transmission line (euros/km/MW)\n  + r: discount rate (0 - 1)\n  + LT: lifetime transmission line\n  + reserve_margin: reserve capacity in percentage (0 - 1), i.e., extra capacity to be built but will now be used.\n  + omega: renewable energy target, 0 - 1.\n  + im = np.zeros([len(df.index), 32]): 32 is number of nodes\n  + arr_demand = np.empty([32, 8760]): 32 is number of nodes, 8760 is number of time steps (in my case, hours). Same for other arrays.\n  + e_l: percentage of extra length of the lines (0 - 1), accounting for routing due to non-straight lines.\n* solver options\n  + solver_name: name of the solver\n  + solver_crossover: crossover. Default is 0 (disabled) \n  + solver_method: method to solve the problem. Default is 2 (barrier method)\n  + solver_threads: number of threads to use. \n  \n### Optimized capacities\n* `optimized_gencap_{pct}_renew`\n  + MW, per technology, per node\n* `optimized_transcap_{pct}_renew`\n  + MW, between nodes\n  \n### Plots\n* `plots_capacities_totals`\n  + For each scenario (pct. of renewables in generation mix), for each energy source the installed capacity\n\n* `plots_capacities_regions`\n  + For each scenario (pcr. of renewables in generation mix), for each energy source, for each region the installed capacity\n\n\n \n',
    'author': 'Ni Wang',
    'author_email': 'N.Wang@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.tudelft.nl/nwang1/grim',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.7,<3.10',
}


setup(**setup_kwargs)
