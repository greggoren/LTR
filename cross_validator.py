
import folds_creator as fc
import os
import subprocess

class cross_validator:
    def __init__(self,k,train_data,number_of_queries=-1,fold_prefix = "folds"):
        self.folds_creator = fc.folds_creator(k,train_data,number_of_queries,fold_prefix)
        self.folds_creator.split_train_file_into_folds()
        self.fold_prefix = fold_prefix
        self.k = k


    def create_train_set_for_ltr(self,test,validation):
        folds = self.folds_creator.folds
        not_train = [test,validation]
        train_set =[]
        for fold in folds:
            if fold not in not_train:
                train_set.extend(folds[fold])
        path = os.path.dirname(__file__)+"\\"
        absolute_path = os.path._getfullpathname(path+ "train.txt")
        if os.path.isfile("/train.txt"):#TODO: make more genric
            os.remove(absolute_path)
        file_for_ltr = open('train.txt', 'w')
        for train_data in train_set:
            file_for_ltr.write("%s\n" % train_data)
        file_for_ltr.close()


    def create_validation_set_for_ltr(self, validation):

        validation_set = self.folds_creator.folds[validation]
        path = os.path.dirname(__file__) + "\\"
        absolute_path = os.path._getfullpathname(path+"validation.txt")
        if os.path.isfile(absolute_path):  # TODO: make more genric
            os.remove(absolute_path)
        file_for_ltr = open(absolute_path, 'w')
        for validation_data in validation_set:
            file_for_ltr.write("%s\n" % validation_data)
        file_for_ltr.close()

    def create_test_set_for_ltr(self, test):

        test_set = self.folds_creator.folds[test]
        path = os.path.dirname(__file__) + "\\"
        absolute_path = os.path._getfullpathname(path + "test.txt")
        if os.path.isfile(absolute_path):  # TODO: make more genric
            os.remove(absolute_path)
        file_for_ltr = open(absolute_path, 'w')
        for test_data in test_set:
            file_for_ltr.write("%s\n" % test_data)
        file_for_ltr.close()

    def run_command(self,command):
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')

    def run_cross_validation_with_lambda_mart(self, test_fold, validation_fold):#TODO: create a dynamic environment for CV
        #test_fold = self.k
        #validation_fold = self.k-1
        prefix = self.folds_creator.fold_prefix
        self.create_train_set_for_ltr(prefix+str(test_fold),prefix+str(validation_fold))
        self.create_validation_set_for_ltr(prefix+str(validation_fold))
        self.create_test_set_for_ltr(prefix+str(test_fold))
        #subprocess.call(['java','-jar','rlib.jar','-train train.txt','-test test.txt','-validate validation.txt','-ranker 6','-metric2t NDCG@10','-metric2T NDCG@10','myModel.txt'],shell=True)
        command = 'java -jar rlib.jar -train train.txt -test test.txt -validate validation.txt -ranker 6 -metric2t NDCG@10 -metric2T NDCG@10 -save myModel'+str(test_fold)+'.txt'
        for output_line in self.run_command(command):
            print(output_line)

    def k_fold_cross_validation(self):
        for phase in range(3,self.k+1):
            self.run_cross_validation_with_lambda_mart(phase, phase - 1)