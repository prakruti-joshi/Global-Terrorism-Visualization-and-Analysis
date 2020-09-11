# Global-Terrorism-Visualization-and-Analysis

Demo video of dashboard: [Link](https://www.youtube.com/watch?v=uTu3GNRqMJE&feature=youtu.be)

This project was undertaken as part of the course: Data Interaction Visualisation and Analyis. We have designed and developed an interactive dashboard to explore [Global Terrorism Database (GTD)](https://start.umd.edu/gtd/), which is maintained by the University of Maryland. The database has information regarding ~180K terrorist events around the world for the years 1970-2017 with detailed attributes like number of deaths, damage, terrorist groups invovled, location etc. The information about the data is provided in the home page of the web application. The dashboard is divided into three main views -

#### 1. Trends
This view emphasis the visualizations and information relating to the time component of the data across the world, region wise or country wise. The location and the details of the terrorist events occuring in a particular year can be seen on the global world map. The connected events can also be visualized on the world map. The view has interactive features such as zooming and panning to oberve the events for a particular country. The most affected country and region in each year can be observed using the bar race chart and interactive pie-chart.

#### 2. Country Statistics
This view displays the information related to terrorist events for a particular country. On selecting a particular country, visual plots display state-wise terror events, numerical statistics over the years, most affected cities, attack type distribution and major terrorist groups active in the country and their impact. 

#### 3. Analysis
This view uses interactive and visual features to describe overall analysis from the data related to the damage and the cause of the events. Information related to terrorist groups with highest damage in history, their active years, worst events in history, most affected countries, motive behind the attacks are presented. Other attributes like weapon type, target type, attack type are explored and their distributions are analysed. 

#### Details:

Visual representations: Map, Line plot, Scatter plot, Pie plot, Bar race chart, Fishbone chart, Bubble plot, Word cloud, radar timeline.
Interactivity: Zooming, Panning, Hover, Click, Drop down, Sliders, Linking of views

The visualisations have been rendered using the libraries of D3.js and amCharts. The web application is hosted using Flask in python. The data in some of the visualizations is pre-processed using Pandas. The level of interactivity is ~1s per action. All the plots can be downloded in the form of image or data. The report details the findings from the visualisation and interaction.


