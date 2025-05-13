---
layout: post
title:  "Need for Tasks"
categories: development management agile project-management
tags: task-management productivity team-collaboration agile-methodologies software-engineering-practices
---

Is it ok to ask developers to keep their tasks up to date? To provide a reasonable task name, description that defines the intention of the task and definition of done (acceptance criteria), estimation, dependencies on other tasks, etc.

When asked to update a task, developers sometimes react with pushback and passive aggression. The main argument for not keeping tasks in order is simplicity of the task: "Everyone understands what's going on in it. No need to update status, to add estimation and description. Everything is clear from the name of the task itself." Then follow complaints about micromanagement and bureaucracy. Those points find support from other team members and soon make you feel like you force the whole team into performing some crazy ritual rather than just being professional and facilitating cooperation and transparency.

Usually, such negative reactions to task maintenance are observed in less experienced developers or teams with inexperienced managers. Senior developers and managers tend to make notes of their work and plans, no matter what. Everyone uses their favourite tool for this. I'm sure that even a junior developer who never adds a single comment to their task jots something down somewhere during work on a task. If not, he is either a genius or has no idea what he's doing.

It's easy to sketch a diagram on a napkin to visualise entity relations when working on a new design for a database schema, and throw the napkin away. This activity feels very natural. Whenever something doesn't fit into a person's head, it's moved to some kind of external storage, like a piece of paper or a text editor. For the developer, it's even simpler, as he works in a text editor, all entities he creates are visualised on the spot. He can easily change them and come up with a design he is happy with, then declare his task as done and say that his code is self-documented. There are plenty of tools that can generate documentation from code as well.

The problem is that this kind of documentation is generated after the task is finished. It means no one can benefit from it. Imagine if the whole team got a chance to see the planned design upfront. Then the manager would be able to evaluate business risks and dependencies, quality assurance could start designing test cases, front-end and back-end could start designing APIs and so on.

There is a big difference between adding the description of planned work to the task that everyone can see and just stating the results of the task afterwards. In the former case, there is a risk that something can go wrong and the developer will be embarrassed by the fact that he couldn't plan his work, or had written pure code. In the latter case, it's very easy to pretend that everything that was done was done as planned and demand that the rest of the team obey the results of the task. It's very common that after the task is done there is no time to change or improve the design, and, for example, the front end must use a badly designed API endpoint to finish the whole feature in time.

That's why tasks must be maintained:
1. Everyone makes some kind of notes, so why not make them directly in the task.
2. Writing a good task description is half of the task. To write description means to think about task from start to end, to understand tasks' context and dependencies.
3. A well-maintained task provides transparency and facilitates cooperation. For example, front-end developer can take a look at progress of back-end task and start working on API calls, or provide his suggestions for the API.
4. A clear scope definition helps to release stress from the developer, as he can try to fit more and more improvements in the scope of a single task. This can prolong the time he spends on the task and make him worry about missing estimates.

# Good task
A well-maintained task means that the task must have:
- **Clear name.**
- A **Description** explaining the **intention** of the task and the planned design (reference to the design document). Even if it's not part of the task maintenance itself, a lack of design in the task description indicates that the design phase has been missed, which means that the team hasn't discussed the feature in detail. This can lead to more expensive fixes in the future.
- Defined **scope** (definition of done, acceptance criteria). Otherwise developer can keep working on the task indefinitely, constantly adding small improvements.
- **Estimation.**  Initial estimation and time spent. This helps to plan the work and improves the estimation skills of the developers.
- Up-to-date **status**. Status makes it easy to identify blockers and spread the load around the team.
- **Updates** that represent the current state of the task. It's ok to update the design if new information has been discovered while working on the task.

But some tasks are so simple and straightforward... Then it will not take long to write a short description and estimate it as small (4h, 1 story point, etc). Consider task: "*Move login button left"* and another one: "*Improve usability of login screen*" with description: "*Users are complaining that the login button is not aligned with the common layout of login screens*". The description of the second task may inspire a developer to investigate best practices for login screens, or anything else relevant to the user experience, since he understands the context of the task. In comparison to just moving the button 10 pixels to the left. Imagine the task is assigned 3 months after it was created.

Regarding planning, if the developer refuses to track time spent on a task. I'm not talking about precise bureaucratic tracking of every single minute and strict reporting. Just to add the number of hours spent after the task is done. For example: "It took me 1 day". Later on, the same developer will struggle with high-level estimations of a new task. He keeps underestimating, but refuses to get better at estimation. The only way to get better at estimation is to practice it with every task.

# Examples from the field
The developer was confused about his tasks and the scope of work he was blocked by.

Part of his task was to design and oversee a medium-sized feature: a couple of API endpoints, database tables and business logic for them. He created tasks without proper descriptions and was confused about how to proceed with further assignments of them to other team members. 

Also he was stuck with current task: "Fix process A" (without proper description as well). And was blocked with the task "Investigate feature B" that another developer was working on.

He felt paralysed and overwhelmed by the "Fix process A" task. This task was never-ending; new small issues were added every day, and the scope was growing. He kept adding new fixes and new pull requests within the scope of the task and began to worry about his performance as a developer, as the original task was expected to be done a week ago.

He created this problem for himself by not defining acceptance criteria for the task. The initial issue that led to the creation of the task was resolved on the first day of work. However, while waiting for the pull request to be approved, he discovered additional improvements. After the code was deployed, QA also found some minor issues. And because of the lack of precise acceptance criteria, he kept adding fixes and improvements to the same task.

Although the initial issue was resolved, he was spending his time and the company's resources on activities that did not add value to the project. What's more, his manager hasn't been able to prioritise his work because the task has been in progress all this time. From the outside, it looks like the developer is still struggling with the initial issue.

If the description was clear, the developer could fix the initial issue and create new tasks for improvements, and QA could create separate tasks to fix minor bugs. These tasks would then be placed at the bottom of the backlog and addressed later, after higher-value tasks have been completed.

The same happened with the "Investigate feature B" task. Another developer started to implement small parts of feature B in the scope of this task, because there was no scope defined for it. The task started to grow, and other team members were not aware of the fact that some part of the feature was being implemented. If the developer has stopped after the investigation phase and created tasks for implementation, his design ideas would become visible to the rest of the team. Someone could review his design and start working on some of the tasks.

# Conclusion
A good task description is an essential part of implementation. A task was created without a description and needed additional features to be implemented. I asked the developer to provide a description of the task, and while defining the acceptance criteria, we discovered that the task itself was unnecessary, because similar business logic had already been implemented, allowing us to reuse existing functionality.

A task description acts as a contract and agreement between the developer, his team and his manager. It nudges the developer to think about the design and catch simple errors early. To write a good task description (acceptance criteria), the developer has to think about the bigger picture, which always helps to create a better design.

Tasks need to be maintained, not for bureaucracy or to have someone to blame, but to make the work visible across the team, to enable the team to plan and understand what's going on.