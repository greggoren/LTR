from abc import ABC, abstractmethod
from scipy import spatial as sp
import os
class generic_budget_cost_creator(ABC):

    @abstractmethod
    def activation_func(self,input):
        pass

    def index_all_features_from_data_set(self,features_path):#TODO: add functionality in model run and connect with this pacakge.
        document_feature_index = {}
        for dirs in os.walk(features_path):
            if dirs[1]:
                first_directory = dirs[0]+"/"+dirs[1][0]
                for files in os.walk(first_directory):
                    for file_name in files[2]:
                        current_file = files[0]+"/"+file_name
                        with open(current_file) as features:
                            for feature in features:
                                feature_data = feature.split()
                                qid = int(feature_data[1].split(":")[1])
                                if not document_feature_index.get(qid,False):
                                    document_feature_index[qid]={}
                                features_length = len(feature_data)

                                document_id = feature_data[features_length-1]

                                document_feature_index[qid][document_id] = []
                                for index in range(2,features_length-2):
                                    data = feature_data[index]
                                    document_feature_index[qid][document_id].append(float(data.split(":")[1]))
                return document_feature_index



    def get_chosen_model_for_queries(self,models_path,chosen_models,query_per_fold_index):
        models_weight_index = {}
        model_wheights_per_fold = {}
        for fold in chosen_models:
            chosen_model_file = models_path + "/" + fold + "/" + chosen_models[fold]
            model_wheights_per_fold[fold] = []
            with open(chosen_model_file) as model_file:
                for line in model_file:
                    if line.__contains__(":"):
                        wheights = line.split()
                        wheights_length = len(wheights)
                        for index in range(1, wheights_length-1):
                            feature_id = int(wheights[index].split(":")[0])
                            if index < feature_id:
                                for repair in range(index,feature_id):
                                    model_wheights_per_fold[fold].append(-float("inf"))
                            model_wheights_per_fold[fold].append(float(wheights[index].split(":")[1]))
            for query in query_per_fold_index[fold]:
                models_weight_index[query]= model_wheights_per_fold[fold]
        return models_weight_index

    def create_budget(self,query_number,queries_budget,competitors,document_features,number_of_competitors,fraction):
        budget = 0.0
        try:
            first_competitor_features = document_features[query_number][competitors[query_number][0]]
            last_competitor_features = document_features[query_number][
                competitors[query_number][number_of_competitors - 1]]
        except:
            return
        for index in range(0, len(first_competitor_features)):
            delta = abs(first_competitor_features[index] - last_competitor_features[index])
            budget += self.activation_func(delta)
        queries_budget[query_number] = fraction * budget

    def get_diameter_documents(self,query_number,document_features):
        candidate_one = ""
        candidate_two = ""
        max_distance = 0.0
        for document_one in document_features[query_number]:
            for document_two in document_features[query_number]:
                distance = sp.distance.cosine(document_features[query_number][document_one],document_features[query_number][document_two])
                if distance > max_distance:
                    max_distance = distance
                    candidate_one = document_one
                    candidate_two = document_two
        return candidate_one,candidate_two


    def create_budget_and_costs_for_data(self, score_file, number_of_competitors, fraction, model_for_query, document_features):#TODO: remove exceptions
        queries_finished = {}
        queries_budget = {}
        competitors = {}
        cost_index = {}
        queries_started = {}
        first_competitor_features_per_query = {}
        with open(score_file) as scores_data:
            for score_record in scores_data:
                data = score_record.split()
                query_number = int(data[0])
                document = data[2]
                if not queries_started.get(query_number,False):
                    queries_started[query_number] = True
                if not queries_finished.get(query_number,False):
                    if not competitors.get(query_number,False):
                        competitors[query_number] = []

                    if len(competitors[query_number]) >= number_of_competitors:
                        self.create_budget(query_number,queries_budget,competitors,document_features,number_of_competitors,fraction)
                        queries_finished[query_number] = True
                        """budget = 0.0
                        queries_finished[query_number] = True
                        try:
                            first_competitor_features = document_features[query_number][competitors[query_number][0]]
                            last_competitor_features = document_features[query_number][competitors[query_number][number_of_competitors-1]]
                        except:
                            continue
                        for index in range(0,len(first_competitor_features)):
                            cost = abs(first_competitor_features[index] - last_competitor_features[index])
                            budget += self.activation_func(cost)
                        queries_budget[query_number] = fraction*budget"""
                    else:
                        competitors[query_number].append(document)
            set_of_queries_started = set(queries_started.keys())
            set_of_queries_finished = set(queries_finished.keys())
            unfinished_queries = set_of_queries_started.difference(set_of_queries_finished)
            for query in unfinished_queries:
                self.create_budget(query_number, queries_budget, competitors, document_features, len(competitors[query]),
                                   fraction)
        for query in competitors:
            cost_index[query] = {}
            try:
                first_competitor_features = document_features[query][competitors[query][0]]
                first_competitor_features_per_query[query] = first_competitor_features
            except:
                continue
            for competitor in competitors[query]:
                try:
                    competitor_features = document_features[query][competitor]
                except:
                    continue
                features_value_and_weight = []
                for index in range(0, len(first_competitor_features)):
                    cost = self.activation_func(first_competitor_features[index] - competitor_features[index])
                    value = model_for_query[query][index]
                    value_for_money = value/cost
                    if value_for_money > 0 and value > -float("inf"):
                        features_value_and_weight.append((str(index),cost,value))

                cost_index[query][competitor]=features_value_and_weight

        return queries_budget, competitors,cost_index
