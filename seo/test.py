from seo import exponential_budget_cost_creator as e
from seo import knapsack_Algorithm as ka
from seo import letor_fold_creator as lfc
from seo import query_to_fold as qtf
import os
from model_running import folds_creator as fc
if __name__=="__main__":
    """g = e.exponential_budget_cost_creator()
    query_per_fold_index ={}

    for i in range(1,6):
        fold = "fold"+str(i)
        query_per_fold_index[fold] = []
        for index in range(1,41):
            query_per_fold_index[fold].append(index)
    chosen_models = {}
    chosen_models['fold1'] = 'svm_model0.1.txt'
    chosen_models['fold2'] = 'svm_model0.1.txt'
    chosen_models['fold3'] = 'svm_model0.1.txt'
    chosen_models['fold4'] = 'svm_model0.1.txt'
    chosen_models['fold5'] = 'svm_model0.1.txt'
    models_path = "C:/study/knapsack_debug"

    qs = g.get_chosen_model_for_queries(models_path,chosen_models,query_per_fold_index)
    features = g.index_all_features_from_data_set("C:/study/knapsack_debug/normalized_features")
    queries_budget, competitors, cost_index = g.create_budget_and_costs_for_data("C:/study/knapsack_debug/svm_model0.01.txt",10,0.3,qs,features)
    for query in queries_budget:
        budget = queries_budget[query]
        for competitor in competitors[query]:
            items=[]
            try:
                items = cost_index[query][competitor]
            except:
                continue
            a=ka.knapsack(items,budget)
            print(a.pack())"""
    q = qtf.qtf("C:/study/letor")
    f = lfc.letor_folds_creator("C:/study/letor","C:/study/letor_fixed1",q)
    f.normalize_and_write_files()

