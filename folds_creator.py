import math
import os
class folds_creator:
    def __init__(self,k,train_file, number_of_queries=-1,fold_prefix="fold"):
        self.k = k
        self.train_file = train_file
        self.number_of_queries = number_of_queries
        self.fold_prefix = fold_prefix
        self.folds = {}


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

        path = os.path.dirname(__file__)+"\\"
        print(path)
        absolute_path = os.path._getfullpathname(path+self.train_file)
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


    def split_train_file_into_folds(self):
        number_of_queries_in_file = math.floor(self.number_of_queries/self.k) #in python 3 it is a float
        query_to_fold = self.init_files(number_of_queries_in_file)
        self.folds = self.go_over_train_file_and_split_to_folds(query_to_fold)
