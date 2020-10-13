import unittest
from app import create_app
from flask import request, jsonify, Response
import errors
import json

DEFAULT_FILENAME = "wsj00a.dmrs"
DEFAULT_PATH = "test_data"

class TestAPI(unittest.TestCase):

   def setUp(self):
      test_app= create_app()
      test_app.testing = True
      self.app = test_app.test_client()

   def tearDown(self):
      self.app = None

   def upload_file(self,filename=DEFAULT_FILENAME):
      filename = "/".join([DEFAULT_PATH,filename])
      data = (open(filename, "rb"),filename)
      return self.app.post("load_graphs", 
      data={"graphs" : data}, 
      content_type="multipart/form-data")

   def post_graphs(self,filename=DEFAULT_FILENAME):
      response = self.upload_file(filename)
      return json.loads(response.get_data(as_text=True))

   def get_graph(self,graph_id):
      self.upload_file()
      response = self.app.get(f"graphs/{graph_id}")
      return json.loads(response.get_data(as_text=True))
   
class TestUpload(TestAPI):

   def test_count_empty(self):
      """ Attempting to count the amount of graphs uploaded with an empty file. """
      self.upload_file("empty.dmrs")
      result = self.app.get("graph_count").get_json()
      self.assertEqual(result["count"],0,msg="Expected 0 graphs to be present.")
   
   def test_count_1_valid(self):
      """ Attempting to count the amount of graphs uploaded with a file containing a single entry. """

      self.upload_file("test_one_entry.dmrs")
      result = self.app.get("graph_count").get_json()
      self.assertEqual(result["count"],1,msg="Expected 1 graph to be present.")

   def test_count_all_valid(self):
      """ Attempting to count the amount of graphs uploaded with a file containing 441 graphs. """
      self.upload_file("wsj00a.dmrs")
      result = self.app.get("graph_count").get_json()
      self.assertEqual(result["count"],441,msg="Expected 441 graphs to be present.")

   def test_upload_invalid_fileType(self):
      """ Attempting to upload an invalid filetype. """
      response_as_dict = self.post_graphs(filename="wsj00a.invalid")
      self.assertDictEqual(response_as_dict,errors.custom_errors["IncorrectFileType"])

   def test_upload_empty_file(self):
      """ Attempting to upload an empty file. """
      response_as_dict = self.post_graphs(filename="empty.dmrs")
      self.assertDictEqual(response_as_dict,errors.custom_errors["EmptyFileUploaded"])

   def test_upload_valid(self):
      """ Attempting to upload a valid file with no malformed graphs. """
      response_as_dict = self.post_graphs()
      self.assertEqual(response_as_dict["status"],200)

   def test_upload_malformed_data(self):
      """ Attempting to upload a valid filetype with malformed graphs (conflicting IDS or broken strucutre). """
      response_as_dict = self.post_graphs(filename="malformed.dmrs")
      self.assertEqual(len(response_as_dict["warnings"]),3)

class TestRead(TestAPI):

   def test_get_graph_valid(self):
      """Testing if a valid graph ID from the wsj00a.dmrs file successfully returns a graph. """
      response = self.get_graph(20004010)
      self.assertEqual(response["status"],200)

   def test_get_graph_not_found(self):
      """Testing if a non-existent graph ID results in an error of type 404. """
      response = self.get_graph(0)
      self.assertEqual(response["status"],404)

   def test_get_graph_error(self):
      """Testing if an invalid graph ID results in an error of type 400. """
      response = self.get_graph("This should fail.")
      self.assertEqual(response["status"],400)

   # Get back to this
   # def test_get_graph_error(self):
   #    """Testing if an invalid graph ID results in an internal server error. """
   #    response = self.get_graph("")
   #    self.assertEqual(response["status"],500)

   # Graph deletion!

