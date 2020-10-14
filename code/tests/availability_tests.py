import signal

INTERVAL_BTW_CHECK = 30
TIMEOUT_THRESHOLD = 600


class TimeoutError(Exception):
    pass


def handler(signum, frame):
    print("System Timed out before all the resources ready")
    raise TimeoutError('The function timed out before the resources get ' +
                       'ready, which might indicate a problem')


def check_status():
    import time
    print("Checking the status of all pods...")
    time.sleep(INTERVAL_BTW_CHECK)
    from kubernetes import client, config

    config.load_kube_config()

    v1 = client.CoreV1Api()
    while (True):
        # perserve some time before check the status
        time.sleep(INTERVAL_BTW_CHECK)

        ret = v1.list_pod_for_all_namespaces(watch=False)
        count = 0

        for i in ret.items:
            if not i.status.container_statuses[0].ready:
                print('{0} is not ready.'.format(i.metadata.name))
                count = count + 1
        if count == 0:
            return


if __name__ == "__main__":
    # setting up the timeout threshold
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(TIMEOUT_THRESHOLD)
    check_status()
