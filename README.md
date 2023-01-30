# InclueBot
A Slack bot to gently work towards more inclusive language

No, it's not a typo.

### Description

A Slack bot to aid in reminding people to use inclusive language when chatting in our public and private channels.

Inspired by this article, we originally implemented a set of Slackbot responses to prompt people in our community on reasons why the use of certain words are discouraged and suggesting alternatives.

InlcueBot is the follow on, and moves from using Slackbot responses (which effect the whole of a workspace) to a dedicated bot that must be invited in to channels to become active. When InclueBot encounters an included term it will respond with an ephemeral message (one that only the poster will see) in the channel.

To track term usage, InclueBot stores the following information in a DynamoDb table;

    the term that triggered the response
    the original text of the message where the term was found
    the Slack channel id (not the name)
    a timestamp of when the term was triggered

To reiterate, since InclueBot is invite only, it will only record this metrics information for the channels (public/private) where it has been invited in. There is no identifying information about the poster/user kept.


### Usage

To bring InclueBot into a channel, either public or private, invite it in

```
/invite @incluebot
```
Once InclueBot is in the channel, it will silently run in the background and when it encounters a term (as listed here) it will send an "ephemeral" message to the user with a helpful message on why it is suggested to avoid using the term, and what other words might serve just as well.

To remove InclueBot from a channel, kick it out
```
/kick @incluebot
```

### Technical Stuff

InclueBot is a Slack App/Bot that was based off of work from this helpful blog post by Rigel De Scala. It uses a combination of API Gateway with Lambda running Python 3.6. It also uses DynamoDB to store usage information.
Next Steps

* Create an accompanying Slash command to access term usage metrics
* Switch to using a hash/dictionary (or python equivalent) to hold the terms, reasons and suggestions for each term in the list so that that it can be easily output from a command.
* Store the terms and responses in a DynamoDB table to make them definable by the users.
* Add in system to allow users to opt-in/out from messages.
* rewrite it in NodeJs.
