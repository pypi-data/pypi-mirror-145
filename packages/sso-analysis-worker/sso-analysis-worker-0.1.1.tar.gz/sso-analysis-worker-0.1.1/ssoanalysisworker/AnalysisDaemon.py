__version__ = '0.1.0'

import argparse
import os.path
import threading
import uuid
from time import sleep

from pyvirtualdisplay import Display

from model.backend_information import BackendInformation
from processes.process_helper import ProcessHelper
from services.rest_client import RestClient

cli = argparse.ArgumentParser()
cli.add_argument("--server-host", type=str, default="https://sso-scanner-mgmt.it.hs-heilbronn.de",
                 help="Host of the backend. Default https://sso-scanner-mgmt.it.hs-heilbronn.de/")
cli.add_argument("--server-port", type=int, default=443, help="Port of the backend. Default 443")
cli.add_argument('--dev-mode', help="Disables the use of a virtual display. Can be used when running on a local "
                                    "machine with display enabled", action="store_true")
cli.add_argument('--name', help="The name displayed at the brain. This is temporary and will not be stored!",
                 required=False, default=None)
cli.add_argument('--uuid-file', help="Define the place of the file where the client stores the unique client id",
                 default=os.path.realpath(os.path.dirname(os.path.abspath(__file__))) + "/.uuid")


def test(running_check_element: threading.Event, analysis_id: int, backend_info: BackendInformation):
    ProcessHelper.prepare_and_run_analysis(backend_info, analysis_id, None, running_check_element)


def stop_job(job, rest_client, running_check):
    if job is not None:
        print("Stopping current job...")
        rest_client.update_latest_activity("Stopping job")
        running_check.clear()
        while job.is_alive():
            sleep(10)
            rest_client.send_daemon_ping()
        print("Successfully stopped")


def get_uuid_of_current_client(path) -> str:
    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write(uuid.uuid4().hex)
    with open(path) as file:
        return file.readline()


def run():
    args = cli.parse_args()
    client_identifier = get_uuid_of_current_client(args.uuid_file)
    disp = None
    if not args.dev_mode:
        try:
            print("Start virtual display...")
            disp = Display(visible=False, size=(1920, 1080))
            disp.start()
        except Exception as err:
            print("Something went wrong: " + err.__str__())
            exit(8787)
    print("Running in daemon mode!")
    run_again = True
    while run_again:
        run_again = False
        try:
            token = None
            rest_client = RestClient(args.server_host, args.server_port)
            while token is None:
                print("Checking if registered at brain " + args.server_host)
                try:
                    token = rest_client.get_notify_daemon_start_get_token(args.name, client_identifier)
                except OSError as err:
                    print("Could not connect to server " + args.server_host + ":" + str(
                        args.server_port) + ". Sleeping 30 sec")
                finally:
                    if token is None:
                        print("Client not registered yet. Sleeping 30 sec")
                        sleep(30)
            print("Got token. Client is initialized")
            rest_client = RestClient(args.server_host, args.server_port, token)
            print("Waiting for job...")
            prev_job_id = '-1'
            running_check = threading.Event()
            running_check.set()
            job = None
            try:
                while True:
                    current_job_id = rest_client.get_job_for_daemon_client()
                    if current_job_id == "-1000":
                        print("Received shutdown command! Will initialize shutdown...")
                        break
                    if current_job_id is None:
                        print("Looks like this client was not cleanly removed from the brain (please stop this client "
                              "before removing it from the brain). Shutting down...")
                        break
                    rest_client.send_daemon_ping()
                    current_activity = "Idle"
                    if job is not None and job.is_alive() and running_check.is_set():
                        current_activity = "Running"
                    if job is not None and not job.is_alive() and current_job_id != "-1":
                        current_activity = "Finished"
                    rest_client.update_latest_activity(current_activity)
                    if current_job_id == prev_job_id:
                        sleep(30)
                        continue
                    else:
                        print("Job info changed! (" + str(prev_job_id) + " --> " + str(current_job_id) + ")")
                        stop_job(job, rest_client, running_check)
                        if current_job_id != "-1":
                            rest_client.update_latest_activity("Starting")
                            job = threading.Thread(target=test, args=(
                                running_check, current_job_id,
                                BackendInformation(args.server_host, args.server_port, token)))
                            running_check.set()
                            job.start()
                        prev_job_id = current_job_id
            finally:
                print("Stopping daemon...")
                stop_job(job, rest_client, running_check)
                rest_client.update_latest_activity("Shutdown")
                print("Current job finished")
                if disp is not None:
                    print("Stopping virtual display")
                    disp.stop()
        except OSError as err:
            print(err)
            print("Got an error. Sleeping 30 sec and start again")
            run_again = True
            sleep(30)
        except KeyboardInterrupt:
            pass
    print("Shutdown completed. Bye!")


if __name__ == "__main__":
    run()
