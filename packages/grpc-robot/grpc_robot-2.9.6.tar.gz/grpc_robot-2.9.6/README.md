# Robot gRPC package
This package allows sending/receiving messages in a gRPC event stream.

## Supported devices
This gRPC ROBOT library is intended to support different Protocol Buffer definitions. Precondition is that python files
generated from Protocol Buffer files are available in a pip package which must be installed before the library
is used.

| Supported device | Pip package                 | Pip package version | Library Name                                 |
|------------------|-----------------------------|---------------------|----------------------------------------------|
| dmi              | device-management-interface | 0.9.1               | [grpc_robot.Dmi](docs/dmi_0_9_1.html)        |
|                  |                             | 0.9.2               | [grpc_robot.Dmi](docs/dmi_0_9_2.html)        |
|                  |                             | 0.9.3               | [grpc_robot.Dmi](docs/dmi_0_9_3.html)        |
|                  |                             | 0.9.4               | [grpc_robot.Dmi](docs/dmi_0_9_4.html)        |
|                  |                             | 0.9.5               | [grpc_robot.Dmi](docs/dmi_0_9_5.html)        |
|                  |                             | 0.9.6               | [grpc_robot.Dmi](docs/dmi_0_9_6.html)        |
|                  |                             | 0.9.8               | [grpc_robot.Dmi](docs/dmi_0_9_8.html)        |
|                  |                             | 0.9.9               | [grpc_robot.Dmi](docs/dmi_0_9_9.html)        |
|                  |                             | 0.10.1              | [grpc_robot.Dmi](docs/dmi_0_10_1.html)       |
|                  |                             | 0.10.2              | [grpc_robot.Dmi](docs/dmi_0_10_2.html)       |
|                  |                             | 0.12.0              | [grpc_robot.Dmi](docs/dmi_0_12_0.html)       |
|                  |                             | 1.0.0               | [grpc_robot.Dmi](docs/dmi_1_0_0.html)        |
|                  |                             | 1.2.1               | [grpc_robot.Dmi](docs/dmi_1_2_1.html)        |
|                  |                             | 1.4.0               | [grpc_robot.Dmi](docs/dmi_1_4_0.html)        |
| voltha           | voltha-protos               | 4.0.13              | [grpc_robot.Voltha](docs/voltha_4_0_13.html) |
|                  |                             | 4.2.0               | [grpc_robot.Voltha](docs/voltha_4_2_0.html)  |

## Tools
The package also offers some keywords for convenience to work with Robot Framework.

List of keywords: 
 - [grpc_robot.Collections](docs/collections.html)
 - [grpc_robot.DmiTools](docs/dmi_tools.html)
 - [grpc_robot.VolthaTools](docs/voltha_tools.html)

The list of keywords may can be extended by request if required.

## Installation

    pip install robot-grpc

## How to use _robot-grpc_ in Robot Framework
The library has a named parameter _version_ to indicate the ProtoBuf file set to be used.

    Import Library    grpc_robot.Dmi
    Import Library    grpc_robot.Voltha
    Import Library    grpc_robot.Collections
    Import Library    grpc_robot.DmiTools
    Import Library    grpc_robot.VolthaTools
    

## How to update the grpc-robot to support newer DMI versions (e.g. 1.4.0)

1. Create a new version folder “dmi_1_4_0” in “<repo dir>/grpc-robot/grpc_robot/services/dmi”
2. Place an __init__.py and a dmi.json file in this folder:
    - In most cases the __init__.py file can be copied from the last dmi version's folder and updated to the dmi version 
        from which the new version shall derive.
    - The dmi.json file must be created. Please check chapter "How to create the dmi.json file"
3. If the new DMI version introduces new RPCs or the types of the parameter and/or the return have been changed for some 
        RPC the according keyword files from the last DMI version must be edited and placed into the new folder. It is 
        not neccessary to update the keyword files if the content of the RPC have changed. For each RPC which shall be 
        supported by the grpc-robot a keyword must be defined in the files. 
4. Update the README.md file with the new version.
5. Update the documentation string of class GrpcDmiRobot in file "<repo dir>/grpc-robot/grpc_robot/grpc_robot.py"
6. Update the tests if required.
7. Update the VERSION file for the library version
8. Create the new package and upload it to pypi.org
    - cd <repo dir>/grpc-robot
    - rm dist/*; python3 setup.py sdist bdist_wheel
    - PYTHONPATH=<repo dir>/grpc-robot source MAKEDOC
    - rm dist/*; python3 setup.py sdist bdist_wheel
    - pip uninstall -y grpc-robot; pip install dist/*.tar.gz
    - twine upload dist/*

## How to create the dmi.json file

The json file is the conversion of the ProtoBuf files content into json format which is used by the library.

1. Clone or update the repository https://github.com/opencord/device-management-interface.git. Make sure the VERSION 
        file shows the desired DMI version. If not checkout the version of interest.
2. In the command line interface run the command:
   - grpc_robot.protop -i <directory which consists of the ProtoBuf files to be converted> -o <output directory for 
        the created json file> dmi <version>

   e.g.
   - grpc_robot.protop -i ~/repositories/device-management-interface/protos/dmi -o <repo dir>/grpc-robot/grpc_robot/services/ dmi 1.4.0
