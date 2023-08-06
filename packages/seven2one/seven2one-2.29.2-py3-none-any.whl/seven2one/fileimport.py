import csv
import copy
from pathlib import Path
from pprint import pprint
from datetime import timedelta

from loguru import logger

from time import sleep


from .utils.ut_fileimport import FileUtils
from . import core, timeseries

class FileImport():

    def __init__(self, core, timeSeries=None):
        global tsClient, coreClient
        coreClient = core
        self.raiseException = coreClient.raiseException
        if timeSeries != None:        
            tsClient = timeSeries       

    def importNewInventory(self, filePath:str, delimiter:str):
        """
        Creates a new inventory from a CSV file
        
        Parameters:
        -----------
        filePath : str
            The file path of the csv file that should be imported.
        delimiter : str
            The CSV delimiter. Choose ',', ';', or 'tab'.

        Example:
        --------
        >>> createInventoryFromCsv(filePath='C:\\temp\\CreateMeterData.csv', delimiter=';')          
        """

        with open(filePath) as f:
            csv_file = csv.reader(f, delimiter=delimiter)
            content = [row for row in csv_file] 

         ## CHECK FILE
        if content[0][0] != 'name':
            msg = f"Wrong format. Expected header 'name' (for inventory) at position (0, 0)."
            if self.raiseException: raise Exception(msg)
            else:
                logger.error(msg)
                return
  
        if content[2][0] != 'name':
            msg = f"Wrong format. Expected header 'name' (for property) at position (2, 0)."
            if self.raiseException: raise Exception(msg)
            else:
                logger.error(msg)
                return

        inventoryName = content[1][0]

        if not inventoryName:
            msg = "Inventory name missing"
            if self.raiseException: raise Exception(msg)
            else:
                logger.error(msg)
                return 
  
        ## PREPARE IMPORT
        propertyList =[]   
        boolKeys = ['nullable', 'isArray', 'isReference'] 
        keys = [item for item in content[2]]
        columns = len(keys)

        for i, row in enumerate(content):
            if i >= 3:
                propertyDict = {}
                for column in range(columns):
                    if content[2][column] in boolKeys:
                        if row[column] == 'false': value = False
                        if row[column] == 'true': value = True
                    elif not row[column]: continue
                    else: value = row[column]
                    propertyDict.setdefault(content[2][column], value)
                propertyList.append(propertyDict)

        ## IMPORT
        logger.debug(propertyList)
        result = core.TechStack.createInventory(self, inventoryName, propertyList)
        if result == {'createInventory': {'errors': None}}: 
            logger.info(f"Inventory {inventoryName} created.")

    def importItems(self, filePath:str, inventoryName:str, delimiter:str=',',
        chunkSize:int = 5000, pause:int = 1) -> None:
        """
        Imports  items from a CSV file. The CSV file only needs a header of
        property definitions. Each line below the header represents a new item.

        Parameters:
        -----------
        filePath : str
            The file path of the csv file that should be imported.
        inventoryName : str
            The field name of the inventory.
        delimiter : str = ','
            The CSV delimiter. Choose ',', ';', or 'tab'.
        chunkSize : int = 5000
            Determines the number of items which are written per chunk. Using chunks
            can be necessary to avoid overloading. Default is 500 items per chunk.
        pause : int = 1
            Between each chunk upload a pause is inserted in order to avoid overloading.

        Example:
        --------
        >>> importItems(filePath='C:\\temp\\Items.csv', delimiter=';'
            inventoryName='meterData')          
        """
        ## TIMEZONE
        #timeZone = FileUtils._timeZone(timeZone)
               
        ## READ FILE
        with open(filePath) as f:
            csv_file = csv.reader(f, delimiter=delimiter)
            content = [row for row in csv_file]   

        ## PREPARE IMPORT   
        properties = core.TechStack.inventoryProperties(coreClient, inventoryName)
        logger.debug(f'Property names: {list(properties["name"])}')

        diff = FileUtils._comparePropertiesBasic(properties, content[0])
        if len(diff) > 0:
            msg = f"Unknown properties: {list(diff)}"
            if self.raiseException: raise Exception(msg)
            else:
                logger.error(msg)
                return 

        dataType, isArray, nullable = FileUtils._analyzeProperties(inventoryName, properties)
        logger.debug(f'Data types: {dataType}')
        logger.debug(f'Array properties: {isArray}')
        logger.debug(f'Nullable properties: {nullable}')
        logger.info(f"File '{filePath}' read and properties analyzed")

        items = FileUtils._createItems(content, dataType, isArray, nullable)
        logger.debug(f'Basic items: {items}' )


        # ## IMPORT
        if len(items) > chunkSize:
            lenResult = 0
            for i in range(0, len(items), chunkSize):
                result = core.TechStack.addItems(coreClient, inventoryName, items[i : i + chunkSize])
                logger.info(f"{len(result)+lenResult} items of {len(items)} imported.")
                sleep(pause)
        else:
            result = core.TechStack.addItems(coreClient, inventoryName, items)
            logger.info(f"{len(result)} items of file '{filePath}' imported.")

        return

    def importTimeSeriesItems(self, filePath:str,  inventoryName:str, delimiter:str=',',
        chunkSize:int = 500, pause:int = 1) -> None:
        """
        Imports time series inventory items from a CSV file. The CSV file only needs a header of
        property definitions. Each line below the header represents a new time series.

        Parameters:
        -----------
        filePath : str
            The file path of the csv file that should be imported.
        inventoryName : str
            The field name of the inventory.
        delimiter : str = ','
            The CSV delimiter. Choose ',', ';', or 'tab'.
        chunkSize : int = 500
            Determines the number of items which are written per chunk. Using chunks
            can be necessary to avoid overloading. Default is 50 items per chunk.
        pause : int = 1
            Between each chunk upload a pause is inserted in order to avoid overloading.
                 
        """

        # if timeZone == None:
        #     timeZone = core._getDefaults()['timeZone']
               
        ## READ FILE
        with open(filePath) as f:
            csv_file = csv.reader(f, delimiter=delimiter)
            content = [row for row in csv_file]   

        ## PREPARE IMPORT
        tsProperties = ['unit', 'timeUnit', 'factor']
        for header in tsProperties:
            if not header in content[0]:
                msg = f"Header {header} not found. Import aborted."
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 
           
        properties = core.TechStack.inventoryProperties(coreClient, inventoryName)
        logger.debug(f'Property names: {list(properties["name"])}')

        diff = FileUtils._comparePropertiesTimeSeries(properties, content[0])
        if len(diff) > 0:
            msg = f"Unknown properties: {list(diff)}"
            if self.raiseException: raise Exception(msg)
            else:
                logger.error(msg)
                return 

        dataType, isArray, nullable = FileUtils._analyzeProperties(inventoryName, properties)
        logger.debug(f'Data types: {dataType}')
        logger.debug(f'Array properties: {isArray}')
        logger.debug(f'Nullable properties: {nullable}')
        logger.info(f"File '{filePath}' read and properties analyzed")

        timeSeriesItems = FileUtils._createTimeSeriesItems(content, dataType, isArray, nullable)
        logger.debug(f'Time series items: {timeSeriesItems}' )


        # ## IMPORT
        if len(timeSeriesItems) > chunkSize:
            lenResult = 0
            for i in range(0, len(timeSeriesItems), chunkSize):
                result = timeseries.TimeSeries.addTimeSeriesItems(tsClient, inventoryName, timeSeriesItems[i : i + chunkSize])
                logger.info(f"{len(result)+lenResult} items of {len(timeSeriesItems)} imported. Waiting {pause} second(s) before continuing...")
                sleep(pause)
        else:
            result = timeseries.TimeSeries.addTimeSeriesItems(tsClient, inventoryName, timeSeriesItems)
            logger.info(f"{len(result)} items of {len(timeSeriesItems)} imported.") 
        return

    def importTimeSeriesData(self, filePath:str, inventoryName:str=None, 
        importKeyProperty:str=None, delimiter:str=',', timeZone:str=None, 
        dateTimeFormat:str=None, fromTimepoint:str=None, toTimepoint:str=None, 
        timeDelta:timedelta=None, chunkSize:int=20000) -> None: 
        """
        Imports time series data from a specific CSV file or a folder with multiple
        CSV files. The first column is the timestamp index, whereas the first row
        consists of inventory item ids or an import key from the time series property
        definitions. Time series values are spanned as matrix between first column and
        first row. 

        Parameters:
        -----------
        filePath: str
            A path to a folder or a specific CSV file
        inventoryName: str
            The field name of the inventory, if not provided in the import file. 
            In the import file the inventory nameis located at position (0,0).
        importKeyProperty: str = None
            By default the inventory item id is used to find map columns with 
            values with time series. As an alternative, the content of a specific
            property can be used as header which will be mapped with the time series.
            This property should be unique.
        delimiter: str = ','
            The CSV delimiter. Choose ',', ';', or 'tab'.
        timeZone: str = None
            A time zone provided in IANA or isoformat (e.g. 'Europe/Berlin' or 'CET'). Defaults
            to the local time zone.
        dateTimeFormat: str = None
            Several date-time formats are supported, however, a custom format according to
            datetime.strftime() and strptime() format codes can be passed to convert the
            timestamp.
        fromTimepoint: str = None
            Specify a timestamp in isoformat from which data should be imported.
        toTimepoint: str = None
            Specify a timestamp in isoformat until which data should be imported.
        timeDelta: datetime.timedelta = None
            Define a time delta to add or substract to the original timestamp.
        chunkSize: int = 20000
            Determines the number of time series datapoints which are written per chunk. Using chunks
            can be necessary to avoid overloading.

        Example:
        --------
        >>> client.FileImport.importTimeSeriesData(
            filePath=file,
            inventoryName='meterData'
            importKeyProperty='name'
            delimiter=';', 
            timeZone='CET', 
            dateTimeFormat='%Y-%b-%d %H:%M:%S'
            fromTimePoint='2023-01-01'
            toTimepoint='2023-03-05'
            timeDelta=-timedelta(hours=1))
            chunkSize=20000
        """

        ## TIMEZONE
        timeZone = FileUtils._timeZone(timeZone)

        ## CHECK FILE PATH
        filePath = Path(filePath)
        if str(filePath).lower().endswith('csv'):
            if not filePath.exists():
                msg = f"File path {filePath} does not exist"
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 

            files = [filePath]
        else:
            if not filePath.exists():
                msg = f"File path {filePath} does not exist"
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 
            
            files = [file for file in filePath.iterdir() if str(file).lower().endswith('csv')]
    
        output = {}
        
        for file in files:

            fileName = file.name
        
            output.setdefault(fileName, 
                {'Time series': 0,
                'Time series errors': 0,
                'Values written': 0,
                'Value errors': 0,
                'Errors': None})

            ## READ FILE
            with open(file) as f:
                csv_file = csv.reader(f, delimiter=delimiter)
                content = [row for row in csv_file]
            logger.debug('CSV file read')

            if inventoryName == None:
                inventoryName = content[0][0]
                if inventoryName == '':
                    msg = "Missing inventory name"
                    if self.raiseException: raise Exception(msg)
                    else:
                        logger.error(msg)
                        return 

                else:
                    logger.debug(f"Inventory name: {inventoryName}")

            tsLength = len(content) - 1

            # CONVERT DATETIME COLUMN
            if dateTimeFormat == None:
                dateTimeFormat = FileUtils._dateFormat(content[1][0])

            for i, row in enumerate(content):
                try:
                    if content[i][0] == '': continue
                    content[i][0] = FileUtils._convertTimestamp(content[i][0], timeZone, dateTimeFormat, timeDelta)
                except Exception as err: 
                    if i >= 1:
                        msg = f"Timestamp {row[0]} could not be converted. {err}"
                        if self.raiseException: raise Exception(msg)
                        else:
                            logger.error(msg)
                            return 
                    pass

            ## GET ITEM ID FROM IMPORT KEY
            if importKeyProperty != None:
                try:
                    items = core.TechStack.items(coreClient, inventoryName, fields=['unit', 'resolution', 'sys_inventoryItemId', importKeyProperty])
                except Exception as err:
                    if self.raiseException: raise Exception(err)
                    else:
                        logger.error(err)
                        return 
                names = content[0].copy()
                del names[0]
                items = items[items[importKeyProperty].isin(names)]
                idMapping = {}
                for item in items.iterrows():
                    idMapping.setdefault(item[1][importKeyProperty],item[1]['sys_inventoryItemId'])

                if len(idMapping) == 0:
                    msg = f"No item ids for importKeyProperty '{importKeyProperty}' found."
                    if self.raiseException: raise Exception(msg)
                    else:
                        logger.error(msg)
                        return 

                logger.debug(f"Id Mapping: {idMapping}")
            else:
                try:
                    items = core.TechStack.items(coreClient, inventoryName, fields=['unit', 'resolution', 'sys_inventoryItemId'])
                    logger.debug("Inventory read for default option (import with ivnentory item ids).")
                except Exception as err:
                    if self.raiseException: raise Exception(err)
                    else:
                        logger.error(err)
                        return 

            # Get the Inventory Id
            try:                      
                inv = core.TechStack.inventories(coreClient, where=f'name eq "{inventoryName}"')
                inventoryId = inv.loc[0, 'inventoryId']
                logger.debug(f"Found inventoryId {inventoryId} for inventory {inventoryName}.")
            except:
                msg = f"No inventory with name '{inventoryName}'."
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 

            ## VERIFY IDS, CREATE DATA_DICTS, IMPORT
            errorDict = {}
            inv = None
            tsItems = [] # only used in bulk operation

            for column in range(1, len(content[0])):
                if importKeyProperty != None:
                    try:
                        inventoryItemId = idMapping[content[0][column]]
                    except:
                        logger.warning(f"ImportKeyProperty '{content[0][column]}' not found.")
                        output[fileName]['Time series errors'] += 1
                        errorDict.setdefault(content[0][column], 'Not found')
                        continue
                else:
                    try:
                        inventoryItemId = content[0][column]
                    except:
                        logger.warning(f"Inventory item id {inventoryItemId} not found.")
                        errorDict.setdefault(content[0][column], 'Not found')
                        continue                

                try:
                    properties = items[items['sys_inventoryItemId'] == inventoryItemId]
                    if properties.empty:
                        logger.warning(f"Inventory item id {inventoryItemId} not found.")
                        output[fileName]['Time series errors'] += 1
                        errorDict.setdefault(content[0][column], 'Not found')
                        continue
                except:
                    logger.warning(f"Inventory item id {inventoryItemId} not found.")
                    continue

                properties = properties.to_dict('records')[0]
                timeUnit = properties['resolution'].split(' ')[-1]
                factor = properties['resolution'].split(' ')[0]

                tsDict = {
                        'sys_inventoryId': inventoryId,
                        'sys_inventoryItemId': None,
                        'data': {
                            'resolution': {
                                'timeUnit': None,
                                'factor': None
                            },
                            'unit': None,
                            'dataPoints': None
                        }
                    }

                valueList = []
                for i, row in enumerate(content):
                    if i >= 1:     
               
                        try:
                            if row[0] == '': continue
                            if fromTimepoint:
                                if row[0] < fromTimepoint: continue
                            if toTimepoint:
                                if row[0] > toTimepoint: continue
                            float(row[column])              
                            valueList.append({'timestamp': row[0], 'value': row[column]})
                        except:
                            errorDict.setdefault(content[0][column], {})
                            errorDict[content[0][column]].setdefault(row[0], row[column])
                            output[fileName]['Value errors'] += 1     

                logger.debug(f"Value list first 5 items: {valueList[:5]}")

                tsDict['sys_inventoryItemId'] = inventoryItemId
                tsDict['data']['unit'] = properties['unit']
                tsDict['data']['resolution']['timeUnit'] = timeUnit
                tsDict['data']['resolution']['factor'] = factor  
                tsDict['data']['dataPoints'] = valueList

                tsItems.append(tsDict)
                output[fileName]['Values written'] += len(valueList)

            logger.debug("Time series collection created")
            output[fileName]['Time series'] = len(tsItems)

            tsItemsEmpty = copy.deepcopy(tsItems)
            for item in tsItemsEmpty:
                del item['data']['dataPoints']
            
            for i in range(0, tsLength, chunkSize):
                tsChunk = copy.deepcopy(tsItemsEmpty)
                for j, ts in enumerate(tsChunk):
                    tsChunk[j]['data'].setdefault('dataPoints', tsItems[j]['data']['dataPoints'][i : i + chunkSize])
                    
                timeseries.TimeSeries.setTimeSeriesDataCollection(self=tsClient, timeSeriesData=tsChunk)    
                logger.info(f"({int(i/chunkSize+1)}/{tsLength//chunkSize+1}) chunks imported.")            

        logger.info(f"Import finished")

        return 

    def importGroupInstanceItems(self, filePath:str, groupInventoryName:str,
        instanceInventoryName, importKeyProperty, delimiter:str=None, chunkSize:int = 500,
        pause:int = 1) -> None:
        """
        Imports  group instance items from a CSV file. The CSV file only needs a header
        of property definitions. The first column is reserved for the groupInventoryItemId.
        Each line below the header represents a new item.

        Parameters:
        -----------
        filePath: str
            The file path of the csv file that should be imported.
        groupInventoryName: str
            The field name of the group inventory.
        instanceInventoryName: str
            The field name of the time series instance inventory belonging to the group.
        importKeyProperty: str
            Provide a property of the parent group time series that is unique.
            (The first column 'groupName' used in the CSV file.)
        delimiter: str = ','
            The CSV delimiter. Choose ',', ';', or 'tab'.
        chunkSize: int = 500
            Determines the number of items which are written per chunk. Using chunks
            can be necessary to avoid overloading.
        pause: int = 1
            Between each chunk upload a pause is inserted in order to avoid overloading.

        """
              
        ## READ FILE
        with open(filePath) as f:
            csv_file = csv.reader(f, delimiter=delimiter)
            content = [row for row in csv_file]   

        ## PREPARE IMPORT
        properties = core.TechStack.inventoryProperties(coreClient, instanceInventoryName)
        logger.debug(f'Property names: {list(properties["name"])}')

        diff = FileUtils._comparePropertiesBasic(properties, content[0][1:-1])
        if len(diff) > 0:
            msg = f"Unknown properties: {list(diff)}"
            if self.raiseException: raise Exception(msg)
            else:
                logger.error(msg)
                return 

        if importKeyProperty != None:
            try:
                items = core.TechStack.items(coreClient, groupInventoryName, fields=['sys_inventoryItemId', importKeyProperty])
            except Exception as err:
                if self.raiseException: raise Exception(err)
                else:
                    logger.error(err)
                    return 
          
            names = [row[0] for row in content]
            del names[0]

            items = items[items[importKeyProperty].isin(names)]

            idMapping = {}
            for item in items.iterrows():
                idMapping.setdefault(item[1][importKeyProperty],item[1]['sys_inventoryItemId'])
            logger.debug(f"Id mapping: {idMapping}")
            if len(idMapping) == 0:
                msg = f"No item ids for importKeyProperty '{importKeyProperty}' found."
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 

        dataType, isArray, nullable = FileUtils._analyzeProperties(instanceInventoryName, properties)
        logger.debug(f'Data types: {dataType}')
        logger.debug(f'Array properties: {isArray}')
        logger.debug(f'Nullable properties: {nullable}')
        logger.info(f"File '{filePath}' read and properties analyzed")

        items = FileUtils._createInstanceItems(content, dataType, isArray, nullable, idMapping)
        logger.debug(f'Instance items: {items}' )

        # ## IMPORT
        if len(items) > chunkSize:
            lenResult = 0
            for i in range(0, len(items), chunkSize):
                result = timeseries.TimeSeries.addTimeSeriesItemsToGroups(tsClient, groupInventoryName, items[i : i + chunkSize])
                logger.info(f"{len(result)+lenResult} items of {len(items)} imported.")
                sleep(pause)
        else:
            result = timeseries.TimeSeries.addTimeSeriesItemsToGroups(tsClient, groupInventoryName, items)
            logger.info(f"{len(items)} items of file '{filePath}' imported.")

        return

    def importGroupInstanceItemsWithData(self, filePath:str, groupInventoryName:str,
        instanceInventoryName:str, groupKeyProperty:str=None, instanceKeyProperties:list=None,
        delimiter:str=',', timeZone:str=None, dateTimeFormat:str=None, fromTimepoint:str=None, 
        toTimepoint:str=None, timeDelta:timedelta=None, chunkSize=20000, pause:int = 1) -> None:
        """
        Imports  group instance items from a CSV file. The CSV file only needs a header
        of property definitions. The first column is reserved for the groupInventoryItemId.
        Each line below the header represents a new item.

        Parameters:
        -----------
        filePath : str
            The file path of the csv file that should be imported.
        groupInventoryName : str
            The field name of the group inventory.
        instanceInventoryName : str
            The field name of the time series instance inventory belonging to the group.
        groupKeyProperty : str
            Is a property of the group item to identify it, which have to be placed 
            in the first line of the file. If None, the group item id is expected. 
        instanceKeyProperties:
            One or two key properties of the instance item to identiy it uniquely. The order must be
            the same as in the import file.
        delimiter : str = ','
            The CSV delimiter. Choose ',', ';', or 'tab'.
        timeZone: str = None
            A time zone provided in IANA or isoformat (e.g. 'Europe/Berlin' or 'CET'). Defaults
            to the local time zone.
        dateTimeFormat: str = None
            Several date-time formats are supported, however, a custom format according to
            datetime.strftime() and strptime() format codes can be passed to convert the
            timestamp.
        fromTimepoint : str = None
            Specify a timestamp in isoformat from which data should be imported.
        toTimepoint : str = None
            Specify a timestamp in isoformat until which data should be imported.
        timeDelta: datetime.timedelta = None
            Define a time delta to add or substract to the original timestamp.
        chunkSize: int = 20000
            Determines the number of time series datapoints which are written per chunk. Using chunks
            can be necessary to avoid overloading.
        pause: int = 1
            Between each chunk upload a pause is inserted in order to avoid overloading.
        """

        ## TIMEZONE
        timeZone = FileUtils._timeZone(timeZone)

        ## CHECK FILE PATH
        filePath = Path(filePath)
        if str(filePath).lower().endswith('csv'):
            if not filePath.exists():
                msg = f"File path {filePath} does not exist"
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 
            files = [filePath]

        else:
            if not filePath.exists():
                msg = f"File path {filePath} does not exist"
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 
            
            files = [file for file in filePath.iterdir() if str(file).lower().endswith('csv')]
    
        output = {}
        
        for file in files:

            fileName = file.name
        
            output.setdefault(fileName, 
                {'Time series instances': 0,
                'Time series instance errors': 0,
                'Values written': 0,
                'Value errors': 0,
                'Errors': None})

            ## READ FILE
            with open(file) as f:
                csv_file = csv.reader(f, delimiter=delimiter)
                content = [row for row in csv_file]
            logger.debug('CSV file read')

            ## PREPARE IMPORT: Get Instance properties
            instanceProperties = []
            for i, row in enumerate(content):
                if i == 0: continue
                if row[0] in ['unit', 'timeUnit', 'factor']: 
                    pass
                elif row[0] == 'data':
                    dataBegin = i + 1
                    break
                elif row[0] == 'values':
                    dataBegin = i + 1
                    break
                else:
                    instanceProperties.append(row[0])
                if i > 100: 
                    logger.error("No keyword 'data' or 'values' found")
                    return

            tsLength = len(content) - dataBegin

            # CONVERT DATETIME COLUMN
            if dateTimeFormat == None:
                dateTimeFormat = FileUtils._dateFormat(content[dataBegin][0])

            for i, row in enumerate(content[dataBegin:]):
                try:
                    if row[0] == '': continue
                    content[dataBegin+i][0] = FileUtils._convertTimestamp(content[dataBegin+i][0], timeZone, dateTimeFormat, timeDelta)
                except Exception as err: 
                    if i >= 1:
                        msg = f"Timestamp {row[0]} could not be converted. {err}"
                        if self.raiseException: raise Exception(msg)
                        else:
                            logger.error(msg)
                            return 
                    pass

            ## PREPARE IMPORT: Compare Instance properties
            properties = core.TechStack.inventoryProperties(coreClient, instanceInventoryName)
            logger.debug(f'Property names: {list(properties["name"])}')

            diff = FileUtils._comparePropertiesBasic(properties, instanceProperties)
            if len(diff) > 0:
                msg = f"Unknown properties: {list(diff)}"
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 

            ## PREPARE IMPORT: Get Mapping of Import Key
            if groupKeyProperty != None:
                try:
                    items = core.TechStack.items(coreClient, groupInventoryName, fields=['sys_inventoryItemId', groupKeyProperty])
                except Exception as err:
                    if self.raiseException: raise Exception(err)
                    else:
                        logger.error(err)
                        return 
            
                names = [column for column in content[0]]
                del names[0]

                items = items[items[groupKeyProperty].isin(names)]

                idMapping = {}
                for item in items.iterrows():
                    idMapping.setdefault(item[1][groupKeyProperty],item[1]['sys_inventoryItemId'])
                logger.debug(f"Id mapping: {idMapping}")
                if len(idMapping) == 0:
                    msg = f"No item ids for groupKeyProperty '{groupKeyProperty}' found."
                    if self.raiseException: raise Exception(msg)
                    else:
                        logger.error(msg)
                        return 

            ## PREPARE IMPORT: Check dataType, Array and nullable properties
            dataType, isArray, nullable = FileUtils._analyzeProperties(instanceInventoryName, properties)
            logger.info(f"File '{filePath}' read and properties analyzed")

            itemContent = FileUtils._createInstanceItemContent(content[:dataBegin])
            tsItemContent = content[:dataBegin]
            items = FileUtils._createInstanceItems(itemContent, dataType, isArray, nullable, idMapping, transpose=True)
            tsItems = FileUtils._createInstanceItems(tsItemContent, dataType, isArray, nullable, idMapping, transpose=True)

            logger.debug(f'Instance items: {items}' )


            # Find position of instance key properties
            
            if instanceKeyProperties == None:
                msg = "No instanceKeyProperties provided."
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 

            instancePropPos = []
            for i, row in enumerate(content[:dataBegin]):
                for property in instanceKeyProperties:
                    if property == row[0]:
                        instancePropPos.append(i)

            try:                      
                inv = core.TechStack.inventories(coreClient, where=f'name eq "{instanceInventoryName}"')
                inventoryId = inv.loc[0, 'inventoryId']
                logger.debug(f"Found inventoryId {inventoryId} for inventory {instanceInventoryName}.")
            except:
                msg = f"No inventory with name '{instanceInventoryName}'."
                if self.raiseException: raise Exception(msg)
                else:
                    logger.error(msg)
                    return 

            ## IMPORT: create group instance items
            errorDict = {}

            for i in range(0, len(items)):
                try:
                    timeseries.TimeSeries.addTimeSeriesItemsToGroups(tsClient, groupInventoryName, [items[i]])
                    sleep(pause)
                except:
                    logger.warning(f"Instance item in column {i+1} could not be created")
                    errorDict.setdefault(i+1, "Instance could not be created")
                try:
                    if len(instanceKeyProperties) == 1:
                        x0 = content[instancePropPos[0]][i+1]
                        instanceTs = core.TechStack.items(coreClient, instanceInventoryName, 
                            where=f'{instanceKeyProperties[0]} eq "{x0}"')
                    if len(instanceKeyProperties) >= 2:
                        x0 = content[instancePropPos[0]][i+1]
                        x1 = content[instancePropPos[1]][i+1]
                        instanceTs = core.TechStack.items(coreClient, instanceInventoryName, 
                            where=f'{instanceKeyProperties[0]} eq "{x0}" and {instanceKeyProperties[1]} eq "{x1}"')
                    inventoryItemId = instanceTs.loc[0, 'sys_inventoryItemId']
                except:
                    logger.warning(f"Instance item in column {i+1} not found")
                    output[fileName]['Time series instance errors'] += 1
                    continue
                sleep(pause)

                tsDict = {
                    'sys_inventoryId': inventoryId,
                    'sys_inventoryItemId': inventoryItemId ,
                    'data': {
                        'resolution': {
                            'timeUnit': tsItems[i]['timeUnit'],
                            'factor': tsItems[i]['factor']
                        },
                        'unit': tsItems[i]['unit'],
                        'dataPoints': None
                    }
                }

                valueList = []
                for row in content[dataBegin:]:
                    try:
                        if fromTimepoint:
                            if row[0] < fromTimepoint: continue
                        if toTimepoint:
                            if row[0] > toTimepoint: continue
                        float(row[i+1])   
                        valueList.append({'timestamp': row[0], 'value': row[i+1]})
                    except:
                        pass
                        errorDict[i+1] = {}
                        errorDict[i+1].setdefault(row[0], row[i+1])
                        output[fileName]['Value errors'] += 1
               
                for k in range(0, tsLength, chunkSize):     
                    tsDict['data']['dataPoints'] = valueList[k : k + chunkSize]
                    try:
                        timeseries.TimeSeries.setTimeSeriesDataCollection(self=tsClient, timeSeriesData=[tsDict])

                    except Exception as err:
                        logger.error(f"Time series values could not be written. Cause: {err}")
                        errorDict[i+1] = err
                        break

                output[fileName]['Values written'] += len(valueList)
            if len(errorDict) > 0:
                output[fileName]['Errors'] = errorDict
                        
        return output