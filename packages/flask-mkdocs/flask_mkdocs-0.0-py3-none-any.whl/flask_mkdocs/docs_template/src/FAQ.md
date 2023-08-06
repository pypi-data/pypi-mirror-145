---
id: FAQ
title: FAQ
description: Frequently Asked Questions
---

## Product FAQ

### Can we call SaaSLess something different? So that it fits our company better?

Yes, SaaSLess is just a tool for building your own Apps. We
happen to call our internal version SaaSJoy. You can call your version whatever suits your team, company, or
brand.

### Is SaaSLess a another web framework?

No, but it can be! SaaSLess is designed to create apps with for all your
infrastructure tooling, services, and documentation. 

### How is SaaSLess licensed?

...

### Why did we open source SaaSLess?

We hope to see SaaSLess become the application standard everywhere. 

### What's the roadmap for SaaSLess?

We envision three phases, which you can learn about in
[our project roadmap](overview/roadmap.md). We have already
begun work on various aspects of all three phases. Looking at the
[milestones for active issues](https://gitlab.com/saasless/saasless/-/milestones)
will also give you a sense of our progress.

### My company doesn't have thousands of developers or services. Is SaaSLess overkill?

Not at all! A core reason to adopt SaaSLess is to standardize how software is
built at your company. It's easier to decide on those standards as a small
company, and grows in importance as the company grows. SaaSLess sets a
foundation, and an early investment in your infrastructure becomes even more
valuable as you grow.

### Our company has a strong design language system/brand that we want to incorporate. Does SaaSLess support this?

Yes! The SaaSLess UI is built using Jinja2 and Bootstrap 4. With the theming capabilities
of Jinja2, you are able to adapt the interface to your brand guidelines.

## Technical FAQ

### Why Bootstrap 4?

...
### What technology does SaaSLess use?

The codebase is a large-scale Flask application that uses modern Python. For
[Phase 2](https://github.com/saasless/saasless#project-roadmap), we plan to
use Node.js and GraphQL.

### What is the end-to-end user flow? The happy path story.

There are three main user profiles for SaaSLess: the integrator, the
contributor, and the software engineer.

The **integrator** hosts the SaaSLess app and configures which plugins are
available to use in the app.

The **contributor** adds functionality to the app by writing plugins.

The **software engineer** uses the app's functionality and interacts with its
plugins.

### What is a "plugin" in SaaSLess?

Plugins are what provide the feature functionality in SaaSLess. They are used
to integrate different systems into SaaSLess's frontend, so that the developer
gets a consistent UX, no matter what tool or service is being accessed on the
other side.

Each plugin is treated as a self-contained web app and can include almost any
type of content. Plugins all use a common set of platform APIs and reusable UI
components. Plugins can fetch data either from the backend or an API exposed
through the proxy.

Learn more about [the different components](overview/what-is-saasless.md) that
make up SaaSLess.

### Why can't I dynamically install plugins without modifications the app?

This decision is part of the core architecture and development flow of
SaaSLess. Plugins have a lot of freedom in what they provide and how they are
integrated into the app, and it would therefore add a lot of complexity to allow
plugins to be integrated via configuration the same way as they can be
integrated with code.

By bundling all plugins and their dependencies into one app bundle it is also
possible to do significant optimizations to the app load time by allowing
plugins to share dependencies between each other when possible. This contributes
to SaaSLess being fast, which is an important part of the user and developer
experience.

### Why are there no published Docker images or helm charts for SaaSLess?

As mentioned above, SaaSLess is not a packaged service that you can use out of
the box. In order to get started with SaaSLess you need to use the
`@saasless/create-app` package to create and customize your own SaaSLess app.

In order to build a Docker image from your own app, you can use the
`yarn build-image` command which is included out of the box in the app template.
By default this image will bundle up both the frontend and the backend into a
single image that you can deploy using your favorite tooling.

There are also some examples that can help you deploy SaaSLess to kubernetes in
the
[contrib](https://github.com/saasless/saasless/tree/master/contrib/kubernetes)
folder.

It is possible that example images will be provided in the future, which can be
used to quickly try out a small subset of the functionality of SaaSLess, but
these would not be able to provide much more functionality on top of what you
can see on a demo site.

### Do I have to write plugins in TypeScript?

No, you can use JavaScript if you prefer. We want to keep the SaaSLess core
APIs in TypeScript, but aren't forcing it on individual plugins.

### How do I find out if a plugin already exists?

You can browse and search for all available plugins in the
[Plugin Marketplace](https://saasless.io/plugins).

If you can't find it in the marketplace, before you write a plugin
[search the plugin issues](https://github.com/saasless/saasless/issues?q=is%3Aissue+label%3Aplugin+)
to see if is in the works. If no one's thought of it yet, great! Open a new
issue as
[a plugin suggestion](https://github.com/saasless/saasless/issues/new/choose)
and describe what your plugin will do. This will help coordinate our
contributors' efforts and avoid duplicating existing functionality.


### Are you planning to have plugins baked into the repo? Or should they be developed in separate repos?

Contributors can add open source plugins to the plugins directory in
[this monorepo](https://github.com/saasless/saasless). Integrators can then
configure which open source plugins are available to use in their instance of
the app. Open source plugins are downloaded as npm packages published in the
open source repository. While we encourage using the open source model, we know
there are cases where contributors might want to experiment internally or keep
their plugins closed source. Contributors writing closed source plugins should
develop them in the plugins directory in their own SaaSLess repository.
Integrators also configure closed source plugins locally from the monorepo.

### Any plans for integrating with other repository managers, such as GitLab or Bitbucket?

We chose GitHub because it is the tool that we are most familiar with, so that
will naturally lead to integrations for GitHub being developed at an early
stage. Hosting this project on GitHub does not exclude integrations with
alternatives, such as
[GitLab](https://github.com/saasless/saasless/issues?q=is%3Aissue+is%3Aopen+GitLab)
or Bitbucket. We believe that in time there will be plugins that will provide
functionality for these tools as well. Hopefully, contributed by the community!
Also note, implementations of SaaSLess can be hosted wherever you feel suits
your needs best.

### Who maintains SaaSLess?

SaaSJoy will maintain the open source core, but we envision different parts of
the project being maintained by various companies and contributors. We also
envision a large, diverse ecosystem of open source plugins, which would be
maintained by their original authors/contributors or by the community. When it
comes to [deployment](https://saasless.io/docs/getting-started/deployment-k8s),
the system integrator (typically, the infrastructure team in your organization)
maintains SaaSLess in your own environment.

For more information, see our
[Owners](https://github.com/saasless/saasless/blob/master/OWNERS.md) and
[Governance](https://github.com/saasless/saasless/blob/master/GOVERNANCE.md).

### Does you provide a managed version of SaaSLess?

No, this is not a service offering. We build the piece of software, and someone
in your infrastructure team is responsible for
[deploying](https://saasless.io/docs/getting-started/deployment-k8s) and
maintaining it.

### How secure is SaaSLess?

We take security seriously. When it comes to packages and code we scan our
repositories periodically and update our packages to the latest versions. When
it comes to deployment of SaaSLess within an organisation it depends on the
deployment and security setup in your organisation. Reach out to us on
[Discord](https://discord.gg/MUpMjP2) if you have specific queries.

Please report sensitive security issues via SaaSJoy's
[bug-bounty program](https://hackerone.com/saasjoy) rather than GitHub.

### Does SaaSLess collect any information that is shared with SaaSJoy?

No. SaaSLess does not collect any telemetry from any third party using the
platform. SaaSJoy, and the open source community, do have access to
[GitHub Insights](https://github.com/features/insights), which contains
information such as contributors, commits, traffic, and dependencies. SaaSLess
is an open platform, but you are in control of your own data. You control who
has access to any data you provide to your version of SaaSLess and who that
data is shared with.

### Can SaaSLess be used to build something other than a developer portal?

Yes. The core frontend framework could be used for building any large-scale web
application where (1) multiple teams are building separate parts of the app, and
(2) you want the overall experience to be consistent. That being said, in
[Phase 2](overview/roadmap.md) of the project we will add features that are
needed for developer portals and systems for managing software ecosystems. Our
ambition will be to keep SaaSLess modular.

### How can I get involved?

Jump right in! Come help us fix some of the
[early bugs and good first issues](https://github.com/saasless/saasless/contribute)
or reach [a new milestone](https://github.com/saasless/saasless/milestones).
Or write an open source plugin for SaaSLess, like this
[Lighthouse plugin](https://github.com/saasless/saasless/tree/master/plugins/lighthouse).
See all the ways you can
[contribute here](https://github.com/saasless/saasless/blob/master/CONTRIBUTING.md).
We'd love to have you as part of the community.
