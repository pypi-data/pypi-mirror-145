# MLFields: ML input management 

## Why I develop this
I feel it is hard to manage features in ML projects;
- During experiment phase, I often do many experiments and lose track of feature history
- During oepration phase, I need to build monitoring system each time

## The solution I want to build in this library
System manages features in following structure
- Project: unit of managing features
    - Set of feature definitions
    - Generated features 
    - Experiments (evaluation of generated features)
