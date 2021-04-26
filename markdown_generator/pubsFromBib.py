#!/usr/bin/env python
# coding: utf-8

# # Publications markdown generator for academicpages
# 
# Takes a set of bibtex of publications and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook ([see more info here](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html)). 
# 
# The core python code is also in `pubsFromBibs.py`. 
# Run either from the `markdown_generator` folder after replacing updating the publist dictionary with:
# * bib file names
# * specific venue keys based on your bib file preferences
# * any specific pre-text for specific files
# * Collection Name (future feature)
# 
# TODO: Make this work with other databases of citations, 
# TODO: Merge this with the existing TSV parsing solution


from pybtex.database.input import bibtex
import pybtex.database.input.bibtex 
import bibtexparser
from bibtexparser.latexenc import unicode_to_latex, latex_to_unicode, protect_uppercase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from time import strptime
import string
import html
import os
import re

#todo: incorporate different collection types rather than a catch all publications, requires other changes to template
publist = {
    "proceeding": {
        "file" : "pubs.bib",
        "venuekey": "booktitle",
        "venue-pretext": "In ",
        "collection" : {"name":"publications",
                        "permalink":"/publications/"}
        
    },
     "journal":{
        "file": "pubs.bib",
        "venuekey" : "journal",
        "venue-pretext" : "In ",
        "collection" : {"name":"publications",
                        "permalink":"/publications/"}
    },
    "misc":{
        "file": "pubs.bib",
        "venuekey" : "howpublished",
        "venue-pretext" : "",
        "collection" : {"name":"publications",
                        "permalink":"/publications/"}
    }, 
     "repport":{
        "file": "pubs.bib",
        "venuekey" : "institution",
        "venue-pretext" : "At ",
        "collection" : {"name":"publications",
                        "permalink":"/publications/"}
    },
    "thesis":{
        "file": "pubs.bib",
        "venuekey": "school",
        "venue-pretext" : "At ",
        "collection" : {"name":"publications",
                        "permalink":"/publications/"}
    }

}

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def delete_field(bibdb, idx, field):
    try:
        del bibdb.entries[idx][field]
    except KeyError:
        pass

def bibfile_latex_to_unicode(bibtex_fname):
    parser = BibTexParser(common_strings=True)
    with open(bibtex_fname) as bibtex_file:
        bibdb = bibtexparser.load(bibtex_file, parser=parser)
    for i, entry in enumerate(bibdb.entries):
        delete_field(bibdb, i, 'file')
        for field in entry.keys():
            bibdb.entries[i][field] = latex_to_unicode(entry[field])
    bibdb.comments = []
    writer = BibTexWriter()
    writer.display_order = ['title','year','author','journal','booktitle']
    clean_file = writer.write(bibdb)
    # Use for debug purposes:
    # with open('tmp.bib','w') as f:
    #     f.write(clean_file)
    return  clean_file



