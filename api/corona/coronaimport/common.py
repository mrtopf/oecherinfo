
import zeep
import copy
class SurvStatRequest:
    """base request for survstat webservice"""

    COUNTY = {"State": "05", "Region": "DEA2", "County": "05334"}

    def __init__(self, incidence=True):
        """initialize client and factory"""
        self.client = zeep.Client(
            "https://tools.rki.de/SurvStat/SurvStatWebService.svc?wsdl")
        self.factory = self.client.type_factory("ns2")
        self.base_request = {
            "Language": "German",
            "Cube": "SurvStat",
            "Measures": {"Count": 0},
            # Totals still included, setting `true` yields duplicates
            "IncludeTotalColumn": False,
            "IncludeTotalRow": False,
            "IncludeNullRows": False,
            "IncludeNullColumns": False,
            "HierarchyFilters": self.factory.FilterCollection(
                [
                    {
                        "Key": {
                            "DimensionId": "[PathogenOut].[KategorieNz]",
                            "HierarchyId": "[PathogenOut].[KategorieNz].[Krankheit DE]",
                        },
                        "Value": self.factory.FilterMemberCollection(
                            ["[PathogenOut].[KategorieNz].[Krankheit DE].&[COVID-19]"]
                        ),
                    },
                    {
                        "Key": {
                            "DimensionId": "[ReferenzDefinition]",
                            "HierarchyId": "[ReferenzDefinition].[ID]",
                        },
                        "Value": self.factory.FilterMemberCollection(
                            ["[ReferenzDefinition].[ID].&[1]"]
                        ),
                    },
                    {
                        "Key": {
                            "DimensionId": "[DeutschlandNodes].[Kreise71Web]",
                            "HierarchyId": "[DeutschlandNodes].[Kreise71Web].[FedStateKey71]",
                        },
                        "Value": self.factory.FilterMemberCollection(
                            [
                                f"[DeutschlandNodes].[Kreise71Web].[FedStateKey71].&[{ self.COUNTY['State'] }].&[{ self.COUNTY['Region'] }].&[{ self.COUNTY['County'] }]"
                            ]
                        ),
                    },
                ]
            ),
        }
        if incidence:
            self.base_request['Measures'] = {"Incidence": 1}


    def __call__(self, request):
        """do the request

        `request` can be
        
        ```
        {
            "ColumnHierarchy": "[ReportingDate].[YearWeek]",
            "RowHierarchy": "[AlterPerson80].[AgeGroupName6]",
        }
        ```
    
        
    
        """
        my_request = copy.copy(self.base_request)
        my_request.update(request)
        self.result = self.client.service.GetOlapData(my_request)
        self.columns = [i["Caption"] for i in self.result.Columns.QueryResultColumn[1:]]
        return self.result
        
