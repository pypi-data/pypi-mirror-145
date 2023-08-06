# 项目描述

主要存放通过gRPC生成的公用代码

# 项目依赖

grpcio==1.37.1
grpcio-tools==1.37.1
protobuf==3.17.0

# 安装

pip install git+http://10.12.17.156:10080/pf-wrf-alg/rpc_common@版本号

# 代码生成流程

- 1、在一个 .proto 文件内定义服务。

例：

```
// [python quickstart](https://grpc.io/docs/quickstart/python.html#run-a-grpc-application)
// python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto

// helloworld.proto
syntax = "proto3";

service Greeter {
    rpc SayHello(HelloRequest) returns (HelloReply) {}
    rpc SayHelloAgain(HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
    string name = 1;
}

message HelloReply {
    string message = 1;
}
```

- 2、用 protocol buffer 编译器生成服务器和客户端代码。

```
# 编译 proto 文件
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto
```

> 1、python -m grpc_tools.protoc: python 下的 protoc 编译器通过 python 模块(module) 实现

> 2、--python_out=. : 编译生成处理 protobuf 相关的代码的路径, 这里生成到当前目录

> 3、--grpc_python_out=. : 编译生成处理 grpc 相关的代码的路径, 这里生成到当前目录

> 4、-I. helloworld.proto : proto 文件的路径, 这里的 proto 文件在当前目录

编译后生成的代码文件:

1、helloworld_pb2.py: 用来和 protobuf 数据进行交互

2、helloworld_pb2_grpc.py: 用来和 grpc 进行交互

- 3、将生成的这两个python文件放入到本项目对应项目名称的目录下

注：新项目需要新建目录
