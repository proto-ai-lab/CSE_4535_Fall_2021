# CSE 4/535 Project 2: Starter Kit

This codebase is a starter kit for Project 2. Usage of this toolkit is **RECOMMENDED**.


## Requirements

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install the requirements. Update apt if you are using EC2 Ubuntu instance.

```bash
sudo apt-get update
sudo apt install python3-pip -y
pip3 install tqdm Flask nltk
```

## Files and Tasks

1. `run_project.py` is the driver file, which will create the Flask app. Implement the logic for getting the postings list, executing DAAT AND query, merging linked list. etc. in this file.
2. `indexer.py` contains code to create and manipulate the index. Implement the necessary functions in indexer.
3. `preprocessor.py` contains code to pre-process documents & queries. Implement the necessary functions in preprocessor.
3. `linkedlist.py` defines the basic data structures for the postings list and the nodes of the postings list. It also contains code to manipulate the postings list. . Implement the necessary functions in linkedlist.
4. Execute `run_project.py` to create your index and start your API endpoint. Your endpoint will be available at `http://<ec2 public ipv4:9999>/execute_query`

## Strategies for completing the project efficiently

- Use EC2 t2.micro (or medium) instance for hosting your Flask app. Make sure the instance is running during grading.
- Run `run_project.py` using nohup in the server. The command is `sudo nohup python3 run_project.py --corpus ./data/input_corpus.txt --output_location ./data/output.json --username your_UB_username> log.txt 2>&1 &`
- The nohup command will create a log file `log.txt` check the log file for execution status. The result of running the queries will be stored in the file output.json
- In order to stop your app, run `sudo lsof -n -i :9999` in command line to get the `PID` of the running nohup process. Kill the process using the command `sudo kill -9 <PID>`
- Don't forget to open the port 9999 on your ec2 instance for TCP connections.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)