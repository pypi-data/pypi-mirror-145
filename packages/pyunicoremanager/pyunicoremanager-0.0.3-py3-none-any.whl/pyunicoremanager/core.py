#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    PyUnicoreManager (It adapts PyUnicore library and uses it from different frameworks)
    Author: Aarón Pérez Martín
    Contact:a.perez.martin@fz-juelich.de
    Organization: Forschungszentrum Jülich

    PyUnicore library (Client for UNICORE using the REST API)
    For full info of the REST API, see https://sourceforge.net/p/unicore/wiki/REST_API/
'''
#

import pyunicore.client as unicore_client
from base64 import b64encode
import os, time, sys, logging, datetime
from enum import IntEnum

def set_logger(name, level='INFO'):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # Configure stream handler for the cells
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s', '%H:%M:%S'))
    handler.setLevel(level)

    logger.addHandler(handler)
    return logging.root.manager.loggerDict[name]


logss = set_logger("ndp.pyunim")


class Method(IntEnum):
    # Different access require a different token and the way to call a job
    ACCESS_LDAP = 0
    ACCESS_COLLAB = 1


class Authentication():
    def __init__(self, token: str, access: Method, server: str, **args):
        self.token = token
        self.access = access
        self.server = server


class Utils():
    @staticmethod
    def execution_time(start, end, num_dec):
        total_time = end - start
        if total_time < 60:
            msg = "Flow time --- " + str(round(total_time, num_dec)) + " seconds ---"
        elif 60 <= total_time < 3600:
            msg = "Flow time --- " + str(round(total_time / 60, num_dec)) + " minutes ---"
        elif 3600 <= total_time < 86400:
            msg = "Flow time --- " + str(round(total_time / 3600, num_dec)) + " hours ---"
        else:
            msg = "Flow time --- " + str(round(total_time / 86400, num_dec)) + " days ---"
        return msg

    @staticmethod
    def generateToken(ldapaccount, ldappassword):
        return b64encode(str.encode(ldapaccount + ":" + ldappassword)).decode("ascii")

    @staticmethod
    def arrayToString(array):
        return ' '.join(map(str, array))

    @staticmethod
    def generate_PythonCompiler(variables):
        return [" cd " + variables["destination_project_path"],
                "date >> text; echo done!"]

    @staticmethod
    def generate_steps_bashscript(variables, filename):
        return ["cd " + variables["destination_project_path"],
                'log=' + variables["destination_log_path"] + '/log$(date "+%Y%m%d")',
                "chmod 764 " + filename + " >>$log ",
                "./ " + filename + ' >>$log']


class Environment_UNICORE():

    def __init__(self, auth: Authentication, **args):
        self.urls, self.conn_info, self.job_info, self.script_info = {}, {}, {}, {}

        # Required for a sever connection
        self.conn_info["token"] = auth.token
        self.conn_info["methodToAccess"] = auth.access
        self.conn_info["serverToConnect"] = auth.server
        self.conn_info["serverToRegister"] = args.get('serverToRegister',
                                                      "https://zam2125.zam.kfa-juelich.de:9112/HBP/rest/registries/default_registry")
       
        # NOTE server_endpoint -> #Storage Endpoint: "PROJECT", "SCRATCH", "HOME",...
        
        env_dict= args.get('env_from_user', None)
        if env_dict and "JobArguments" in env_dict.keys():
            self.job_info.update(env_dict) #it must contain "JobArguments" 


class PyUnicoreManager(object):
    def __init__(self, environment, **args):

        self.storage = None
        self.env = environment

        self.verbose = args.get('verbose', False)
        self.check_environment = args.get('check_environment', False)
        self.clean_job_storages = args.get('clean_job_storages', False)
        has_errors = False

        if self.env.conn_info["token"] is None:
            logss.error("Token is required!")
            has_errors = True
        try:
            # Accesing with LDAP or COLLAB token have have different parameters in the PyUnicore.Transport
            # oidc=False doesnt work with collab token
            self.transport = None
            if Method.ACCESS_LDAP == self.env.conn_info["methodToAccess"]:
                self.transport = unicore_client.Transport(self.env.conn_info["token"], oidc=False)
            elif Method.ACCESS_COLLAB == self.env.conn_info["methodToAccess"]:
                self.transport = unicore_client.Transport(self.env.conn_info["token"])
            try:
                # Important: To be sure of selecting the proper internal mapping of UNICORE links to a specific project
                self.transport.preferences = "group:" + str(self.env.job_info["server_project"]) # used to Upload/download files
                
                self.registry = unicore_client.Registry(self.transport, self.env.conn_info["serverToRegister"])
                self.site = self.registry.site(self.env.conn_info["serverToConnect"])

                self.client = unicore_client.Client(self.transport, self.site.site_url)
            except Exception as e:
                logss.error("Server: " + str(self.env.job_info["server"])+ " is not responding. " + str(e))

            try:
                for storage in self.site.get_storages():
                    if storage.storage_url.endswith(self.env.job_info["server_endpoint"]):
                        self.storage = storage
                        break
            except Exception as e:
                logss.error("Source not available for " + self.env.job_info["JobArguments"]["Project"])
                return None

            if not self.storage:
                logss.error("Source not available " + self.env.job_info["server_endpoint"])
                has_errors = True

            if self.clean_job_storages:
                self.clean_storages(endswith="-uspace")

            # Get the object Storage
            # Endpoint of Storage is mapped from env variables of your account into the UNICORE

            # we need to access to the right project folder into the HPC system
            # First, setting an environment variable by a job
            if self.check_environment:
                logss.info("Checking current $PROJECT into UNICORE system")
                job_cmd, result = self.one_run(
                        steps=["jutil env activate -p " + str(self.env.job_info["JobArguments"]["Project"]),"echo $PROJECT"],
                        parameters=self.env.job_info["JobArguments"])

                if len(result["stderr"]) > 0:
                    logss.error("Error " + result["stderr"])
                    #has_errors = True

                logss.info("Variable $PROJECT on HPC is " + result["stdout"])

            if has_errors:
                logss.error("\nPlease provide the right parameters.")
        
        except Exception as e:
            logss.error("Error creating workflow: " + str(e))
            return None
            
    def check_env_vars_HPC(self):
        
        logss.info("Getting Environment variables on",self.env.job_info["server"])
        return self.one_run(steps=["printenv"], parameters=self.env.job_info["JobArguments"])
        
    def getStorage(self):
        if (self.verbose):
            for storage in self.client.get_storages():
                logss.info(storage.storage_url)

        return self.client.get_storages()

    def getJobs(self, status=None):
        result = []
        list = self.client.get_jobs()
        if status:
            for j in list:
                if j.properties['status'].lower() == status.lower():
                    result.append(j)
            return result
        else:
            return list

    def getSites(self):
        return unicore_client.get_sites(self.transport)

    def clean_storages(self, endswith):
        count = 0
        if len(self.client.get_storages()) >= 200 and len(endswith) > 0:
            logss.info("Cleaning storage endpoints. Working on it...")
            for storage in self.client.get_storages():
                msg = ""
                if storage.storage_url.endswith(str(endswith)):
                    self.transport.delete(url=storage.storage_url)
                    count += 1
                    msg = str(storage.storage_url).split("/")[-1] + " has been removed"
                else:
                    msg = "Keep: " + str(storage.storage_url)

                if self.verbose:
                    logss.info(msg)
            logss.info("Storage endpoints removed: " + str(count))
        else:
            logss.info("Storage endpoints are still under limit: " + str(len(self.client.get_storages())))

    def createJob(self, list_of_steps, job_args=None):

        executable = ""
        for item in list_of_steps[:-1]:
            executable += item + " \n "
        executable += list_of_steps[-1]  # Last element can not contain the new line symbol

        if (self.verbose):
            logss.info("Executing commands...")
            for item in list_of_steps:
                logss.info(">" + str(item))

        job = dict(job_args) if job_args else dict()
        job['Executable'] = executable

        return job

    def __run_job(self, job, wait_process=True):
        result_job = {}
        try:
            cmd_job = self.client.new_job(job_description=job)

            logss.info("Job status... " + str(cmd_job.properties['status']))

            # Wait until the job finishes
            while (cmd_job.properties['status'] == "QUEUED"):
                time.sleep(0.25)
            
            logss.info(cmd_job.properties['status'])
            if wait_process: 
                cmd_job.poll()

                wd = cmd_job.working_dir
                result_job["stderr"] = ''.join([x.decode('utf8') for x in wd.stat("/stderr").raw().readlines()])
                result_job["stdout"] = ''.join([x.decode('utf8') for x in wd.stat("/stdout").raw().readlines()])
                if self.verbose:
                    logss.info(result_job.items())
                if (cmd_job.properties['status'] == "FAILED"):
                    raise Exception(str(result_job["stderr"]))                
                else:
                    logss.info('Job finished!')
            else:
                logss.info('Job is running!. You could stop it!')
        except Exception as e:
            logss.error(str(e))
            return None, None
        return cmd_job, result_job

    def uploadFiles(self, filesToUpload):
        try:
            if len(filesToUpload) == 0:
                logss.info("Nothing to upload")
                return

            # Uploading files
            logss.info("Uploading to " + str(self.storage.storage_url))
            list_files = list()
            
            for file_info in filesToUpload:
                filename = str(file_info[0]).split('/')[-1]
                
                # it works like this server_endpoint(PROJECT,SCRATCH,...)/folder/file
                self.storage.upload(str(file_info[0]), destination=os.path.join(file_info[1]))
                if (self.verbose):
                    logss.info(" - Uploaded file " + filename)  # getting the last element
                list_files.append(filename)
            logss.info("Uploaded all files: "+str(list_files))
            return True
        except Exception as e:
            logss.error("Uploading error", e)
            return False

    def downloadFiles(self, filesToDownload):
        try:
            if len(filesToDownload) == 0:
                logss.info("Nothing to download")
                return

            logss.info("Downloading from " + self.storage.storage_url)
            list_files = list()
            for file_info in filesToDownload:
                filename = str(file_info[1]).split('/')[-1]  # getting the last element
                remote = self.storage.stat(file_info[1])  # internal links works like this ../PROJECT/ "collab/filename"
                remote.download(os.path.join(file_info[0]))
                if (self.verbose):
                    logss.info(" - Downloaded file" + filename)
                list_files.append(filename)
            logss.info("Downloaded all files: "+str(list_files))
            return True
        except Exception as e:
            logss.error("Downloading error", str(e))
            return False

    def one_run(self, steps, parameters, wait_process=True):
        if len(steps) == 0:
            logss.info("No instructions to execute")
            return
        # Executing a job
        if self.verbose:
            logss.info("STEPS: "+ str(steps))
            logss.info("ARGUMENTS: "+ str(parameters))
            
        job = self.createJob(list_of_steps=steps, job_args=parameters)
        cmd_job, result_job = self.__run_job(job, wait_process)
        return cmd_job, result_job

#################
