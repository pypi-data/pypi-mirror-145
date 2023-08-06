from distutils.core import setup
setup(
name="my_covid_report",
version="1.0",
description="covid-19 data report by WhaleG",
author="WhaleG",
py_modules=["covid_report.getdata","covid_report.data_processing","covid_report.covid_visualization"]
)
