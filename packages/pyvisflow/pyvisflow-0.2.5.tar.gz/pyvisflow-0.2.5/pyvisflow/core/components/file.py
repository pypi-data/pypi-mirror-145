from typing import TYPE_CHECKING, Any, Dict, List, Union
from pyvisflow.core.props.dataFilterProp import DataFilterPropInfo

from pyvisflow.core.props.fnsMethodProp import FnsMethodPropInfo
from pyvisflow.core.props.methodProp import LambdaMethodPropInfo
from pyvisflow.core.props.typeProp import BoolTypePropInfo, StrTypePropInfo, SubscriptableTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from .components import Component
from pyvisflow.utils.data_gen import get_global_id
from pyvisflow.core.reactive import Reactive
from pyvisflow.core.props.absProp import AbsPropInfo
# if TYPE_CHECKING:
    

class File(Component):
    def __init__(self) -> None:
        super().__init__('file', TComponentType.builtIn)
        self.__info_id=f'data-{get_global_id()}'

    @property
    def columns(self):
        p = self.get_prop('details.columns')
        return SubscriptableTypePropInfo(p)

    @property
    def data(self):
        return FileData(self,self.get_prop('details'))



    def _ex_get_react_data(self) -> Dict[str, Any]:
        data= super()._ex_get_react_data()
        data.update({
            'infoID':self.__info_id,
            'details':{
                'columns':[],
                'data':list(list())
            },
        })
        return data



class FileData(Reactive):

    def __init__(self,file:File,details_binding:AbsPropInfo) -> None:
        super().__init__()
        self.__file=file
        self.details_binding=details_binding
        self.set_prop('details',details_binding)


    def __getitem__(self, column: Union[str, StrTypePropInfo]):
        p = DataFilterPropInfo('row')
        subs = SubscriptableTypePropInfo[str, StrTypePropInfo](p)

        return subs[column]

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data =  super()._ex_get_react_data()
        data.update({
            'details':{
                'columns':[],
                'data':list(list())
            }
        })
        return data

    def filter(self,condition: BoolTypePropInfo):
        lambdaFn = LambdaMethodPropInfo(condition,['row'])
        fns = FnsMethodPropInfo('filter',[self.details_binding,lambdaFn],'dataFns')
        return FileData(self.__file,fns) 

    def orderby(self,columns: Union[List[str],str],asc:Union[List[bool],bool]):
        if isinstance(columns,str):
            columns=[columns]
        if isinstance(asc,bool):
            asc=[asc]    

        if len(asc)>1:
            assert  (len(columns)==len(asc)),'columns len must be eq asc len'
        asc_values = ['asc' if v else 'desc' for v in asc]
        fns = FnsMethodPropInfo('sort',[self.details_binding,columns,asc_values],'dataFns')
        return FileData(self.__file,fns) 

    def groupby(self,keys:List[str]):
        fns = FnsMethodPropInfo('groupby',[self.details_binding,keys],'dataFns')
        return FileData(self.__file,fns) 