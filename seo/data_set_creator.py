
import sys
from seo import letor_fold_creator as lfc
from model_running import cross_validator as cv
from seo import exponential_budget_cost_creator as e
if __name__ == "__main__":

    data_set_location = "C:/study/letor"
    new_data_set_location = "C:/study/letor_fixed1"
    l = lfc.letor_folds_creator(data_set_location,new_data_set_location,False)
    l.split_train_file_into_folds()


