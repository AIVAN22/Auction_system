from app.server import Server

if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.start()
