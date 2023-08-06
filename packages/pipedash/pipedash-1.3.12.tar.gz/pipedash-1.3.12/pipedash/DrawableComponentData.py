from pipedash.helper import Serializable

class DrawableDataInfo(Serializable):
    fields: []
    registry: {}
    model: {}
    query: {}
    aggregation: {}
    pass

class DrawableComponentData(Serializable):
    pass