# unix-linux-17-hw9
Unix Linux Q3 2017 HW9

For Homework 9 you will be responsible for hosting your own API endpoint that will facilitate starting and stopping any service on your host.

This git repo provides a very basic stub for setting up a flask web application that can receive requests.
You need to finish the implementation of the service_mgmt.service_mgmt() function so that it uses subprocess to make the appropriate calls to /usr/sbin/service.

## Prerequisites
- Install pip (apt-get install python-pip)
- Install requirements (pip install -r requirements.txt)

## Files in this repository
* app.py - flask app entry point including route handling logic
* invalidusage.py - InvalidUsage Exception class.  Facilitates handling 4xx responses while still passing back json responses
* service_mgmt.py - Service Management codebase for implementing calls to /usr/sbin/service from the API

## service_mgmt.py implementation
I've already implemented the service_mgmt() method and integreated into the flask app.  It is your job to write the section that uses subprocess to execute service start/stop/status/restart commands on the provided service.  You are expected to honor:
* input: 2 parameters
  * service - the service to perform the action on - sshd, apache, etc.  eg: /usr/sbin/service <service> stop
  * action - the action to perform - stop, start, status, restart.  eg: /usr/sbin/service apache <action>
* output: tuple of (response_message, success)
  * response_message - output from the /usr/sbin/service call.  eg:  * Stopping web server apache2 *
  * success - boolean on if the command was successful.  Should be based on subprocess exit code.  eg: True

For more information about the subprocess module see https://docs.python.org/2/library/subprocess.html
## Flask things
### Starting your app
* Given that this Flask API will be restarting services it will need root privileges to do so
  * Run the program as root vs. using sudo
  * Give the user running the program NOPASSWD sudo permissions to execute /usr/sbin/service
* executing the app.py script will startup the built in web server and listen on 127.0.0.1:8080 by default
```
ho-mbp-713:unix-linux-17-hw9 chenry$ ./app.py 
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
127.0.0.1 - - [11/May/2017 00:16:57] "GET /v1/services/status HTTP/1.1" 200 -
```

### Debug
There is a debug flag configurable at https://github.com/chenry3/unix-linux-17-hw9/blob/master/app.py#L11
The debug flag (http://flask.pocoo.org/docs/0.10/quickstart/#debug-mode) will
* cause exceptions to raise and return the stack trace in the HTTP response
* auto-restart your web server when changes are written to code files

### Flask app routing
Lines https://github.com/chenry3/unix-linux-17-hw9/blob/master/app.py#L25-L26 contain the request routing.  Anything not matching any app routes will 404.  Notice the app route has <action> surrounded by < and >.  This means that it is a dynamic value and will be passed into the function with the value substituded in.  This is why the services() function has 1 parameter defined called action.

### Interface binding
Due to security concerns by default the flask applicatoin will startup only bound to 127.0.0.1.  Once you have finished testing and are confident in your product, you should firewall port 8080 and change the 'host' parameter at https://github.com/chenry3/unix-linux-17-hw9/blob/master/app.py#L79 to 0.0.0.0

### Restful HTTP Methods
Different types of resquests in the RESTful HTTP model should be used depending on your request.  See http://restful-api-design.readthedocs.io/en/latest/methods.html

In this case it probably makes senes to use:
* GET - status calls
* PUT - start, stop, and restart calls

### Testing
You should be able to test your API by submitting curl requests to it.  You will need to pass in some json to specify parameters.  Here are some examples:

* see the status of the apache2 daemon:
```
chenry@ulc-129:~/git/unix-linux-17-hw9$ curl -i -H "Content-Type: application/json" -X PUT -d '{"service": "apache2"}' http://localhost:8080/v1/services/status
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 1628
Server: Werkzeug/0.12.2 Python/2.7.12
Date: Tue, 30 May 2017 06:37:34 GMT

{
  "output": "status:apache2 - ['\\xe2\\x97\\x8f apache2.service - LSB: Apache2 web server\\n', '   Loaded: loaded (/etc/init.d/apache2; bad; vendor preset: enabled)\\n', '  Drop-In: /lib/systemd/system/apache2.service.d\\n', '           \\xe2\\x94\\x94\\xe2\\x94\\x80apache2-systemd.conf\\n', '   Active: active (running) since Sun 2017-04-23 21:48:49 PDT; 1 months 5 days ago\\n', '     Docs: man:systemd-sysv-generator(8)\\n', '  Process: 19269 ExecReload=/etc/init.d/apache2 reload (code=exited, status=0/SUCCESS)\\n', '    Tasks: 55\\n', '   Memory: 7.4M\\n', '      CPU: 42min 46.800s\\n', '   CGroup: /system.slice/apache2.service\\n', '           \\xe2\\x94\\x9c\\xe2\\x94\\x8016149 /usr/sbin/apache2 -k start\\n', '           \\xe2\\x94\\x9c\\xe2\\x94\\x8019286 /usr/sbin/apache2 -k start\\n', '           \\xe2\\x94\\x94\\xe2\\x94\\x8019287 /usr/sbin/apache2 -k start\\n', '\\n', 'May 27 06:25:02 ulc-129 apache2[15230]:  *\\n', 'May 27 06:25:02 ulc-129 systemd[1]: Reloaded LSB: Apache2 web server.\\n', 'May 28 06:25:02 ulc-129 systemd[1]: Reloading LSB: Apache2 web server.\\n', 'May 28 06:25:02 ulc-129 apache2[17359]:  * Reloading Apache httpd web server apache2\\n', 'May 28 06:25:03 ulc-129 apache2[17359]:  *\\n', 'May 28 06:25:03 ulc-129 systemd[1]: Reloaded LSB: Apache2 web server.\\n', 'May 29 06:25:02 ulc-129 systemd[1]: Reloading LSB: Apache2 web server.\\n', 'May 29 06:25:02 ulc-129 apache2[19269]:  * Reloading Apache httpd web server apache2\\n', 'May 29 06:25:02 ulc-129 apache2[19269]:  *\\n', 'May 29 06:25:02 ulc-129 systemd[1]: Reloaded LSB: Apache2 web server.\\n']/[]", 
  "success": true
}

```

* restart the sshd daemon:
```
chenry@ulc-129:~/git/unix-linux-17-hw9$ curl -i -H "Content-Type: application/json" -X PUT -d '{"service": "sshd"}' http://localhost:8080/v1/services/restart       
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 59
Server: Werkzeug/0.12.2 Python/2.7.12
Date: Tue, 30 May 2017 06:38:26 GMT

{
  "output": "restart:sshd - []/[]", 
  "success": true
}
```

* stop the cron daemon:
```
chenry@ulc-129:~/git/unix-linux-17-hw9$ curl -i -H "Content-Type: application/json" -X PUT -d '{"service": "cron"}' http://localhost:8080/v1/services/stop
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 56
Server: Werkzeug/0.12.2 Python/2.7.12
Date: Tue, 30 May 2017 06:39:21 GMT

{
  "output": "stop:cron - []/[]", 
  "success": true
}
```


