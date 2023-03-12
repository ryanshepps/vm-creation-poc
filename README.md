# Automatic VM Creation

### **Requirements**

|Dependency|Version|
|-|-|
|python|3.9.13|
|gcloud|2022.02.11|
|az|2.45.0|

### **Installation**

```bash
pip install -r requirements.txt
```

### **Running**

#### **Pre Run**

In order to run the example `automate.py`, you need to be logged into Google Cloud Platform via the `gcloud` CLI:

```bash
gcloud auth application-default login
```

You must have a quota project tied to your account:

```bash
gcloud auth application-default set-quota-project $PROJECT_ID
```

And the current account that you're logged into must have the correct permissions for the tasks you want to do on the Google Compute Engine.

You must also log in to the Microsoft Azure via the `az` CLI:

```bash
az login
```

#### **Run**

Finally, you can run `automate.py` with:

```bash
python automate.py
```

### **Configuration**

#### **Google Cloud Platform**

The `project` key must be a project that has a billing account tied to it and has the Google Compute Engine API enabled.

##### **Base Requirements**

|key|required|example|
|---|--------|-------|
|name|Yes|linuxserver01|
|project|No|vm-creation-poc-379200|
|team|No|Toronto Office Web Team|
|purpose|No|webserver|
|os|No|linux|
|image|Yes|debian-10-buster-v20230206|
|imageproject|Yes|debian-cloud|
|zone|Yes|northamerica-northeast2-a|

##### **Extras**

|key|required|example|
|---|--------|-------|
|ports|No|80, 443, 3333|
|description|No|Linux is the best!|

#### **Microsoft Azure**

The `resource-group` must have a subscription tied to it.

##### **Base Requirements**

|key|required|example|
|---|--------|-------|
|purpose|No|webserver|
|os|No|linux|
|name|Yes|linuxserver01|
|resource-group|Yes|images|
|team|No|Toronto Office Web Team|
|image|Yes|Debian|
|location|Yes|canadacentral|
|admin-username|Yes|azureuser|

##### **Extras**

|key|required|example|
|---|--------|-------|
|ports|No|80, 443, 3333|

### **Project Structure**

The user is only required to know how to format key values in the configuration and how they want to compose their virtual machines (only from a configuration file for now).

#### **APIs and Abstractions**

The code is structured so that new APIs can be added easily. If one was to add AWS to the list of APIs for automatic VM creation, it would be as easy as implementing abstractions for AWS (in `classes/abstractions/`), and adding the new implemented abstractions to `automate.py`.

#### **Logger**

Because it is a requirement to log some output before creating VMs, I implemented a beefed up logger so that I can customize the logs that I'm outputting. This greatly helped me during my debugging so I could know which logs are coming from where, when they are coming and the amount that I should be paying attention to them.

#### **VMDocumenter**

It's also a requirement that the VMs that get created are documented. It's for this reason that I created the VMDocumenter class to reduce the amount of duplication between composers.

#### **Report**

A report on VM creation for the various cloud platforms can be found in `docs/Automatic Virtual Machine Creation Report.pdf`.