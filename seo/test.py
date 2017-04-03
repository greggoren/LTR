from seo import exponential_budget_cost_creator as e

from seo import query_to_fold as qtf

from seo import competition_maker as cm

from seo import linear_budget_cost_creator as l
from seo import logarithmic_budget_cost_creator as lb
from multiprocessing import Pool as p
from functools import partial
import matplotlib.pyplot as plt
def simulation(chosen_models,data_set_location,query_to_fold_index,score_file,budget_creator):

    c = cm.competition_maker(20, budget_creator,score_file, 10, data_set_location, 0.1, chosen_models, query_to_fold_index)
    return c.competition(budget_creator.model)


if __name__ == "__main__":

    data_set_location = "C:/study/letor_fixed"
    q = qtf.qtf(data_set_location)
    q.create_query_to_fold_index()

    score_file = "C:/study/simulation_data/test_scores_trec_format/SVM/final_score_combined.txt"


    cost_model = "log_0.1.jpg"
    pool = p(2)
    lg =lb.logarithmic_budget_cost_creator("log")#l.linear_budget_cost_creator(factor) #e.exponential_budget_cost_creator()##  # #
    e = e.exponential_budget_cost_creator("exp")
    li = l.linear_budget_cost_creator("linear")

    chosen_models = lg.recover_models_per_fold("C:/study/simulation_data/models/SVM",
                                              "C:/study/simulation_data/test_scores_trec_format/SVM/")
    f = partial(simulation,chosen_models,data_set_location,q.query_to_fold_index,score_file)

    g_input =[lg,e,li]
    #g_input = [li]
    results = pool.map(f,g_input)
    fig = plt.figure()
    fig.suptitle('Average Kendall-tau measure', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Kendal-tau')

    for result in results:

        key =result.keys()[0]
        print result
        kendal_stats = result[key]["kendall"]
        if key == "exp":
            ax.plot(kendal_stats[0],kendal_stats[1],'g')
        elif key == "log":
            ax.plot(kendal_stats[0], kendal_stats[1], 'r')
        else:
            ax.plot(kendal_stats[0], kendal_stats[1], 'b')
    plt.savefig("kendall_tau.jpg")
    plt.clf()
    fig = plt.figure()
    fig.suptitle('Average winner changing', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('winner changed')
    for result in results:

        key =result.keys()[0]

        winner_stats = result[key]["winner"]
        if key == "exp":
            ax.plot(winner_stats[0],winner_stats[1],'g')
        elif key == "log":
            ax.plot(winner_stats[0], winner_stats[1], 'r')
        else:
            ax.plot(winner_stats[0], winner_stats[1], 'b')

    plt.savefig("winner_swap.jpg")
    plt.clf()
    fig = plt.figure()
    fig.suptitle('Average cosine distance', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Cosine distance')
    for result in results:
        key =result.keys()[0]
        cos_stats = result[key]["cos"]
        if key == "exp":
            ax.plot(cos_stats[0],cos_stats[1],'g')
        elif key == "log":
            ax.plot(cos_stats[0], cos_stats[1], 'r')
        else:
            ax.plot(cos_stats[0], cos_stats[1], 'b')
    plt.savefig("cos_dist.jpg")
    plt.clf()

    fig = plt.figure()
    fig.suptitle('Average Kendall-tau with original rank', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Kendal tau')
    for result in results:

        key = result.keys()[0]
        orig_stats = result[key]["orig"]
        if key == "exp":
            ax.plot(orig_stats[0], orig_stats[1], 'g')
        elif key == "log":
            ax.plot(orig_stats[0], orig_stats[1], 'r')
        else:
            ax.plot(orig_stats[0], orig_stats[1], 'b')
    plt.savefig("orig_tau.jpg")
    plt.clf()

"""data_set_location = sys.argv[1]
    print data_set_location
    new_data_set_location = sys.argv[2]
    final_path = sys.argv[3]

    qrel_path = sys.argv[4]

    g = e.exponential_budget_cost_creator()

    q.create_query_to_fold_index()
    l = lfc.letor_folds_creator(data_set_location,new_data_set_location,True)
    o = odsc.competition_maker()
    c = cv.cross_validator(5,l,"LTOR")
    c.k_fold_cross_validation("SVM",qrel_path)
    document_features = g.index_all_features_from_data_set(l.features_path)
    model_for_query = g.get_chosen_model_for_queries(c.models_path,c.chosen_models,q.query_to_fold_index)
    queries_budget, competitors, cost_index,first_competitor_features_per_query = g.create_budget_and_costs_for_data(c.final_score_path+"/final_score_combined.txt",10,0.3,model_for_query,document_features)
    features_to_change = o.get_features_to_change(queries_budget,competitors,cost_index)

    o.rewrite_optimized_data_set(final_path,features_to_change,l.features_path,first_competitor_features_per_query,competitors)
    #ll = lfc.letor_folds_creator(final_path,final_path,True)
    #nc = cv.cross_validator(5,"",ll,"LTOR_OPT")
    #nc.k_fold_cross_validation("SVM","")"""