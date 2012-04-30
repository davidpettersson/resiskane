from haystack import indexes, site
from models import Station

class StationIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name_auto = indexes.EdgeNgramField(model_attr='name')
    
site.register(Station, StationIndex)
