# PyAnka
An unofficial python wrapper library for Anka

[![Build Status](https://app.bitrise.io/app/fee9bac962541792/status.svg?token=Jyx0mNC_PO1UYIPdrci4eA&branch=main)](https://app.bitrise.io/app/fee9bac962541792)
[![PyPI](https://img.shields.io/pypi/v/pyanka.svg?color=blue)](https://pypi.python.org/pyanka)

## Requirements
You will need python3^  and the anka cli. 
```
brew install python3
brew install --cask anka-virtualization
```

## Installing
```
pip3 install pyanka
```

## Dev Notes
You can run test locally via the bitrise CLI (`brew install bitrise`)
by running `bitrise run ci`

The library at this point is not feature ready, but sufficient for the Bitrise Infrastructure team's 
current requirements.

## Usage

Import the module and instalce it with the AnkaVm() constructor, this will require you to name the virtual machine in question.

See the examples below or the [example](https://github.com/bitrise-io/PyAnka/blob/main/examples/example.py) file.

```python
import anka from pyanka

# Create an instance of the Anka VM Class
    vm = anka.AnkaVm("test-vm")

    # Start up an already existing VM that is stopped, or suspended
    vm.start()

    # Show runtime properties of an already existing VM
    # This method returns a JSON object, that you can use as a dictionary
    vm.show()

    # CLone an already existing VM
    # You need to define the name of the to be cloned VM
    # The method will initialise an instance of the class with the ne name for you.
    clone = vm.clone("cloned-vm")
    clone.show()

    # Suspend a running VM
    vm.suspend()

    # stop a running or suspended VM
    vm.stop()

    # Delete a VM, this needs to be in a stopped state
    vm.delete()

    # Copy a file from the host machine to the virtual machine
    # TODO make it work both ways
    vm.copy("./example.file", "/tmp/example.file")

    # run a shell command on the virtual machine, and get back the stdout or stderr
    vm.run("ls", "-la")
```

## Authors
| Name             | Mail Address                | GitHub Profile                                             |
|------------------|-----------------------------|------------------------------------------------------------|
| Sandor Feher     | sandor.feher@bitrise.io     | [fehersanyi-bitrise](https://github.com/fehersanyi-bitrise)|
