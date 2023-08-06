---
template: home.html
title: FlaskJoy Docs
hide: {}
 # - navigation # Hide navigation
 # - toc        # Hide table of contents
sections:
  Hero:
    title: Your toolkit for web applications in Python
    img: 
      src: images/saasless-dashboard.png
    text: |
        SaaSLess is an command line interface and web app that makes it easy for developers to <span class="em">build</span>, 
                <span class="em">release</span>, and <span class="em">operate</span> production ready Python applications on the cloud.
    buttons:
      - url: overview/
        title: Get Started
      - url: https://demo.saasjoy.app
        title: Demo
      - url: https://gitlab.com/saasless/saasless
        title: Repo
        
  Features:
  
    # Development Environment
    - title: Start with a Complete Development Environment
      text: |
        <p>
          Run a <span class="em">single command</span> to quickly get started with a containerized Python
          application using best practices on AWS. 
        </p>
        <p>
         Develop your application to run anywhere:
          <a href="docs/concepts/services/#request-driven-web-service">Raspberry Pi</a>,
          <a href="docs/concepts/services/#load-balanced-web-service">AWS Lambda/a>,
          <a href="docs/concepts/services/#backend-service">Kubernetes</a>, <a href="docs/concepts/jobs/">Heroku</a>
          Focus your time on writing business logic instead of connecting infrastructure
        </p>
      img: "images/webgpio_changes.png"
      features:
        - title: VSCode configured for Python
          description: Edit, Test and Debug your code.
          url: overview
          icon: .icons/octicons/file-code-24.svg
        - title: Debug your app anywhere
          description: Connect to your app for inspection and debugging
          url: overview
          icon: .icons/octicons/file-code-24.svg
        - title: Run tests directly from your code
          description: Use VSCode to run specific tests
          url: overview
          icon: .icons/octicons/file-code-24.svg

    # Testing
    - title: End-to-End Testing when you need it
      text: |
        Ensure high quality code with end-to-end testing
      img: "images/test-results.png"
      features:
        - title: Code-Coverage Reports
          description: See what code has been tested.
          url: features/coverage.md
          icon: .icons/octicons/file-code-24.svg
        - title: Browser Tests
          description: Write tests that control the browser
          url: overview
          icon: .icons/octicons/file-code-24.svg
        - title: Use Documentation as Tests
          description: Examples in your Python documentation will automatically be executed as tests.
          url: overview
          icon: .icons/octicons/file-code-24.svg

    # Documentation
    - title: Your Project deserves Professional Documentation.
      text: |
        Easily include code, images, diagrams into Markdown files to build
        beautiful and complete documentation.
      img: "images/adr-viewer.png"
      features:
        - title: Architectural Decision Records
          description: ADRs keep track of important technical decisions and help onboard new developers
          url: features/adr.md
          icon: .icons/octicons/file-code-24.svg
        - title: Automated Changelog
          description: Keep a changelog of features along with the app's documentation.
          url: features/changelog.md
          icon: .icons/octicons/file-code-24.svg
        - title: Analyze documentation quality
          description: Seesee what code is missing documentation.
          url: overview
          icon: .icons/octicons/file-code-24.svg

    # Continious Integration
    - title: Continious Integration
      text: |
        <p> SaaSLess provides commands to create multiple deployment environments in separate AWS accounts and regions, as well as commands to build your container images, deploy your services, and run automated tests. 
        </p>
      img: "images/gitlab-ci-screenshot.png"
      features:
        - title: GitLab-CI configured for Python
          description: Deploy and Track your application from GitLab
          url: overview
          icon: .icons/octicons/terminal-24.svg
        - title: Deploy to any cloud environment
          description: Launch your application on AWS Lambda, EC2, Fargate, etc.
          url: overview
          icon: .icons/octicons/file-binary-24.svg
        - title: Automated releases
          description: Create a continious delivery pipeline to test and launch your apps
          url: overview
          icon: .icons/aws/codepipeline-32.svg

    # Operations and Workflows
    - title: Operations is part of the workflow
      text: |
            <p>
              Coding, testing, and deploying services are only part of the application lifecycle for the developer. 
              SaaSLess also supports workflows around troubleshooting and debugging to help when things go wrong. <a href="docs/commands/svc-logs/">Tail
              your logs</a>, <a href="docs/commands/svc-exec">get a shell</a> to a running container, <a href="docs/commands/svc-status/">view the health</a> of your services
              from the comfort of your terminal.
            </p>
      #img: "images/deploy_log.png"
      img: "images/lambda-logs.gif"
      features:
        - title: Run tasks manualy
          description: Run one-off tasks for operational workloads like migrations and backups
          url: overview
          icon: .icons/aws/fargate-32.svg
        - title: Monitoring
          description: View logs and alerts from your app
          url: overview
          icon: .icons/aws/cloudwatch-32.svg
        - title: Errors and Issue Tracking
          description: Create GitLab issues from app's runtime errors
          url: overview
          icon: .icons/aws/codepipeline-32.svg

    # Users and Roles
    - title: Manage Users, Roles, and Permissions
      text: |
         Use the web admin, command-line or code to manage different kinds of users and their access
         to the app.
      img: "images/auth0.webp"
      features:
        - title: Use any database for Users and Roles
          description: Use any database to store your user information.
          url: overview
          icon: .icons/octicons/terminal-24.svg
        - title: Connect to your preferred auth provider.
          description: Use Auth0, Okta, Google, Facebook, or any OAuth provider to autheticate users.
          url: overview
          icon: .icons/octicons/file-binary-24.svg
        - title: Two-Factor and Passwordless Authentication
          description: Use modern authentication mechanisms for enhanced security.
          url: overview
          icon: .icons/aws/codepipeline-32.svg


    # Deployment
    - title: Deploy the app anywhere.
      text: |
         The application is build on Flask, meaning it can be run anywhere with Python installed.
         This project comes with everything you need to deploy to servers, desktops, devices, and the cloud.
      features:
        - title: See the Raspberry Pi App
          description: Decide what languages users see
          url: overview
          icon: .icons/octicons/terminal-24.svg
        - title: Deploy to AWS Lalmbda
          description: Use the command-line to create new translation files for additional languages.
          url: overview
          icon: .icons/octicons/file-binary-24.svg
        - title: Create a desktop app
          description: Customize how users store their prefered language.
          url: overview
          icon: .icons/aws/codepipeline-32.svg

    # i18n
    - title: Speak the User's Language
      text: |
         Easily add new languages and translations.  Share links to the translation UI to get help from users and collegues.
         Your uses can select their preferred language, or you can provide an algorithm to determin the best language.
      img: "images/poredit.png"
      features:
        - title: Set the default language settings
          description: Decide what languages users see
          url: overview
          icon: .icons/octicons/terminal-24.svg
        - title: Create new translations
          description: Use the command-line to create new translation files for additional languages.
          url: overview
          icon: .icons/octicons/file-binary-24.svg
        - title: Customize user preferences.
          description: Customize how users store their prefered language.
          url: overview
          icon: .icons/aws/codepipeline-32.svg

    # Theme
    - title: Create a Theme and Brand
      text: |
         Select the colors and layout of your app or
         create completely new themes by editing the provided HTML templates.
      img: "images/studio.png"
      features:
        - title: Set the App brand name and logos
          description: Decide what languages users see
          url: overview
          icon: .icons/octicons/terminal-24.svg
        - title: Change the color and layout of the app.
          description: Use the command-line to create new translation files for additional languages.
          url: overview
          icon: .icons/octicons/file-binary-24.svg
        - title: Create or install new themes.
          description: Customize how users store their prefered language.
          url: overview
          icon: .icons/aws/codepipeline-32.svg

  Documentation:
    - title: Getting Started
      info: Step-by-step instructions to get started
      url: 'installation'
      cta: 'See the Tutorials'
      color: '#42b7ca'
    - title: How-To Guides
      info: Task-specific guides for advanced users.
      url: 'guides/guides'
      cta: 'See the Guides'
      color: '#425fca'
    - title: Background Information
      info: Explainations and discussions for more understanding.
      url: 'background/background'
      cta: 'See the Discussions'
      color: '#9c42ca'
    - title: Technical References
      info: Details you may need while working
      url: 'references/references'
      cta: 'Check the References'
      color: violet

---


