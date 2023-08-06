from typing import List, Union
import requests
class Measures:
    """
    Class containing methods to work with Measures through the SFM API
    """
    def get_measure_id(self, *object_ids: Union[str, List[str]]) -> List[str]:
        """
        Gets the measure id from SFM for a given object id in case you do
        not already have the measure id for the source you are getting values from. 
        This is needed because there is no api endpoint for trend data in SFM
        that takes object id as a paremeter, meaning you have to have the 
        measure id if you want trend data

        Args: 
            object_id (Union[str, List[str]]): The object id you want to get the measure_id for
            token (str): The token used to authenticate the api request
        
        Returns:
            measure_ids (List[str]): returns a list of measure ids
        """
        measure_ids = []
        for object_id in object_ids:
            measure_resp = requests.get(url=f"{self.sfm_url}/Measures", params={'dataobject_id': object_id}, headers=self.headers, verify=False).json()
            measure_id = measure_resp["Results"][0]['Id']
            measure_ids.append(measure_id)
        return measure_ids
    def update_measures(self):
        options = {
            "Title": "string",
            "MeasureType": "Daily",
            "Definition": "string",
            "Description": "string",
            "Source": "string",
            "ValueSource": "None",
            "TargetSource": "None",
            "UnitOfMeasure": "string",
            "Formula": "string",
            "FormatString": "string",
            "Category": "S",
            "ShowLastValidValue": true,
            "BaseType": "string",
            "AggregateFunction": "AVG",
            "Dependents": [
                "00000000-0000-0000-0000-000000000000"
            ],
            "DefaultTarget": {
                "TargetType": "string",
                "IsInclusive": true,
                "GreenUpperValue": 0,
                "GreenLowerValue": 0
            },
            "TileDisplayType": "StandardTile",
            "TrendDisplayType": "Standard",
            "TargetType": "GreenUpperRange",
            "YearToDateOption": "ManualCapture",
            "TargetBoundaries": "Inclusive"
        }
        pass
    def create_measure(self, measures: list(object)) -> object:
        
        """
        Creates a measure

        Args:
            measures: list of measure objects to create
            measure_group_id: Desired measure group to assign measure to
            title: desired title for the measure
            measure_type: Type of measure. Ex. 'Daily'
            description: Description of measure
            dependents (List[str], optional): list of the measure id's to include as dependents of this measure. Defaults to []
        """
        created_measures = []
        for measure in measures:
            params={
                "Title": "string",
                "MeasureType": "Daily",
                "Definition": "string",
                "Description": "string",
                "Source": "string",
                "ValueSource": "None",
                "TargetSource": "None",
                "UnitOfMeasure": "string",
                "Formula": "string",
                "FormatString": "string",
                "Category": "S",
                "ShowLastValidValue": True,
                "BaseType": "string",
                "AggregateFunction": "AVG",
                "Dependents": measure['dependents'] if 'dependents' in measure else [],
                "DefaultTarget": {
                    "TargetType": "string",
                    "IsInclusive": True,
                    "GreenUpperValue": 0,
                    "GreenLowerValue": 0
                },
                "TileDisplayType": "StandardTile",
                "TrendDisplayType": "Standard",
                "TargetType": "GreenUpperRange",
                "YearToDateOption": "ManualCapture",
                "TargetBoundaries": "Inclusive"
            }
            params={}
            created_measure = requests.post(url=f"{self.sfm_url}/MeasureGroups/{measure['measure_group_id']}/Measures", params=params, headers=self.headers, verify=False).json()
            created_measures.append(created_measure)
        return created_measures
        



