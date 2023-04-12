import uvicorn


def main():
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=5005,
        reload=True
    )


if __name__ == '__main__':
    main()
