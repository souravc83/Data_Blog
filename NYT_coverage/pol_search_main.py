"""
@author:Sourav Chatterjee
@date:06/20/2014
@brief: use nytimes api to get data on how much different politicians are in the news
"""

#import from standard module
import time
import numpy as np # to save files

#local module imports
import nytapi
reload (nytapi) #use to load latest version when changing constantly
import process_nytapi
reload(process_nytapi)


def savefile(xfile,yfile,fnamestr='testfile.txt'):
    """
    saves a file given lists for x and y values
    @param xfile: string list containing x values
    @param yfile: int list containing y values
    @param fnamestr: file name String
    """
    if len(xfile)!=len(yfile):
        print "list names are not equal,cannot write file";
        return;
    thefile=open(fnamestr,'w');
        
    for i in range(len(xfile)):
        thefile.write("%s\t%d\n"%(xfile[i],yfile[i]));
    thefile.close();    
    return;
    

def count_pol_coverage(pol_name_str):
    """
    calculates the number of articles written about a politician over time
    @param: pol_name_str: string with name of politician,e.g. "Hillary Clinton"
    """
    article_search=nytapi.article_search_api();
    
    #always first set api key
    article_search.set_api_key('6d35e713a27934716115205ee8ae733b:6:69503175');
    
    #set other parameters
    article_search.set_search_term(pol_name_str);
    #article_search.set_begin_date(4,2,2014);
    #article_search.set_end_date(5,1,2014);
    article_search.set_sort_order("oldest");
    article_search.set_output_field("pub_date")
    
    #make calls in a loop
    months=range(1,6);
    count_list=[];
    for month in months:
        time.sleep(0.5);#pause between calls, so not to throttle
        article_search.set_begin_date(month,2,2014);
        article_search.set_end_date(month+1,1,2014);
         #call api
        article_search.call_api(); 
        #process api call to plot data
        process_api=process_nytapi.process_nytapi(article_search.return_articles);    
        #process_api.pretty_print();#debug to check if working properly
        #print process_api.get_hitcount();
        count_list.append(process_api.get_hitcount());
    
    total_hit=sum(count_list);
       
    return total_hit;

def proper_name(search_str,counter):
    [first,last]=search_str.split('+');
    proper_str=str(counter)+'.'+first+'_'+last;
    return proper_str;
    

def party_pol_coverage(candidate_list,filename='testfile.txt'):
    
    #create dict
    cand_dict={};
    #initialize dict
    for candidate in candidate_list:
        cand_dict[candidate]=0;
    
    for candidate in candidate_list:
        cand_dict[candidate]=count_pol_coverage(candidate);
        print candidate;
        time.sleep(2);
        
    name_list=[];
    count_list=[];
    counter=0;
    for name in sorted(cand_dict,key=cand_dict.get,reverse=True):
        counter+=1;
        prop_name=proper_name(name,counter);
        name_list.append(prop_name);
        count_list.append(cand_dict[name]);
        print prop_name+'\t'+str(cand_dict[name]);    
      
    savefile(name_list,count_list,filename);

def main():
    
    repub_cand_list=['Rand+Paul',
                    'Sarah+Palin',
                    'Bobby+Jindal',
                    'Chris+Christie',
                    'Ted+Cruz',
                    'Marco+Rubio',
                    'Rick+Perry',
                    'Jeb+Bush',
                    'Paul+Ryan',
                    'Scott+Walker',
                    'Condoleezza+Rice',
                    'Kelly+Ayotte',
                    'Mike+Huckabee',
                    'John+Kasich',
                    'Rick+Santorum',
                    'Peter+King',
                    'Jon+Huntsman',
                    'Mike+Pence',
                    'Scott+Brown',
                    'Mitch+Daniels'];
                    
    dem_cand_list=['Hillary+Clinton',
                    'Elizabeth+Warren',
                    'Andrew+Cuomo',
                    'Joe+Biden',
                    'Howard+Dean',
                    'Martin+O\'Malley',
                    'Joe+Manchin',
                    'Amy+Klobuchar',
                    'Kathleen+Sebelius',
                    'Bernie+Sanders'];
                    
    
    #party_pol_coverage(dem_cand_list,'dem_freq14.txt');
    party_pol_coverage(repub_cand_list,'rep_freq14.txt');
    
    
    

if __name__ == "__main__":
    main()        