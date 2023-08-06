<p align="center">
    <em>Rasa NLU engine backported from main Rasa project</em>
</p>
<p align="center">
<a href="https://travis-ci.org/madkote/rasa-nlu-contrib" target="_blank">
    <img src="https://travis-ci.org/madkote/rasa_nlu_contrib.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/madkote/rasa-nlu-contrib" target="_blank">
    <img src="https://codecov.io/gh/madkote/rasa_nlu_contrib/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/rasa-nlu-contrib" target="_blank">
    <img src="https://img.shields.io/pypi/v/rasa_nlu_contrib.svg" alt="Package version">
</a>
</p>

# rasa-nlu-contrib
Rasa NLU engine backported from main Rasa project

Rasa NLU (Natural Language Understanding) is a tool for understanding what is being said in short pieces of text.
For example, taking a short message like:

> *"I'm looking for a Mexican restaurant in the center of town"*

And returning structured data like:

```
  intent: search_restaurant
  entities: 
    - cuisine : Mexican
    - location : center
```

Rasa NLU is primarily used to build chatbots and voice apps, where this is called intent classification and entity extraction.
To use Rasa, *you have to provide some training data*.
That is, a set of messages which you've already labelled with their intents and entities.
Rasa then uses machine learning to pick up patterns and generalise to unseen sentences. 

You can think of Rasa NLU as a set of high level APIs for building your own language parser using existing NLP and ML libraries.

## Installation
* Minimal `pip install rasa-nlu-contrib`
* Full `pip install rasa-nlu-contrib[all]`
  - server
  - spacy
  - tensorflow
* HTTP server `pip install rasa-nlu-contrib[server]`
* Spacy `pip install rasa-nlu-contrib[spacy]`
* Tensorflow `pip install rasa-nlu-contrib[tensorflow]`
* Chinise `pip install rasa-nlu-contrib[zh]`
* Duckling `pip install rasa-nlu-contrib[duckling]`
* Mitie `pip install rasa-nlu-contrib[mitie]`

Full list for copy-and-paste:
```
pip install rasa-nlu-contrib
pip install rasa-nlu-contrib[all]
pip install rasa-nlu-contrib[server]
pip install rasa-nlu-contrib[spacy]
pip install rasa-nlu-contrib[tensorflow]
pip install rasa-nlu-contrib[zh]
pip install rasa-nlu-contrib[duckling]
pip install rasa-nlu-contrib[mitie]
```

## Changes
See [release notes](CHANGES.md)

## Usage
For details see [legacy documentation](https://legacy-docs.rasa.com/docs/nlu/).

### Python API
```python
import os
import pprint

from rasa_nlu.model import Interpreter
from rasa_nlu.train import train

model_name = 'nlu'
project_name = 'project_demo'

here = os.path.abspath(os.path.dirname(__file__))
path_config = os.path.join(here, 'sample_configs', 'config_supervised_embeddings.yml')  # noqa E501
path_data = os.path.join(here, 'data', 'examples', 'rasa', 'demo-rasa.md')
path_models = os.path.join(here, 'demo_models')

trainer, interpreter, persisted_path = train(  # @UnusedVariable
    path_config,
    path_data,
    path=path_models,
    project=project_name,
    fixed_model_name=model_name
)
message = "let's see some italian restaurants"
result = interpreter.parse(message)
pprint.pprint(result)

interpreter = Interpreter.load(os.path.join(path_models, project_name, model_name))  # noqa E501
message = "let's see some italian restaurants"
result = interpreter.parse(message)
pprint.pprint(result)
```

### HTTP API
```sh
python demo.py http

curl 'localhost:5000/'
curl 'localhost:5000/status'
curl 'localhost:5000/version'

curl 'localhost:5000/parse?q=hello&project=project_demo&model=nlu'
```

### Docker
```sh
docker-compose up

curl 'localhost:5000/'
curl 'localhost:5000/status'
curl 'localhost:5000/version'

curl 'localhost:5000/parse?q=hello&project=project_demo&model=nlu'
```

# License
This project is licensed under the terms of the MIT license.
Code of Rasa is licensed under the terms of the Apache 2.0 license.
[Copy of the license](LICENSE) and [additional notes](NOTICE).

# Development and how to contribute
Issues and suggestions are welcome through *issues*
