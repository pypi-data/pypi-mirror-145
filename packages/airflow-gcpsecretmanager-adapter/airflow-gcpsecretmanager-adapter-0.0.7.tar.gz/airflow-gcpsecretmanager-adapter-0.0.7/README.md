# airflow-gcpsecretmanager-adapter
## Overview
This repository contains a Python package to allow Airflow variables that do not align with GCP Secret Manager naming convention to be used with the secrets backend. GCP Secret Manager has constraints on the characters that may be used when naming a secret (alphanumerics, hyphens and underscores only), however variables in Airflow are not restricted in any way. Therefore in some cases it may be necessary to transform the name of the Airflow variable to a format acceptable for Secret Manager to use. For example the Airflow variable name:

```
global::myvar
```

is not permitted as a GCP secret name, so this must instead be translated to:

```
global-myvar
```
which *is* permitted.

This package can be installed as an alternative secrets backend within Airflow, as described here: https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html#roll-your-own-secrets-backend


## Installation

```bash
pip install airflow-gcpsecretmanager-adapter
```

## Current replacements

| Source characters | Replaced with |
--------------------|----------------
| ::                | -             |
| :                 | -             |

