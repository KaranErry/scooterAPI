# Personal Transport API

## Introduction

### Stack

The implementation of this app uses Python/Flask, with JSON as the database. The 'geopy' library was used for accurately calculating the “crow flies” distance between two sets of coordinates. 

### Setup

#### On the web

The API is live at https://scooter-reservation.herokuapp.com

#### On local dev environment

* Clone the repository
* Run `python3 app.py`
* App will run on http://localhost:8080

## 🧭 Dev Workflow

- Create an **Issue**
- Create a **branch** from that issue:
  `feature/issue-#/short-name`, `bugfix/issue-#/short-name`, or `chore/issue-#/short-name`
- Open a **PR** with `Closes #<issue number>`
- Merge when checks pass — the issue closes automatically
- The Project board reflects status (To Do → In Progress → Done)


## API Endpoints

### View All Available Scooters

#### Endpoints:
```
GET /
GET /view_all_available
```

#### Parameters: 

None

#### Success Responses:

* **Code**: 200 <br />
  **Content**: JSON list of objects, with each object containing the following properties:

|     Key     | Data Type |                                      Description of Value                                      |
|:-----------:|:------------------:|:-------------------------------------------------------------------------------------------:|
|      id     |       string       |      The id of the scooter. This can be used to start and end reservations (see below).     |
|     lat     |   floating point   |                 Latitude coordinate of the current location of the scooter.                 |
|     lng     |   floating point   |                 Longitude coordinate of the current location of the scooter.                |
| is_reserved |       boolean      | Whether or not the scooter is currently reserved. Only unreserved scooters can be reserved. |


#### Error Responses:

* **Code**: 422 <br />
  **Content**: JSON object with a `msg` property that gives a brief description of the error trigger.

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

#### Success Responses:

* **Code**: 200 <br />
  **Content**: JSON list of objects, with each object containing the following properties:

| Key | Data Type |                                  Description of Value                                 |
|:---:|:------------------:|:----------------------------------------------------------------------------------:|
|  id |       string       | The id of the scooter. This can be used to start and end reservations (see below). |
| lat |   floating point   |             Latitude coordinate of the current location of the scooter.            |
| lng |   floating point   |            Longitude coordinate of the current location of the scooter.            |


#### Error Responses:

* **Code**: 422 <br />
  **Content**: JSON object with a `msg` property that gives a brief description of the error trigger.


### Reserve a Scooter

#### Endpoints:
```
GET /reservation/start
```

#### Parameters:

| Parameter | Data Type Expected |                                                       Description                                                      |
|:---------:|:------------------:|:----------------------------------------------------------------------------------------------------------------------:|
|     id    |       string       | The id of the scooter that is to be reserved. Go to _search_ or _view all available scooters_ to find out scooter IDs. |

#### Success Responses:

* **Code**: 200 <br />
  **Content**: JSON object with a `msg` property that gives a brief description of the successful operation.


#### Error Responses:

* **Code**: 422 <br />
  **Content**: JSON object with a `msg` property that gives a brief description of the error trigger.


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

#### Success Responses:

* **Code**: 200 <br />
  **Content**: JSON object containing the following properties:

| Parameter | Original Data Type |                                                                                           Description                                                                                          |
|:---------:|:------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    msg    |       string       | Short message a brief description of the successful operation                                 |
| txn_id    | string             | The transaction ID / reference number associated with the successful payment transaction to be kept for the payee's records. |


#### Error Responses:

* **Code**: 422 <br />
  **Content**: JSON object with a `msg` property that gives a brief description of the error trigger.
