import os
class evaluator:
    def __init__(self):
        self.query_doc_index={}


    def prepare_index_of_test_file(self,test_file):
        with open(test_file) as test_data:

            row_number = 0
            for data_record in test_data:
                query_id = data_record.split(" ")[1].split(":")[1]
                document_name = data_record.split("#")[1].rstrip()
                print (document_name)
                if not self.query_doc_index.get(row_number,False):
                    self.query_doc_index[row_number]={}
                    self.query_doc_index[row_number][query_id]=document_name
                row_number += 1

    def create_file_in_trec_eval_format(self,scores_file,final_scores_directory):
        scores_file_name = os.path.basename(scores_file)
        trec_eval_formatted_file = open(final_scores_directory+"/"+scores_file_name,'w')
        with open(scores_file) as scores_data:
            row_number = 0
            for score_record in scores_data:
                score = score_record.rstrip()
                query_id = self.query_doc_index[row_number].keys()[0]
                document_name = self.query_doc_index[row_number][query_id]

                trec_eval_formatted_file.write(query_id+"\tQ0\t"+document_name+"\t"+str(row_number)+"\t"+str(score)+"\tindri\n")
                row_number += 1
            trec_eval_formatted_file.close()