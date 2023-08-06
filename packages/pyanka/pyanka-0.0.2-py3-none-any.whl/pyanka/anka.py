"""
Anka wrapper library
"""
from typing import List
import subprocess
import json

class VMNotFoundException(Exception):
    """
    Custom error for missing VMs
    """
    def __init__(self, message="The vistual machine does not exist") -> None:
        self.message = message
        super().__init__()

class AnkaProcess:
    """
    This class represents the Anka client
    """
    PATH = "/usr/local/bin/anka"
    def __init__(self, binary_path=None):
        if binary_path is None:
            self.bin = self.PATH
        else:
            self.bin = binary_path

    def runner(self, args: list) -> tuple:
        """
        A helper function to run subprocesses.
        """
        args.insert(0, self.bin)
        try:
            process_output = subprocess.run(args, capture_output=True, text=True, check=True)
            return process_output.stdout, process_output.returncode
        except FileNotFoundError as err:
            return None, err.errno
        except Exception as err:
            return None, err.args[0]

    def show(self, vm_name):
        """
        Show a VM's runtime properties
        """
        string_data, err = self.runner(["--machine-readable", "show", vm_name])
        if err != 0:
            return None, 3
        json_data = json.loads(str(string_data))
        return json_data, err


class AnkaVm:
    """
    This class is representing an Anka Virtual machine
    on initialising it, you need to provide a VM name
    to use.
    """

    def __init__(self, name: str, process_runner=None):
        if process_runner is None:
            self.process = AnkaProcess()
        else:
            self.process = process_runner
        self.name = name

    def start(self) -> tuple:
        """
        Start or resume a stopped or suspended VM
        """
        args = ["--machine-readable", "start", self.name]
        state, err = self.process.show(vm_name=self.name)
        if err != 0:
            return None, err
        json_state = json.loads(state)
        if json_state["body"]["status"] != "running":
            try:
                output, err = self.process.runner(args)
                if err != 0:
                    return None, err
                json_output = json.loads(output)
                return json_output, err
            except VMNotFoundException:
                return None, 3
        return None, err

    def suspend(self) -> tuple:
        """
        Suspend a running VM
        """
        args = ["--machine-readable", "suspend", self.name]
        state, err = self.process.show(vm_name=self.name)
        json_state = json.loads(state)
        if json_state["body"]["status"] != "running":
            return json_state, err
        output, err = self.process.runner(args)
        state = json.loads(output)
        return state["status"], err

    def stop(self) -> tuple:
        """
        Shut down a VM
        """
        args = ["--machine-readable", "stop", self.name]
        state, err = self.process.show(vm_name=self.name)
        json_state = json.loads(state)
        if json_state["body"]["status"] == "suspended":
            return json_state["status"], err
        output, err = self.process.runner(args)
        state = json.loads(output)
        return state["status"], err

    def clone(self, target: str):
        """
        Clone a suspended or stopped VM
        Takes one argument, the name for the copy, and clones a suspended or stopped VM
        """
        args = ["--machine-readable", "clone", self.name, target]
        cmd = self.process.runner(args)
        if cmd.returncode == 0:
            vm_clone = AnkaVm(target)
            return vm_clone, 0
        return None, cmd.stderr

    def delete(self):
        """
        Delete a VM
        """
        args = ["--machine-readable", "delete", "--yes", self.name]
        self.process.runner(args)

    def run(self, *args: List[str]):
        """
        Run a command inside of a VM (will start VM if suspended or stopped)
        Takes a list of arguments in the form of:
        cmd *args fe.: ("ls", "-la")
        """
        return self.process.runner(["--machine-readable", "run", self.name, *args])

    def copy(self, source: str, destination: str):
        """
        Copy files in and out of the VM and host.
        Takes two arguments, the source file/folder you want to copy
        and the desired destination.
        In this implementation the copy will always be recursive.
        """
        dest = f"{self.name}:{destination}"
        return self.process.runner(["--machine-readable", "cp", "-R", source, dest])
