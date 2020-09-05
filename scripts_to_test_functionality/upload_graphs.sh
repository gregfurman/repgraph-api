curl http://localhost:8000/load_graphs -H "Content-Type: application/json" -d '[
   {
      "id": "1",
      "source": "acyclic+connected",
      "input": "These funds now account for several billions of dollars in assets.",
      "tokens": [
         {
            "index": 0,
            "form": "these",
            "lemma": "these"
         },
         {
            "index": 1,
            "form": "funds",
            "lemma": "fund"
         },
         {
            "index": 2,
            "form": "now",
            "lemma": "now"
         },
         {
            "index": 3,
            "form": "account",
            "lemma": "account"
         },
         {
            "index": 4,
            "form": "for",
            "lemma": "for"
         },
         {
            "index": 5,
            "form": "several",
            "lemma": "several"
         },
         {
            "index": 6,
            "form": "billions",
            "lemma": "1000000000",
            "carg": "1000000000"
         },
         {
            "index": 7,
            "form": "of",
            "lemma": "of"
         },
         {
            "index": 8,
            "form": "dollars",
            "lemma": "dollar"
         },
         {
            "index": 9,
            "form": "in",
            "lemma": "in"
         },
         {
            "index": 10,
            "form": "assets.",
            "lemma": "asset"
         }
      ],
      "nodes": [
         {
            "id": 0,
            "label": "_these_q_dem",
            "anchors": [
               {
                  "from": 0,
                  "end": 0
               }
            ]
         },
         {
            "id": 1,
            "label": "_fund_n_1",
            "anchors": [
               {
                  "from": 1,
                  "end": 1
               }
            ]
         },
         {
            "id": 2,
            "label": "_now_a_1",
            "anchors": [
               {
                  "from": 2,
                  "end": 2
               }
            ]
         },
         {
            "id": 3,
            "label": "_account_v_for",
            "anchors": [
               {
                  "from": 3,
                  "end": 3
               }
            ]
         },
         {
            "id": 4,
            "label": "_several_a_1",
            "anchors": [
               {
                  "from": 5,
                  "end": 5
               }
            ]
         },
         {
            "id": 5,
            "label": "generic_entity",
            "anchors": [
               {
                  "from": 6,
                  "end": 6
               }
            ]
         },
         {
            "id": 6,
            "label": "card",
            "anchors": [
               {
                  "from": 6,
                  "end": 6
               }
            ]
         },
         {
            "id": 7,
            "label": "_dollar_n_1",
            "anchors": [
               {
                  "from": 8,
                  "end": 8
               }
            ]
         },
         {
            "id": 8,
            "label": "_in_p",
            "anchors": [
               {
                  "from": 9,
                  "end": 9
               }
            ]
         },
         {
            "id": 9,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 10,
                  "end": 10
               }
            ]
         },
         {
            "id": 10,
            "label": "_asset_n_1",
            "anchors": [
               {
                  "from": 10,
                  "end": 10
               }
            ]
         },
         {
            "id": 11,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 8,
                  "end": 10
               }
            ]
         },
         {
            "id": 12,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 5,
                  "end": 10
               }
            ]
         }
      ],
      "edges": [
         {
            "source": 0,
            "target": 1,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 2,
            "target": 3,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 3,
            "target": 1,
            "label": "ARG1",
            "post-label": "NEQ"
         },
         {
            "source": 3,
            "target": 5,
            "label": "ARG2",
            "post-label": "NEQ"
         },
         {
            "source": 12,
            "target": 5,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 4,
            "target": 5,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 5,
            "target": 7,
            "label": "ARG1",
            "post-label": "NEQ"
         },
         {
            "source": 6,
            "target": 5,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 11,
            "target": 7,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 8,
            "target": 7,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 8,
            "target": 10,
            "label": "ARG2",
            "post-label": "NEQ"
         },
         {
            "source": 9,
            "target": 10,
            "label": "RSTR",
            "post-label": "H"
         }
      ],
      "tops": [
         3
      ]
   },
   {
      "id": "2",
      "source": "cylic+connected",
      "input": "These funds now account for several billions of dollars in assets.",
      "tokens": [
         {
            "index": 0,
            "form": "these",
            "lemma": "these"
         },
         {
            "index": 1,
            "form": "funds",
            "lemma": "fund"
         },
         {
            "index": 2,
            "form": "now",
            "lemma": "now"
         },
         {
            "index": 3,
            "form": "account",
            "lemma": "account"
         },
         {
            "index": 4,
            "form": "for",
            "lemma": "for"
         },
         {
            "index": 5,
            "form": "several",
            "lemma": "several"
         },
         {
            "index": 6,
            "form": "billions",
            "lemma": "1000000000",
            "carg": "1000000000"
         },
         {
            "index": 7,
            "form": "of",
            "lemma": "of"
         },
         {
            "index": 8,
            "form": "dollars",
            "lemma": "dollar"
         },
         {
            "index": 9,
            "form": "in",
            "lemma": "in"
         },
         {
            "index": 10,
            "form": "assets.",
            "lemma": "asset"
         }
      ],
      "nodes": [
         {
            "id": 0,
            "label": "_these_q_dem",
            "anchors": [
               {
                  "from": 0,
                  "end": 0
               }
            ]
         },
         {
            "id": 1,
            "label": "_fund_n_1",
            "anchors": [
               {
                  "from": 1,
                  "end": 1
               }
            ]
         },
         {
            "id": 2,
            "label": "_now_a_1",
            "anchors": [
               {
                  "from": 2,
                  "end": 2
               }
            ]
         },
         {
            "id": 3,
            "label": "_account_v_for",
            "anchors": [
               {
                  "from": 3,
                  "end": 3
               }
            ]
         },
         {
            "id": 4,
            "label": "_several_a_1",
            "anchors": [
               {
                  "from": 5,
                  "end": 5
               }
            ]
         },
         {
            "id": 5,
            "label": "generic_entity",
            "anchors": [
               {
                  "from": 6,
                  "end": 6
               }
            ]
         },
         {
            "id": 6,
            "label": "card",
            "anchors": [
               {
                  "from": 6,
                  "end": 6
               }
            ]
         },
         {
            "id": 7,
            "label": "_dollar_n_1",
            "anchors": [
               {
                  "from": 8,
                  "end": 8
               }
            ]
         },
         {
            "id": 8,
            "label": "_in_p",
            "anchors": [
               {
                  "from": 9,
                  "end": 9
               }
            ]
         },
         {
            "id": 9,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 10,
                  "end": 10
               }
            ]
         },
         {
            "id": 10,
            "label": "_asset_n_1",
            "anchors": [
               {
                  "from": 10,
                  "end": 10
               }
            ]
         },
         {
            "id": 11,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 8,
                  "end": 10
               }
            ]
         },
         {
            "id": 12,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 5,
                  "end": 10
               }
            ]
         }
      ],
      "edges": [
         {
            "source": 0,
            "target": 1,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 2,
            "target": 3,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 3,
            "target": 1,
            "label": "ARG1",
            "post-label": "NEQ"
         },
         {
            "source": 3,
            "target": 5,
            "label": "ARG2",
            "post-label": "NEQ"
         },
         {
            "source": 12,
            "target": 5,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 5,
            "target": 4,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 4,
            "target": 6,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 6,
            "target": 5,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 5,
            "target": 7,
            "label": "ARG1",
            "post-label": "NEQ"
         },
         {
            "source": 11,
            "target": 7,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 8,
            "target": 7,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 8,
            "target": 10,
            "label": "ARG2",
            "post-label": "NEQ"
         },
         {
            "source": 9,
            "target": 10,
            "label": "RSTR",
            "post-label": "H"
         }
      ],
      "tops": [
         3
      ]
   },
   {
      "id": "3",
      "source": "acylic+disconnected",
      "input": "These funds now account for several billions of dollars in assets.",
      "tokens": [
         {
            "index": 0,
            "form": "these",
            "lemma": "these"
         },
         {
            "index": 1,
            "form": "funds",
            "lemma": "fund"
         },
         {
            "index": 2,
            "form": "now",
            "lemma": "now"
         },
         {
            "index": 3,
            "form": "account",
            "lemma": "account"
         },
         {
            "index": 4,
            "form": "for",
            "lemma": "for"
         },
         {
            "index": 5,
            "form": "several",
            "lemma": "several"
         },
         {
            "index": 6,
            "form": "billions",
            "lemma": "1000000000",
            "carg": "1000000000"
         },
         {
            "index": 7,
            "form": "of",
            "lemma": "of"
         },
         {
            "index": 8,
            "form": "dollars",
            "lemma": "dollar"
         },
         {
            "index": 9,
            "form": "in",
            "lemma": "in"
         },
         {
            "index": 10,
            "form": "assets.",
            "lemma": "asset"
         }
      ],
      "nodes": [
         {
            "id": 0,
            "label": "_these_q-dem",
            "anchors": [
               {
                  "from": 0,
                  "end": 0
               }
            ]
         },
         {
            "id": 1,
            "label": "_fund_n_1",
            "anchors": [
               {
                  "from": 1,
                  "end": 1
               }
            ]
         },
         {
            "id": 2,
            "label": "_now_a_1",
            "anchors": [
               {
                  "from": 2,
                  "end": 2
               }
            ]
         },
         {
            "id": 3,
            "label": "_account_v_for",
            "anchors": [
               {
                  "from": 3,
                  "end": 3
               }
            ]
         },
         {
            "id": 4,
            "label": "_several_a_1",
            "anchors": [
               {
                  "from": 5,
                  "end": 5
               }
            ]
         },
         {
            "id": 5,
            "label": "generic_entity",
            "anchors": [
               {
                  "from": 6,
                  "end": 6
               }
            ]
         },
         {
            "id": 6,
            "label": "card",
            "anchors": [
               {
                  "from": 6,
                  "end": 6
               }
            ]
         },
         {
            "id": 7,
            "label": "_dollar_n_1",
            "anchors": [
               {
                  "from": 8,
                  "end": 8
               }
            ]
         },
         {
            "id": 8,
            "label": "_in_p",
            "anchors": [
               {
                  "from": 9,
                  "end": 9
               }
            ]
         },
         {
            "id": 9,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 10,
                  "end": 10
               }
            ]
         },
         {
            "id": 10,
            "label": "_asset_n_1",
            "anchors": [
               {
                  "from": 10,
                  "end": 10
               }
            ]
         },
         {
            "id": 11,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 8,
                  "end": 10
               }
            ]
         },
         {
            "id": 12,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 5,
                  "end": 10
               }
            ]
         }
      ],
      "edges": [
         {
            "source": 0,
            "target": 1,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 2,
            "target": 3,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 3,
            "target": 1,
            "label": "ARG1",
            "post-label": "NEQ"
         },
         {
            "source": 12,
            "target": 5,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 4,
            "target": 5,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 5,
            "target": 7,
            "label": "ARG1",
            "post-label": "NEQ"
         },
         {
            "source": 6,
            "target": 5,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 11,
            "target": 7,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 8,
            "target": 7,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 8,
            "target": 10,
            "label": "ARG2",
            "post-label": "NEQ"
         },
         {
            "source": 9,
            "target": 10,
            "label": "RSTR",
            "post-label": "H"
         }
      ],
      "tops": [
         3
      ]
   },
   {
      "id": "4",
      "source": "cylic+disconnected",
      "input": "These funds now account for several billions of dollars in assets.",
      "tokens": [
         {
            "index": 0,
            "form": "these",
            "lemma": "these"
         },
         {
            "index": 1,
            "form": "funds",
            "lemma": "fund"
         },
         {
            "index": 2,
            "form": "now",
            "lemma": "now"
         },
         {
            "index": 3,
            "form": "account",
            "lemma": "account"
         },
         {
            "index": 4,
            "form": "for",
            "lemma": "for"
         },
         {
            "index": 5,
            "form": "several",
            "lemma": "several"
         },
         {
            "index": 6,
            "form": "billions",
            "lemma": "1000000000",
            "carg": "1000000000"
         },
         {
            "index": 7,
            "form": "of",
            "lemma": "of"
         },
         {
            "index": 8,
            "form": "dollars",
            "lemma": "dollar"
         },
         {
            "index": 9,
            "form": "in",
            "lemma": "in"
         },
         {
            "index": 10,
            "form": "assets.",
            "lemma": "asset"
         }
      ],
      "nodes": [
         {
            "id": 0,
            "label": "_these_q_dem",
            "anchors": [
               {
                  "from": 0,
                  "end": 0
               }
            ]
         },
         {
            "id": 1,
            "label": "_fund_n_1",
            "anchors": [
               {
                  "from": 1,
                  "end": 1
               }
            ]
         },
         {
            "id": 2,
            "label": "_now_a_1",
            "anchors": [
               {
                  "from": 2,
                  "end": 2
               }
            ]
         },
         {
            "id": 3,
            "label": "_account_v_for",
            "anchors": [
               {
                  "from": 3,
                  "end": 3
               }
            ]
         },
         {
            "id": 4,
            "label": "_several_a_1",
            "anchors": [
               {
                  "from": 5,
                  "end": 5
               }
            ]
         },
         {
            "id": 5,
            "label": "generic_entity",
            "anchors": [
               {
                  "from": 6,
                  "end": 6
               }
            ]
         },
         {
            "id": 6,
            "label": "card",
            "anchors": [
               {
                  "from": 6,
                  "end": 6
               }
            ]
         },
         {
            "id": 7,
            "label": "_dollar_n_1",
            "anchors": [
               {
                  "from": 8,
                  "end": 8
               }
            ]
         },
         {
            "id": 8,
            "label": "_in_p",
            "anchors": [
               {
                  "from": 9,
                  "end": 9
               }
            ]
         },
         {
            "id": 9,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 10,
                  "end": 10
               }
            ]
         },
         {
            "id": 10,
            "label": "_asset_n_1",
            "anchors": [
               {
                  "from": 10,
                  "end": 10
               }
            ]
         },
         {
            "id": 11,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 8,
                  "end": 10
               }
            ]
         },
         {
            "id": 12,
            "label": "udef_q",
            "anchors": [
               {
                  "from": 5,
                  "end": 10
               }
            ]
         }
      ],
      "edges": [
         {
            "source": 0,
            "target": 1,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 2,
            "target": 3,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 3,
            "target": 1,
            "label": "ARG1",
            "post-label": "NEQ"
         },
         {
            "source": 12,
            "target": 5,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 5,
            "target": 4,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 4,
            "target": 6,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 6,
            "target": 5,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 5,
            "target": 7,
            "label": "ARG1",
            "post-label": "NEQ"
         },
         {
            "source": 11,
            "target": 7,
            "label": "RSTR",
            "post-label": "H"
         },
         {
            "source": 8,
            "target": 7,
            "label": "ARG1",
            "post-label": "EQ"
         },
         {
            "source": 8,
            "target": 10,
            "label": "ARG2",
            "post-label": "NEQ"
         },
         {
            "source": 9,
            "target": 10,
            "label": "RSTR",
            "post-label": "H"
         }
      ],
      "tops": [
         3
      ]
   }
]'

