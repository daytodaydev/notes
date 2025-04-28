### Disclaimer
All events and characters are fictional. Any similarity to real-life events is a coincidence.

### Abstract
This is a note about bad DevOps and proposes a way to enable good DevOps in the organisation. The proposal is to grant every developer (or development team) permissions and responsibility to manage the operations of their own services. While this may sound obvious and there are a lot of materials on this topic, I'd like to share my experience that reinforces the belief in letting developers maintain the infrastructure.

I'll use devops (lowercase) for engineers who have the so-called "DevOps" role, similar to developer, manager, etc. DevOps (camel-case) - for the methodology itself.

### Introduction
You might wonder why DevOps should be enabled. Perhaps your company has a dedicated devops team with a devops lead, or hires devops contractors. What else could be done to improve DevOps? Hire more devops engineers?

Despite all materials on DevOps emphasizing that it is a set of practices, methodology, culture and toolset, there are still organisations that have devops engineers as a role. These devops engineers often become bottlenecks or a very valuable resource in the company.

DevOps should be enabled because it's a practice that teams must follow rather than a role that can be hired for.

### Typical structure
In many organisations I've seen, there were different types of developers: front-end, back-end, automations, machine learning, data, etc. They build features and services that work on their local machines. But to make them work in production, they had to go to a separate, often isolated, group of devops engineers.

Devops engineers often have the ownership of everything related to infrastructure. They create your account when you join the company, they can sometimes give you access to the server and they erase any records about your presence after you leave. Of course, eventually, IT support or other departments are created to manage accounts and other day-to-day tasks. But in the early stages, devops engineers handle all infrastructure and tooling setup.

This makes everyone accustomed to the idea that the devops engineer is in control of almost everything. No one dares to change such a status quo.

The devops engineer looks at your code, declares it 'not deployable', gets angry and frustrated, uses unfamiliar jargon, and a couple of weeks later, gets back to you with a CI/CD pipeline that does the magic. You push the code, it appears in production and you are relieved, hoping not to speak to the devops engineer again. 

### Bottleneck
I can recall two types of devops engineers: good and bad. But no matter how good or bad they are, eventually they become a scarce resource upon whom the entire team depends. Their work can seem like complex magic, creating an impression that they shouldn't be disturbed by 'ordinary' developers.

There was always some kind of wall between developers and devops engineers hiding the infrastructure, a wall behind which the developer has limited visibility, control, and ownership.

How do you know the wall exists? If deployment to the test environment fails and the entire team is waiting for a devops engineer to check the logs, the wall is there.

You might argue this happens because developers are lazy, but it's the wall. It might be built by a 'bad' devops engineer guarding their territory or by a 'good' one, who operates so well that developers never needed to look behind the wall. Now, with the deployment pipeline down, everyone assumes it's a minor glitch the 'good' devops engineer will resolve instantly.

The bottleneck is created. Development teams wait for the devops engineer's availability, and managers plan work with regard to devops resources.

Most devops engineers are good enough to keep the bottleneck manageable. But even with 'good' ones, a time comes when more devops engineers are needed.

The problems multiply with a 'bad' devops engineer - one who enjoys their power and control, who understands that nothing can be done to take their power away.

