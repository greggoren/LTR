from seo import exponential_budget_cost_creator as e
from seo import letor_fold_creator as lfc
from seo import query_to_fold as qtf
from model_running import cross_validator as cv
from seo import optimized_data_set_creator as odsc
import sys
if __name__ == "__main__":
    data_set_location = sys.argv[0]
    final_path = sys.argv[1]
    qrel_path = sys.argv[2]
    g = e.exponential_budget_cost_creator()
    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()
    l = lfc.letor_folds_creator(data_set_location,data_set_location,q,True)
    o = odsc.files_rewriter()
    c = cv.cross_validator(5,"",l,"LTOR")
    c.k_fold_cross_validation("SVM",qrel_path)
    document_features = g.index_all_features_from_data_set(l.features_path)
    model_for_query = g.get_chosen_model_for_queries(c.models_path,c.chosen_models,q.query_to_fold_index)
    queries_budget, competitors, cost_index,first_competitor_features_per_query = g.create_budget_and_costs_for_data(c.final_score_path+"/final_score_combined.txt",10,0.3,model_for_query,document_features)
    features_to_change = o.get_features_to_change(queries_budget,competitors,cost_index)

    o.rewrite_optimized_data_set(final_path,features_to_change,l.features_path,first_competitor_features_per_query,competitors)
    #ll = lfc.letor_folds_creator(final_path,final_path,True)
    #nc = cv.cross_validator(5,"",ll,"LTOR_OPT")
    #nc.k_fold_cross_validation("SVM","")


