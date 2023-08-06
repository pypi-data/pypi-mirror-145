# DPC (Kafka Data Producer and Consumer)

A library to produce and consume messages in a kafka cluster


## Using the Library


``` bash
git clone github.com/chepkoyallan/dpc.git

cd dpc

python setup.py install

```
## Using the code for Producing
```python
from dpc.producer import Producer
import json


if __name__=='__main__':


    msg = {
        "Li": "Rflow"
    }

    address = "137.184.249.97"
    port = "50051"
    topic = "test_li_topic"
    message=json.dumps(msg).encode('utf-8')

    produce = Producer(
        topic=topic, address=address, port=port, message=message
    )

    response = produce.produce()
    print(response)
```
## Using the code for Consuming
```python
from dpc.consumer import Consumer
import json

if __name__=='__main__':
    
    group = "test-consumer-group"
    address = "137.184.249.97"
    port = "50051"
    topic = "test_li_topic"

    consumer = Consumer(
        group=group, topic=topic, address=address, port=port
    )

    response = consumer.consume()
    for x in response:
      print(x)
```

## Getting Started To Contribute [For DEVelopers]

```
git clone github.com/chepkoyallan/dpc.git
```

### install and create and activate virtual environment

```
python3 install virtualenv
```

create virtualenv

```
virtualenv venv
```

activate virtual environment

```
source venv bin/activate
```
### Installing packages

```
pip install -r requirements.txt
```


## Author

* **Allan Kiplangat, LI, Fu** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