### Anecdote
There was a devops engineer who deployed a system using `docker compose` directly on AWS EC2 instances. The deployment pipeline simply executed `docker compose up` on an EC2 instance. Basic auto scaling was configured, but if there is a need to scale one specific service, a new instance has to be started with all other services (which don't need to scale).

Example:
```
|EC2 Instance |                           |New EC2 Instance                 |
|-------------|                           |---------------------------------|
|- Service A  | To scale Service A  --->  |- Service A                      |    
|- Service B  | new instance starts.      |- Service B (no need to scale it)|
```

This engineer was one of the most senior devops engineers in the company. The project was in production for a couple of years and AWS ECS/EKS had been available long before the project was started.

When I joined the company, I raised concerns about this architecture. A decision was made to migrate from `docker compose` to AWS ECS.

The devops engineer started to plan the migration. After a couple of weeks of 'planning' he provided an estimate of **6 months**.

Adding to the absurdity, the company's lead devops engineer fully supported this six-month estimate.

What made this even more surprising was that this wasn't their first time managing AWS infrastructure using Terraform.
They maintained an internal repository of reference Terraform modules, often copy-pasting code for new projects.

Essentially, everything was in place, and they just had to put new ECS task definitions within existing Terraform modules, which should not take 6 months.

### Analysis
How could a situation like this happen in a modern tech world? Why wasn't this devops engineer hesitant to provide such an estimate (which implied a week of work per simple Terraform module)?

He was confident no one would question his estimate. Moreover, no one else could do the work.

In fact, he was right. That's how the work of devops engineers is perceived in general. No one reviews their work in detail. Developers hand over code and are grateful that it works in production.

The only difference this time was that he had become overconfident, and he didn't expect someone familiar with DevOps tools and who had worked with good devops engineers previously.

After a long discussion, he agreed that he overestimated the effort 'a little'. But in the end, the migration took longer than 6 months (it was hard to conclude if it was due to existing processes or intentional delays).

### Solution
Can this kind of 'devops hell' be prevented?

The state of modern DevOps tools makes it feasible to avoid devops bottlenecks. It requires initial setup effort but pays off as the team and system grow.

To avoid devops bottlenecks, the whole team has to be responsible for the operations of their functionality.

When developers have freedom and capacity to control their deployment pipelines and experiment with the infrastructure, it improves service operations dramatically. Developers understand the context of their services better than any devops engineer. They don't need to fit their service into some generic devops template, which speeds up the operations and leaves space to adopt new tools.

The only aspect that must be controlled carefully with such an approach is to make sure that every team's infrastructure is protected from unwanted changes from other teams. Precise permission control must be implemented for this purpose.

### Fine-grained permissions
Implement fine-grained permission controls in your infrastructure. Regardless of the specific tooling (IAM, RBAC, etc.), aim for a state where you can confidently grant a junior developer permissions (e.g., to run `terraform apply`) knowing their actions affect only their service's resources in a specific environment (e.g., test), or perhaps to deploy a PoC to production behind a feature flag.

In general:
1. Create a 'manage-roles' role to create roles and permission boundaries per specific service or functionality.
2. Use 'manage-roles' role to define a fine-grained role for the specific Terraform configuration.
3. Make the specific Terraform module to assume the fine-grained role during `terraform apply`.

For instance, if a new database (`test-db-quote`) is needed, the `manage-roles` role is used to create a dedicated role (`test-db-quote-role`) with only the necessary database creation/management permissions.

Since the person who maintains the infrastructure for the `test-db-quote` will not have permissions for `manage-roles`,that person can use a sandbox environment to define all required permissions for the `test-db-quote-role` and submit request to the 'admin' to create new role for them. This process naturally leads to well-documented, least-privilege permissions for each system component.

After `test-db-quote-role` is created, anyone can be allowed to assume this role to work with the `test-db-quote` without the risk of breaking other parts of the infrastructure.

This sounds like additional work and overhead, but compare it to the case when the devops engineer says that no one has access to the specific environment so that's why they apply all configurations with a single 'admin' role.

In the latter scenario, onboarding more people to help with infrastructure becomes risky and slow, as the necessary fine-grained roles don't exist. The temptation to put aside least-privilege principle and start applying all Terraform configurations using the 'admin' role increases.

Furthermore, developers working on infrastructure feel less stressed knowing they cannot break anything outside their scope of work.

### Conclusion
Empower your developers with the necessary permissions to manage their services' infrastructure. Establish a process to define and utilize fine-grained, least-privilege permissions.  Make sure developers can break only their own resources and let them figure out how to deploy the service. 

This approach improves maintenance and deployment agility because the developers, knowing their service best, can implement operational requirements directly. By removing the communication overhead and waiting time associated with a separate devops team's capacity, developers can address infrastructure needs immediately, leading to faster iteration and more resilient systems.
