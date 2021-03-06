"""
 --------------------------------------------------
| _      __      _         _    _         _        |
| \ \    / /    | |       | |  | |       | |       |
| \ \  / /_   _ | | _ __  | |__| | _   _ | |__     |
|  \ \/ /| | | || || '_ \ |  __  || | | || '_ \    |
|   \  / | |_| || || | | || |  | || |_| || |_) |   |
|    \/  \__,_||_||_| |_||_|  |_| \__,_||_.__/     |
 ---------------------------------------------------
Usage:
  vulnhub stats [--vendor] [--product]
  vulnhub search [-c --cpe] [-v --cve] [-y --year] [-j --json] [-l --limit] [--no-limit] <search_term>
  vulnhub populate [-c --cpe] [-v --cve] [-a --all]
  vulnhub update [-v --cve]
  vulnhub config [--generate] [--driver]
  vulnhub dbinit [--no-confirm] [-c --cpe] [-v --cve] [-all]
  vulnhub --version
  vulnhub (-h | --help)

Commands:
    stats              Display stats on Vulnerable products.
    search             Search NVD database by CPE, CVE or Year.
    populate           Populate Local copy of NVD Database.
    update             Update a specific dictionary
    config             Change configuration.
    dbinit             Initialize database and create tables.

Options:
  -c, --cpe            Search by CPE URI.
  -v, --cve            Search by CVE Identifier.
  -y, --year           Search by Year.
  -j, --json           JSON Output for search results.
  -l, --limit=limit    Limit Search results.
  --no-limit           Get all results without default limit.
  -a --all             Update Both CVE and CPE Dictionaries.
  --no-confirm         Drop database without being asked for confirmation.
  --generate           Generate a new Configuration.
  --driver             Set a new database driver.
  -h --help            vulnhub help and usage.

Maintainer: Uday Korlimarla
Report bugs to <skorlimarla@unomaha.edu>
"""

import os
import sys

from docopt import docopt
from vulnhub.core import queries
from vulnhub.config import config
from vulnhub.database import populate_cves
from vulnhub.database import populate_cpes


# Package entry point
def main(sysargv=None):
    """
    VulnHub Entry Point
    Command and Options processing with docopt
    :param sysargv: Arguments from CLI - user input and options
    :return:
    """
    argv = docopt(
        doc=__doc__.format(os.path.basename(sys.argv[0])),
        argv=sysargv
        )
    search_term = argv['<search_term>']

    # Setting up Default Limit
    search_limit = 5
    if argv['--no-limit']:
        search_limit = None

    try:
        search_limit = int(argv['--limit'])
    except ValueError:
        pass
    except TypeError:
        pass

    if argv['search']:
        if argv['--cpe']:
            sys.stdout.write(queries.search_vulnerable_products(search_term, search_limit))
            sys.stdout.write("\n")
        elif argv['--cve']:
            sys.stdout.write(queries.search_vulnerabilities(search_term, search_limit))
            sys.stdout.write("\n")
        elif argv['--year']:
            # Default year to search
            year = 2016
            try:
                year = search_term
            except ValueError:
                pass
            except TypeError:
                pass
            finally:
                sys.stdout.write(queries.search_by_year(year, search_limit))
                sys.stdout.write("\n")
        elif argv['--json']:
            print("JSON Feature is native! This will be deprecated")
        else:
            print(docopt(__doc__))
    elif argv['stats']:
        if argv['--product']:
            queries.product_frequency()
        elif argv['--vendor']:
            queries.vendor_frequency()
        else:
            print(docopt(__doc__))
    elif argv['update']:
        if argv['--cve']:
            populate_cves.update_cve_dictionary()
    elif argv['populate']:
        if argv['--cpe']:
            print("Populating CPE Dictionary")
            populate_cpes.start_cpe_population()
        elif argv['--cve']:
            print("Populating CVE Dictionary")
            populate_cves.start_cve_population()
        elif argv['--all']:
            print("Populating CPE Dictionary")
            populate_cpes.start_cpe_population()
            print("Populating CVE Dictionary")
            populate_cves.start_cve_population()
        else:
            print(docopt(__doc__))
    elif argv['config']:
        if argv['--generate']:
            config.generate_config()
        elif argv['--driver']:
            print("SQL Driver change option is not implemented")
    elif argv['dbinit']:
        # Implement confirmation message - for later
        if argv['--no-confirm']:
            pass
        if argv['--cpe']:
            queries.drop_cpes()
        elif argv['--cve']:
            queries.drop_cves()
        elif argv['--all']:
            queries.initialize()
        else:
            pass
    elif argv['--help']:
        print(docopt(__doc__))
    else:
        print(docopt(__doc__))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

