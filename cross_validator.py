
import folds_creator as fc
import os
import subprocess

class cross_validator:
    def __init__(self,k,train_data,number_of_queries=-1,fold_prefix = "folds"):
        self.folds_creator = fc.folds_creator(k,train_data,number_of_queries,fold_prefix)
        self.folds_creator.split_train_file_into_folds()
        self.fold_prefix = fold_prefix
        self.k =k
        self.number_of_trees_for_test = [500, 250]
        self.number_of_leaves_for_test = [5, 10]
        self.test_metric = ["NDCG@20", "P@10", "P@5", "MAP"]
        self.svm_c_params_to_test = [0.1, 0.01, 0.001]


    def create_train_set_for_ltr(self,test,validation):

        folds = self.folds_creator.folds
        not_train = [test,validation]
        train_set =[]
        for fold in folds:
            if fold not in not_train:
                train_set.extend(folds[fold])
        path = os.path.dirname(__file__)+"/"
        absolute_path = os.path.abspath(path+ "train.txt")
        if os.path.isfile("/train.txt"):
            os.remove(absolute_path)
        file_for_ltr = open('train.txt', 'w')
        for train_data in train_set:
            file_for_ltr.write("%s" % train_data)
        file_for_ltr.close()


    def create_validation_set_for_ltr(self, validation):

        validation_set = self.folds_creator.folds[validation]
        path = os.path.dirname(__file__) + "/"
        absolute_path = os.path.abspath(path+"validation.txt")
        if os.path.isfile(absolute_path):
            os.remove(absolute_path)
        file_for_ltr = open(absolute_path, 'w')
        for validation_data in validation_set:
            file_for_ltr.write("%s" % validation_data)
        file_for_ltr.close()

    def create_test_set_for_ltr(self, test):

        test_set = self.folds_creator.folds[test]
        path = os.path.dirname(__file__) + "/"
        absolute_path = os.path.abspath(path + "test.txt")
        if os.path.isfile(absolute_path):
            os.remove(absolute_path)
        file_for_ltr = open(absolute_path, 'w')
        for test_data in test_set:
            file_for_ltr.write("%s" % test_data)
        file_for_ltr.close()

    def run_command(self,command):
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True)
        return iter(p.stdout.readline, b'')

    def run_cross_validation_with_lambda_mart(self, test_fold, validation_fold,number_of_trees,number_of_leaves,metric):

        prefix = self.folds_creator.fold_prefix
        self.create_train_set_for_ltr(prefix+str(test_fold),prefix+str(validation_fold))
        self.create_validation_set_for_ltr(prefix+str(validation_fold))
        self.create_test_set_for_ltr(prefix+str(test_fold))
        command = 'java -jar ./RankLib-2.5.jar -train train.txt -test test.txt' \
                  ' -validate validation.txt -ranker 6 -qrels qrels.txt -metric2t '+metric + ' -metric2T '+metric+' ' \
                  '-tree '+str(number_of_trees) +' -leaf '+str(number_of_leaves)
        for output_line in self.run_command(command):
            print(output_line)
            if "on test data:" in str(output_line):
                score = str(output_line).split("on test data:")[1]
                return score

    def k_fold_cross_validation_lambdamart(self):
        results_file = open("results.txt",'w')
        results_file.write("#trees\t#leaves\tscore\tmetric\n")
        for metric in self.test_metric:
            for number_of_trees in self.number_of_trees_for_test:
                for number_of_leaves in self.number_of_leaves_for_test:
                    mean_score = 0
                    for phase in range(2,self.k+1):
                        score = self.run_cross_validation_with_lambda_mart(phase, phase - 1,number_of_trees,number_of_leaves,metric)
                        score = score.split('\\r\\n')[0]
                        mean_score += float(score)
                    mean_score += float(self.run_cross_validation_with_lambda_mart(1, 3,number_of_trees,number_of_leaves,metric).split('\\r\\n')[0])
                    mean_score = mean_score/self.k
                    results_file.write(str(number_of_trees)+"\t"+str(number_of_leaves)+"\t"+str(mean_score)+"\t"+metric+"\n")
        results_file.close()

    def k_fold_cross_validation_svm(self):
        for c_value in self.svm_c_params_to_test:
            for phase in range(1,self.k+1):
                self.run_cross_validation_with_svm(c_value)
        print("")


    def evaluate_svm(self,prediction_file):
        print()

    def run_cross_validation_with_svm(self,c_value):
        learning_command = "svm_rank_learn -c "+str(c_value)+" train.txt svm_model.txt"
        for output_line in self.run_command(learning_command):
            print(output_line)

        #TODO:handle what happens if no model file created

        test_command = "svm_rank_classify test.txt svm_model.txt predictions.txt"
        for output_line in self.run_command(test_command):
            print(output_line)

        #TODO:handle what happens if no predictions file created

        self.evaluate_svm("predictions.txt")
