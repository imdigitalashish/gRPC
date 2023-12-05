import greet_pb2_grpc
import greet_pb2
import time
import grpc


def get_client_stream_requests():
    while True:
        name = input("Please enter a name ( or nothing to stop chatting ): ")

        if name == "":
            break

        hello_request = greet_pb2.HelloRequest(greeting="Hello", name=name)
        yield hello_request
        # time.sleep(1)

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("1. Say Hello - Unary")
        print("2. ParrotHello - Server Side Streaming")
        print("3. ChattyClientHello - Client Side Streaming")
        print("4. InteractingHello - Both Streaming")

        rpc_call = input('which rpc you want to call: ')

        if rpc_call == "1":
            hello_request = greet_pb2.HelloRequest(greeting="Hllo", name="Youtube")
            hello_reply = stub.SayHello(hello_request)
            print("Say Hello Reply")
        elif rpc_call == "2":
            hello_request = greet_pb2.HelloRequest(greeting="hello", name="Ashish")
            hello_replies = stub.ParrotSaysHello(hello_request)

            for hello_reply in hello_replies:
                print("ParraySayHelo Response Recieved")
                print(hello_reply)
        elif rpc_call == "3":
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())

            print("ChattyClientSaysHello Recieved: ")
            print(delayed_reply)
        
        elif rpc_call == "4":
            responses = stub.InteractingHello(get_client_stream_requests())

            for response in responses:
                print("INTERACTING RESPONSES: ")
                print(response)
        


if __name__ == "__main__":
    run()