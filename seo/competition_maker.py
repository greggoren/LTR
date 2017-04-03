from seo import knapsack_algorithm as ka
from copy import deepcopy
from scipy.stats import kendalltau as kt
from seo import generic_budget_cost_creator as gbcc
import math
import matplotlib.pyplot as plt
class competition_maker:

    def __init__(self,num_of_iterations,budget_creator,score_file,number_of_competitors,data_set_location,fraction,chosen_models,query_per_fold):
        self.num_of_iterations = num_of_iterations
        self.budget_creator = budget_creator
        self.score_file = score_file
        self.number_of_competitors = number_of_competitors
        self.data_set_location = data_set_location
        self.fraction = fraction
        self.chosen_models = chosen_models
        self.query_per_fold = query_per_fold

    def get_features_to_change(self,queries_budget,competitors,cost_index):
        features_to_change = {}
        for query in queries_budget:
            budget = queries_budget[query]
            features_to_change[query] = {}
            for competitor in competitors[query]:
                items = cost_index[query][competitor]
                packer = ka.knapsack(items, budget)
                features =[feature[0] for feature in packer.pack()]
                features_to_change[query][competitor] = features
        return features_to_change


    def update_competitors(self,features_to_change,competitors_features,value_for_change):
        for query in competitors_features:
            for doc in competitors_features[query]:
                features = competitors_features[query][doc]
                length = len(features)
                for index in range(length):
                    if features_to_change.get(query, False):
                        if index in features_to_change[query][doc]:

                            competitors_features[query][doc][index]=value_for_change[query][index]
        return competitors_features

    def competition(self,cost_model):
        results = {}
        query_tagged ={}
        competitors = self.budget_creator.get_competitors_for_query(self.score_file, self.number_of_competitors)
        reference_of_indexes = deepcopy(competitors)
        document_feature_index = self.budget_creator.index_features_for_competitors(competitors,self.data_set_location,True)
        model_weights_per_fold_index = self.budget_creator.get_chosen_model_weights_for_fold(self.chosen_models)
        x_axis =[]
        y_axis = []
        changed_winner_averages =[]
        average_distances = []
        original_reference = []
        budget_per_query, average_distance = self.budget_creator.create_budget_per_query(self.fraction,
                                                                                         document_feature_index)
        for iteration in range(0,self.num_of_iterations):
            print "iteration number ",iteration+1
            sum_of_kendalltau = 0
            dummy_var ,average_distance = self.budget_creator.create_budget_per_query(self.fraction,document_feature_index)
            cost_index,value_for_change = self.budget_creator.create_items_for_knapsack(competitors, document_feature_index,model_weights_per_fold_index,self.query_per_fold)
            features_to_change = self.get_features_to_change(budget_per_query,competitors,cost_index)
            document_feature_index = self.update_competitors(features_to_change,deepcopy(document_feature_index),value_for_change)
            competitors_new,query_tagged = self.get_new_rankings(document_feature_index,model_weights_per_fold_index,self.query_per_fold,budget_per_query,deepcopy(competitors),deepcopy(query_tagged))
            number_of_time_winner_changed = 0
            denominator = 0
            sum_of_original_kt=0
            for query in competitors_new:
                old_rank = self.transition_to_rank_vector(query,reference_of_indexes,competitors[query])
                new_rank = self.transition_to_rank_vector(query,reference_of_indexes,competitors_new[query])
                orig_rank = self.transition_to_rank_vector(query,reference_of_indexes,reference_of_indexes[query])

                kendall_tau,p_value = kt(old_rank,new_rank)
                if query == 29977:
                    print "budget ",budget_per_query[query]
                    print "old ", old_rank
                    print "new ", new_rank
                if not math.isnan(kendall_tau):
                    sum_of_kendalltau+=kendall_tau
                    denominator += 1
                    if old_rank.index(1) != new_rank.index(1):
                        number_of_time_winner_changed += 1
                        """if iteration+1 >= 18:
                            print "query ",query
                            print "budget  ",budget_per_query[query]
                            print "old ", old_rank
                            print "new ", new_rank"""
                original_kt,p_val = kt(new_rank,orig_rank)
                if not math.isnan(original_kt):
                    sum_of_original_kt += original_kt
            print "number of times winner changed ",number_of_time_winner_changed

            average = sum_of_kendalltau/denominator
            average_distances.append(average_distance)
            changed_winner_averages.append(float(number_of_time_winner_changed)/denominator)
            x_axis.append(iteration+1)
            y_axis.append(average)
            original_reference.append(float(sum_of_original_kt)/denominator)
            competitors = deepcopy(competitors_new)

        results["kendall"]=(x_axis,y_axis)
        results["cos"] = (x_axis,average_distances)
        results["winner"] = (x_axis,changed_winner_averages)
        results["orig"] =(x_axis,original_reference)
        meta_results = {}
        meta_results[self.budget_creator.model] = results
        return meta_results


    def get_new_rankings(self,document_features,model_weights,query_per_fold,budget_per_query,competitors,query_tagged):
        new_competitors={}
        for query in document_features:
            if budget_per_query[query]>0:
                doc_scores={}
                weights = model_weights[query_per_fold[query]]
                for doc in document_features[query]:
                    doc_features = document_features[query][doc]
                    score = self.dot_product(doc_features,weights)
                    doc_scores[doc]=score
                sorted_ranking = sorted(doc_scores,key=doc_scores.__getitem__,reverse=True)
                if query == 29977:
                    print doc_scores
                length_of_rankings = len(sorted_ranking)
                if doc_scores[sorted_ranking[0]]==doc_scores[sorted_ranking[length_of_rankings-1]]:
                    if not query_tagged.get(query,False):
                        query_tagged[query]=(doc_scores[sorted_ranking[0]],doc_scores[sorted_ranking[length_of_rankings-1]])
                    elif query_tagged[query][0]==doc_scores[sorted_ranking[0]] and query_tagged[query][0]==doc_scores[sorted_ranking[length_of_rankings-1]]:
                        new_competitors[query]=competitors[query]
                        continue
                    else:
                        query_tagged.pop(query,None)
                elif doc_scores[sorted_ranking[0]]==doc_scores[sorted_ranking[1]]:
                    if not query_tagged.get(query,False):
                        query_tagged[query] = (doc_scores[sorted_ranking[0]],doc_scores[sorted_ranking[length_of_rankings-1]])
                    elif query_tagged[query][0]==doc_scores[sorted_ranking[0]] and query_tagged[query][1]==doc_scores[sorted_ranking[length_of_rankings-1]]:
                        new_competitors[query] = competitors[query]
                        continue
                    else:
                        query_tagged.pop(query, None)
                new_competitors[query] = sorted_ranking
            else:
                new_competitors[query]=competitors[query]
        return new_competitors,query_tagged



    def dot_product(self,list1,list2):
        return sum([i*j for (i, j) in zip(list1, list2)])

    def transition_to_rank_vector(self,query,reference_of_indexes,list_of_docs):
        original_list = reference_of_indexes[query]
        rank_vector = []
        for doc in original_list:
            rank_vector.append(list_of_docs.index(doc)+1)
        return rank_vector


    """def rewrite_optimized_data_set(self,final_files_location,features_to_change,data_set_location,value_for_change_index,competitors):
        for fold in os.walk(data_set_location):
            if not fold[1]:
                fold_number = os.path.basename(fold[0])
                for file in os.walk(fold[2]):
                    file_name = fold[0]+"/"+file
                    destination_file = open(final_files_location+"/"+fold_number+"/"+file)
                    with open(file_name) as data_set:
                        for data_record in data_set:
                            split_record = data_record.split()
                            qid = int(split_record[1].split(":")[1])
                            record_length = len(split_record)
                            doc_id = split_record[record_length-1]
                            new_record = split_record[0]+" "+split_record[1]+" "
                            if doc_id in competitors[qid]:
                                for feature_index in range(2,record_length-2):
                                    if str(feature_index) in features_to_change[qid][doc_id]:
                                        new_record += str(feature_index)+":"+value_for_change_index[qid][doc_id][feature_index]+" "
                                    else:
                                        new_record+= split_record[feature_index]+" "

                                new_record+=split_record[record_length-2]+" "+split_record[record_length-1]+"\n"
                                destination_file.write(new_record)
                            else:
                                destination_file.write(data_record)
                        destination_file.close()"""