class TestNodeNeighbours(TestAPI):

   def test_node_neighbour_graph_not_exist(self):
      """Attempts to get a node's neighbours in a graph that does not exist. """
      self.upload_file()
      response = self.app.get("display_node_neighbours/200_3")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

   def test_node_neighbour_node_not_exist(self):
      """Attempts to get a node's neighbours in a graph where the node does not exist. """
      self.upload_file()
      response = self.app.get("display_node_neighbours/20034007_5")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

   def test_node_neighbour_graph_and_node_not_exist(self):
      """Attempts to get a node's neighbours in a graph where the node does not exist. """
      self.upload_file()
      response = self.app.get("display_node_neighbours/3_8")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

   def test_node_neighbour_valid(self):
      """Attempts to get a node's neighbours in a graph where both the graph and neighbout exist. """
      self.upload_file()
      response = self.app.get("display_node_neighbours/20013011_2")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]["20013011"]
      expected = json.loads('{"edges":[{"src":2,"trg":0,"label":"ARG1/NEQ"},{"src":2,"trg":4,"label":"ARG2/NEQ"}],"a_nodes":{"0":{"label":"generic_entity","anchors":[0]}},"s_nodes":{"2":{"label":"_attract_v_1","anchors":[1]},"4":{"label":"_attention_n_to","anchors":[2]}},"tokens":{"0":{"form":"\u201cthat","lemma":"that"},"2":{"form":"attention","lemma":"attention"}},"tops":"2"}')
      self.assertEqual(response_as_dict["edges"],expected["edges"])
      self.assertEqual(response_as_dict["a_nodes"],expected["a_nodes"])
      self.assertEqual(response_as_dict["s_nodes"],expected["s_nodes"])
      self.assertEqual(response_as_dict["tokens"],expected["tokens"])


   def test_node_no_neighbours(self):
      """Testing if node with no neighbours is checked for adjacent nodes. """
      self.upload_file("properties.dmrs")
      response = self.app.get("display_node_neighbours/20013015_2")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]["20013015"]
      self.assertEqual(len(response_as_dict["s_nodes"]),1)
      self.assertEqual(response_as_dict["tops"],"2")
      self.assertCountEqual(response_as_dict["a_nodes"],{})
      self.assertCountEqual(response_as_dict["edges"],[])
      self.assertCountEqual(response_as_dict["tokens"],{})

class TestGraphComparison(TestAPI):

   def test_comparison_graph_not_exist(self):
      """
      Testing if no graphs are returned when trying to compare a valid graph ID with 
      a non-existent ID. 
      """
      self.upload_file()
      response = self.app.get("compare/20013011_2")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict['status'],404)

   def test_comparison_both_graphs_not_exist(self):
      """
      Testing if no graphs are returned when trying to compare 2 non-existent IDs. 
      """
      self.upload_file()
      response = self.app.get("compare/5_2")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict['status'],404)
   
   def test_comparison_diff_sentences(self):
      """
      Testing if error returned whe comparing 2 valid graphs of different
      sentences.
      """
      self.upload_file()
      response = self.app.get("compare/20013011_20013012")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict['status'],400)

   def test_comparison_valid_same(self):
      """
      Testing if no differences found when comparing the same graph with itself.
      """
      self.upload_file()
      response = self.app.get("compare/20013011_20013011")
      response_as_dict = json.loads(response.get_data(as_text=True))['output']
      self.assertDictEqual(response_as_dict['graph_1'],{"20013011" : {"edges":[],"nodes":[]}})
      self.assertDictEqual(response_as_dict['graph_2'],{"20013011" : {"edges":[],"nodes":[]}})

   def test_comparison_valid(self):
      """
      Testing for differences found when comparing 2 graphs of the same sentence. 
      All instances of NEQ were changed to EQ.
      """
      self.upload_file("duplicate.dmrs")
      response = self.app.get("compare/20010002_20010004")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      expected_resp = {'matching': {'edges': [{'src': 'neg', 'trg': 'loc_nonsp', 'label': 'ARG1/H'}, {'src': 'neg', 'trg': 'unknown', 'label': 'MOD/EQ'}, {'src': '_this_q_dem', 'trg': '_year_n_1', 'label': 'RSTR/H'}], 'nodes': ['_year_n_1', 'neg', '_this_q_dem', 'loc_nonsp', 'unknown']}, 'graph_1': {'20010002': {'edges': [{'src': 'loc_nonsp', 'trg': '_year_n_1', 'label': 'ARG2/NEQ'}, {'src': 'loc_nonsp', 'trg': 'unknown', 'label': 'ARG1/NEQ'}], 'nodes': []}}, 'graph_2': {'20010004': {'edges': [{'src': 'loc_nonsp', 'trg': '_year_n_1', 'label': 'ARG2/EQ'}, {'src': 'loc_nonsp', 'trg': 'unknown', 'label': 'ARG1/EQ'}], 'nodes': []}}} 
      self.assertCountEqual(response_as_dict['matching'],expected_resp['matching'])
      self.assertCountEqual(response_as_dict['graph_1'],expected_resp['graph_1'])
      self.assertCountEqual(response_as_dict['graph_2'],expected_resp['graph_2'])

