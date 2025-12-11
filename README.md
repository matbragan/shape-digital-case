# Shape's Data Engineering Interview Tech Case

An **FPSO** vessel contains some equipment, and we call each piece of
equipment an "asset." Each asset has multiple sensors. Every time an
equipment failure happens, we collect data from all sensors attached to
the offending asset, and store this data in a log file. The timestamps
are in UTC.

This archive contains three files:

- a log file named `equipment_failure_sensors.txt`;
- a file named `equipment_sensors.csv` containing the relationships
  between the sensors and the assets;
- and a file named `equipment.json` with equipment data.

## Instructions

Create a pipeline to answer the following questions:

1. How many equipment failures happened?
2. Which piece of equipment had most failures?
3. Find the average amount of failures per asset across equipment
   groups, ordered by the total number of failures in ascending order.
4. For each asset, rank the sensors which present the most number of
   failures, and also include the equipment group in the output.

Notes:

- You're free to modify the files into any format, as long as the
  relevant information is preserved.

- Structure the data in a way that queries will be optimized according
  to the data retrieval process regarding equipment, sensors, and dates.
  Data can also be manipulated in ACID transactions.

- Use Python, SQL and/or PySpark. You may use third-party tools and
  libraries, as long as you can explain why a third-party dependency is
  required and/or recommended, and can explain the choices you made.

## Results

Your code will be evaluated based on the following criteria:

- Quality, readability, and maintainability of the code.
- Use of software engineering best practices and design patterns.
- Scalability and performance of the solution when dealing with
  large datasets.
