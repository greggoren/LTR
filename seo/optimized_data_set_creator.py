from seo import knapsack_algorithm as ka
import os
class files_rewriter:

    def get_features_to_change(self,queries_budget,competitors,cost_index):
        features_to_change = {}
        for query in queries_budget:
            budget = queries_budget[query]
            for competitor in competitors[query]:
                items = []
                try:
                    items = cost_index[query][competitor]
                except:
                    continue
                packer = ka.knapsack(items, budget)
                features =[feature[0] for feature in packer.pack()]
                features_to_change[query]={}
                features_to_change[query][competitor] = features
        return features_to_change

    def rewrite_optimized_data_set(self,final_files_location,features_to_change,data_set_location,value_for_change_index,competitors):
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
                        destination_file.close()
