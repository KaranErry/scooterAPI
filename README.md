# Scooter Reservation API

## Introduction

### Stack

The implementation of this app uses Python/Flask, with JSON as the database. Other frameworks used are:

* 'requests' framework for getting the body of requests
* 'geopy' library for accurately calculating the “crow flies” distance between two lat/lng points

### Setup

* Clone the repository
* Run `python3 app.py`

## API Endpoints

### View All Available Scooters

#### Endpoints:
```
GET /
GET /view_all_available
```

#### Parameters: 

None

#### Returns:

JSON string, with the following parameters:

|  Parameter  | Original Data Type |                                         Description                                         |
|:-----------:|:------------------:|:-------------------------------------------------------------------------------------------:|
|      id     |       string       | The id of the scooter. This can be used to start and end reservations (see below).          |
|     lat     |   floating point   | Latitude coordinate of the current location of the scooter.                                 |
|     lng     |   floating point   | Longitude coordinate of the current location of the scooter.                                |
| is_reserved |       boolean      | Whether or not the scooter is currently reserved. Only unreserved scooters can be reserved. |

### Search for Scooters

#### Endpoints:
```
GET /search
```

#### Parameters:

| Parameter |   Data Type Expected   |                                                          Description                                                          |
|:---------:|:----------------------:|:-----------------------------------------------------------------------------------------------------------------------------:|
|    lat    |     floating point     | Latitude coordinate of the desired location at which to reserve a scooter.                                                    |
|    lng    |     floating point     | Longitude coordinate of the desired location at which to reserve a scooter.                                                   |
|   radius  | integer/floating point | The radius of the search, i.e. The radius of the area around the desired location that is acceptable for reserving a scooter. |

#### Returns:

JSON string, with the following parameters:

| Parameter |   Original Data Type   |                                                          Description                                                          |
|:---------:|:----------------------:|:-----------------------------------------------------------------------------------------------------------------------------:|
|    lat    |     floating point     | Latitude coordinate of the desired location at which to reserve a scooter.                                                    |
|    lng    |     floating point     | Longitude coordinate of the desired location at which to reserve a scooter.                                                   |
|   radius  | integer/floating point | The radius of the search, i.e. The radius of the area around the desired location that is acceptable for reserving a scooter. |


#### Throws (list of errors thrown by foreseeable mistakes):

|                  Error                 |                                                  Description                                                 |
|:--------------------------------------:|:------------------------------------------------------------------------------------------------------------:|
| werkzeug.exceptions.BadRequestKeyError | Thrown when the query string is badly formed, i.e. the parameters that are expected are not contained in it. |


### Reserve a Scooter

#### Endpoints:
```
GET /reservation/start
```

#### Parameters:

| Parameter | Data Type Expected |                                                       Description                                                      |
|:---------:|:------------------:|:----------------------------------------------------------------------------------------------------------------------:|
|     id    |       string       | The id of the scooter that is to be reserved. Go to _search_ or _view all available scooters_ to find out scooter IDs. |

#### Returns:

JSON string, with the following parameters:

| Parameter | Original Data Type |                                                                           Description                                                                           |
|:---------:|:------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|   result  |       boolean      |                    The outcome of the request to reserve a scooter. True if the reservation request was successful and False if unsuccessful.                   |
|    msg    |       string       | Short message accompanying _result_. If result is True, then it displays a 'success' sentence', If result was False, it might display a helpful error message.  |


#### Throws (list of errors thrown by foreseeable mistakes):

|                  Error                 |                                                  Description                                                 |
|:--------------------------------------:|:------------------------------------------------------------------------------------------------------------:|
| werkzeug.exceptions.BadRequestKeyError | Thrown when the query string is badly formed, i.e. the parameters that are expected are not contained in it. |


### End Reservation for a Scooter

#### Endpoints:
```
GET /reservation/end
```

#### Parameters:

| Parameter | Data Type Expected |                                                            Description                                                            |
|:---------:|:------------------:|:---------------------------------------------------------------------------------------------------------------------------------:|
|     id    |       string       | The id of the scooter whose reservation is to be ended. The scooter must have been reserved first in order to end a reservation.  |
|    lat    |   floating point   | Latitude coordinate of the final location of the scooter where the trip is to be ended.                                           |
|    lng    |   floating point   | Longitude coordinate of the final location of the scooter where the trip is to be ended.                                          |

#### Returns:

JSON string, with the following parameters:

| Parameter | Original Data Type |                                                                                           Description                                                                                          |
|:---------:|:------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|   result  |       boolean      | The outcome of the request to end reservation of a scooter and pay the cost. True if the end-reservation request and payment were successful and False if either was unsuccessful.             |
|    msg    |       string       | Short message accompanying _result_. If result is True, then it displays a 'success' sentence', If result was False, it might display a helpful error message.                                 |
| txn_id    | string             | If the payment went through, then txn_id is the unique transaction ID / reference number to be kept for the user's records. If _result_ is False, then there will not be a 'txn_id' parameter. |


#### Throws (list of errors thrown by foreseeable mistakes):

|                  Error                 |                                                  Description                                                 |
|:--------------------------------------:|:------------------------------------------------------------------------------------------------------------:|
| werkzeug.exceptions.BadRequestKeyError | Thrown when the query string is badly formed, i.e. the parameters that are expected are not contained in it. |