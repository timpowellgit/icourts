import os
import re
import MySQLdb
import getpass

ECHR_QUERY = "SELECT date FROM case_doc WHERE doc_id =%s "
ECJ_QUERY = "SELECT date FROM cases WHERE celex = %s "

class MySentences(object):
     def __init__(self, dirname, yearmin = 1950, yearmax = 2016, court = "ECJ"):
         self.dirname = dirname
         self.yearmax = yearmax
         self.yearmin = yearmin
         self.court = court
         #p = getpass.getpass()
         self._connection = MySQLdb.connect(host="127.0.0.1",user="tfv338", passwd="Rectass30",db="%s" %("ecj_copy" if court =="ECJ" else "echr_copy"),port=3306, charset='utf8', use_unicode=True)
         # self._sentences = []
         self._q_string = ECJ_QUERY if court == "ECJ" else ECHR_QUERY


     def __iter__(self):
        sentences = self._construct_sentences()
        for sentence in sentences:
          yield sentence


     def _get_celex(self):
        pass
     def _construct_sentences(self):
        with self._connection:
          print self.court
          cur = self._connection.cursor()

          for dir, subdirs, fnames in os.walk(self.dirname):
              for fname in fnames:
                  if 'HTML' in fname or 'html' in fname:
                    if self.court == "ECJ":
                      celex = fname.split('_')[0]
                      if "(" in celex:
                        celex = celex.split('(')[0]

                         
                      cur.execute("SELECT date FROM case_doc WHERE celex = %s ", (celex,))
                    elif self.court == "ECHR":
                      docid= fname.split('.')[0]
                      cur.execute("SELECT date FROM case_doc WHERE doc_id = %s ", (docid,))
                    try:
                      date = cur.fetchall()[0][0]
                      if date.year <= self.yearmax and date.year > self.yearmin:
                        for line in open(os.path.join(dir, fname)):
                            line = re.sub(r'\W',' ',line)
                              
                            line = line.lower().split()
                              # print os.path.join(dir, fname)
                            if len(line) >= 3:

                                  # self._sentences.append(line)
                              yield line
                    except IndexError:
                        # There are some inconsistencies in the database and therefore 
                        # we cannot fully handle this error that is caused by not being able to
                        # find the celex number
                        continue
                    except AttributeError:
                       #Some entries have no date
                      continue

class Get_all_sentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):

        for dir, subdirs,fnames in os.walk(self.dirname):
            for fname in fnames: 
                if 'HTML' in fname: 
                    for line in open(os.path.join(dir, fname)):
                        line = re.sub(r'\W',' ',line) 
                        line = line.lower().split()
                        if len(line) >= 3:
                            yield line
        

class MyAnnotatedSentences(MySentences):
    def __init__(self, dirname, yearmin = 1950, yearmax = 2016, step = 3, cutoff=1989):
        super(MyAnnotatedSentences, self).__init__(dirname, yearmin, yearmax)
        self.cutoff = cutoff
        self.step= step
        # you can do other things here too
    # def _construct_sentences(self):
    #      years = range(self.yearmin, self.yearmax, self.step)
   

    #     with self._connection:
    #         cur = self._connection.cursor()
    #         for dir, subdirs, fnames in os.walk(self.dirname):
    #             for fname in fnames:
                    
    #                 if 'HTML' in fname:
    #                     celex = fname.split('_')[0]
    #                     cur.execute("SELECT date FROM cases WHERE celex = %s ", (celex,))
    #                     try:
    #                         date = cur.fetchall()[0][0]

    #                         if date.year > self.cutoff :

    #                             if date.year not in years:

    #                                 listed = years+[date.year]
    #                                 index =listed.index(date.year)
    #                                 year = listed[index-1]
    #                             else:
    #                                 year = date.year
    #                         else:
    #                             year = self.cutoff
    #                         for line in open(os.path.join(dir, fname)):
    #                             line = re.sub(r'\W',' ',line)
                                
    #                             line = line.lower()
    #                             line = re.sub(r'effectiveness ','effectiveness_%s ' %(year),line).split()
                                
                                
    #                             yield line
    #                     except:
    #                         pass