class TestGraphNodes(TestAPI):

   def test_search_empty(self):
      """ 
      Testing node label search with no labels.
      """
      self.upload_file()
      response = self.app.post("node_search",data='{"labels" : []}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))

      self.assertEqual(response_as_dict["status"],400)

   def test_search_crash(self):
      """ 
      Testing node label search's ability to prevent a crash.
      """
      self.upload_file()
      response = self.app.post("node_search",data='{"labels" : "["fail"]"}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],400)

   def test_search_fail(self):
      """ 
      Testing node label search with a label that does not exist within the data.
      """
      self.upload_file()
      response = self.app.post("node_search",data='{"labels" : ["fail"]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)


   def test_search_fail_list(self):
      """ 
      Testing node label search's ability to prevent a crash.
      """
      self.upload_file()
      response = self.app.post("node_search",data='{"labels" : "[1,2,3]"}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

   def test_search_pass_single_some(self):
      """ 
      Testing node label search with a single label where some have label.
      """
      self.upload_file("label_test.dmrs")
      response = self.app.post("node_search",data='{"labels" :["udef_q"] }',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      graph_ids = set([20003013,20001002])
      self.assertEqual(response_as_dict["output"].keys() & graph_ids,set())
      
   def test_search_graph_ids(self):
      """ 
      Test if graphs that contain a specified label have had their IDs successfully
      returned in a list.
      """
      self.upload_file("label_test.dmrs")
      response = self.app.post("node_search",data='{"labels" :["udef_q"] }',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      graph_ids = set([20003013,20001002])
      self.assertEqual(set(response_as_dict["graph_ids"]),graph_ids)
         
   def test_search_pass_1(self):
      """ 
      Testing node label search where all graphs have label.
      """
      self.upload_file("label_test.dmrs")
      response = self.app.post("node_search",data='{"labels" :["proper_q"] }',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      graph_ids = set([20001001,20001002,20003001,20003002,20003003,20003004,20003005,20003008,20003009,20003010,20003011,20003012,20003013,20003007])
      self.assertEqual(response_as_dict["output"].keys() & graph_ids,set())

   def test_search_pass_2(self):
      """ 
      Testing node label search where some graphs have 1 or more labels.
      """
      self.upload_file("label_test.dmrs")
      response = self.app.post("node_search",data='{"labels" :["_inc_n_1","generic_entity"] }',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      graph_ids = set([20003013,20003003])
      self.assertEqual(response_as_dict["output"].keys() & graph_ids,set())

class TestGraphProperties(TestAPI):

   def test_connected_acyclic(self):
      """Testing if connected acyclic graph's properties are identified and returned. """
      self.upload_file("properties.dmrs")
      response = self.app.get("graph_properties/20013011")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertTrue(eval(response_as_dict["output"]["connected"]))
      self.assertTrue(eval(response_as_dict["output"]["acyclic"]))

   def test_connected_cyclic(self):
      """Testing if connected cyclic graph's properties are identified and returned. """
      self.upload_file("properties.dmrs")
      response = self.app.get("graph_properties/20013012")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertTrue(eval(response_as_dict["output"]["connected"]))
      self.assertFalse(eval(response_as_dict["output"]["acyclic"]))

   def test_disconnected_acyclic(self):
      """Testing if disconnected acyclic graph's properties are identified and returned. """
      self.upload_file("properties.dmrs")
      response = self.app.get("graph_properties/20013013")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertFalse(eval(response_as_dict["output"]["connected"]))
      self.assertTrue(eval(response_as_dict["output"]["acyclic"]))

   def test_disconnected_cyclic(self):
      """Testing if disconnected cyclic graph's properties are identified and returned. """
      self.upload_file("properties.dmrs")
      response = self.app.get("graph_properties/20013014")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertFalse(eval(response_as_dict["output"]["connected"]))
      self.assertFalse(eval(response_as_dict["output"]["acyclic"]))

   def test_longest_paths(self):
      """
      Testing if the longest paths of graph 20011002 are correctly found.
      """
      self.upload_file()
      response = self.app.get("graph_properties/20011002")
      response_as_dict = json.loads(response.get_data(as_text=True))

      longest_directed_paths = response_as_dict["output"]["longest_directed_path"]
      longest_undirected_paths = response_as_dict["output"]["longest_undirected_path"]
      longest_directed_expected =  ['[47, 30, 33, 32]', '[47, 30, 33, 46]'] 
      longest_undirected_expected = ['[0, 1, 13, 47, 30, 32, 33, 46, 40, 36, 38, 35, 34]', '[0, 1, 13, 47, 30, 32, 33, 46, 44, 43, 45, 41, 42]']

      self.assertCountEqual((list(longest_directed_paths.keys())),(longest_directed_expected))
      self.assertCountEqual((list(longest_undirected_paths.keys())),(longest_undirected_expected))

class TestPagination(TestAPI):

   def test_invalid_page_lower(self):
      """ 
      Testing page out of bounds error.
      """
      self.upload_file()
      response = self.app.get("get_graphs/0")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

   def test_invalid_page_upper(self):
      """ 
      Testing page out of bounds error.
      """
      self.upload_file()
      response = self.app.get("get_graphs/90")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

   def test_one_entry_dataset(self):
      """ 
      Testing how many graphs are returned when a dataset has a single graph.
      """
      self.upload_file("test_one_entry.dmrs")
      response = self.app.get("get_graphs/1")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["returned"],1)

   def test_graphs_per_page(self):
      """ 
      Testing random page (15) to check if predetermined number of 
      graphs per page were returned.
      """
      self.upload_file()
      response = self.app.get("get_graphs/15")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["returned"],5)

   def test_correct_graphs_returned(self):
      """ 
      Testing to see if correct graphs were returned in page 1 of
      default dataset.
      """
      self.upload_file()
      response = self.app.get("get_graphs/1")
      response_as_dict = json.loads(response.get_data(as_text=True))
      graph_ids_expected = [20001001,20001002,20003001,20003002,20003003]
      graph_ids_returned = [int(graph["id"]) for graph in response_as_dict["graphs"]]
      graph_ids_list_returned = response_as_dict["graph_ids"]
      self.assertCountEqual(graph_ids_expected,graph_ids_returned)
      self.assertCountEqual(graph_ids_expected,graph_ids_list_returned)

class TestGraphList(TestAPI):

   def test_graph_list_fail(self):
      """ 
      Testing page out of bounds error.
      """
      self.upload_file()
      response = self.app.get("get_graphs",data='{"graph_id_list" : [1,2,3]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)
   
   def test_graph_list_crash(self):
      """ 
      Testing page out of bounds error.
      """
      self.upload_file()
      response = self.app.get("get_graphs",data='{"graph_id_list" : "["1,"2",3]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],400)   

   def test_graph_list_pass(self):
      """ 
      Testing pass without failure.
      """
      self.upload_file()
      response = self.app.get("get_graphs",data='{"graph_id_list" : ["20003001","20003002","20003003"]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertCountEqual(response_as_dict["graph_ids"],['20003001','20003002','20003003'])

   def test_graph_list_pass_errors(self):
      """ 
      Testing getting list of errors for graph ids that do not return objects.
      """
      self.upload_file()
      response = self.app.get("get_graphs",data='{"graph_id_list" : ["20003001", "200030988", "20003003"]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertCountEqual(response_as_dict["graph_ids"],['20003001','20003003'])
      self.assertEqual(len(response_as_dict["error_logs"]),1)

class TestSubgraphSearch(TestAPI):
   
   def test_search_pass_one_match(self):
      """ 
      Testing a subgraph being searched for and succeeding with 1 match.
      """
      self.upload_file()
      response = self.app.post("search_subgraph",data='{ "links" : ["_account_v_for-Arg1/NEQ-_fund_n_1" , "_now_a_1-Arg1/EQ-_account_v_for" ,"_these_q_dem-RSTR/H-_fund_n_1"]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      self.assertCountEqual(response_as_dict["graph_ids"],[20034012])

   def test_search_pass_all(self):
      """ 
      Testing subgraph pattern to match all graphs and succeeding.
      """
      self.upload_file()
      response = self.app.post("search_subgraph",data='{"links" :["*-*/*-*"]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      self.assertEqual(len(response_as_dict["graph_ids"]),441)

   def test_search_wildcard_one_match(self):
      """ 
      Testing subgraph pattern to match all graphs and succeeding.
      """
      self.upload_file()
      response = self.app.post("search_subgraph",data='{ "links" : ["*-Arg1/*-*","_now_a_1-Arg1/EQ-_account_v_for","_these_q_dem-RSTR/H-_fund_n_1"]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      self.assertEqual(len(response_as_dict["graph_ids"]),1)

   def test_search_no_matches(self):
      """ 
      Testing a subgraph being searched for and succeeding.
      """
      self.upload_file()
      response = self.app.post("search_subgraph",data='{"links" : ["xxx-xxx/xxx-xxx"]}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

class TestSentenceSearch(TestAPI):

   def test_single_letter_match(self):
      """Test to successfully match a single letter."""
      self.upload_file()
      response = self.app.post("sentence",data='{ "sentence" : "t"}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      self.assertCountEqual(response_as_dict["graph_ids"],[20003020])

   def test_single_letter_no_match(self):
      """Test to fail to match a single letter."""
      self.upload_file()
      response = self.app.post("sentence",data='{ "sentence" : "x"}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

   def test_single_word_match(self):
      """Test to successfully match a single word."""
      self.upload_file()
      response = self.app.post("sentence",data='{ "sentence" : "concern"}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      self.assertCountEqual(response_as_dict["graph_ids"],[
            20020014,
            20023002,
            20030001,
            20034022,
            20037051
        ])

   def test_single_word_no_match(self):
      """Test to fail to match a single word."""
      self.upload_file()
      response = self.app.post("sentence",data='{ "sentence" : "black"}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

   def test_single_term_match(self):
      """Test to match a single 2 word term."""
      self.upload_file()
      response = self.app.post("sentence",data='{ "sentence" : "concern to"}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      self.assertCountEqual(response_as_dict["graph_ids"],[20020014])

   def test_to_match_sentence(self):
      """Test to succesfully match a full sentence."""
      self.upload_file()
      response = self.app.post("sentence",data='{ "sentence" : "Champagne and dessert followed."}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))["output"]
      self.assertCountEqual(response_as_dict["graph_ids"],[20010008])

   def test_to_fail_to_match_empty_sentence(self):
      """Test to fail to match a full sentence."""
      self.upload_file()
      response = self.app.post("sentence",data='{ "sentence" : ""}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)      

   def test_to_fail_due_to_length(self):
      """Test to fail to match a full sentence."""
      self.upload_file()
      example_string=" ".join([str(x) for x in range(1000)])
      response = self.app.post("sentence",data= f'{{ "sentence" :  "{example_string}" }}',content_type="application/json")
      response_as_dict = json.loads(response.get_data(as_text=True))
      self.assertEqual(response_as_dict["status"],404)

if __name__ == '__main__':
    unittest.main()