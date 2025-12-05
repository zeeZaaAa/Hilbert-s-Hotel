# KMITL OBJECT ORIENTED DATA STRUCTURES class project

This is a Hilbert's Hotel project, created to explain the paradox of infinity in the Object-Oriented Data Structures class.

## Description
Hilbert's Hotel (or Hilbert's Paradox) is a thought experiment by David Hilbert illustrating that a fully occupied hotel with infinite rooms can always accommodate more guests, even infinitely many, by calculating existing guests to new rooms 

## Features
* **Interactive Web Simulation:** Visualizes the state of the Infinite Hotel and room calculating using FastHTML.
* **Infinite Buses of Infinite Guests:** Illustrates the complex solution using Cantor's diagonalization principle.

## Implementation Details
This project utilizes Object-Oriented principles and the following data structures to model the paradox:
* **Hash Table:** Used internally to efficiently manage and map room numbers to guests.
* **Diagonalization Logic:** Implements the mathematical logic (similar to **Cantor's Diagonal Loop**) necessary to handle scenarios involving doubly-infinite sets of guests.

## Stack & language:
* FastHTML
* FastAPI
* Python

## Prerequisites:
* pip

## Project setup
```bash
$ pip install -r requirements.txt
```

## Getting Started

First, run the development server:

```bash
$ python run_all.py
```

Open [http://localhost:5003](http://localhost:5003) with your browser to see the result!.

