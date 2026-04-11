---
title: "Solution Generator | Google Cloud"
source: "https://cloud.google.com/solution-generator/zRFIAzxj68IArt3H1eSGXbA2zGydxTDVVuZfsQR2XjtpzbdFNyHWCg==?q=i+need+a+mod+or+extension+for+obsidian+that+loads+and+operates+like+a+virtual+file+set+that+is+contained+in+text+blobs+that+use+a+delimiter+such+as+%23+filename.extension+with+a+hash+value+for+that+page+%28.%2F+..%2F+relative+to+blob+location%29.++the+origin+setup+blobs+are+named+in+caps+ie+BRIDGE_CORE+this+is+grandfather+BLOB+BRIDGE_CORE_DEV+is+the+grandfather+adjusted+in+runtime...I+want+my+ai+builders+to+be+able+to+read+ant+blob+files+but+the+ability+to+only+save+with+the+their+tag+id+appended+to+it++CORE_BRIDGE_DEV_GEM++this+becomes+their+sandbox+used+freely...+i+have+a+methodology+to+propagate+from+their+sandbox+to+runtime+dev+then+to+grandfather...+I+need+the+mechanism+for+this+Functionality..&bqc=1&attributed_url=https%3A%2F%2Fcloud.google.com%2Fvertex-ai%23extract-summarize-and-classify-data#extract-summarize-and-classify-data"
author:
published:
created: 2026-04-08
description:
tags:
  - "clippings"
---
Recent use cases

i need a mod or extension for obsidian that loads and operates like a virtual file set that is contained in text blobs that use a delimiter such as # filename.extension with a hash value for that page (./../ relative to blob location). the origin setup blobs are named in caps ie BRIDGE\_CORE this is grandfather BLOB BRIDGE\_CORE\_DEV is the grandfather adjusted in runtime...I want my ai builders to be able to read ant blob files but the ability to only save with the their tag id appended to it CORE\_BRIDGE\_DEV\_GEM this becomes their sandbox used freely... i have a methodology to propagate from their sandbox to runtime dev then to grandfather... I need the mechanism for this Functionality..

This solution outlines a mechanism for managing virtual file sets stored as text blobs, enabling AI builders to interact with these files in a sandboxed environment while maintaining a controlled propagation methodology.

The solution leverages Cloud Storage as the primary repository for the text blobs, providing a scalable and durable storage solution. Cloud Identity will be used to manage user and group access, which is then enforced through Cloud IAM for granular permissions on Cloud Storage buckets and objects. Cloud Composer, built on Apache Airflow, can orchestrate the complex workflows involved in propagating changes from AI builder sandboxes to development and then to the grandfather (production) environment. Cloud Logging and Cloud Monitoring will provide essential operational visibility, tracking access, performance, and potential issues within the storage and orchestration layers. The Cloud SDK will be instrumental for programmatic interaction with Cloud Storage, enabling automation of file uploads, downloads, and management.

Here's a list of step-by-step guide to solve the problem:

- **Set up [Cloud Storage](https://cloud.google.com/#) buckets:** Create separate Cloud Storage buckets for the "grandfather" blobs (e.g., `BRIDGE_CORE`), "development" blobs (e.g., `BRIDGE_CORE_DEV`), and individual AI builder "sandbox" blobs (e.g., `CORE_BRIDGE_DEV_GEM`).
- **Define blob structure:** Ensure the text blobs adhere to the specified format, using delimiters like `# filename.extension` and including hash values for page integrity.
- **Configure [Cloud Identity](https://cloud.google.com/#) and [Cloud IAM](https://cloud.google.com/#):**
	- Create user groups in Cloud Identity for "AI Builders," "Developers," and "Grandfather Admins."
		- Use Cloud IAM to grant specific permissions:
		- AI Builders: Read access to `BRIDGE_CORE` and `BRIDGE_CORE_DEV` buckets, and read/write access to their respective sandbox buckets (e.g., `CORE_BRIDGE_DEV_GEM`). Crucially, restrict AI builders from directly modifying `BRIDGE_CORE` or `BRIDGE_CORE_DEV`.
				- Developers: Read access to `BRIDGE_CORE` and read/write access to `BRIDGE_CORE_DEV`.
				- Grandfather Admins: Full control over all buckets.
- **Implement workflow orchestration with [Cloud Composer](https://cloud.google.com/#):**
	- Develop Apache Airflow DAGs (Directed Acyclic Graphs) within Cloud Composer to manage the propagation process.
		- **Sandbox to Development:** A DAG could be triggered (e.g., manually by an AI builder or on a schedule) to review and merge changes from a sandbox bucket (e.g., `CORE_BRIDGE_DEV_GEM`) into the `BRIDGE_CORE_DEV` bucket. This DAG would involve validation steps and potentially human approval.
		- **Development to Grandfather:** Another DAG would handle the propagation from `BRIDGE_CORE_DEV` to `BRIDGE_CORE`, likely with stricter review and approval processes.
- **Utilize [Cloud SDK](https://cloud.google.com/#) for programmatic access:** Develop scripts or applications using the Cloud SDK to:
	- Upload new blobs to sandbox buckets.
		- Read blobs from various buckets for AI builder operations.
		- Facilitate the merging and propagation of blobs as part of the Cloud Composer workflows.
- **Monitor and log with [Cloud Monitoring](https://cloud.google.com/#) and [Cloud Logging](https://cloud.google.com/#):**
	- Set up Cloud Logging to capture all access events to Cloud Storage buckets, including who accessed what and when. This is crucial for auditing and security.
		- Configure Cloud Monitoring to track storage usage, request rates, and error rates for all buckets, providing insights into system health and performance.
		- Create alerts in Cloud Monitoring for unusual activity or errors.

Insightful questions to help the user clarify their requirements and refine the solution:

- What is the expected volume and size of these text blobs? This will help in optimizing Cloud Storage configurations and potential cost considerations.
- What are the specific validation and approval steps required for propagating changes from sandbox to development and then to grandfather? This will directly influence the complexity of the Cloud Composer DAGs.
- How will the AI builders interact with these virtual file sets? Will they use a custom application, command-line tools, or an existing Obsidian extension that can be integrated with Cloud Storage APIs?
- Are there any specific performance requirements for reading and writing these blobs, especially for the AI builders?
- What is the desired level of automation for the propagation process? Are manual review and approval steps always required, or can some stages be fully automated?

Generative AI is experimental. Information quality and accuracy may vary.

Key products used

Cloud Storage

Store the text blobs containing virtual files

Cloud Storage would serve as the secure, durable, and scalable repository for all your text blobs, including the "grandfather" blobs like BRIDGE\_CORE and the AI builders' sandbox blobs. It would reliably store these virtual file sets, allowing for efficient retrieval and management of the delimited text content.

Go deeper

Supporting products that may be needed to form a complete workload

Cloud Logging

Cloud Logging tracks all access and modifications to your virtual file blobs, ensuring accountability and security for your AI builders' actions.

Cloud Monitoring

Cloud Monitoring provides insights into the performance and usage of your virtual file system, helping optimize resource allocation and identify bottlenecks.

Cloud Composer

Cloud Composer orchestrates the propagation of changes from AI builder sandboxes to development and production environments, automating your methodology.

## Talk to a Google Cloud sales representative

## Request a call back

We’ll share your use case and recommendation with a sales agent and get back to you shortly.

Google Account

Floyd Nun

floydnun@gmail.com