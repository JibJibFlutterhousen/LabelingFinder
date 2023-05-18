# LabelingFinder

This is a python implementation of LabelingFinder - previously implemented in Java found here: https://github.com/JibJibFlutterhousen/LabelingFinderJava.

LabelingFinder contains functions to facilitate a parallel search for a vertex labeling that induces an injective edge labeling for a supplied graph. There are functions that return the sets used in graceful labelings (https://en.wikipedia.org/wiki/Graceful_labeling), harmonious labelings (https://en.wikipedia.org/wiki/Graph_labeling), Gamma-harmonious labelings (upcomming citation), and Pi-harmonious labelings (upcoming citation). The user must write and supply a function used to combine vertex labels.

ExampleScript contains examples demonstrating how to locate a valid vertex labeling with all 4 described labeling schemes, as well as the ability for LabelingFinder to work appropriately with trees where it is common to allow exactly one repeated vertex label.
