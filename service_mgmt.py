from subprocess import Popen, PIPE

def service_mgmt(action, service):
    """
    service_mgmt function.  Facilitates executing commands on services
    :type action: string
    :param action: action to perform on service.
                   start, stop, restart, status
    :type service: string
    :param service: service to perform action on.
                    must be a valid linux service
    :type return: tuple
    :return tuple: (response_message, success)
                   response_message: output from the service call
                   success: boolean if command was successful
    """
    # TODO: implement actually calling the service binary using subprocess
    command = ['/bin/true']

    # execute command using Popen
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    # poll the subprocess call for data (exit code, stderr/stdout, etc.)
    while not isinstance(p.returncode, int):
        p.poll()

    # successful command
    if p.returncode == 0:
        success = True
    # unsuccessful command
    else:
        success = False

    # return results
    return ("{0}:{1} - {2}/{3}".format(action,service, p.stdout.readlines(),p.stderr.readlines()), success)
