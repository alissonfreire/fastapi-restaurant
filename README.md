
# Restaurant Orders API

This project is a RESTful API built with the FastAPI framework for managing orders in a restaurant. The API allows users to create, read, update, and delete orders. It is containerized using Docker and Docker Compose, and includes tests and API documentation.

## Features

- Create, read, update, and delete orders.
- API documentation available at `/docs`.
- Fully containerized with Docker and Docker Compose.
- Includes tests to ensure API functionality.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/restaurant-orders-api.git
    cd restaurant-orders-api
    ```

2. Build and start the containers:

    ```sh
    docker-compose up --build
    ```

3. The API will be available at `http://localhost:8000`.

### Running Tests

To run the tests, execute the following command:

```sh
docker-compose run --rm app task test
```

### API Documentation

API documentation is automatically generated and can be accessed at:

```
http://localhost:8000/docs
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
