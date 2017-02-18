import math
import os
import time
class folds_creator:
    def __init__(self,k,train_file, number_of_queries=-1,fold_prefix="fold"):
        self.k = k
        self.train_file = train_file
        self.number_of_queries = number_of_queries
        self.fold_prefix = fold_prefix
        self.folds = {}
        self.working_path = ""


    def init_files(self, number_of_queries_in_fold):
        query_to_fold = {}
        fold_number = 1
        current_number_of_queries = 0
        for query_number in range(1,self.number_of_queries+1):

            if current_number_of_queries >= number_of_queries_in_fold:
                fold_number += 1
                current_number_of_queries=0

            query_to_fold[query_number] = self.fold_prefix + str(fold_number)
            current_number_of_queries += 1

        return query_to_fold


    def go_over_train_file_and_split_to_folds(self, query_to_fold):

        path = os.path.dirname(__file__)+"/"
        print(path)
        absolute_path = os.path.abspath(path+self.train_file)
        folds = {}
        with open(absolute_path) as train_set:
            for doc in train_set:
                features = doc.split(" ")
                query_number = features[1].split(":")[1]
                query_number = int(query_number)
                fold_name = query_to_fold[query_number]
                if not folds.get(fold_name,False):
                    folds[fold_name] =[]
                folds[fold_name].append(doc)

        return folds

    def create_folds_splited_into_folders(self):
        print("starting working set creation")
        path = os.path.dirname(__file__)
        parent_path = os.path.abspath(os.path.join(path, os.pardir))
        if not os.path.exists(parent_path + "/working_sets"):
            os.makedirs(parent_path + "/working_sets")
        self.working_path = working_path = parent_path+"/working_sets"+time.time()+"/"

        for fold in range(2,self.k+1):
            self.create_files_in_working_folder(fold,fold-1,working_path)
        self.create_files_in_working_folder(1,self.k,working_path)
        print("working set creation is done")


    def create_files_in_working_folder(self,test_fold,validation_fold,path):
        if not os.path.exists(path+"fold"+str(test_fold)):
            os.makedirs(path+"fold"+str(test_fold))
        print("creating fold"+str(test_fold))
        not_train = [self.fold_prefix+str(test_fold),self.fold_prefix+str(validation_fold)]
        train_set = []
        for fold in self.folds:
            if fold not in not_train:
                print(fold)
                train_set.extend(self.folds[fold])

        train_path = os.path.abspath(path+"fold"+str(test_fold)+"/"+ "train.txt")
        train_for_ltr = open(train_path, 'w')
        for train_data in train_set:
            train_for_ltr.write("%s" % train_data)
        train_for_ltr.close()
        print("finished train.txt")
        validation_path = os.path.abspath(path+"fold"+str(test_fold)+"/"+ "validation.txt")
        validation_file = open(validation_path,'w')
        validation_set = self.folds[self.fold_prefix+str(validation_fold)]
        for validation_data in validation_set:
            validation_file.write("%s" % validation_data)
        validation_file.close()
        print("finished validation.txt")
        test_path = os.path.abspath(path+"fold"+str(test_fold)+"/"+ "test.txt")
        test_file = open(test_path,'w')
        test_set = self.folds[self.fold_prefix+str(test_fold)]
        for test_data in test_set:
            test_file.write(test_data)
        test_file.close()
        print("finished test.txt")




    def split_train_file_into_folds(self):
        number_of_queries_in_file = math.floor(float(float(self.number_of_queries)/self.k))
        query_to_fold = self.init_files(number_of_queries_in_file)
        self.folds = self.go_over_train_file_and_split_to_folds(query_to_fold)
        self.create_folds_splited_into_folders()