for pubsource in publist:
    filecontents = bibfile_latex_to_unicode(publist[pubsource]["file"])
    parser = bibtex.Parser()
    bibdata = parser.parse_string(filecontents)

    #loop through the individual references in a given bibtex file
    for bib_id in bibdata.entries:
        #reset default date
        pub_year = "1900"
        pub_month = "01"
        pub_day = "01"
        
        b = bibdata.entries[bib_id].fields    
            
        
        try:
            pub_year = f'{b["year"]}'

            #todo: this hack for month and day needs some cleanup
            if "month" in b.keys(): 
                if(len(b["month"])<3):
                    pub_month = "0"+b["month"]
                    pub_month = pub_month[-2:]
                elif(b["month"] not in range(12)):
                    tmnth = strptime(b["month"][:3],'%b').tm_mon   
                    pub_month = "{:02d}".format(tmnth) 
                else:
                    pub_month = str(b["month"])
            if "day" in b.keys(): 
                pub_day = str(b["day"])

                
            pub_date = pub_year+"-"+pub_month+"-"+pub_day
            
            #strip out {} as needed (some bibtex entries that maintain formatting)
            clean_title = b["title"].replace("{", "").replace("}","").replace("\\","").replace(" ","-")    

            url_slug = re.sub("\\[.*\\]|[^a-zA-Z0-9_-]", "", clean_title)
            url_slug = url_slug.replace("--","-")

            md_filename = (str(pub_date) + "-" + url_slug + ".md").replace("--","-")
            html_filename = (str(pub_date) + "-" + url_slug).replace("--","-")
            bib_filename = (str(pub_date) + "-" + url_slug + ".bib").replace("--","-")

            #Build Citation from text
            citation = ""

            #citation authors - todo - add highlighting for primary author?
            for author in bibdata.entries[bib_id].persons["author"]:
                citation = citation+" "+author.first_names[0]+" "+author.last_names[0]+", "

            #citation title
            citation = citation + "\"" + html_escape(b["title"].replace("{", "").replace("}","").replace("\\","")) + ".\""

            #add venue logic depending on citation type
            venue = publist[pubsource]["venue-pretext"]+b[publist[pubsource]["venuekey"]].replace("{", "").replace("}","").replace("\\","")

            citation = citation + " " + html_escape(venue)
            citation = citation + ", " + pub_year + "."
            
            ## YAML variables
            md = "---\ntitle: \""   + html_escape(b["title"].replace("{", "").replace("}","").replace("\\","")) + '"\n'
            
            md += """collection: """ +  publist[pubsource]["collection"]["name"]

            md += """\npermalink: """ + publist[pubsource]["collection"]["permalink"]  + html_filename
            
            note = False
            if "note" in b.keys():
                if len(str(b["note"])) > 5:
                    md += "\nexcerpt: '" + html_escape(b["note"]) + "'"
                    note = True

            md += "\ndate: " + str(pub_date) 

            md += "\nvenue: '" + html_escape(venue) + "'"


            md += "\nvenuetype: '" + str(pubsource) + "'"
            
            url = False
            if "url" in b.keys():
                if len(str(b["url"])) > 5:
                    md += "\npaperurl: '" + b["url"] + "'"
                    url = True
            elif "doi" in b.keys():
                if len(str(b["url"])) > 5:
                    md += "\npaperurl: 'https://doi.org/" + b["doi"] + "'"
                    url = True

            slides = False
            if "slides" in b.keys():
                if len(str(b["slides"])) > 5:
                    md += "\nslides: '" + b["slides"] + "'"                    
                    slides = True
                    del bibdata.entries[bib_id].fields["slides"]

            poster = False
            if "poster" in b.keys():
                if len(str(b["poster"])) > 5:
                    md += "\nposter: '" + b["poster"] + "'"
                    poster = True
                    del bibdata.entries[bib_id].fields["poster"]


            code = False
            if "code" in b.keys():
                if len(str(b["code"])) > 5:
                    md += "\ncode: '" + b["code"] + "'"
                    code = True
                    del bibdata.entries[bib_id].fields["code"]


            video = False
            if "video" in b.keys():
                if len(str(b["video"])) > 5:
                    md += "\nvideo: '" + b["video"] + "'"
                    video = True
                    del bibdata.entries[bib_id].fields["video"]



            md += "\nexcerpt: ' '"

            md += "\ncitation: '" + html_escape(citation) + "'"

            md += "\n---"
            
            ## Markdown description for individual page
            if note:
                md += "\n" + html_escape(b["note"]) + "\n"
                del bibdata.entries[bib_id].fields["note"]

            # Moved this icon-link generation to template single.html and archive-single.html
            # if url:
            #     md += "\n[<span><i class=\"fas fa-fw fa-file-pdf\"></i></span> Paper](" + b["url"] + "){:target=\"_blank\"} " 
            # else:
            #     md += "\nUse [Google Scholar](https://scholar.google.com/scholar?q="+html.escape(clean_title.replace("-","+"))+"){:target=\"_blank\"} for full citation"
            
            # if slides:
            #     md += "\n[<span><i class=\"fas fa-fw fa-file-powerpoint\"></i></span> Slides](" + b["slides"] + "){:target=\"_blank\"}"
            # if poster:
            #     md += "\n[<span><i class=\"fas fa-fw fa-image\"></i></span> Poster](" + b["poster"] + "){:target=\"_blank\"}"
            # if video:
            #     md += "\n[<span><i class=\"fas fa-fw fa-video\"></i></span> Video](" + b["video"] + "){:target=\"_blank\"}"

            # if code:
            #     md += "\n[<span><i class=\"fas fa-fw fa-file-code\"></i></span> Code](" + b["code"] + "){:target=\"_blank\"}"


            md += "\n"

            md_filename = os.path.basename(md_filename)

            with open("../_publications/" + md_filename, 'w') as f:
                f.write(md)
            print(f'SUCESSFULLY PARSED {bib_id}: \"', b["title"][:60],"..."*(len(b['title'])>60),"\"")

            # Create individual bib file for entry to be downloaded
            entrybib = bibdata.entries[bib_id].to_string('bibtex')
            with open('../_publications/'+bib_filename, 'w') as f:
                f.write(entrybib)


        # field may not exist for a reference
        except KeyError as e:
            print(f'WARNING Missing Expected Field {e} from entry {bib_id}: \"', b["title"][:30],"..."*(len(b['title'])>30),"\"")
            continue
