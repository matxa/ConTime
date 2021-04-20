# ConTime

### — Making it easier for (sub)contractors to manage employees.

[contime.work](https://www.contime.work/)

Try the lite version at [lite.contime.work](https://lite.contime.work/)

Hello, my name is **Marcelo**, and I am the developer behind the project ConTime. ConTime is a web application that makes it easy for subcontractors and contractors to manage their employees' hours.

**The inspiration** for this project came about when I was working for a contractor. At this position I was working from Monday — Saturday, and every Saturday, before 12pm I had to send a picture of a spreadsheet That I would make documenting how many hours I worked that week, along with a description of what I did every day. As time passed I started noticing that all my co-workers had to do the same thing.

With this, **I saw an emerging problem**, both on the employee's side and the employer's side. The employees only had a picture to prove that they worked a certain amount of hours. And the employer only had a picture to base on in order to make payments, what if the employer wants to know the total hours worked by all its employees that given week, he/she has to manually calculate it, or even worse log everything in an Excel file manually just by looking at the picture. After witnessing this painful and unreliable process, I thought to myself why not create an application that would make this process safer and more reliable.

**ConTime’s intention** is to make it easier for (sub)contractors to manage their employees' hours. The idea behind ConTime is to allow (sub)contractors to create an account, login in, and from there add or remove employees, each employee in the Employer’s list, upon login will see a timesheet which he/she can fill documenting hours worked, along with location and job description, then submit it, so it can then be visible to the employer. The (sub)contractors will get all the information submitted to him/her displayed on his dashboard in an elegant way. The (sub)contractor will have the option to filter out information displayed making it easier to see the more relevant information, such as total hours worked. (sub)contractors will be able to click on an employee and from there see all their work history from the first day of work to the present day. And the most exciting feature will be to have an option to export all this data in CSV format.

# **— Team & Roles**

I am the only developer at ConTime so far, that means that I am responsible for every aspect of the project I am responsible for building the API, BackEnd, FrontEnd.

# **— Architecture**

[https://miro.medium.com/max/1400/0*7_ljCgsf1XsQZ9KL](https://miro.medium.com/max/1400/0*7_ljCgsf1XsQZ9KL)

# **— Technologies**

## **The technologies I used for building the BackEnd include the API:**

- *Python*: [ Flask, JSON module, MongoEngine, WTForm ]

Flask is my framework of choice simply because it is lightweight, and less opinionated, unlike Django. With flask I was able to learn how things work on the low level, like how to implement a login system from scratch.

The JSON module makes it easier to work with json files and api requests.

MongoEngine is a python mongoDB driver that allows the application to communicate with the database.

WTForm module doesn’t only make it easier for create and style html forms, but it also makes it easy for the data flow between the FrontEnd and the BackEnd.

- *MongoDB*: —MongoDB Atlas cloud base database

After a lot of research I decided to opt the use of MongoDB, more importantly I am using mongoDB Atlas, which is a cloud base database, The main reason why I opt to use it is because of how scalable it can be.

## **The technologies I used for building the FrontEnd:**

- [ HTML, CSS, JQuery, Figma ]

For the frontend I made the choice not use any additional frameworks, because I wanted the first version of the project to be a learning process for me. Not using any additional frameworks for the frontend allowed me to learn about how everything works on a low level, and I’ve leaned how to better manipulate the DOM.

# **— Features**

- Easy to use Dashboard
- Add and remove employees
- View employees full working history

# **— Technical Challenge**

The most difficult technical challenge about this project is researching every aspect of the project. I have to stop every time I don’t know about a topic or don’t understand something, to research and get myself familiar with the topic. This causes me to always jump back and forth between development and research. A good example of this is when I was building the Login System. I implemented my login system using Flask-Login, but before I could start developing it I had to go online and read through the documentation, I was confident that after reading the documentation I would be able to get started implementing my own Login System, But to my surprise I really wasn’t because there was way more to it then what I had read from the documentation. So whenever something didn’t work as expected I had to stop development and go back online looking for resources. The most difficult thing is finding the right resources, one that can explain the topic in a way that I can relate to and understand. But most importantly find a resource that is up to date. The workaround I found for this challenge is to take a tutorial on whatever I am trying to implement, then when I feel like I am ready to start developing that part in my project I’ll already have a sense of what to do if I encountered anything unexpected.

# **— What I learned**

Working on a big project such as ConTime, has thought me a lot. Most importantly I’ve leaned how to better research and plan for a project. There is also many technical takes aways. I am more comfortable now using the frontend technologies I used for the this project. I have a better understanding on how API’s work and also how to better build them. I learned so much about different ways I can deploy a web application.

Even though I learned a lot from this project, there are a couple things I would of done differently. I would do more research on how to better structure a flask application. I would find a way to better manage my time between research and development. Lastly I would make sure I am not the only person working on the project.

I’ve learned a lot about myself as a software engineer while working on this project, One being that I can create anything if I put my mind and time into it. I’ve also learned that there is always more to any technology, no matter how easy it is to learn. Most importantly I now know for sure that web-stack is a software engineering path I want to take.

# **— Follow me**

**Who am I?**

*— My name is Marcelo Ramos Martins, a software engineering student at Holberton School. I am a passionate problem solver, and a curious learner.*

*— [GitHub](https://github.com/matxa)*

*— [LinkedIn](https://www.linkedin.com/in/marcelo-ramos-martins-537a231b6/)*
