"""
@author:Sourav Chatterjee
@date:6/20/14
@brief: processes json field obtained from nyt api
"""
#import standard modules
import json
#import local modules

class process_nytapi:
    """
    main class to process result from api
    """
    
    def __init__(self,result):
        self.result=result;
        
    def pretty_print(self):
        print json.dumps(self.result, indent=4, sort_keys=True);
        return;
    
    def get_hitcount(self):
        hitcount=self.result["response"]["meta"]["hits"];
        return hitcount;
        
        