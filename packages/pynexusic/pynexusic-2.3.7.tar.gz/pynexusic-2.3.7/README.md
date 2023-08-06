# pynexusic
```pynexusic``` is a package that allows communication with the following tools:
- Wood NEXUS IC
- Maximo
- OSI PI
- Documentum

### Python library installation
``` python
pip install pynexusic
```

### Library documentation
1) Import ```utils```
    ```python
    from pynexusic import utils
   ```
       
2) Launch documentation
    ```python
    utils.launchDocs()
    ```

### External documentation
#### NEXUS IC
NEXUS IC REST API documentation can be found in the following link:

https://docs.nexusic.com/6.7/ic-web.rest.v2.html

*A specific NEXUS IC version can be specified in the above link by changing **6.7** to the desired NEXUS IC version*

#### OSI PI
OSI PI API documentation can be found in the following link:

https://techsupport.osisoft.com/Documentation/PI-Web-API/help.html

#### Maximo
Maximo API documentation can be found in the following link:

https://www.ibm.com/support/knowledgecenter/SS8CCV_7.6.0.8/com.ibm.mams.doc/overview/c_product_overview.html

### Examples
#### NEXUS IC Examples
- Example 1: Get system version
    1) Import ```NEXUSIC_RESTAPI```
        ```python
       from pynexusic import NEXUSIC_RESTAPI as api
        ```
       
    2) Initialize ```NEXUSIC_REST``` class
        ```python
       NX_REST = api.NEXUSIC_REST(baseURI, api_key=APIKey)
        ```
        *where **APIKey** is the user's API Key provided by the system administrator*
       
    3) Execute required function
        ```python
        result, result_status_code = NX_REST.getVersion()
        ```
        Output:
        ```python
        result = {'version': 'x.x.xxxxx.x', 'schema': 'x.xxx'}
        result_code = 200
        ```
       
- Example 2: Run reports and get python object response
    1) Import ```NEXUSIC_RESTAPI```
        ```python
       from pynexusic import NEXUSIC_RESTAPI as api
        ```
       
    2) Initialize ```NEXUSIC_REST``` class
        ```python
       NX_REST = api.NEXUSIC_REST(baseURI, api_key=APIKey)
        ```
       *where **APIKey** is the user's API Key provided by the system administrator*
       
    3) Execute required report
        ```python
        result, result_status_code = NX_REST.getDashboard(report_name)
        ```
       *where **report_name** is the name of the report to be executed in NEXUS IC*
       
        Output:
        ```python
        result = {'name': 'xxxxxxxxxxx', 
                  'elements': [{'type': 'section', 'data': {}}, 
                               {'type': 'paragraph', 'data': {'text': [{'value': 'xxxxxx'}]}}
                              ]
                  }
        result_code = 200
       ```
        
        *The values of the **elements** key will contain the data configured in the NEXUS IC report template*
 
#### OSI PI Examples
- Example 1: Get full list of points in the database
    1) Import ```OSIPI_WebAPI```
        ```python
       from pynexusic import OSIPI_WebAPI as OSIPI
        ```
       
    2) Initialize ```OSIPI_WebAPI``` class
        ```python
       OSIPI_obj = OSIPI.OSIPI_WebAPI(piwebapi_uri, username, password)
        ```
        *an example for **piwebapi_uri** is https://[domain].com/piwebapi*
    
    3) Execute required function
        ```python
        result, result_status_code = OSIPI_obj.getPointsList(pageSize=20000)
        ```
       
       Output:
        ```python
        result = [{'ServerName': 'xxxxxxxxxxx',
                    'Points': [{'WebId': 'xxxxxxxxxx', 
                                'Id': xxxxx,
                                ...}],
                    'ResponseStatus': 200
                  }]
        result_status_code = None
       ```

- Example 2: Get stream summary data
    1) Import ```OSIPI_WebAPI```
        ```python
       from pynexusic import OSIPI_WebAPI as OSIPI
        ```
       
    2) Initialize ```OSIPI_WebAPI``` class
        ```python
       OSIPI_obj = OSIPI.OSIPI_WebAPI(piwebapi_uri, username, password)
        ```
        *an example for **piwebapi_uri** is https://[domain].com/piwebapi*
    
    3) Execute required function
        ```python
        result, result_status_code = OSIPI_obj.getStreamDataSummary(webID, startTime='*-2mo', endTime='*-1mo', summaryType='Average')
        ```
       *where **webID** is the required stream webID, for more details see OSI PI documentation*
    
        Output:
        ```python
        result = {'Links': {},
                    'Items': [{'Type': 'Average', 
                                'Value': {'Timestamp': 'xxxxxxxx',
                                            'Value': xxxxxx,
                                            ...}
                                }]
                  }
        result_status_code = 200
       ```
    
#### Maximo Examples
To be developed soon

#### Documentum Examples
- Example 1: Getting all repositories
    1) Import ```DOCUMENTUM_API```
        ```python
       from pynexusic import DOCUMENTUM_API as api
        ```
       
    2) Initialize ```DOCUMENTUM_API``` class
        ```python
       doc_api = api.DOCUMENTUM_API(url, username=username, password=password, verbose=True)
        ```
       
    3) Getting all repositories
        ```python
        repos = doc_api.get_repositories()
        ```
       
        Output:
        ```python
        repos = [{'id': 'xxxx', 'title': 'xxxx' ...}
                 ...
                ]
        ```
       
