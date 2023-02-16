Deploying AWS Lambdas with Terraform
####################################

:date: 2021-01-03 15:00
:author: smetj
:category: technology
:slug: deploying_aws_lambdas_with_terraform
:tags: devops

.. role:: highlight(code)
   :language: text

|picture|



After reading the comments of this `Hackernews post`_ I noticed that a
sentiment people seem to share is that Terraform isn't really suited to deploy
`AWS Lambdas`_. Whether that's true or not I'll leave that up to you to
decide. Nevertheless I have been using a simple Terraform recipe which has
proven to be quite useful to myself.  In this article I will explain the
different parts involved.



Lambda code repository
----------------------

I believe it's reasonable to assume your Lambda code is stored in some code
repository such as Github, Gitlab, Bitbucket and so on. These allow you to
download the lambda code (including its dependencies depending how you
organize your code) as a ZIP archive similar to the following patterns:

- https://some-internal-bitbucket/rest/api/latest/projects/INFRA/repos/lambda-test123/archive?at=refs%2Ftags%2F1.0.0&format=zip
- https://github.com/smetj/lambda-example/archive/1.2.7.zip

Additionally, like any other code, you probably version your lambda code using
the necessary version tags, which makes it useful to deploy a specific version
of the lambda code.

Given these 2 properties, let's take a look at how we can leverage that using
Terraform.

Terraform resources
-------------------

In order to keep this article short I'll only cover the Terraform resources
relevant to this topic since some additional resources are required to have a
working deployment.

Download the archive
====================

.. code-block:: terraform

    resource "null_resource" "download_lambda" {
      triggers = {
        lambda_version = var.lambda_version
      }

      provisioner "local-exec" {
        command = <<BASH
        test -d .tmp || mkdir .tmp
        curl -o .tmp/lambda-${var.lambda_version}.zip "https://some-internal-bitbucket/rest/api/latest/projects/INFRA/repos/lambda-test123/archive?at=refs%2Ftags%2F${var.lambda_version}&format=zip"
    BASH
      }
    }

Make sure your Terraform code has a :highlight:`var.lambda_version` which is
expected to correspond to the repository version tag of your lambda code. It
allows you to be explicit about which version you want to be deployed.

The :highlight:`triggers` definition makes sure the
:highlight:`null_resource.download_lambda` is **only** executed when a new version
is defined compared to the previous deployment.  The :highlight:`local-exec`
provisioner executes a *curl* command which downloads the desired
ZIP archive and stores it into a local *.tmp* directory with the
:highlight:`var.lambda_version` value embedded to the filename. This is
important as that will trigger the :highlight:`aws_lambda_function` resource
as soon as the lambda filename has changed, leading to the actual deployment
to AWS Lambda.

Cleanup the archive
===================

.. code-block:: terraform

    resource "null_resource" "cleanup_lambda" {
      provisioner "local-exec" {
        when    = destroy
        command = "rm -rf .tmp"
      }
    }

This :highlight:`null_resource` is not really necessary but it does a little
house holding by cleaning up the *.tmp* directory the moment the
stack is destroyed.


Deploying the lambda archive
============================

.. code-block:: terraform

    resource "aws_lambda_function" "lambda" {
      filename      = ".tmp/lambda-${var.lambda_version}.zip"
      function_name = "${local.stack}-${local.stack_name}-something"
      role          = aws_iam_role.lambda.arn
      handler       = "main.handler"
      timeout       = 20
      runtime       = "python3.8"

      vpc_config {
        subnet_ids         = var.subnet_ids
        security_group_ids = [aws_security_group.lambda.id]
      }
      depends_on = [
        null_resource.download_lambda,
      ]
    }

The important bit here is the :highlight:`filename` value which changes the
moment you decide to deploy a new version by setting
:highlight:`var.lambda_version` triggering the resource to be re-applied
effectively leading to the new lambda being deployed to AWS.  Additionally
it's important to note that the :highlight:`depends_on` parameter needs to
have the :highlight:`null_resource.download_lambda` entry as that makes sure
the archive is downloaded first prior to triggering the deployment resource.


Final words
-----------

A disadvantage of this approach is that it's platform specific since you'll be
shelling out various bash commands. Surely this can be accommodated to fit
other platforms.  Besides that relying on shelling out CLI commands as part of
your Terraform deployment is always a bit *hacky*. On the other hand it serves
its purpose really well and has proven to be quite useful to myself so it
might be for you too.

If you have any questions or remarks, don't hesitate to reach out through the
comments or via Twitter (@smetj).

.. _Hackernews post: https://news.ycombinator.com/item?id=25588898#25591164
.. _AWS Lambdas: https://aws.amazon.com/lambda/
.. |picture| image:: images/deploying_aws_lambdas_with_terraform.png
