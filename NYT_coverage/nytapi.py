"""
@author: Sourav Chatterjee
@version:0.1
@date: 06/21/14
@brief: Python wrapper around the NYtimes article search API
"""

#import standard modules
from urllib2 import urlopen
import json
import sys
import pprint

#import local modules


class baseapi:
    """
    base class of api. All classes derive from this.
    """
    #def __init__(self):
        
        
    def set_api_key(self,api_key):
        self.api_key=api_key;
    
class article_search_api(baseapi):
    """
    class for the article search api class
    derives from base api class
    follows from the following definition of search query:
    http://api.nytimes.com/svc/search/v2/articlesearch.response-format?
    [q=search term&fq=filter-field:(filter-term)&additional-params=values]&api-key=####
    """
    
    def __init__(self):
        self.baseurl="http://api.nytimes.com/svc/search/v2/articlesearch.json?"; 
        self.input_params={};#dict of input parameters.
        #tried list for input_params but breaks down for reassignment         
    
    def check_date(self,month,day,year):
        if (month<1 or month>12):
            raise error('Month should be between 1 and 12');
        if(day<1 or day>31):
            raise error('Day should be between 1 and 31');
        #Todo: Feb and 30 day month, 4 digit year check
        
        return;
    
    def manip_date(self,month,day,year):
        if(day<10):
            strday='0'+str(day);
        else:
            strday=str(day);
        
        if(month<10):
            strmonth='0'+str(month);
        else:
            strmonth=strmonth;
        
        stryear=str(year);
        return [strmonth,strday,stryear];
        
    def set_begin_date(self,month,day,year):
        """
        @param: month: int between 1 and 12
        @param: day: int between 1 and 31
        @param: year: int 4 digits
        """
        self.check_date(month,day,year);
        [strmonth,strday,stryear]=self.manip_date(month,day,year);
        self.begin_date_str="&begin_date="+stryear+strmonth+strday;
        self.input_params['begin_date_str']=self.begin_date_str;
        return;
    
    def set_end_date(self,month,day,year):
        """
        @param: month: int between 1 and 12
        @param: day: int between 1 and 31
        @param: year: int 4 digits
        """
        self.check_date(month,day,year);
        [strmonth,strday,stryear]=self.manip_date(month,day,year);
        self.end_date_str="&end_date="+stryear+strmonth+strday;
        self.input_params['end_date_str']=self.end_date_str;
        return;
    
    def set_search_term(self,searchterm):
        """
        @param: search term string
        """    
        self.search_str="q="+searchterm;
        return;
    
    def set_filter_field(self,filter_field):
        """
        @param: string filter_field
        """    
        self.filter_field_str="fq="+str(filter_field)+":";
    
    def set_sort_order(self,sortstr):
        if(sortstr!="oldest" and sortstr!="newest"):
            print("Sort order has to be either oldest or newest");
            return;
        self.sort_order_str="&sort="+sortstr;
        self.input_params['sort_order_str']=self.sort_order_str;
        return;
    
    def set_output_field(self,output_str):
        """
        @param:output_str:string of comma separated list of output params
        """
        self.output_str="&fl="+output_str;
        self.input_params['output_str']=self.output_str;
        return;    
    
    
    def generate_call_string(self):
        """
        function that generates the final call string;
        """
        if(self.api_key is None):
            raise error("API Key is not defined");#Should base class do this?        
        
        self.call_url=self.baseurl;
        if hasattr(self,'search_str'):
            self.call_url+=self.search_str;
        if hasattr(self,'filter_field_str'):
            self.call_url=self.call_url+'&'+self.filter_field_str;
        
        #loop over the parameters dict
        for key in self.input_params:
           self.call_url+=self.input_params[key];
        
        #finally add api key. at this point already checked it exists
        self.call_url=self.call_url+'&'+"api-key="+str(self.api_key);
        return;
        
    
    def call_api(self):
        """
        function that writes the final call string and executes the call
        """
        #generate the final call string
        self.generate_call_string();
        #debug
        #print (self.call_url);
         
        #finally make api call
        try: 
            #pass;  
            self.return_articles= json.loads(urlopen(self.call_url).read());
            #print json.dumps(self.return_articles, indent=4, sort_keys=True)
        except :#elaborate on this later
            print("Exception,response did not go through:");
            e = sys.exc_info()[0]
            print(e);
            raise;
        return;
        
               
        
            