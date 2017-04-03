from seo import exponential_budget_cost_creator as e

from seo import query_to_fold as qtf

from seo import competition_maker as cm

from seo import linear_budget_cost_creator as l
from seo import logarithmic_budget_cost_creator as lb
from multiprocessing import Pool as p
from functools import partial
import matplotlib.pyplot as plt
from seo import letor_fold_creator as lfc
from model_running import cross_validator as cv
from seo import competition_maker as odsc
import sys

if __name__=="__main__":
    data_set_location = sys.argv[1]
    print data_set_location
    new_data_set_location = sys.argv[2]

    qrel_path = sys.argv[3]


    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()
    l = lfc.letor_folds_creator(data_set_location,new_data_set_location,True)
    c = cv.cross_validator(5,l,"LTOR_MART")
    c.k_fold_cross_validation("LAMBDAMART",qrel_path)
