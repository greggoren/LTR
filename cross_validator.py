
import folds_creator as fc

class cross_validator:
    def __init__(self,k,train_data,number_of_queries=-1,fold_prefix = "folds"):
        self.folds_creator = fc.folds_creator(k,train_data,number_of_queries,fold_prefix)
        self.fold_prefix = fold_prefix
        self.k = k


    def create_train_set_for_ltr(self,test,validation):
        folds = self.folds_creator.folds
        not_train = [test,validation]
        train_set =[]
        for fold in folds:
            if fold not in not_train:
                train_set.extend(folds[fold])
        file_for_ltr = open('train.txt', 'w')
        for train_data in train_set:
            file_for_ltr.write("%s\n" % train_data)
        file_for_ltr.close()



    def run_cross_validation(self):#TODO: create a dynamic environment for CV
        test_fold = self.k
        validation_fold = self.k-1

