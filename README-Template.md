# Data Analysis

Canaria's scripts for collecting, processing and analysing HRV data in Python. This includes processing data collected from [Arduino Nano](https://github.com/TeamCanaria/Prototype) from the Prototype repository, through serial and through bluetooth.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Install commands are provided in the following links

>1. Download and install [Jupyter Notebooks](https://jupyter.org/install.html)
>2. Get familiar with iPython notebooks and Jupyter [here](https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook)
>3. Python libraries required are [pySerial](https://github.com/pyserial/pyserial),  [PyBluez](https://github.com/karulis/pybluez) and [AWS SDK for Python](https://aws.amazon.com/sdk-for-python/)

## Installing

### Collecting data

Once the prerequisites are installed, we can start to walkthrough the different data science tools available to us.

GCUH has provided some C code that supposedly will have a Raspberry Pi receive data from ICU equipment and process it in a GUI software. These scripts are contained in the DatexCollectionSoftware/ and DatexPi/ directories but due to compile errors, we haven't been able to see it in action.

```
gcc `pkg-config --cflags --libs gtk+-2.0` main.c -o DatexConnectionSoftware
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
