# ADR-1: Adopt ADR
```
Status: Accepted
Created: 2018-08-16
Accepted: 2018-08-17
```
## Context
It is very important to keep track of which decisions were taken, when and foremost why.  
## Decision
In order to help document decision processes we adopt the ADR (Architecture Decision Record) system [https://github.com/joelparkerhenderson/architecture_decision_record]().

Characteristics of a good ADR:  
- Point in Time - Identify when the Architecture Decision (hereinafter AD) was made
- Rationale - Explain the reason for making the particular AD
- Immutable record - The decisions made in a previously published ADR should not be altered
- Specificity - Each ADR should be about a single AD

#### Document format
Every ADR document MUST follow format:
```
# Title
A concise title of the ADR, imperative and short, like a git commit message.  

Status: It can be chosen between [Proposal, Accepted, Superseded-by].
Created: creation date in the format YYYY-mm-dd
Accepted: when the decision was considered final in the format YYYY-mm-dd
Superseded: when the decision was considered replaced by an other ADR in the format YYYY-mm-dd

## Context
A neutral description of the facts that led to such decision, the reasons behind it and the forces at play. Include considerations about the current status of your organisation and team composition if meaningful.

## Decision
The active response to the previous section. Given the context "We will ...".

## Consequences
A description of the state after the decision has been implemented, and its implications. All consequences should be listed here, not just the "positive" ones. A particular decision may have positive, negative, and neutral consequences, but all of them affect the team and the project in the future.
```

The document MUST be saved in Markdown and MUST use a naming convention as: `YYYY-mm-dd-ADR-# Title.md`.  

When a AD is made that invalidates or replaces a previous ADR then a new ADR MUST be created, the old ADR status MUST be changed to `superseded-by` bearing a reference (ADR number is enough) to the ADR superseding it.

We MUST host all the ADRs documents on Github and use the pull request feature to add new documents, this will allow to add comments and keep track of them.

- For each new ADR create then a new branch with the ADR reference number and create a pull request with master.  
The pull request is then the place to comment before making the ADR final.

- At the moment of the creation of the pull request the ADR is considered created and under evaluation. At the moment of  merging the pull request the ADR will be considered final. The `status` inside the document should reflect those changes.

- In the case of a new ADR superseding this document, the pull request for the new ADR should also take care of changing the status of the document to superseded.

We MUST adopt [RFC2119](https://www.ietf.org/rfc/rfc2119.txt) when indicating requirements inside the document.

## Consequences
Adopting this system will require extra effort to maintain the various proposals and update their status but this should be quickly outperformed by the benefits coming from being able to recollect exactly why certain decisions where made and avoid useless reiteration and exploration over decision paths already analysed in the past.
