import requests
FORUM_ID=''
class MeasureGroups:
    def get_measure_groups(self,forum_id: str):
        """
        Function to grab all measure groups for a forum structure

        Parameters:
            forum_id: forum structure to get measures from
        """
        api_resp = requests.get(
                        url=f"{self.sfm_url}/ForumStructures/{forum_id}/MeasureGroups", 
                        headers=self.headers, 
                        verify=False
                    )
        if api_resp.status_code == 200:
            return api_resp.json()
        else:
            return api_resp
    def create_measure_group(self,forum_id: str, names: list(str)):
        """
        Checks if a measure group with name already exists. 
        If not, it makes a measure group with the specified name on the specified forum structure

        Paramters: 
            forum_id: the forum_id to create the measure group for
            names: the names of each measure group you want to create
        
        """
        try:
            existing_names = []
            measure_groups = requests.get(
                url=f"{self.sfm_url}/ForumStructures/{forum_id}/MeasureGroups", 
                headers=self.headers, 
                verify=False
            ).json()
            for name in names:
                temp = False
                for measure_group in measure_groups:
                    if measure_group['GroupName'] == name:
                        temp = True
                if not temp:
                    api_resp = requests.put(
                        url=f"{self.sfm_url}/ForumStructures/{forum_id}/MeasureGroups", 
                        params={'name': name}, 
                        headers=self.headers, 
                        verify=False
                    )
                    print(api_resp)
                else:
                    existing_names.append(name)
            if len(existing_names) > 0:
                print('These names already exist', existing_names)
        except Exception as e :
            print(e)
        return existing_names
    def delete_measure_groups():
        pass
    