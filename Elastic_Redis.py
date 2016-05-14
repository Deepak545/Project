from flask import Flask, jsonify
import elasticsearch
import redis

app = Flask(__name__)

languages = [
    {
        'rank': 1,
        'Name': 'Python',
        'About': 'It\'s a widely used high-level, simple and powerful language.', 
        'Creator': 'Guido van Rossum'
    },
    {
        'rank': 2,
        'Name': 'C',
        'About': 'C is a general-purpose, high-level language and imperative language.', 
        'Creator': 'Dennis M. Richie'
    },
	{
		'rank': 3,
        'Name': 'Ruby',
        'About': 'Ruby is a  dynamic and object-oriented scripting language.', 
        'Creator': 'Yukihiro Matsumoto'
	},
	{
		'rank': 4,
        'Name': 'Scala',
        'About': 'Scala is a general purpose and functional programming language.', 
        'Creator': 'Martin Odersky'
	},
	{
		'rank': 5,
        'Name': 'Java',
        'About': 'Java is an object-oriented programming language.', 
        'Creator': 'James Gosling'
	}
]



#### API 1 :: To Enter data into Redis and Elasticsearch ####
 
@app.route('/index', methods=['POST'])
def insert_data():
    if not request.json or not 'Name' in request.json:
        abort(400)
    language = {
        'rank': languages[-1]['rank'] + 1,
        'Name': request.json['Name'],
        'About': request.json.get('About', ""),
        'Creator': 'creator'
    }
    languages.append(language)
    return jsonify({'language': language}), 201

	
	
	

#### API 2 :: To Index or Retrieve the data from Redis ####

#### Indexing data into Radis
languages = {
            'rank': 6,
            'Name': 'PHP',
            'About': ' PHP is a widely-used, open source scripting language',
            'Creator': 'Rasmus Lerdorf'
        }
		
result = redis.StrictRedis()

result.set('languages', languages)


#### To Retrieve data from Redis

@app.route('/index', methods=['GET'])
def get_data():
    return jsonify({'languages': languages)
	
	         #### OR ####
	
####	This method is another version of get_data that uses a specific key like 'rank' here

####@app.route('/index', methods=['GET'])
####def get_data(language_rank):
####    language = [language for language in languages if language['rank'] == language_rank]
####    if len(language) == 0:
####        abort(404)
####    return jsonify({'language': language[0]})



#### Retrieving  data from Redis

result.get('languages')




#### API 3 :: To Retrieve the data from ElasticSearch ####

#### Indexing data into ElasticSearch

curl -XPUT '/index' -d '{
                            'rank':6,
                            'Name': 'PHP',
                            'About': 'PHP is a widely-used, open source scripting language',
                            'Creator': 'Rasmus Lerdorf'
                        }'

						
						
#### To Retrieve data from ElasticSearch

@app.route('/search', methods=['GET'])
def search_data():
    return jsonify({'languages': languages})

	
#### Retrieving data from ElasticSearch

curl -XGET '/search_search?q=title: Python'

if __name__ == '__main__':
    app.run(debug=True)

