import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "retbrown-cdk-ecr-deployment",
    "version": "1.0.3",
    "description": "CDK construct to deploy docker image to Amazon ECR",
    "license": "Apache-2.0",
    "url": "https://github.com/retbrown/retbrown-cdk-ecr-deployment",
    "long_description_content_type": "text/markdown",
    "author": "retbrown",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/retbrown/retbrown-cdk-ecr-deployment"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "retbrown_cdk_ecr_deployment",
        "retbrown_cdk_ecr_deployment._jsii"
    ],
    "package_data": {
        "retbrown_cdk_ecr_deployment._jsii": [
            "retbrown-cdk-ecr-deployment@1.0.3.jsii.tgz"
        ],
        "retbrown_cdk_ecr_deployment": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.135.0, <2.0.0",
        "aws-cdk.aws-iam>=1.135.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.135.0, <2.0.0",
        "aws-cdk.core>=1.135.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.49.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
