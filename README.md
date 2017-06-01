# TOC Project 2017

Template Code for TOC Project 2017

A telegram bot based on a finite state machine

### Run Locally
You can either setup https server or using `ngrok` as a proxy.

**`ngrok` would be used in the following instruction**

```sh
ngrok http 5000
```

After that, `ngrok` would generate a https URL.

You should set `WEBHOOK_URL` (in app.py) to `your-https-URL/hook`.

#### Run the sever

python3 app.py

## Finite State Machine
![fsm](./img/show-fsm.png)

## Usage
The initial state is set to `user`.

Note:It can only input Foreign Article

Every time `user` state is triggered to `advance` to another state, it will let you to choose your options to get what you want.

* user
	* Input: The article name you want to search,then follew the option to choose the information.


## Author
Collin (https://github.com/collin85820/TOC-Project.git)
