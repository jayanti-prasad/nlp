import os
from argparse import Namespace


def get_params():
    cfg = Namespace (
       input_file='input_data/SICK_train.txt',
       output_dir="output",
       lib_dir="lib",
       stanford_basedir="/Users/jayanti/Software/nlp-tools/stanford/",
       parser="stanford-parser-full-2018-10-17/stanford-parser.jar",
       postagger="stanford-postagger-full-2018-10-16/stanford-postagger.jar",
       model="stanford-english-corenlp-2018-10-05-models.jar"
      )

    return cfg 


def split_text(cfg, filepath):
    with open(filepath) as datafile, \
        open(os.path.join(cfg.output_dir, 'a.txt'), 'w') as afile, \
        open(os.path.join(cfg.output_dir, 'b.txt'), 'w') as bfile,  \
        open(os.path.join(cfg.output_dir, 'id.txt'), 'w') as idfile, \
        open(os.path.join(cfg.output_dir, 'sim.txt'), 'w') as simfile:
        datafile.readline()
        for line in datafile:
            i, a, b, sim, ent = line.strip().split('\t')
            idfile.write(i + '\n')
            afile.write(a + '\n')
            bfile.write(b + '\n')
            simfile.write(sim + '\n')
    print("wrote split_text") 



class StanfordParser:
    def __init__(self, cfg):
 
       self.cfg = cfg 
       parser = cfg.stanford_basedir + os.sep + cfg.parser
       postagger = cfg.stanford_basedir + os.sep + cfg.postagger
       model = cfg.stanford_basedir + os.sep + cfg.model
       class_path=[cfg.lib_dir, parser, postagger, model] 
       self.class_path = ":".join(class_path) 

       if not os.path.exists(cfg.output_dir):
          os.makedirs(cfg.output_dir)

    
    def compile_src(self):

       if not os.path.exists(cfg.lib_dir):
          os.makedirs(cfg.lib_dir)

       if not os.path.exists(cfg.lib_dir + os.sep + "ConstituencyParse.class"):
           print("Compiling java source files !")
           cmd = ('javac -cp %s *.java -d %s' % (self.class_path, cfg.lib_dir))
           os.system(cmd)

       
    def dependency_parse(self, filepath, tokenize=True):
        print('\nDependency parsing ' + filepath)

        prefix = os.path.splitext(os.path.basename(filepath))[0]
     
        tokpath = os.path.join(self.cfg.output_dir, prefix + '.toks')
        parentpath = os.path.join(self.cfg.output_dir, prefix + '.parents')
        relpath = os.path.join(self.cfg.output_dir, prefix + '.rels')

        tokenize_flag = '-tokenize - ' if tokenize else ''
        cmd = ('java -cp %s DependencyParse -tokpath %s -parentpath %s -relpath %s %s < %s'
               % (self.class_path, tokpath, parentpath, relpath, tokenize_flag, filepath))
        os.system(cmd)
 
        print("dependency parsing done !")

    def constituency_parse(self, filepath, tokenize=True):

        prefix = os.path.splitext(os.path.basename(filepath))[0]
 
        tokpath = os.path.join(self.cfg.output_dir, prefix + '.toks')
        parentpath = os.path.join(self.cfg.output_dir, prefix + '.cparents')

        tokenize_flag = '-tokenize - ' if tokenize else ''
        cmd = ('java -cp %s ConstituencyParse -tokpath %s -parentpath %s %s < %s'
           % (self.class_path, tokpath, parentpath, tokenize_flag, filepath))
        os.system(cmd)

        print("constituency  parsing done !")

if __name__ == "__main__":

    cfg = get_params()


    S = StanfordParser(cfg)
   
    # create class files if not present 
    S.compile_src()

    # read input and create split text 
    split_text(cfg, cfg.input_file)

    # create dependency for the first & second sentence 
    S.dependency_parse(cfg.output_dir + os.sep + "a.txt")
    S.dependency_parse(cfg.output_dir + os.sep + "b.txt")

    # create constituency for the first & second sentence 
    S.constituency_parse(cfg.output_dir + os.sep + "a.txt")
    S.constituency_parse(cfg.output_dir + os.sep + "b.txt")