- Example 2: Getting a specific repositories
    1) Import ```DOCUMENTUM_API```
        ```python
       from pynexusic import DOCUMENTUM_API as api
        ```
       
    2) Initialize ```DOCUMENTUM_API``` class
        ```python
       doc_api = api.DOCUMENTUM_API(url, username=username, password=password, verbose=True)
        ```
       
    3) Getting a specific repositories
        ```python
        repo = doc_api.get_repository(repo_name)
        ```
       *where **repo_name** is the name of the report to be extracted from Documentum*
       
        Output:
        ```python
        repo = {'id': 'xxxx', 'title': 'xxxx' ...}
       ```
        

### Change history
#### (V2.3.7) Changes
- NEXUSIC_RESTAPI:
    1) Changed the error handler for the ```validate_and_return_response``` function to raise an Exception instead of returning a string
    2) In the ```getLookupListItem``` function: Added the ability to pass the Lookup list name as a filter parameter
#### (V2.3.6) Changes
- OSIPI_WebAPI:
    1) Improved ```validate_and_return_response``` function error handler
#### (V2.3.5) Changes
- MAXIMO_API:
    1) Added ```use_oslc``` to ```oslc_update_record``` function to allow using either oslc or rest in the Post call
#### (V2.3.4) Changes
- NEXUSIC_RESTAPI:
    1) Fixed a bug in ```createNewRecord``` function
#### (V2.3.3) Changes
- MAXIMO_API:
    1) Added ```oslc_create_new_record``` function
    2) Added ```oslc_update_record``` function
    3) Added ```mbo_exec_method``` function
#### (V2.3.2) Changes
- Docs:
    1) Added library Sphinx docs
#### (V2.3.1) Changes
- MAXIMO_API:
    1) Added the ability to run API calls using _mif
    2) Added ```mbo_update_record``` function
    3) Added ```mbo_get_table``` function
- DOCUMENTUM_API:
    1) Added new connector to DOCUMENTUM
#### (V2.2.1) Changes
- NEXUSIC_RESTAPI:
    1) Added ```jobStatus``` function
    2) Added ```jobContent``` function
    3) Added ```importLibrary``` function
#### (V2.2.0) Changes
- NEXUSIC_RESTAPI:
    1) Added ```generateReport_v2``` function
    2) Added ```get_rt_id``` function
    3) Added ```importRepository``` function
    4) Added ```importMultimedia``` function
    5) Updated ```createNewEvents``` function to import events multimedia
- MAXIMO_API:
    1) Added ```get_mx_wos``` function
    2) Added ```get_mx_srs``` function
    3) Added ```mxapi_post_request``` function
    4) Added ```mbo_create_new_record``` function
    5) Renamed ```get_table``` to ```oslc_get_table```
#### (V2.1.8) Changes
- NEXUSIC_RESTAPI:
    1) Added ```createNewAssets``` function
#### (V2.1.7) Changes
- NEXUSIC_RESTAPI:
    1) Added ```component_id``` field in the event input dictionary in ```createNewEvents``` function
    2) Optimized ```createNewEvents``` function performance
#### (V2.1.6) Changes
- NEXUSIC_RESTAPI:
    1) Added the following arguments to ```createNewEvents``` function:
       - ```sameAsset```
       - ```sameWorkpack```
       - ```sameEventType```
       - ```sameSurveySet```
    2) Fixed a bug in ```createNewEvents``` function to import continuous events
#### (V2.1.5) Changes
- NEXUSIC_RESTAPI:
    1) Added ```getLookupListItem``` function
#### (V2.1.4) Changes
- NEXUSIC_RESTAPI:
    1) ```__init__.py``` version import bug fix
#### (V2.1.3) Changes
- NEXUSIC_RESTAPI:
    1) Added the ability to get multiple pages in the ```getTable``` function
    2) Removed ```current_attempt``` arugment from:
       - getAssetLocationByName
       - getAssetLocationByID
       - getAssetChildren
       - getAssetTypesID
       - getTableDBNames 
       - getAssetByFullLocation
       - getTableDefInfo
#### (V2.1.2) Changes
- NEXUSIC_RESTAPI:
    1) Added ```getAssetByFullLocation``` function
    2) Added ```getTableDefInfo``` function
    3) Added ```createNewEvents``` function
- OSIPI_WebAPI:
    1) Added docstring
- MAXIMO_API:
    1) Added docstring
#### (V2.1.1) Changes:
- OSIPI_WebAPI:
    1) Added the ability to retrieve multiple AssetServers and DataServers in ```get_system_links``` function
    2) Added the ability to get points list for a specific DataServer in ```getPointsList``` function.
#### (V2.1.0) Changes: 
- NEXUSIC_RESTAPI:
    1) Added ```createNewRecord``` function
- MAXIMO_RESTAPI:
    1) Added read only connector class
- OSIPI_WebAPI:
    1) Added read only connector class
#### (V2.0.5) Changes: 
- NEXUSIC_RESTAPI: 
    1) Improved disconnection error handler
    2) ```getAssetChildren``` function: Added the ability to search at a specific level
    3) Added ```getAssetTypesID``` function
    4) Added ```getTableDBNames``` function
#### (V2.0.4) Changes: 
- NEXUSIC_RESTAPI: 
    1) Added ```getAssetLocationByName``` function
    2) Added ```getAssetLocationByID``` function
    3) Added ```getAssetChildren``` function
#### (V2.0.3) Changes: 
- NEXUSIC_RESTAPI: 
    1) Added the ability to authenticate using two modes (APIKEY and BASIC)
        - APIKEY: Requires an API Key to authenticate
        - BASIC: Requires username and password
#### (V2.0.2) Changes: 
- NEXUSIC_RESTAPI: 
    1) Added the ability to bypass SSL verification
#### (V2.0.1) Changes: 
- Initial deployment in pypi.org
#### License
This project is licensed under the MIT license.
