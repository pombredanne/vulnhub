````
                                                 __      __      _         _    _         _
                                                 \ \    / /     | |       | |  | |       | |
                                                  \ \  / /_   _ | | _ __  | |__| | _   _ | |__
                                                   \ \/ /| | | || || '_ \ |  __  || | | || '_ \ 
                                                    \  / | |_| || || | | || |  | || |_| || |_) |
                                                     \/   \__,_||_||_| |_||_|  |_| \__,_||_.__/ 
                                                                                                
 ````                                               
[![Build Status](https://travis-ci.org/UShan89/vulnhub.svg?branch=master)](https://travis-ci.org/UShan89/vulnhub)

# vulnhub
Search National Vulnerability Database (NVD) locally for Vulnerabilities (CVEs) and Vulnerable packages (CPEs)

## Language & Requirements
   * Python 3.5.2 (Tested on Ubuntu 16:04)
   * Postgres 9.6 (Docker image or Local development server)

## License & Contributions


   [**vulnhub is licensed under GNU GPL-2.0**](https://raw.githubusercontent.com/UShan89/vulnhub/master/LICENSE)
   [**Easy to read License Information is available here**](https://tldrlegal.com/license/gnu-general-public-license-v2)
   Contributions will be accepted as pull requests.
   Report bugs by creating new issue.

# Installation


   * Step1: Install external dependencies (#Dependencies)
   * `libpq-dev` `libxml2-dev` `libxslt-dev` are the required dependencies.
   * (Optional) If `pip3` is not installed, installed pip3 with `apt-get install python3-pip`
   * Python dependencies are installed automatically
   * To install:
	    1. Clone repository `git clone https://github.com/UShan89/vulnhub vulnhub`
	    2. Change directory to vulnhub `cd vulnhub`
	    3. Install vulnhub with pip `pip3 install .` (using python3-pip)

# configuration

   * Initial setup requires the following configuration
        * Create a directory `.vulnhub` in the user root directory and navigate to the directory.
            * Instance: If root is `/home/ushan`, then the directory of interest is `/home/ushan/.vulnhub`
        * Create a Configuration JSON File as below with appropriate changes. Save the file as `dbconfig.json`.
        
        
             {
                "DATABASE": {
                                "drivername": "postgres",
                                "host": "localhost",
                                "port": "5432",
                                "username": "postgres",
                                "password": "password",
                                "database": "nvddb"
                             }
              }
        
        
# Usage

[**Visit the USAGE guide**](USAGE.md) 
    
# Database

---
    POSTGRES on Docker
        Step 1: Install docker 
            visit Docker installation instructions**](http://www.docker.com/products/overview) 
        Step 2: Pull postgres docker image
            `docker pull postgres:latest`
        Step 3: Start postgres container
        Step 4:`docker run --rm -e POSTGRES_PASSWORD=password -p 5432:5432 --name nvd_instance postgres`
            `--rm` option Automatically remove the container when it exits
            `-p 5432:5432` is portmapping as `<docker_host_port>:<container_port>`
            `-e` Option is to enable a password. Change `password` to a value of choice (Recommended)
            `--name` option sets friendly name for the container
    Databases supported:
        * POSTGRES
        * SQLITE (Install Sqlite-dev library for ubuntu)
        * MySQL  (Install mysql client library for ubuntu)
---

# NVD Data

---
    * CPE
        * CPE version 2.3 is used
        * CPE version 2.2 is used for backward compatibility with CVEs.
        * Vendor, Product and Version information is saved for each CPE
        * CPEs are classified into three categories
            * `a - application`
            * `h - Hardware/Firmware`
            * `o - Operating System`
        * Pro   duct URLs
            * A CPE product reference (Change Log) from vendor site is saved.
            * Not All CPEs have a product reference.
            * This field is Optional
         * Product Text
            * Product text is a simple description of a CPE as vendor, product and version.
            * Not all CPEs have text field.
            * This field is optional.
        * Parsing & Populating
            * Official CPE 2.3 dictinary is parsed with xmltodict.
            Parsing fails on Windows - PIP Reference #1 in Issues.
            * CPE parsing limits platform to Linux and has been tested on Ubuntu 16:04.
            * Postgres bulk insert option is used to populate the database with CPEs.
     
    * CVE
        * CVE Identifier is saved. CVE 2.0 dictionaries are used.
        * Accompanying CVE Information is saved.
            * Vulnerability Summary (Vulnerability Information Text) is saved as Summary.
            * CWE (Software Weakness Identifier) is saved.
            * CVSS Base Score & CIA metrics are saved.
            * Published and Modified dates are saved.
            * Vulnerability Source and Source References are saved.
            * CPEs assocaited with a CVE are saved into an array (Python List)
        * Parsing and Populating
            * xmltodict python Library is used to parse all CVE XML dictionaries.
            * CVE feeds are spidered from NVD Feeds and zipped (*.zip) versions are used instead of gunzip (*.gz) formats.
            * CVEs are populated from the last known year to the latest year as the order.
            * Postgres bulk insert option is used to populate the database with CVEs.
---

# Dependencies

---
    * The Following are External dependencies (Ubuntu)
        * libpq-dev (Client library for Postgres).
        * libxml2-dev are libxslt-dev Python lxml parser dependencies.

    * The following Python dependencies are used (Immediate dependencies)
        * wget (Download files from remote locations)
        * sqlalchemy (Python ORM for database agnostic CRUD operations)
        * psycopg2 (PostgreSQL adapter for Python)
        * docopt (Command Line Options)
        * xmltodict (Parse XML)
        * plotly (Generate Plots and Graphs)
        * pylint (PEP8 and Python code styling guide helper)
---       
        
---
    * Code structure (Dependency structure)
---------------------

    bs4 (vulnhub.util.spider_cves)
    docopt (vulnhub.vulnhub)
    sqlalchemy 
      \-dialects 
      | \-postgresql (vulnhub.database.schema)
      \-engine 
      | \-url (vulnhub.database.schema)
      \-exc (vulnhub.database.datapipeline)
      \-ext 
      | \-declarative (vulnhub.database.schema)
      \-orm (vulnhub.database.datapipeline)
      \-pool (vulnhub.database.schema)
    vulnhub (vulnhub.vulnhub)
      \-config (vulnhub.vulnhub)
      \-core (vulnhub.vulnhub)
      \-database 
      | \-datapipeline (vulnhub.database.populate_cpes,vulnhub.core.queries,vulnhub.database.populate_cves)
      | \-schema (vulnhub.database.datapipeline)
      \-util 
        \-cpexmlparser (vulnhub.database.populate_cpes)
        \-cvexmlparser (vulnhub.database.populate_cves)
        \-sharedactions (vulnhub.database.populate_cpes,vulnhub.database.populate_cves)
        \-spider_cves (vulnhub.database.populate_cves)
    wget (vulnhub.util.sharedactions)
    xmltodict (vulnhub.util.cpexmlparser,vulnhub.util.cvexmlparser)
---

# Populating CVES - Order

---
    * The current order for populating CVEs as following:
    
        `https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Recent.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2002.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2003.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2004.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2005.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2006.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2007.xml.zip`
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2008.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2009.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2010.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2011.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2012.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2013.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2014.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2015.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2016.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Modified.xml.zip` 
        `https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Recent.xml.zip`
     
    * CVE Feeds are spidered and downloaded in the order.
    * A CVE that appears in older document will be replaced with information from the latest document
    * Updates download and use `Modified` and `Recent` feeds only.
    
----

# Maintainer

---
    Maintainer: Uday Korlimarla
    Report bugs to <skorlimarla@unomaha.edu>
---
