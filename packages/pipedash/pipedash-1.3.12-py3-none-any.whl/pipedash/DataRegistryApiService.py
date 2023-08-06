import requests


class DataRegistryApiService(object):

    def __init__(self, registry):
        self.registry = registry

        return None

    def queryData(self, model, query, options):

        fieldPath = model["name"]

        if "group" in model and model["group"] is not None:
            fieldPath = model["group"]+"/"+fieldPath
        if "namespace" in model and model["namespace"] is not None:
            fieldPath = model["namespace"]+"/"+fieldPath

        filter = query["mongoQuery"] if query is not None and "mongoQuery" in query else {}


        query_data = {
                "filter": filter,
                "query": query,
                "model": model
            }

        headers = {
                "authheader": options["registry"]["auth"]
            }


        if "fields" in options:
            fieldsmap = {}
            for k in options["fields"]:
                fieldsmap[k["name"]] = "1"
            query_data["fields"] = fieldsmap

        if self.registry is not None and "endpoint" in self.registry:

            try:
                data = requests.post(self.registry["endpoint"]+"/api/data/"+fieldPath,
                                     json=query_data, headers=headers)
                json_data = data.json()

                if json_data["success"]:
                    return json_data["results"]

            except Exception as e:
                print("Error in query data", e)

        else:
            print("The registry can not be found")

        return None
